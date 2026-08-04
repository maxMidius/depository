from pathlib import Path

from nicegui import app, ui

FILE_PATH = Path(__file__).resolve()
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


def create_ui() -> None:
    global location_label

    ui.page_title('NiceGUI + Leaflet Demo')

    ui.add_head_html('''
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<link rel="stylesheet" href="/static/leaflet/helloLeaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script src="/static/leaflet/helloLeaflet.js"></script>
''', shared=True)

    with ui.row().classes('w-full items-center gap-2'):
        ui.button('Paris', on_click=lambda: ui.run_javascript('window.leafletDemo.goToParis()')).classes('bg-blue-600 text-white')
        ui.button('London', on_click=lambda: ui.run_javascript('window.leafletDemo.goToLondon()')).classes('bg-slate-700 text-white')
        ui.button('+ Zoom', on_click=lambda: ui.run_javascript('window.leafletDemo.zoomIn()')).classes('bg-emerald-600 text-white')
        ui.button('- Zoom', on_click=lambda: ui.run_javascript('window.leafletDemo.zoomOut()')).classes('bg-amber-600 text-white')
        ui.button('Toggle circle', on_click=lambda: ui.run_javascript('window.leafletDemo.toggleCircle()')).classes('bg-purple-600 text-white')
        ui.button('Remove selected marker', on_click=lambda: ui.run_javascript('window.leafletDemo.removeSelectedMarker()')).classes('bg-red-600 text-white')

    ui.markdown('''
### Leaflet in NiceGUI
This demo shows a few Leaflet features that work well inside a NiceGUI app:
- interactive map tiles
- marker and popup rendering
- circle overlays
- polygon overlays
- click-to-add markers
''')

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
