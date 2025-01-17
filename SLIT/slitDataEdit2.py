import streamlit as st  
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode  
import pandas as pd  
import numpy as np  

# Initialize session state for the dataframe if it doesn't exist  
if 'df' not in st.session_state:  
    # Create sample data  
    st.session_state.df = pd.DataFrame({  
        'Name': ['John', 'Jane', 'Bob'],  
        'Age': [25, 30, 35],  
        'City': ['New York', 'London', 'Paris']  
    })  

st.title('AG Grid Example with Add/Delete Rows')  

# Button to add a new row  
if st.button('Add Row'):  
    new_row = pd.DataFrame({  
        'Name': ['New Name'],  
        'Age': [0],  
        'City': ['New City']  
    })  
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)  

# Configure grid options  
gb = GridOptionsBuilder.from_dataframe(st.session_state.df)  
gb.configure_default_column(editable=True)  
gb.configure_selection(selection_mode='multiple', use_checkbox=True)  
gb.configure_grid_options(enableRangeSelection=True)  

grid_options = gb.build()  

# Display the grid  
grid_response = AgGrid(  
    st.session_state.df,  
    gridOptions=grid_options,  
    update_mode=GridUpdateMode.MODEL_CHANGED,  
    fit_columns_on_grid_load=True,  
    allow_unsafe_jscode=True  
)  

# Get the updated dataframe  
updated_df = grid_response['data']  
st.session_state.df = pd.DataFrame(updated_df)  

# Delete selected rows  
if st.button('Delete Selected Rows'):  
    selected_rows = grid_response['selected_rows']  
    if selected_rows:  
        # Get indices of selected rows  
        selected_indices = [i for i, row in st.session_state.df.iterrows()   
                          if row.to_dict() in selected_rows]  
        # Drop selected rows  
        st.session_state.df = st.session_state.df.drop(selected_indices)  
        st.experimental_rerun()  

# Display the current dataframe (optional)  
st.write("Current DataFrame:")  
st.write(st.session_state.df)  
