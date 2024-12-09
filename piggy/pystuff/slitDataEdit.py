import streamlit as st    
import pandas as pd    
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode    
from datetime import datetime    
import uuid    

# Set page config    
st.set_page_config(page_title="AG-Grid Example", layout="wide")    

# Initialize session state for data if it doesn't exist    
if 'data' not in st.session_state:    
    # Create initial sample data    
    initial_data = {    
        'Department': ['IT', 'HR', 'IT'],  # Added Department column  
        'ID': [str(uuid.uuid4()) for _ in range(3)],    
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],    
        'Age': [30, 25, 35],    
        'Birth Date': ['1993-01-15', '1998-05-20', '1988-11-30'],    
        'Active': [True, False, True]    
    }    
    st.session_state.data = pd.DataFrame(initial_data)    

def add_row():    
    new_row = pd.DataFrame({    
        'Department': ['New Department'],  # Added Department  
        'ID': [str(uuid.uuid4())],    
        'Name': ['New Employee'],    
        'Age': [0],    
        'Birth Date': [datetime.now().strftime('%Y-%m-%d')],    
        'Active': [True]    
    })    
    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)    
    st.rerun()  

def delete_selected_rows(grid_response):    
    selected_rows = grid_response.selected_rows    
    if len(selected_rows) > 0:    
        selected_df = pd.DataFrame(selected_rows)    
        indices_to_delete = st.session_state.data.index[    
            st.session_state.data['ID'].isin(selected_df['ID'])    
        ]    
        st.session_state.data = st.session_state.data.drop(indices_to_delete).reset_index(drop=True)    

def update_data(grid_response):    
    st.session_state.data = pd.DataFrame(grid_response['data'])    

st.title("AG-Grid Example with CRUD Operations")    

# Add row button    
if st.button("Add Row"):    
    add_row()    

# Configure grid options    
gb = GridOptionsBuilder.from_dataframe(st.session_state.data)    
gb.configure_default_column(editable=True, resizable=True)    

# Configure specific column types    
gb.configure_column('Department', rowGroup=True)  # Enable grouping for Department  
gb.configure_column('ID', editable=False)    
gb.configure_column('Name')    
gb.configure_column('Age', type=['numericColumn', 'numberColumnFilter'])    
gb.configure_column('Birth Date', type=['dateColumn', 'dateColumnFilter'])    
gb.configure_column('Active', type=['booleanColumn', 'booleanColumnFilter'])    

# Enable selection    
gb.configure_selection(selection_mode='multiple', use_checkbox=True)    

# Configure grouping options  
gb.configure_grid_options(  
    groupDefaultExpanded=1,  # Expand first level by default  
    groupSelectsChildren=True,  # Selecting group selects children  
    groupSelectsFiltered=True,  
    autoGroupColumnDef={  
        "headerName": "Department",  
        "minWidth": 200,  
        "cellRendererParams": {  
            "suppressCount": False,  # Show count of employees in group  
        }  
    }  
)  

grid_options = gb.build()    

# Display the grid    
grid_response = AgGrid(    
    st.session_state.data,    
    grid_options,    
    update_mode=GridUpdateMode.MODEL_CHANGED,    
    allow_unsafe_jscode=True,    
    theme='material'    
)    

# Update the data when grid changes    
update_data(grid_response)    

# Delete selected rows button    
if st.button("Delete Selected Rows"):    
    delete_selected_rows(grid_response)    
    st.rerun()  

# Add department statistics  
st.write("### Department Statistics")  
dept_stats = st.session_state.data.groupby('Department').agg({  
    'ID': 'count',  
    'Age': ['mean', 'min', 'max']  
}).round(2)  

dept_stats.columns = ['Employee Count', 'Average Age', 'Min Age', 'Max Age']  
st.write(dept_stats)  

# Display the updated data below the grid    
st.write("Current Data:")    
st.write(st.session_state.data)    
