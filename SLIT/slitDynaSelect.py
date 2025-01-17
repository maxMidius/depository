import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Define the options for dropdowns
CATEGORY_OPTIONS = ['Fruits', 'Vegetables']
DEPENDENT_OPTIONS = {
    'Fruits': ['Apples', 'Bananas'],
    'Vegetables': ['Cabbage', 'Cauliflower', 'Broccoli']
}

# Initialize data if not exists
if 'data' not in st.session_state:
    initial_data = {
        'Category': ['Fruits', 'Vegetables', 'Fruits'],
        'Example': ['Apples', 'Cabbage', 'Bananas'],
        'Quantity': [10, 5, 8]
    }
    st.session_state.data = pd.DataFrame(initial_data)

# JavaScript function to handle dependent dropdown
category_dependent_dropdown = JsCode("""
function categoryValueFormatter(params) {
    if (params.value === undefined) return '';
    return params.value;
}

function exampleValueFormatter(params) {
    if (params.value === undefined) return '';
    return params.value;
}

function exampleValueGetter(params) {
    if (params.data === undefined) return '';
    return params.data.Example;
}

function exampleValueSetter(params) {
    if (params.data === undefined) return false;
    params.data.Example = params.newValue;
    return true;
}

function getExampleValues(params) {
    const category = params.data.Category;
    if (category === 'Fruits') return ['Apples', 'Bananas'];
    if (category === 'Vegetables') return ['Cabbage', 'Cauliflower', 'Broccoli'];
    return [];
}
""")

def create_grid():
    gb = GridOptionsBuilder.from_dataframe(st.session_state.data)

    # Configure Category column
    gb.configure_column('Category',
                       editable=True,
                       cellEditor='agSelectCellEditor',
                       cellEditorParams={'values': CATEGORY_OPTIONS})

    # Configure Example column with dependent dropdown
    gb.configure_column('Example',
                       editable=True,
                       cellEditor='agSelectCellEditor',
                       valueFormatter=category_dependent_dropdown + '.exampleValueFormatter',
                       valueGetter=category_dependent_dropdown + '.exampleValueGetter',
                       valueSetter=category_dependent_dropdown + '.exampleValueSetter',
                       cellEditorParams={
                           'values': JsCode('params => getExampleValues(params)')
                       })

    # Configure Quantity column
    gb.configure_column('Quantity', editable=True)

    # Configure grid options
    gb.configure_grid_options(
        onCellValueChanged=JsCode("""
        function(params) {
            if (params.colDef.field === 'Category') {
                params.data.Example = '';
            }
        }
        """)
    )

    return gb.build()

# Create Streamlit app
st.title('Editable Grid with Dependent Dropdowns')

grid_options = create_grid()
grid_response = AgGrid(
    st.session_state.data,
    grid_options,
    allow_unsafe_jscode=True,
    reload_data=False
)

# Update session state if grid data changes
if grid_response['data'] is not None:
    st.session_state.data = pd.DataFrame(grid_response['data'])

# Display current data
st.write("Current Data:")
st.write(st.session_state.data)

# Add new row button
if st.button("Add New Row"):
    new_row = pd.DataFrame({
        'Category': ['Fruits'],
        'Example': [''],
        'Quantity': [0]
    })
    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
    st.rerun()
