window.leafletDemo = {
  mapElementId: 'leaflet-demo-map',
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
    const mapElement = document.getElementById(this.mapElementId);
    if (!mapElement) {
      // NiceGUI may mount content after script load; retry shortly.
      setTimeout(() => this.init(), 100);
      return;
    }

    if (this.map) {
      this.markerTableBody = document.getElementById('marker-table-body');
      this.map.invalidateSize();
      return;
    }

    this.map = L.map(this.mapElementId, { zoomControl: true });
    this.map.setView([44.9672, -103.7719], 4);
    this.markerTableBody = document.getElementById('marker-table-body');

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      minZoom: 3,
      maxZoom: 15,
      
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(this.map);


  //  this.polygon = L.polygon([[48.86, 2.34], [48.85, 2.36], [48.85, 2.32]]).addTo(this.map);
  //this.polygon.bindPopup('Polygon overlay');

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

    //this.map.on('click', (event) => {
      //const lat = event.latlng.lat;
      //const lng = event.latlng.lng;
      //const marker = L.marker([lat, lng], { icon: this.defaultIcon }).addTo(this.map);
      //marker.bindPopup(`Clicked at ${lat.toFixed(3)}, ${lng.toFixed(3)}`).openPopup();
      //this.bindMarkerHover(marker);
      //this.addMarkerToTable(lat, lng, marker);
      //fetch(`/leaflet_click?lat=${encodeURIComponent(lat)}&lng=${encodeURIComponent(lng)}`)
      //  .catch((err) => console.error('Leaflet click error', err));
    //});

    

    const refreshWhenVisible = () => {
      const rect = mapElement.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        this.map.invalidateSize();
      } else {
        requestAnimationFrame(refreshWhenVisible);
      }
    };
    setTimeout(refreshWhenVisible, 0);
    window.addEventListener('resize', () => this.map.invalidateSize());
  },

  addMarkerToTable(lat, lng, marker) {
    const id = this.nextMarkerId++;
    marker.__id = id;
    this.markers.push(marker);
    let name = marker.getPopup() ? marker.getPopup().getContent() : `Marker ${id}`;

    const row = document.createElement('tr');
    row.dataset.id = id;
    row.innerHTML = `<td>${id}</td><td>${name}</td><td>${lat.toFixed(4)}</td><td>${lng.toFixed(4)}</td>`;
    row.addEventListener('click', () => window.leafletDemo.selectMarkerById(id));
    this.markerTableBody.appendChild(row);
  },

  bindMarkerHover(marker) {
    marker.on('mouseover', () => marker.openPopup());
    marker.on('mouseout', () => marker.closePopup());
    return marker;
  },

  goToDSMS(lat, long) {

    this.init();
    if (!this.map || !this.markerTableBody) {
      return;
    }

    this.map.invalidateSize();
    this.map.setView([lat, long], 11);

    var circle = L.circle([lat, long], {
      radius: 22000,
      color: '#0284c7',
      fillColor: '#38bdf8',
      fillOpacity: 0.15,
    }).addTo(this.map);

    const marker = L.marker([lat, long], { icon: this.defaultIcon || L.divIcon({
      html: '<div style="background:#2563eb; width:14px; height:14px; border-radius:50%; border:2px solid white; box-shadow:0 0 0 4px rgba(37,99,235,0.25);"></div>',
      className: 'leaflet-div-icon',
      iconSize: [18, 18],
      iconAnchor: [9, 9],
    }) }).addTo(this.map);
    marker.bindPopup(`DSMS at ${lat.toFixed(3)}, ${long.toFixed(3)}`).openPopup();
    this.bindMarkerHover(marker);

    this.addMarkerToTable(lat, long, marker);

    // Fetch and display assets from the backend
    fetch('/get_assets')
      .then(response => {
        console.log('Asset response status:', response.status);
        return response.json();
      })
      .then(data => {
        console.log('Asset data received:', data);
        if (data.ok && data.assets) {
          console.log('Processing', data.assets.length, 'assets');
          data.assets.forEach((asset, index) => {
            console.log(`Asset ${index}:`, asset);
            // Ensure coordinates are valid numbers
            const lat = parseFloat(asset.lat);
            const lng = parseFloat(asset.long);
            if (isNaN(lat) || isNaN(lng)) {
              console.warn('Invalid coordinates for asset:', asset);
              return;
            }
            const assetMarker = L.marker([lat, lng], { 
              icon: this.defaultIcon || L.divIcon({
                html: '<div style="background:#2563eb; width:14px; height:14px; border-radius:50%; border:2px solid white; box-shadow:0 0 0 4px rgba(37,99,235,0.25);"></div>',
                className: 'leaflet-div-icon',
                iconSize: [18, 18],
                iconAnchor: [9, 9],
              })
            }).addTo(this.map);
            assetMarker.bindPopup(`${asset.name}`);
            this.bindMarkerHover(assetMarker);
            //assetMarker.bindPopup(`${asset.name}`).openPopup();
            this.addMarkerToTable(lat, lng, assetMarker);
            console.log('Added asset marker for:', asset.name);
          });
        } else {
          console.error('Failed to fetch assets:', data.error);
        }
      })
      .catch((err) => console.error('Asset fetch error:', err));

    // Display the marker table
    if (this.markerTableBody.parentElement) {
      this.markerTableBody.parentElement.style.display = 'block';
      this.markerTableBody.parentElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
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
document.addEventListener('DOMContentLoaded', () => window.leafletDemo.init());
