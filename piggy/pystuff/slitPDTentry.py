import streamlit as st
import pandas as pd
import json
import plotly.express as px
import uuid

# Initialize session state
if 'projects' not in st.session_state:
    st.session_state.projects = {}

def generate_id():
    return str(uuid.uuid4())[:8]

def calculate_rollups(project_id):
    if project_id in st.session_state.projects:
        project = st.session_state.projects[project_id]
        for del_id in project['deliverables']:
            deliverable = project['deliverables'][del_id]
            total_effort = sum(task['effort'] for task in deliverable['tasks'].values())
            team_members = set()
            for task in deliverable['tasks'].values():
                team_members.update(task['team_members'])
            deliverable['effort'] = total_effort
            deliverable['team_members'] = list(team_members)

def save_state(filename):
    try:
        with open(filename, 'w') as f:
            json.dump(st.session_state.projects, f)
        return True
    except Exception as e:
        st.error(f"Error saving: {str(e)}")
        return False

def load_state(filename):
    try:
        with open(filename, 'r') as f:
            st.session_state.projects = json.load(f)
        return True
    except Exception as e:
        st.error(f"Error loading: {str(e)}")
        return False

def delete_project(project_id):
    del st.session_state.projects[project_id]

def delete_deliverable(project_id, deliverable_id):
    del st.session_state.projects[project_id]['deliverables'][deliverable_id]

def delete_task(project_id, deliverable_id, task_id):
    del st.session_state.projects[project_id]['deliverables'][deliverable_id]['tasks'][task_id]
    calculate_rollups(project_id)

st.title("Project Management System")

# Sidebar for project management
with st.sidebar:
    st.header("Project Management")

    # Save/Load functionality
    st.subheader("Save/Load Projects")
    filename = st.text_input("Filename", "projects.json", key="filename_input")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save", key="save_button"):
            if save_state(filename):
                st.success("Saved successfully!")
    with col2:
        if st.button("Load", key="load_button"):
            if load_state(filename):
                st.success("Loaded successfully!")

    # Create new project
    st.subheader("Create New Project")
    project_type = st.selectbox("Project Type", 
                              ["Development", "Research", "Infrastructure"],
                              key="project_type_select")
    project_title = st.text_input("Project Title", key="project_title_input")
    if st.button("Create Project", key="create_project_button"):
        if project_title:
            project_id = generate_id()
            st.session_state.projects[project_id] = {
                'id': project_id,
                'type': project_type,
                'title': project_title,
                'deliverables': {}
            }
            st.success(f"Created project: {project_title}")

