x="""
I need a streamlit app which has
1. Deliverables with completion dates
2. One or more releases - each release includes one or more deliverables
3. Let us create some sample data for  say 10 deliverables and  3 releases spread over 6 months
4.  Want to display the deliverables and releases on a timeline
5.  Furthermore want to be able to change the deliverable dates interactively and see the effect on release dates
"""

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

    # Sample deliverables
    deliverable_names = [
        "User Authentication Module",
        "Database Schema Design",
        "API Integration",
        "Frontend Dashboard",
        "Payment Gateway",
        "Reporting Module",
        "Mobile App Version",
        "Security Audit",
        "Performance Optimization",
        "Documentation"
    ]

    # Generate random dates for deliverables
    for i, name in enumerate(deliverable_names):
        random_days = random.randint(15, 180)
        completion_date = start_date + timedelta(days=random_days)
        deliverables.append({
            'Deliverable': name,
            'Completion Date': completion_date,
            'Release': f"R{(i // 3) + 1}"  # Assign 3-4 deliverables per release
        })

    st.session_state.deliverables_data = pd.DataFrame(deliverables)

# Title
st.title("Project Timeline Manager")

# Create two columns
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Deliverables")

    # Edit deliverables
    edited_df = st.data_editor(
        st.session_state.deliverables_data,
        column_config={
            "Completion Date": st.column_config.DateColumn(
                "Completion Date",
                min_value=datetime(2024, 1, 1),
                max_value=datetime(2024, 12, 31),
                format="DD-MM-YYYY",
            )
        },
        hide_index=True,
    )

    # Update the session state with edited data
    st.session_state.deliverables_data = edited_df

with col2:
    st.subheader("Timeline View")

    # Calculate release dates (latest date among deliverables in each release)
    release_dates = edited_df.groupby('Release')['Completion Date'].max().reset_index()
    release_dates['Task'] = release_dates['Release']
    release_dates['Start'] = release_dates['Completion Date'] - timedelta(days=1)
    release_dates['Finish'] = release_dates['Completion Date']

    # Prepare data for timeline
    df_plot = pd.DataFrame({
        'Task': edited_df['Deliverable'],
        'Start': edited_df['Completion Date'] - timedelta(days=5),  # 5 days before completion
        'Finish': edited_df['Completion Date'],
        'Resource': edited_df['Release']
    })

    # Combine deliverables and releases for the timeline
    df_plot = pd.concat([df_plot, release_dates[['Task', 'Start', 'Finish', 'Resource']]])

    # Create the timeline
    fig = ff.create_gantt(
        df_plot,
        colors={f'R{i+1}': f'rgb({random.randint(100,255)}, {random.randint(100,255)}, {random.randint(100,255)})' 
                for i in range(3)},
        index_col='Resource',
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True
    )

    # Update layout
    fig.update_layout(
        height=600,
        title_text="Project Timeline",
        xaxis_title="Date",
    )

    # Display the timeline
    st.plotly_chart(fig, use_container_width=True)

# Display release summary
st.subheader("Release Summary")
release_summary = release_dates[['Release', 'Completion Date']].sort_values('Completion Date')
st.dataframe(release_summary, hide_index=True)

