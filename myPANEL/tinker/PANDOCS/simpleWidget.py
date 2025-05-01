import panel as pn
import param

# Define a simple parameterized class
class MyWidget(param.Parameterized):
    value = param.Integer(default=0, bounds=(0, 100))

    def view(self):
        return pn.Column(
            pn.widgets.IntSlider.from_param(self.param.value),
            pn.bind(self.callback, self.param.value)
        )

    def callback(self, value):
        return f'The slider value is: {value}'

# Instantiate the class
widget = MyWidget()

# Make the panel servable
widget.view().servable("My Widget Demo")

# Start the server
pn.serve()
