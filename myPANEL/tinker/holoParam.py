import panel as pn
import pandas as pd
import holoviews as hv
import param

# Initialize extensions
pn.extension('dataframe')
hv.extension('bokeh')

# Sample DataFrame
df = pd.DataFrame({
    'Category': ['A', 'B', 'A', 'B'],
    'Value': [10, 20, 30, 40]
})

# Create a reactive class to handle filtering
class DataExplorer(param.Parameterized):
    category = param.Selector(objects=['All', 'A', 'B'], default='All')
    value_threshold = param.Integer(default=0, bounds=(0, 50))
    
    def get_filtered_data(self):
        if self.category == 'All':
            filtered = df[df['Value'] > self.value_threshold]
        else:
            filtered = df[(df['Category'] == self.category) & (df['Value'] > self.value_threshold)]
        return filtered
    
    @param.depends('category', 'value_threshold')
    def view_table(self):
        return pn.pane.DataFrame(self.get_filtered_data(), width=400)
    
    @param.depends('category', 'value_threshold')
    def view_chart(self):
        data = self.get_filtered_data()
        return hv.Bars(data, kdims=['Category'], vdims=['Value']).opts(
            title="Filtered Data",
            width=400, height=300
        )

# Create the explorer instance
explorer = DataExplorer()

# Create widgets from the parameters
category_select = pn.widgets.Select.from_param(explorer.param.category)
value_slider = pn.widgets.IntSlider.from_param(explorer.param.value_threshold)

# Display the dashboard
pn.Column(
    "## Interactive Data Exploration",
    pn.Row(
        pn.Column("### Filters", category_select, value_slider),
        pn.Column("### Data", explorer.view_table)
    ),
    "### Chart",
    explorer.view_chart
).servable()