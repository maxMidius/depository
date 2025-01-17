import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import random

# Set page configuration
st.set_page_config(layout="wide", page_title="Project Timeline Manager")

# Initialize session state for data if it doesn't exist
if 'deliverables_data' not in st.session_state:
    # Generate sample data
    start_date = datetime(2024, 1, 1)
    deliverables = []

    # Sample deliverables with default durations (in days)
    default_deliverables = [
        ("User Authentication Module", 15, "R1"),
        ("Database Schema Design", 30, "R1"),
        ("API Integration", 45, "R1"),
        ("Frontend Dashboard", 60, "R2"),
        ("Payment Gateway", 75, "R2"),
        ("Reporting Module", 90, "R2"),
        ("Mobile App Version", 105, "R3"),
        ("Security Audit", 120, "R3"),
        ("Performance Optimization", 135, "R3"),
        ("Documentation", 150, "R3")
    ]

    # Create deliverables with dates
    for name, days, release in default_deliverables:
        completion_date = start_date + timedelta(days=days)
        deliverables.append({
            'Deliverable': name,
            'Completion Date': completion_date,
            'Release': release,
            'Duration': 5  # Default duration for each task in days
        })

    st.session_state.deliverables_data = pd.DataFrame(deliverables)

# Title and description
st.title("Interactive Project Timeline Manager")
st.write("Edit dates and durations to see how they affect the timeline and releases.")

# Create two columns
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Edit Deliverables")

    # Create a form for editing
    edited_df = st.data_editor(
        st.session_state.deliverables_data,
        column_config={
            "Completion Date": st.column_config.DateColumn(
                "Completion Date",
                min_value=datetime(2024, 1, 1),
                max_value=datetime(2024, 12, 31),
                format="DD-MM-YYYY",
            ),
            "Duration": st.column_config.NumberColumn(
                "Duration (days)",
                min_value=1,
                max_value=30,
                step=1,
            )
        },
        hide_index=True,
        num_rows="fixed",
    )

    # Update the session state with edited data
    st.session_state.deliverables_data = edited_df

with col2:
    st.subheader("Timeline View")

    # Calculate start dates based on completion dates and duration
    edited_df['Start'] = edited_df['Completion Date'] - pd.to_timedelta(edited_df['Duration'], unit='D')

    # Calculate release dates
    release_dates = edited_df.groupby('Release')['Completion Date'].max().reset_index()
    release_dates['Task'] = release_dates['Release']
    release_dates['Start'] = release_dates['Completion Date'] - timedelta(days=1)
    release_dates['Finish'] = release_dates['Completion Date']
    release_dates['Resource'] = release_dates['Release']

    # Prepare data for timeline
    df_plot = pd.DataFrame({
        'Task': edited_df['Deliverable'],
        'Start': edited_df['Start'],
        'Finish': edited_df['Completion Date'],
        'Resource': edited_df['Release']
    })

    # Combine deliverables and releases for the timeline
    df_plot = pd.concat([df_plot, release_dates[['Task', 'Start', 'Finish', 'Resource']]])

    # Get unique resources and create color dictionary
    unique_resources = df_plot['Resource'].unique()
    colors_dict = {
        resource: f'rgb({random.randint(100,255)}, {random.randint(100,255)}, {random.randint(100,255)})'
        for resource in unique_resources
    }

    # Create the timeline
    fig = ff.create_gantt(
        df_plot,
        colors=colors_dict,
        index_col='Resource',
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True,
        height=400,
    )

    # Update layout
    fig.update_layout(
        title_text="Project Timeline",
        xaxis_title="Date",
        height=600,
    )

    # Display the timeline
    st.plotly_chart(fig, use_container_width=True)

# Display release summary
st.subheader("Release Summary")
release_summary = release_dates[['Release', 'Completion Date']].sort_values('Completion Date')
st.dataframe(release_summary, hide_index=True)

# Add some metrics
st.subheader("Project Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    project_duration = (edited_df['Completion Date'].max() - edited_df['Start'].min()).days
    st.metric("Total Project Duration", f"{project_duration} days")

with col2:
    avg_task_duration = edited_df['Duration'].mean()
    st.metric("Average Task Duration", f"{avg_task_duration:.1f} days")

with col3:
    total_tasks = len(edited_df)
    st.metric("Total Deliverables", total_tasks)
