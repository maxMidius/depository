from pathlib import Path

from nicegui import app, ui
try:
    from .configParser import extract_config
except ImportError:
    from configParser import extract_config


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
DEFAULT_LAT = 44.9672
DEFAULT_LNG = -103.7719
last_submitted_coords = {'lat': DEFAULT_LAT, 'lng': DEFAULT_LNG}
pending_dsms_target = None


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


def parse_coord(value, fallback: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def handle_submit(demo_lat, demo_long) -> None:
    global pending_dsms_target
    lat = parse_coord(demo_lat.value, DEFAULT_LAT)
    lng = parse_coord(demo_long.value, DEFAULT_LNG)
    last_submitted_coords['lat'] = lat
    last_submitted_coords['lng'] = lng
    pending_dsms_target = {'lat': lat, 'lng': lng}
    ui.navigate.to('/COALESCE Laydown')


def go_to_laydown() -> None:
    global pending_dsms_target
    pending_dsms_target = {
        'lat': last_submitted_coords['lat'],
        'lng': last_submitted_coords['lng'],
    }
    ui.navigate.to('/COALESCE Laydown')


def create_ui(show_form: bool = True) -> None:
    global location_label

    ui.page_title('COALESCE DSMS Demo')

    ui.add_head_html('''
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<link rel="stylesheet" href="/static/leaflet/helloLeaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script src="/static/leaflet/helloLeaflet.js"></script>
''', shared=True)

    # Ask for demo location lat, long
    #ui.markdown('''
### COALESCE DSMS Demo
#This application displays:
#- a laydown of demo assets around the specified location
# ''')

    if show_form:
        with ui.card().style('padding: 20px;'):
            ui.label('DSMS Demo Location Information').style('font-weight: bold; font-size: 18px;')
            # Stack text boxes vertically
            with ui.row().style('gap: 10px;'):
                demo_lat = ui.input('Lattitude').props('outlined')
                demo_long = ui.input('Longitude').props('outlined')
                ui.button('Submit', on_click=lambda: handle_submit(demo_lat, demo_long)).classes('bg-blue-600 text-white')

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

def execute_go_to_dsms(lat: float, lng: float) -> None:
        # Retry briefly until the Leaflet demo API is ready on the Laydown page.
        ui.run_javascript(f'''
(() => {{
    const targetLat = {lat};
    const targetLng = {lng};
    let attempts = 0;
    const maxAttempts = 40;

    const tryRun = () => {{
        const api = window.leafletDemo;
        if (api && typeof api.goToDSMS === 'function') {{
            api.goToDSMS(targetLat, targetLng);
            return;
        }}
        attempts += 1;
        if (attempts < maxAttempts) {{
            setTimeout(tryRun, 150);
        }}
    }};

    tryRun();
}})();
''')

def layout(content_func):
    with ui.header().classes('bg-gray-800 text-white p-4'):
        ui.label('COALESCE DSMS Demo').style('font-weight: bold; font-size: 20px;')

    with ui.row().classes('bg-gray-200 p-2'):
        ui.button('Home', on_click=lambda: ui.navigate.to('/'))
        ui.button('Laydown', on_click=go_to_laydown)
        ui.button('Dashboard', on_click=lambda: ui.navigate.to('/dashboard'))

    content_func()

@ui.page('/')
def home_page():
    layout(lambda: create_ui(show_form=True))

@ui.page('/COALESCE Laydown')
def laydown_page():
    global pending_dsms_target
    dsms_target = pending_dsms_target
    pending_dsms_target = None
    if dsms_target is None:
        dsms_target = {
            'lat': last_submitted_coords['lat'],
            'lng': last_submitted_coords['lng'],
        }
    lat = parse_coord(dsms_target.get('lat'), DEFAULT_LAT)
    lng = parse_coord(dsms_target.get('lng'), DEFAULT_LNG)
    layout(lambda: create_ui(show_form=False))
    ui.timer(0.1, lambda: execute_go_to_dsms(lat, lng), once=True)

@ui.page('/dashboard')
def dashboard_page():
    layout(lambda: ui.label('Dashboard content goes here'))

def main() -> None:
    ui.run()

if __name__ == "__main__":
    main()
