import streamlit as st
import plotly.express as px
import pandas as pd

# Data for the hierarchy
data = {
    "Project": ["Project A", "Project A", "Project A", "Project A", "Project A"],
    "Deliverable": ["Deliverable 1", "Deliverable 1", "Deliverable 2", "Deliverable 2", "Release 1"],
    "Task": ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"]
}

df = pd.DataFrame(data)

# Create a sunburst chart
fig = px.sunburst(
    df,
    path=["Project", "Deliverable", "Task"],
    title="Project to Deliverables to Tasks",
    width=800,
    height=600
)

# Display in Streamlit
st.plotly_chart(fig)
