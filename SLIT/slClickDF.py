import streamlit as st

# Sample data
data = {
    'first_column': [1, 2, 3, 4],
    'second_column': [5, 6, 7, 8],
    'third_column': ['A', 'B', 'C', 'D']
}

# Function to handle cell clicks
def handle_click(column, index):
    st.write(f"Clicked cell: {column}, {index}")

# Create a DataFrame with clickable cells
df = st.dataframe(data, on_click=handle_click)

# Add some additional styling to the DataFrame (optional)
df.css("{color: red; font-weight: bold;}")
