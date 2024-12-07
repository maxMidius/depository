import streamlit as st  
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode  
import pandas as pd  
from datetime import datetime  
import numpy as np  

# Initialize session state for the dataframe if it doesn't exist  
if 'df' not in st.session_state:  
    # Create sample data with different column types  
    st.session_state.df = pd.DataFrame({  
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],  
        'Age': [25, 30, 35],  
        'Active': [True, False, True],  
        'Join Date': [datetime.now().date() for _ in range(3)],  
        'Salary': [50000.0, 65000.0, 75000.0]  
    })  

# Initialize selected rows in session state  
if 'selected_rows' not in st.session_state:  
    st.session_state.selected_rows = []  

st.title('Advanced AG Grid Example')  

# Custom CSS for the grid  
grid_css = {  
    '.ag-cell-inline-editing': {'padding': '10px !important'},  
    '.ag-header-cell-label': {'font-weight': 'bold'}  
}  

def handle_selection(grid_return):  
    st.session_state.selected_rows = grid_return['selected_rows']  

# Configure column definitions with different types  
column_defs = [  
    {  
        'field': 'Name',  
        'editable': True,  
        'resizable': True,  
        'sortable': True,  
        'filter': True  
    },  
    {  
        'field': 'Age',  
        'editable': True,  
        'type': 'numberColumn',  
        'filter': 'agNumberColumnFilter'  
    },  
    {  
        'field': 'Active',  
        'editable': True,  
        'type': 'boolean',  
        'cellRenderer': 'agCheckboxCellRenderer'  
    },  
    {  
        'field': 'Join Date',  
        'editable': True,  
        'type': 'dateColumn',  
        'filter': 'agDateColumnFilter'  
    },  
    {  
        'field': 'Salary',  
        'editable': True,  
        'type': 'numberColumn',  
        'valueFormatter': JsCode("""  
            function(params) {  
                return '$' + params.value.toLocaleString();  
            }  
        """)  
    }  
]  

# Button to add a new row  
if st.button('Add Row'):  
    new_row = pd.DataFrame({  
        'Name': ['New Employee'],  
        'Age': [0],  
        'Active': [True],  
        'Join Date': [datetime.now().date()],  
        'Salary': [0.0]  
    })  
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)  

# Configure grid options  
gb = GridOptionsBuilder.from_dataframe(st.session_state.df)  
gb.configure_default_column(editable=True, resizable=True)  
gb.configure_selection(selection_mode='multiple', use_checkbox=True)  
gb.configure_grid_options(enableRangeSelection=True)  

# Apply column definitions  
for col_def in column_defs:  
    gb.configure_column(**col_def)  

grid_options = gb.build()  

# Display the grid  
grid_response = AgGrid(  
    st.session_state.df,  
    gridOptions=grid_options,  
    update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,  
    fit_columns_on_grid_load=True,  
    allow_unsafe_jscode=True,  
    custom_css=grid_css,  
    height=400,  
    key='grid_1',  
    on_grid_ready=handle_selection  
)  

# Update the dataframe with any edits  
st.session_state.df = pd.DataFrame(grid_response['data'])  

# Delete selected rows  
if st.button('Delete Selected Rows'):  
    if st.session_state.selected_rows:  
        # Get names of selected rows  
        selected_names = [row['Name'] for row in st.session_state.selected_rows]  
        # Create mask for rows to keep  
        mask = ~st.session_state.df['Name'].isin(selected_names)  
        # Update dataframe  
        st.session_state.df = st.session_state.df[mask]  
        # Clear selected rows  
        st.session_state.selected_rows = []  
        # Rerun to refresh the grid  
        st.experimental_rerun()  

# Debug information  
st.write("Selected Rows:")  
st.write(st.session_state.selected_rows)  

st.write("Current DataFrame:")  
st.write(st.session_state.df)  
