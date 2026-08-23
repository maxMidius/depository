from pathlib import Path

from nicegui import app, ui
from .configParser import extract_config

card = None;

FILE_PATH = Path(__file__).resolve()
print(f"Leaflet demo file path: {FILE_PATH}")
# Prefer the static directory that actually contains the Leaflet demo assets.
STATIC_DIR = next(
    (
        parent / 'static'
        for parent in FILE_PATH.parents
        if (parent / 'static' / 'leaflet' / 'helloLeaflet.js').is_file()
    ),
    None,
)
if STATIC_DIR is None:
    STATIC_DIR = next((parent / 'static' for parent in FILE_PATH.parents if (parent / 'static').is_dir()), None)
if STATIC_DIR is None:
    raise RuntimeError(f"Could not find a 'static' ancestor for: {FILE_PATH}")
APP_ROOT = STATIC_DIR.parent
if not STATIC_DIR.is_dir():
    raise RuntimeError(
        f"Static asset directory not found: {STATIC_DIR}. "
        "Reinstall the package so static files are included."
    )
app.add_static_files('/static', str(STATIC_DIR))

last_location = {'lat': None, 'lng': None}
location_label = None


def update_location(lat: float, lng: float) -> None:
    last_location['lat'] = lat
    last_location['lng'] = lng
    if location_label is not None:
        location_label.set_text(f'Last click: lat {lat:.4f}, lng {lng:.4f}')


@app.get('/leaflet_click')
def leaflet_click(lat: float, lng: float):
    update_location(lat, lng)
    return {'ok': True, 'lat': lat, 'lng': lng}


@app.get('/get_assets')
def get_assets():
    """Return a list of assets (RU locations) from the configuration."""
    try:
        assets = extract_config()
        return {'ok': True, 'assets': assets}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def create_ui() -> None:
    global location_label

    ui.page_title('COALESCE DSMS Demo')

    ui.add_head_html('''
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<link rel="stylesheet" href="/static/leaflet/helloLeaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script src="/static/leaflet/helloLeaflet.js"></script>
''', shared=True)

    # Ask for demo location lat, long
    global card

#    ui.label('COALESCE DSMS Demo').classes('text-2xl font-bold')
    ui.markdown('''
### COALESCE DSMS Demo
This application displays:
- a laydown of demo assets around the specified location
''')
    with ui.card().style('padding: 20px;'):
        ui.label('DSMS Demo Location Information').style('font-weight: bold; font-size: 18px;')
        # Stack text boxes vertically
        with ui.row().style('gap: 10px;'):
            demo_lat = ui.input('Lattitude').props('outlined')
            demo_long = ui.input('Longitude').props('outlined')
            ui.button('Submit', on_click=lambda: ui.run_javascript(f'window.leafletDemo.goToDSMS({demo_lat.value or 44.9672}, {demo_long.value or -103.7719})')).classes('bg-blue-600 text-white')

    with ui.element('div').classes('w-full').style('height: 520px;') as map_wrapper:
        map_wrapper.props('id=leaflet-demo-map-wrapper')
        ui.html('<div id="leaflet-demo-map"></div>', sanitize=False)

    location_label = ui.label('Last click: none yet')
    ui.html('''
<div class="marker-table-wrapper">
  <table id="marker-table">
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Lat</th>
        <th>Lng</th>
      </tr>
    </thead>
    <tbody id="marker-table-body"></tbody>
  </table>
</div>
''', sanitize=False)
    ui.label('Click a row in the table to highlight the matching marker on the map.')


def main() -> None:
    create_ui()
    ui.run()

if __name__ == "__main__":
    main()