# Main content area
if st.session_state.projects:
    selected_project_id = st.selectbox(
        "Select Project",
        options=list(st.session_state.projects.keys()),
        format_func=lambda x: st.session_state.projects[x]['title'],
        key="project_select"
    )

    project = st.session_state.projects[selected_project_id]

    # Project details and editing
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        new_title = st.text_input("Project Title", value=project['title'], key=f"edit_proj_title_{project['id']}")
    with col2:
        new_type = st.selectbox("Project Type", 
                               ["Development", "Research", "Infrastructure"],
                               index=["Development", "Research", "Infrastructure"].index(project['type']),
                               key=f"edit_proj_type_{project['id']}")
    with col3:
        if st.button("Delete Project", key=f"del_proj_{selected_project_id}"):
            delete_project(selected_project_id)
            st.rerun()

    # Update project details
    project['title'] = new_title
    project['type'] = new_type

    # Deliverables section
    st.subheader("Deliverables")

    # Add new deliverable
    with st.expander("Add New Deliverable"):
        del_title = st.text_input("Deliverable Title", key="new_deliverable_title")
        if st.button("Add Deliverable", key="add_deliverable_button"):
            if del_title:
                del_id = generate_id()
                project['deliverables'][del_id] = {
                    'id': del_id,
                    'title': del_title,
                    'effort': 0,
                    'team_members': [],
                    'tasks': {}
                }
                st.success(f"Added deliverable: {del_title}")

    # Display deliverables
    for del_id, deliverable in project['deliverables'].items():
        with st.expander(f"Deliverable: {deliverable['title']}"):
            # Deliverable editing
            col1, col2 = st.columns([3, 1])
            with col1:
                new_del_title = st.text_input("Deliverable Title", 
                                            value=deliverable['title'],
                                            key=f"edit_del_title_{del_id}")
                deliverable['title'] = new_del_title
            with col2:
                if st.button("Delete Deliverable", key=f"del_del_{del_id}"):
                    delete_deliverable(selected_project_id, del_id)
                    st.rerun()

            st.write(f"Total Effort: {deliverable['effort']}")
            st.write(f"Team Members: {', '.join(deliverable['team_members'])}")

            # Add new task
            st.subheader("Add New Task")
            task_title = st.text_input(
                "Task Title", 
                key=f"task_title_{del_id}"
            )
            task_effort = st.number_input(
                "Effort", 
                min_value=1, 
                max_value=20, 
                value=1,
                key=f"task_effort_{del_id}"
            )
            task_team = st.multiselect(
                "Team Members", 
                ["Team Member 1", "Team Member 2", "Team Member 3", "Team Member 4"],
                key=f"task_team_{del_id}"
            )

            if st.button(f"Add Task", key=f"add_task_{del_id}"):
                if task_title:
                    task_id = generate_id()
                    deliverable['tasks'][task_id] = {
                        'id': task_id,
                        'title': task_title,
                        'effort': task_effort,
                        'team_members': task_team
                    }
                    calculate_rollups(selected_project_id)
                    st.success(f"Added task: {task_title}")

            # Display tasks with editing capability
            if deliverable['tasks']:
                st.subheader("Tasks")
                for task_id, task in deliverable['tasks'].items():
                    col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
                    with col1:
                        new_task_title = st.text_input("Task Title",
                                                     value=task['title'],
                                                     key=f"edit_task_title_{task_id}")
                        task['title'] = new_task_title
                    with col2:
                        new_task_effort = st.number_input("Effort",
                                                        min_value=1,
                                                        max_value=20,
                                                        value=task['effort'],
                                                        key=f"edit_task_effort_{task_id}")
                        task['effort'] = new_task_effort
                    with col3:
                        new_team_members = st.multiselect(
                            "Team Members",
                            ["Team Member 1", "Team Member 2", "Team Member 3", "Team Member 4"],
                            default=task['team_members'],
                            key=f"edit_task_team_{task_id}"
                        )
                        task['team_members'] = new_team_members
                        calculate_rollups(selected_project_id)
                    with col4:
                        if st.button("Delete Task", key=f"del_task_{task_id}"):
                            delete_task(selected_project_id, del_id, task_id)
                            st.rerun()

    # Visualization section
    st.header("Visualizations")

    # Prepare data for sunburst chart
    sunburst_data = []
    for del_id, deliverable in project['deliverables'].items():
        # Add deliverable level
        sunburst_data.append({
            'id': deliverable['id'],
            'parent': project['id'],
            'name': deliverable['title'],
            'value': deliverable['effort']
        })
        # Add task level
        for task_id, task in deliverable['tasks'].items():
            sunburst_data.append({
                'id': task_id,
                'parent': deliverable['id'],
                'name': task['title'],
                'value': task['effort']
            })

    # Add project level
    sunburst_data.append({
        'id': project['id'],
        'parent': '',
        'name': project['title'],
        'value': sum(d['effort'] for d in project['deliverables'].values())
    })

    df_sunburst = pd.DataFrame(sunburst_data)

    if not df_sunburst.empty:
        fig = px.sunburst(
            df_sunburst,
            ids='id',
            parents='parent',
            names='name',
            values='value',
            title='Project Hierarchy and Effort Distribution'
        )
        st.plotly_chart(fig)

else:
    st.info("No projects yet. Create a new project using the sidebar.")


#===========================================================================

