import param
import panel as pn
from panel.custom import ReactComponent

class MaterialComponent(ReactComponent):
    """Base class for Material UI components"""

    _importmap = {
        "imports": {
            "@mui/material/": "https://esm.sh/@mui/material@5.14.20/",  # Use a valid version
        }
    }


class Button(MaterialComponent):
    """Material UI Button component"""

    disabled = param.Boolean(default=False)
    label = param.String(default='')
    variant = param.Selector(objects=["contained", "outlined", "text"])

    _esm = """
    import Button from '@mui/material/Button';

    export function render({ model }) {
      const [label] = model.useState("label")
      const [variant] = model.useState("variant")
      const [disabled] = model.useState("disabled")
      return (
        <Button disabled={disabled} variant={variant}>{label || 'Click me!'}</Button>
      )
    }
    """


class ClickableButton(Button):
    """Extended MUI Button with click event support"""
    # Make sure to explicitly declare the label parameter to match the original Button class
    label = param.String(default='')
    clicked = param.Boolean(default=False)
    
    _esm = """
    import Button from '@mui/material/Button';

    export function render({ model }) {
      const [label] = model.useState("label")
      const [variant] = model.useState("variant")
      const [disabled] = model.useState("disabled")
      const [clicked, setClicked] = model.useState("clicked")
      
      // Use the proper setter function from useState
      const handleClick = () => {
        console.log("Button clicked in React component");
        // Set clicked to true
        setClicked(true);
        // Reset after a timeout to ensure it can be clicked again
        setTimeout(() => setClicked(false), 100);
      };
      
      return (
        <Button 
          disabled={disabled} 
          variant={variant}
          onClick={handleClick}
        >
          {label || 'Click me!'}
        </Button>
      )
    }
    """


class Rating(MaterialComponent):
    """Material UI Rating component"""

    value = param.Number(default=0, bounds=(0, 5))

    _esm = """
    import Rating from '@mui/material/Rating'

    export function render({model}) {
      const [value, setValue] = model.useState("value")
      return (
        <Rating
          value={value}
          onChange={(event, newValue) => setValue(newValue) }
        />
      )
    }
    """


class DiscreteSlider(MaterialComponent):
    """Material UI Discrete Slider component"""

    marks = param.List(default=[
        {'value': 0, 'label': '0°C'},
        {'value': 20, 'label': '20°C'},
        {'value': 37, 'label': '37°C'},
        {'value': 100, 'label': '100°C'},
    ])

    value = param.Number(default=20)

    _esm = """
    import Box from '@mui/material/Box';
    import Slider from '@mui/material/Slider';

    export function render({ model }) {
      const [value, setValue] = model.useState("value")
      const [marks] = model.useState("marks")
      return (
        <Box sx={{ width: 300 }}>
          <Slider
            aria-label="Restricted values"
            defaultValue={value}
            marks={marks}
            onChange={(e) => setValue(e.target.value)}
            step={null}
            valueLabelDisplay="auto"
          />
        </Box>
      );
    }
    """