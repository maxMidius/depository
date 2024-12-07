import streamlit as st  
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode  
import pandas as pd  

def main():  
    st.title('Editable Data Grid Example')  

    # Initial sample data  
    if "data" not in st.session_state:  
        st.session_state.data = pd.DataFrame({  
            'ID': [1, 2, 3],  
            'Name': ['Alice', 'Bob', 'Charlie'],  
            'Age': [25, 30, 35],  
            'Job': ['Engineer', 'Doctor', 'Artist']  
        })  

    # Load the data from session state  
    df = st.session_state.data  

    # Set up grid options  
    gb = GridOptionsBuilder.from_dataframe(df)  
    gb.configure_default_column(editable=True, groupable=True)  
    gb.configure_column("Job", editable=True, cellEditor='agSelectCellEditor',  
                        cellEditorParams={'values': ['Engineer', 'Doctor', 'Artist', 'Lawyer', 'Chef']})  
    gb.configure_grid_options(domLayout='normal')  
    gridOptions = gb.build()  

    # Display the grid  
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

    # Get the updated data from the grid  
    updated_df = pd.DataFrame(grid_response['data'])  

    # Buttons to add or delete rows  
    col1, col2 = st.columns(2)  

    with col1:  
        if st.button('Add Row'):  
            # Add a new row with default values  
            new_row = {'ID': updated_df['ID'].max() + 1 if not updated_df.empty else 1,  
                       'Name': '',  
                       'Age': 0,  
                       'Job': ''}  
            updated_df = pd.concat([updated_df, pd.DataFrame([new_row])], ignore_index=True)  

    with col2:  
        if st.button('Delete Selected Row'):  
            # Delete the selected row(s) based on the AgGrid selection  
            selected_rows = grid_response['selected_rows']  
            if selected_rows:  
                selected_ids = [row['ID'] for row in selected_rows]  
                updated_df = updated_df[~updated_df['ID'].isin(selected_ids)]  
            else:  
                st.warning("No row selected for deletion!")  

    # Save the updated data back to session state  
    st.session_state.data = updated_df  

    # Display the updated dataframe  
    st.write('Updated Dataframe:')  
    st.dataframe(updated_df)  

if __name__ == "__main__":  
    main()  
