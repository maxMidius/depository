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
      this.markerTableBody = document.getElementById('marker-table-body');
      this.map.invalidateSize();
      return;
    }

    this.map = L.map('leaflet-demo-map', { zoomControl: true });
    this.map.setView([48.8566, 2.3522], 13);
    this.markerTableBody = document.getElementById('marker-table-body');

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(this.map);

    L.marker([48.8566, 2.3522])
      .addTo(this.map)
      .bindPopup('<b>Paris</b><br>Leaflet marker demo')
      .openPopup();

    this.circle = L.circle([48.8566, 2.3522], {
      radius: 1200,
      color: '#0284c7',
      fillColor: '#38bdf8',
      fillOpacity: 0.25,
    }).addTo(this.map);

    this.polygon = L.polygon([[48.86, 2.34], [48.85, 2.36], [48.85, 2.32]]).addTo(this.map);
    this.polygon.bindPopup('Polygon overlay');

    if (!this.defaultIcon) {
      this.defaultIcon = L.divIcon({
        html: '<div style="background:#2563eb; width:14px; height:14px; border-radius:50%; border:2px solid white; box-shadow:0 0 0 4px rgba(37,99,235,0.25);"></div>',
        className: 'leaflet-div-icon',
        iconSize: [18, 18],
        iconAnchor: [9, 9],
      });
      this.highlightIcon = L.divIcon({
        html: '<div style="background:#dc2626; width:18px; height:18px; border-radius:50%; border:2px solid white; box-shadow:0 0 0 6px rgba(220,38,38,0.25);"></div>',
        className: 'leaflet-div-icon',
        iconSize: [20, 20],
        iconAnchor: [10, 10],
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
    row.addEventListener('click', () => window.leafletDemo.selectMarkerById(id));
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
        fillOpacity: 0.25,
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
    this.init();

    let markerId = this.selectedMarkerId;
    if (!markerId && this.markerTableBody) {
      const selectedRow = this.markerTableBody.querySelector('tr.selected');
      if (selectedRow) {
        markerId = Number(selectedRow.dataset.id);
      }
    }

    if (markerId) {
      this.removeMarkerById(markerId);
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
  },
};

window.addEventListener('load', () => window.leafletDemo.init());
