import streamlit as st
from streamlit_flow_component import flow_component
from pdtModels import Project, Deliverable, Task, Session
import json

st.set_page_config(layout="wide")
st.title("Project Management Flow")

# Initialize session
session = Session()

def get_all_projects():
    return session.query(Project).all()

def create_node_data(item, node_type):
    return {
        "id": f"{node_type}_{item.short_id}",
        "type": node_type,
        "data": {
            "label": item.brief,
            "short_id": item.short_id,
            "tags": json.dumps(item.tags) if item.tags else "[]"
        }
    }

def create_edge_data(source_id, target_id):
    return {
        "id": f"e_{source_id}-{target_id}",
        "source": source_id,
        "target": target_id
    }

def get_flow_data():
    nodes = []
    edges = []
    
    projects = get_all_projects()
    for project in projects:
        project_node = create_node_data(project, "project")
        nodes.append(project_node)
        
        for deliverable in project.deliverables:
            deliverable_node = create_node_data(deliverable, "deliverable")
            nodes.append(deliverable_node)
            edges.append(create_edge_data(project_node["id"], deliverable_node["id"]))
            
            for task in deliverable.tasks:
                task_node = create_node_data(task, "task")
                nodes.append(task_node)
                edges.append(create_edge_data(deliverable_node["id"], task_node["id"]))
    
    return {"nodes": nodes, "edges": edges}

# Sidebar for CRUD operations
with st.sidebar:
    st.header("Add/Edit Items")
    
    operation = st.selectbox("Operation", ["Add", "Edit", "Delete"])
    item_type = st.selectbox("Item Type", ["Project", "Deliverable", "Task"])
    
    if operation == "Add":
        with st.form("add_form"):
            short_id = st.text_input("Short ID")
            brief = st.text_input("Brief Description")
            tags = st.text_area("Tags (JSON format)", "{}")
            
            if item_type in ["Deliverable", "Task"]:
                effort = st.number_input("Effort", min_value=1)
                team = st.text_area("Team (JSON format)", "{}")
            
            if item_type == "Deliverable":
                projects = get_all_projects()
                project_choices = {p.short_id: p.id for p in projects}
                project_id = st.selectbox("Project", list(project_choices.keys()))
            
            if item_type == "Task":
                deliverables = session.query(Deliverable).all()
                deliverable_choices = {d.short_id: d.id for d in deliverables}
                deliverable_id = st.selectbox("Deliverable", list(deliverable_choices.keys()))
            
            if st.form_submit_button("Add"):
                try:
                    tags_dict = json.loads(tags)
                    if item_type == "Project":
                        new_item = Project(
                            short_id=short_id,
                            brief=brief,
                            tags=tags_dict
                        )
                    elif item_type == "Deliverable":
                        team_dict = json.loads(team)
                        new_item = Deliverable(
                            short_id=short_id,
                            brief=brief,
                            tags=tags_dict,
                            team=team_dict,
                            effort=effort,
                            project_id=project_choices[project_id]
                        )
                    else:  # Task
                        team_dict = json.loads(team)
                        new_item = Task(
                            short_id=short_id,
                            brief=brief,
                            team=team_dict,
                            effort=effort,
                            deliverable_id=deliverable_choices[deliverable_id]
                        )
                    
                    session.add(new_item)
                    session.commit()
                    st.success(f"{item_type} added successfully!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    session.rollback()

# Main content area for flow diagram
flow_data = get_flow_data()

# Custom node colors and styles
stylesheet = [
    {
        "selector": 'node[type="project"]',
        "style": {
            "background-color": "#4CAF50",
            "color": "white"
        }
    },
    {
        "selector": 'node[type="deliverable"]',
        "style": {
            "background-color": "#2196F3",
            "color": "white"
        }
    },
    {
        "selector": 'node[type="task"]',
        "style": {
            "background-color": "#FFC107",
            "color": "black"
        }
    }
]

# Render flow diagram
st.subheader("Project Flow Diagram")
flow = flow_component(
    nodes=flow_data["nodes"],
    edges=flow_data["edges"],
    stylesheet=stylesheet,
    height=600
)

# Display selected node information
if flow and flow.get("selected"):
    st.subheader("Selected Item Details")
    selected_id = flow["selected"]
    selected_type = selected_id.split("_")[0]
    selected_short_id = selected_id.split("_")[1]
    
    if selected_type == "project":
        item = session.query(Project).filter_by(short_id=selected_short_id).first()
    elif selected_type == "deliverable":
        item = session.query(Deliverable).filter_by(short_id=selected_short_id).first()
    else:
        item = session.query(Task).filter_by(short_id=selected_short_id).first()
    
    if item:
        st.json({
            "short_id": item.short_id,
            "brief": item.brief,
            "tags": item.tags if hasattr(item, "tags") else None,
            "team": item.team if hasattr(item, "team") else None,
            "effort": item.effort if hasattr(item, "effort") else None
        })
