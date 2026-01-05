#-------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------

from nicegui import ui, app
from fastapi import Request
from pathlib import Path

from explainer import Explainer
from explainer.builders.flowgraph import flowgraph

# ---------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
app.add_static_files('/static', str(ROOT / 'static'))

ui.add_head_html('<script src="/static/explainer_core.js?v=999"></script>')
# ---------------------------------------------------------------------
# JS → Python event bridge
# ---------------------------------------------------------------------
cyto_handlers = {}

def on_cyto(event_name, handler):
    cyto_handlers[event_name] = handler

@app.post('/cyto/event/{event_name}')
async def cyto_event(event_name: str, request: Request):
    data = await request.json()
    handler = cyto_handlers.get(event_name)
    if handler:
        handler(data)
    return {'status': 'ok'}

# ---------------------------------------------------------------------
# Register callbacks
# ---------------------------------------------------------------------
on_cyto('node_click', lambda d: print('Node clicked:', d))
on_cyto('edge_click', lambda d: print('Edge clicked:', d))
on_cyto('expand', lambda d: print('Expanded:', d))
on_cyto('collapse', lambda d: print('Collapsed:', d))
on_cyto('ball_arrive', lambda d: print('Ball arrived:', d))
on_cyto('ball_done', lambda d: print('Ball done:', d))

# ---------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------
explainer = Explainer(container_id='cy')

with ui.column():
    explainer.mount_container()

    elements = flowgraph([
        ('Start', 'Load'),
        ('Load', 'Process'),
        ('Process', 'Finish'),
    ])

    ui.button('Init graph', on_click=lambda: explainer.init(elements))
    ui.button('Blink Process', on_click=lambda: explainer.blink('Process', color='red'))
    ui.button('Collapse Load', on_click=lambda: explainer.collapse('Load'))
    ui.button('Expand Load', on_click=lambda: explainer.expand('Load'))
    ui.button('Create Ball', on_click=lambda: explainer.create_sprite('ball', color='blue', size=18, startNode='Start'))
    ui.button('Move Ball', on_click=lambda: explainer.move_sprite('ball', ['Start', 'Load', 'Process', 'Finish'], speed=700))

ui.run()
