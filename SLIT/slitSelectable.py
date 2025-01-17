import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, GridOptionsBuilder

def main():
    st.title("st_aggrid with Dropdown Editable Column")

    # Sample Data
    data = {'Product': ['A', 'B', 'C', 'D'],
            'Category': ['Electronics', 'Clothing', 'Food', 'Electronics'],
            'Quantity': [10, 5, 20, 15],
            'Status': ['Pending', 'Shipped', 'Delivered', 'Processing']}
    df = pd.DataFrame(data)

    # Dropdown Options for 'Status' column
    status_options = ['Pending', 'Shipped', 'Delivered', 'Processing', 'Cancelled', 'Returned']

    # Configure Grid Options
    gb = GridOptionsBuilder.from_dataframe(df)

    # Make 'Status' column editable and add dropdown
    gb.configure_column('Status', editable=True, cellEditor='agSelectCellEditor',
                        cellEditorParams={'values': status_options})

    # Configure other columns (optional)
    gb.configure_column('Product', editable=False)  # Make Product read-only
    gb.configure_column('Category', editable=False)
    gb.configure_column('Quantity', type=['numericColumn', 'numberFilter', 'editable']) # numeric and editable

    gb.configure_default_column(min_column_width=100) # Set minimum column width

    gridOptions = gb.build()

    # Display the grid
    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        height=350,
        width='100%',
        update_mode=GridUpdateMode.MODEL_CHANGED, # Update dataframe on cell edit
        allow_unsafe_jscode=True, # Set it to True to allow js function to be injected
        enable_enterprise_modules=False,
        fit_columns_on_grid_load=False,
        )

    if grid_response['data'] is not None:
        updated_df = grid_response['data']
        st.subheader("Updated DataFrame:")
        st.dataframe(updated_df)  # Display the updated DataFrame

if __name__ == "__main__":
    main()
