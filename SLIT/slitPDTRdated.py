import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Sample Data
deliverables_data = {
    'deliverable_id': ['D1', 'D2', 'D3', 'D4', 'D5'],
    'deliverable_name': [
        'User Authentication Module', 
        'Database Schema', 
        'API Integration',
        'UI Dashboard',
        'Report Generator'
    ],
    'completion_date': [
        '2024-03-15',
        '2024-03-30',
        '2024-04-15',
        '2024-05-01',
        '2024-05-15'
    ]
}

# Release to Deliverables mapping
release_deliverables = {
    'R1.0': ['D1', 'D2'],
    'R1.5': ['D3'],
    'R2.0': ['D4', 'D5']
}

# Create DataFrame
deliverables_df = pd.DataFrame(deliverables_data)
deliverables_df['completion_date'] = pd.to_datetime(deliverables_df['completion_date'])

# Calculate release dates
release_dates = {}
for release, delivs in release_deliverables.items():
    max_date = deliverables_df[
        deliverables_df['deliverable_id'].isin(delivs)
    ]['completion_date'].max()
    release_dates[release] = max_date

# Create Streamlit app
st.title("Deliverables and Releases Timeline")

# Create figure
fig = go.Figure()

# Add deliverables as markers
fig.add_trace(go.Scatter(
    x=deliverables_df['completion_date'],
    y=deliverables_df['deliverable_name'],
    mode='markers+text',
    name='Deliverables',
    marker=dict(size=15, color='blue'),
    text=deliverables_df['deliverable_id'],
    textposition="middle right"
))
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Sample Data
deliverables_data = {
    'deliverable_id': ['D1', 'D2', 'D3', 'D4', 'D5'],
    'deliverable_name': [
        'User Authentication Module', 
        'Database Schema', 
        'API Integration',
        'UI Dashboard',
        'Report Generator'
    ],
    'completion_date': [
        '2024-03-15',
        '2024-03-30',
        '2024-04-15',
        '2024-05-01',
        '2024-05-15'
    ]
}

# Release to Deliverables mapping
release_deliverables = {
    'R1.0': ['D1', 'D2'],
    'R1.5': ['D3'],
    'R2.0': ['D4', 'D5']
}

# Create DataFrame
deliverables_df = pd.DataFrame(deliverables_data)
deliverables_df['completion_date'] = pd.to_datetime(deliverables_df['completion_date'])

# Calculate release dates
release_dates = {}
for release, delivs in release_deliverables.items():
    max_date = deliverables_df[
        deliverables_df['deliverable_id'].isin(delivs)
    ]['completion_date'].max()
    release_dates[release] = max_date

# Create Streamlit app
st.title("Deliverables and Releases Timeline")

# Create figure
fig = go.Figure()

# Add deliverables as markers
fig.add_trace(go.Scatter(
    x=deliverables_df['completion_date'],
    y=deliverables_df['deliverable_name'],
    mode='markers+text',
    name='Deliverables',
    marker=dict(size=15, color='blue'),
    text=deliverables_df['deliverable_id'],
    textposition="middle right"
))

# Add releases as separate scatter points
for release, date in release_dates.items():
    fig.add_trace(go.Scatter(
        x=[date],
        y=[max(deliverables_df['deliverable_name'])],  # Position at top
        mode='markers+text',
        name=release,
        marker=dict(size=20, color='red', symbol='diamond'),
        text=[release],
        textposition="top center"
    ))

# Update layout
fig.update_layout(
    title="Deliverables and Releases Timeline",
    xaxis_title="Date",
    yaxis_title="Deliverables",
    height=500,
    showlegend=True,
    xaxis=dict(
        type='date',
        tickformat='%Y-%m-%d'
    )
)

# Display the timeline
st.plotly_chart(fig)

# Display tables
col1, col2 = st.columns(2)

with col1:
    st.subheader("Deliverables")
    display_df = deliverables_df.copy()
    display_df['completion_date'] = display_df['completion_date'].dt.strftime('%Y-%m-%d')
    st.dataframe(display_df)

with col2:
    st.subheader("Release Dates")
    release_dates_df = pd.DataFrame([
        {"Release": k, "Effective Date": v.strftime('%Y-%m-%d')}
        for k, v in release_dates.items()
    ])
    st.dataframe(release_dates_df)

# Display release contents
st.subheader("Release Contents")
for release, delivs in release_deliverables.items():
    st.write(f"**{release}** includes:")
    delivs_info = deliverables_df[deliverables_df['deliverable_id'].isin(delivs)].copy()
    delivs_info['completion_date'] = delivs_info['completion_date'].dt.strftime('%Y-%m-%d')
    st.table(delivs_info[['deliverable_id', 'deliverable_name', 'completion_date']])
# Add releases as separate scatter points
for release, date in release_dates.items():
    fig.add_trace(go.Scatter(
        x=[date],
        y=[max(deliverables_df['deliverable_name'])],  # Position at top
        mode='markers+text',
        name=release,
        marker=dict(size=20, color='red', symbol='diamond'),
        text=[release],
        textposition="top center"
    ))

# Update layout
fig.update_layout(
    title="Deliverables and Releases Timeline",
    xaxis_title="Date",
    yaxis_title="Deliverables",
    height=500,
    showlegend=True,
    xaxis=dict(
        type='date',
        tickformat='%Y-%m-%d'
    )
)

# Display the timeline
st.plotly_chart(fig)

# Display tables
col1, col2 = st.columns(2)

with col1:
    st.subheader("Deliverables")
    display_df = deliverables_df.copy()
    display_df['completion_date'] = display_df['completion_date'].dt.strftime('%Y-%m-%d')
    st.dataframe(display_df)

with col2:
    st.subheader("Release Dates")
    release_dates_df = pd.DataFrame([
        {"Release": k, "Effective Date": v.strftime('%Y-%m-%d')}
        for k, v in release_dates.items()
    ])
    st.dataframe(release_dates_df)

# Display release contents
st.subheader("Release Contents")
for release, delivs in release_deliverables.items():
    st.write(f"**{release}** includes:")
    delivs_info = deliverables_df[deliverables_df['deliverable_id'].isin(delivs)].copy()
    delivs_info['completion_date'] = delivs_info['completion_date'].dt.strftime('%Y-%m-%d')
    st.table(delivs_info[['deliverable_id', 'deliverable_name', 'completion_date']])
