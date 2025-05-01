import panel as pn
import param

from panel.custom import JSComponent


class SimpleDiv(JSComponent):

    #value = param.Integer()

    _esm = """
    export function render({ model }) {
      let div1 = document.createElement("div");
      div1.innerHTML = `Hello JSCOMP`;
      return div1
    }
    """

SimpleDiv().servable()