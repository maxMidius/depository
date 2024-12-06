import streamlit as st  
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode  
import pandas as pd  

def main():  
    st.title('Editable Data Grid Example')  

    # Sample data  
    data = {  
        'ID': [1, 2, 3],  
        'Name': ['Alice', 'Bob', 'Charlie'],  
        'Age': [25, 30, 35],  
        'Job': ['Engineer', 'Doctor', 'Artist']  
    }  
    df = pd.DataFrame(data)  

    # Set up grid options  
    gb = GridOptionsBuilder.from_dataframe(df)  
    gb.configure_default_column(editable=True, groupable=True)  
    gb.configure_column("Job", editable=True, cellEditor='agSelectCellEditor',  
                        cellEditorParams={'values': ['Engineer', 'Doctor', 'Artist', 'Lawyer', 'Chef']})  
    gb.configure_grid_options(domLayout='normal')  
    gridOptions = gb.build()  

    # Grid update mode  
    grid_response = AgGrid(  
        df,  
        gridOptions=gridOptions,  
        height=300,  
        width='100%',  
        data_return_mode=DataReturnMode.AS_INPUT,  
        update_mode=GridUpdateMode.MODEL_CHANGED,  
        fit_columns_on_grid_load=False,  
        enable_enterprise_modules=True,  
        allow_unsafe_jscode=True,  # Set it to True to allow js injection  
    )  

    new_df = grid_response['data']  
    st.write('Updated Dataframe:', new_df)  

    # Button to add rows  
    if st.button('Add Row'):  
        new_df = new_df.append({'ID': new_df['ID'].max() + 1, 'Name': '', 'Age': 0, 'Job': ''}, ignore_index=True)  
        AgGrid(new_df)  

    # Button to delete the last row  
    if st.button('Delete Last Row'):  
        if len(new_df) > 0:  
            new_df = new_df[:-1]  
        AgGrid(new_df)  

if __name__ == "__main__":  
    main()  
