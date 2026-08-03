from nicegui import app, ui

ui.page_title('NiceGUI + Leaflet Demo')

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


ui.add_head_html('''
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<style>
  #leaflet-demo-map {
    height: 100%;
    width: 100%;
    min-height: 520px;
    border-radius: 12px;
    border: 1px solid #d1d5db;
  }
  #leaflet-demo-map-wrapper {
    height: 520px;
    width: 100%;
    min-height: 520px;
  }
  .leaflet-container {
    height: 100%;
    width: 100%;
  }
  #marker-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
  }
  #marker-table th,
  #marker-table td {
    border: 1px solid #d1d5db;
    padding: 6px 8px;
    text-align: left;
  }
  #marker-table tr.selected td {
    background: #fef2f2;
    font-weight: 600;
  }
</style>
<script>
window.leafletDemo = {
  map: null,
  circle: null,
  polygon: null,
  markers: [],
  nextMarkerId: 1,
  selectedMarkerId: null,
  highlightedMarker: null,
  markerTableBody: null,
  defaultIcon: null,
  highlightIcon: null,
  init() {
    if (this.map) {
      this.map.invalidateSize();
      return;
    }

    this.map = L.map('leaflet-demo-map', { zoomControl: true });
    this.map.setView([48.8566, 2.3522], 13);
    this.markerTableBody = document.getElementById('marker-table-body');

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map);

    L.marker([48.8566, 2.3522]).addTo(this.map)
      .bindPopup('<b>Paris</b><br>Leaflet marker demo')
      .openPopup();

    this.circle = L.circle([48.8566, 2.3522], {
      radius: 1200,
      color: '#0284c7',
      fillColor: '#38bdf8',
      fillOpacity: 0.25
    }).addTo(this.map);

    this.polygon = L.polygon([[48.86, 2.34], [48.85, 2.36], [48.85, 2.32]]).addTo(this.map);
    this.polygon.bindPopup('Polygon overlay');

    if (!this.defaultIcon) {
      this.defaultIcon = L.divIcon({
        html: '<div style="background:#2563eb; width:14px; height:14px; border-radius:50%; border:2px solid white; box-shadow:0 0 0 4px rgba(37,99,235,0.25);"></div>',
        className: 'leaflet-div-icon',
        iconSize: [18, 18],
        iconAnchor: [9, 9]
      });
      this.highlightIcon = L.divIcon({
        html: '<div style="background:#dc2626; width:18px; height:18px; border-radius:50%; border:2px solid white; box-shadow:0 0 0 6px rgba(220,38,38,0.25);"></div>',
        className: 'leaflet-div-icon',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
      });
    }

    this.map.on('click', (event) => {
      const lat = event.latlng.lat;
      const lng = event.latlng.lng;
      const marker = L.marker([lat, lng], { icon: this.defaultIcon }).addTo(this.map);
      marker.bindPopup(`Clicked at ${lat.toFixed(3)}, ${lng.toFixed(3)}`).openPopup();
      this.addMarkerToTable(lat, lng, marker);
      fetch(`/leaflet_click?lat=${encodeURIComponent(lat)}&lng=${encodeURIComponent(lng)}`)
        .catch((err) => console.error('Leaflet click error', err));
    });

    setTimeout(() => this.map.invalidateSize(), 150);
    window.addEventListener('resize', () => this.map.invalidateSize());
  },
  addMarkerToTable(lat, lng, marker) {
    const id = this.nextMarkerId++;
    marker.__id = id;
    this.markers.push(marker);

    const row = document.createElement('tr');
    row.dataset.id = id;
    row.innerHTML = `<td>${id}</td><td>${lat.toFixed(4)}</td><td>${lng.toFixed(4)}</td>`;
    row.addEventListener('click', () => this.selectMarkerById(id));
    this.markerTableBody.appendChild(row);
  },
  goToParis() {
    this.init();
    this.map.setView([48.8566, 2.3522], 13);
  },
  goToLondon() {
    this.init();
    this.map.setView([51.5072, -0.1276], 13);
  },
  toggleCircle() {
    this.init();
    if (this.circle) {
      this.circle.remove();
      this.circle = null;
    } else {
      this.circle = L.circle([48.8566, 2.3522], {
        radius: 1200,
        color: '#0284c7',
        fillColor: '#38bdf8',
        fillOpacity: 0.25
      }).addTo(this.map);
    }
  },
  zoomIn() {
    this.init();
    this.map.zoomIn();
  },
  zoomOut() {
    this.init();
    this.map.zoomOut();
  },
  selectMarkerById(markerId) {
    this.init();
    const marker = this.markers.find((item) => item.__id === markerId);
    if (!marker) {
      this.clearHighlight();
      return;
    }
    if (this.highlightedMarker && this.highlightedMarker !== marker) {
      this.highlightedMarker.setIcon(this.defaultIcon);
    }
    marker.setIcon(this.highlightIcon);
    marker.openPopup();
    this.map.panTo(marker.getLatLng());
    this.highlightedMarker = marker;
    this.selectedMarkerId = markerId;
    this.updateSelectedRow();
  },
  updateSelectedRow() {
    if (!this.markerTableBody) {
      return;
    }
    Array.from(this.markerTableBody.children).forEach((row) => {
      row.classList.toggle('selected', Number(row.dataset.id) === this.selectedMarkerId);
    });
  },
  clearHighlight() {
    this.init();
    if (this.highlightedMarker) {
      this.highlightedMarker.setIcon(this.defaultIcon);
      this.highlightedMarker = null;
    }
    this.selectedMarkerId = null;
    this.updateSelectedRow();
  },
  removeSelectedMarker() {
    if (this.selectedMarkerId) {
      this.removeMarkerById(this.selectedMarkerId);
    }
  },
  removeMarkerById(markerId) {
    this.init();
    const marker = this.markers.find((item) => item.__id === markerId);
    if (marker) {
      this.map.removeLayer(marker);
      this.markers = this.markers.filter((item) => item !== marker);
      if (this.highlightedMarker === marker) {
        this.highlightedMarker = null;
      }
      const row = this.markerTableBody.querySelector(`tr[data-id="${markerId}"]`);
      if (row) {
        row.remove();
      }
      this.selectedMarkerId = null;
      this.updateSelectedRow();
    }
  }
};
window.addEventListener('load', () => window.leafletDemo.init());
</script>
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
<div style="margin-top: 12px;">
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

ui.run()
