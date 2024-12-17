import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="My Company",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to style the header and layout
st.markdown("""
    <style>
    /* Hide default Streamlit header */
    .stApp header {
        background-color: transparent;
    }

    /* Style for top banner */
    .top-banner {
        background-color: #007BFF;
        padding: 1rem;
        margin: -6rem -4rem 2rem;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }

    /* Adjust sidebar spacing */
    .css-1d391kg {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Top banner
st.markdown('<div class="top-banner">My Company</div>', unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 4])

# Sidebar content
with st.sidebar:
    st.markdown("### 🏠 Home")
    st.markdown("---")
    st.markdown("This is the collapsible sidebar")
    st.markdown("Navigation could go here")

# Main content area
st.markdown("### Data Table")
data = {
    'Name': ['John Doe', 'Jane Smith'],
    'Department': ['IT', 'HR'],
    'Status': ['Active', 'Active']
}

# Create a DataFrame
import pandas as pd
df = pd.DataFrame(data)

# Display the table
st.table(df)

# Additional content can be added here
st.markdown("### Additional Information")
st.write("Add more content here as needed")

# You can add more sections, charts, or other components below
