import panel as pn
import param
from panel.custom import JSComponent

class MyButton(JSComponent):
    clicks = param.Integer(default=0)
    _esm = """
    export function render({model, el}) {
      const button = document.createElement('button');
      button.textContent = 'Click me!';
      button.onclick = () => {
        model.clicks += 1;
      };
      el.appendChild(button);
    }
    """

button = MyButton()

pn.Column(
    "# Custom ESM Button Example",
    button,
    pn.bind(lambda c: f"Button clicked: {c} times", button.param.clicks)
).servable()