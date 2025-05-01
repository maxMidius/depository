import panel as pn
import pandas as pd 
import hvplot.pandas 
import holoviews as hv

# Initialize extensions
pn.extension('dataframe')
hv.extension('bokeh')

# Sample DataFrame
df = pd.DataFrame({
    'Category': ['A', 'B', 'A', 'B'],
    'Value': [10, 20, 30, 40]
})

# Create widgets
category_filter = pn.widgets.Select(name="Category", options=['All', 'A', 'B'], value='All')
value_slider = pn.widgets.IntSlider(name="Value Threshold", start=0, end=50, step=5, value=0)

# Define a function to filter the DataFrame
@pn.depends(category_filter, value_slider)
def get_filtered_df(category, threshold):
    if category == 'All':
        filtered = df[df['Value'] > threshold]
    else:
        filtered = df[(df['Category'] == category) & (df['Value'] > threshold)]
    return filtered

# Create a bar chart
@pn.depends(category_filter, value_slider)
def get_bar_chart(category, threshold):
    filtered = get_filtered_df(category, threshold)
    if filtered.empty:
        return hv.Text(0, 0, "No data matches the filter criteria")
    return filtered.hvplot.bar(x='Category', y='Value', title="Filtered Data")

# Display the dashboard
pn.Column(
    "## Interactive Data Exploration",
    pn.Row(
        pn.Column("### Filters", category_filter, value_slider),
        pn.Column("### Data", pn.pane.DataFrame(get_filtered_df))
    ),
    "### Chart",
    get_bar_chart
).servable()