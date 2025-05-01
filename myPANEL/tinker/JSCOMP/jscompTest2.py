import panel as pn
import param

from panel.custom import JSComponent


class SimpleDiv(JSComponent):

    value = param.Integer()

    _esm = """
    export function render({ model }) {
      let div1 = document.createElement("div");
      console.log(model.value)
      div1.innerHTML = `Hello ${model.value} buttons <br>`;
      for (let i = 0; i < model.value; i++) {
        console.log(i)
        let but = document.createElement("button");
        but.innerHTML = `Hello ${i}`;
        but.onclick = function() {
          console.log("Hello " + i);
        }
        div1.appendChild(but);
      }
      return div1
    }
    """

SimpleDiv(value=3).servable()
