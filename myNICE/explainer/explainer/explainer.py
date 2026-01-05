#------------------------------
# vi: sw=4 ts=4 expandtab
#------------------------------
from nicegui import ui, app
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ensure static is mounted (defensive)
app.add_static_files('/static', str(ROOT / 'static'))


class Explainer:
    def __init__(self, container_id: str = 'cy'):
        self.container_id = container_id
        self._ensure_js_loaded()

    def _ensure_js_loaded(self) -> None:
        ui.add_head_html('<script src="/static/explainer_core.js"></script>')

    def mount_container(self):
        from nicegui import ui
        ui.html(
            f'<div id="{self.container_id}" style="width: 800px; height: 600px;"></div>', sanitize=False
        )

    def init(self, elements: list, layout: str = 'breadthfirst', style: dict | None = None):
        import json
        elements_js = json.dumps(elements)
        style_js = 'null' if style is None else json.dumps(style)
        ui.run_javascript(
            f'Explainer.init("{self.container_id}", {elements_js}, {style_js}, "{layout}")'
        )

    def expand(self, node_id: str):
        ui.run_javascript(f'Explainer.expand("{node_id}")')

    def collapse(self, node_id: str):
        ui.run_javascript(f'Explainer.collapse("{node_id}")')

    def show(self, node_id: str):
        ui.run_javascript(f'Explainer.show("{node_id}")')

    def hide(self, node_id: str):
        ui.run_javascript(f'Explainer.hide("{node_id}")')

    def blink(self, node_id: str, color: str = 'yellow', duration: int = 800):
        ui.run_javascript(
            f'Explainer.blink("{node_id}", {{color: "{color}", duration: {duration}}})'
        )

    def create_sprite(self, sprite_id: str, color='red', size=20, startNode=None):
        start_js = f'"{startNode}"' if startNode else 'null'
        ui.run_javascript(
            f'Explainer.createSprite("{sprite_id}", {{color: "{color}", size: {size}, startNode: {start_js}}});'
        )

    def move_sprite(self, sprite_id: str, path: list[str], speed: int = 600):
        import json
        path_js = json.dumps(path)
        ui.run_javascript(
            f'Explainer.moveSprite("{sprite_id}", {path_js}, {{speed: {speed}}});'
        )
