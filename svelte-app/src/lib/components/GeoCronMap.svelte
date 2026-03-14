<script>
  import 'maplibre-gl/dist/maplibre-gl.css';

  const GC_TIME_MIN = -1200;
  const GC_TIME_MAX = 800;

  const HISTORICAL_EVENTS = [
    { year: -1177, label: 'Bronze Age Collapse' },
    { year: -753, label: 'Rome Founded' },
    { year: -509, label: 'Roman Republic' },
    { year: -334, label: "Alexander's Conquest" },
    { year: -264, label: 'First Punic War' },
    { year: -146, label: 'Carthage Destroyed' },
    { year: -44, label: 'Caesar Assassinated' },
    { year: -27, label: 'Roman Empire' },
    { year: 14, label: 'Death of Augustus' },
    { year: 79, label: 'Vesuvius' },
    { year: 117, label: 'Peak Extent' },
    { year: 165, label: 'Antonine Plague' },
    { year: 235, label: 'Crisis of 3rd C.' },
    { year: 284, label: 'Diocletian' },
    { year: 330, label: 'Constantinople' },
    { year: 395, label: 'Empire Split' },
    { year: 410, label: 'Sack of Rome' },
    { year: 476, label: 'Fall of West' },
    { year: 541, label: 'Justinianic Plague' },
    { year: 632, label: 'Islamic Expansion' },
    { year: 750, label: 'Abbasid Caliphate' },
  ];

  const POLITY_COLORS = [
    '#9b6dd7', '#7b5ea7', '#6d5baf', '#8e7cc3', '#b39ddb',
    '#5b8dd9', '#7986cb', '#64b5f6', '#4fc3f7', '#4dd0e1',
    '#4fad7a', '#66bb6a', '#81c784', '#aed581', '#c5e1a5',
    '#d94f4f', '#e57373', '#ef5350', '#f06292', '#ce93d8',
    '#c9944a', '#e6b86e', '#ffb74d', '#ffa726', '#ff8a65',
  ];

  // State
  let gcYear = $state(-200);
  let gcPlaying = $state(false);
  let gcAnimId = $state(null);
  let gcLayerVisibility = $state({ borders: true, routes: true, wrecks: true, arcs: true });
  let loaded = $state(false);
  let loadError = $state(false);

  // Data state
  let gcBorders = $state(null);
  let gcRoutes = $state(null);
  let gcRouteNodes = $state(null);
  let gcWrecks = $state(null);
  let gcArcs = $state(null);
  let gcLeadData = $state(null);

  // Derived
  let yearDisplay = $derived(formatYearDisplay(gcYear));
  let contextText = $derived(getContextForYear(gcYear));

  // Stats (derived from data + year)
  let statWrecks = $derived(computeStatWrecks(gcWrecks, gcYear));
  let statEmpires = $derived(computeStatEmpires(gcBorders, gcYear));
  let statRoutes = $derived(computeStatRoutes(gcRoutes, gcYear));
  let statLead = $derived(computeStatLead(gcLeadData, gcYear));

  // Map instance (not reactive — maplibre manages its own state)
  let gcMap = null;

  // DOM refs
  let mapContainerEl = $state(null);
  let sparklineEl = $state(null);
  let wrapEl = $state(null);
  let sliderEl = $state(null);

  // Reactive state for template-driven rendering
  let eventTicks = $state([]);
  let hoverVisible = $state(false);
  let hoverLeft = $state('0px');
  let hoverTop = $state('0px');
  let hoverEmpire = $state('');
  let hoverLines = $state(/** @type {Array<{text: string, sub?: string}>} */ ([]));
  let fsCollapsed = $state(false);

  // ---------------------------------------------------------------------------
  // Pure helpers
  // ---------------------------------------------------------------------------

  function yearLabel(y) {
    if (y < 0) return Math.abs(y) + ' BCE';
    if (y === 0) return '1 BCE';
    return y + ' CE';
  }

  function getContextForYear(y) {
    let best = null, bestDist = Infinity;
    for (const ev of HISTORICAL_EVENTS) {
      const d = Math.abs(ev.year - y);
      if (d < bestDist) { bestDist = d; best = ev; }
    }
    if (best && bestDist <= 30) return best.label + ' (' + yearLabel(best.year) + ')';
    return '';
  }

  function formatYearDisplay(y) {
    return { abs: Math.abs(y), era: y < 0 ? 'BCE' : 'CE' };
  }

  function polityColor(name) {
    let hash = 0;
    for (let i = 0; i < name.length; i++) hash = ((hash << 5) - hash) + name.charCodeAt(i);
    return POLITY_COLORS[Math.abs(hash) % POLITY_COLORS.length];
  }

  async function loadJSON(url) {
    const resp = await fetch(url);
    return resp.json();
  }

  // ---------------------------------------------------------------------------
  // Derived stat helpers
  // ---------------------------------------------------------------------------

  function computeStatWrecks(wrecks, year) {
    if (!wrecks) return 0;
    let count = 0;
    for (const f of wrecks.features) {
      if (f.properties.from <= year && f.properties.to >= year) count++;
    }
    return count;
  }

  function computeStatEmpires(borders, year) {
    if (!borders) return 0;
    let count = 0;
    for (const f of borders.features) {
      if (f.properties.from <= year && f.properties.to >= year) count++;
    }
    return count;
  }

  function computeStatRoutes(routes, year) {
    if (!routes) return 0;
    let count = 0;
    for (const f of routes.features) {
      if (f.properties.from <= year && f.properties.to >= year) count++;
    }
    return count;
  }

  function computeStatLead(leadData, year) {
    if (!leadData) return null;
    let closest = leadData[0];
    let minDist = Infinity;
    for (const d of leadData) {
      const dist = Math.abs(d.y - year);
      if (dist < minDist) { minDist = dist; closest = d; }
    }
    return closest ? closest.v.toFixed(2) + ' kt/a' : null;
  }

  // ---------------------------------------------------------------------------
  // Map helpers
  // ---------------------------------------------------------------------------

  function drawSparkline(canvas, data, currentYear) {
    const ctx = canvas.getContext('2d');
    const W = canvas.width = canvas.offsetWidth * 2;
    const H = canvas.height = canvas.offsetHeight * 2;
    ctx.clearRect(0, 0, W, H);

    if (!data || data.length === 0) return;

    const maxV = Math.max(...data.map(d => d.v));
    const minY = data[0].y, maxY = data[data.length - 1].y;
    const rangeY = maxY - minY || 1;

    ctx.beginPath();
    ctx.strokeStyle = 'rgba(201,148,74,0.6)';
    ctx.lineWidth = 1.5;
    for (let i = 0; i < data.length; i++) {
      const x = ((data[i].y - minY) / rangeY) * W;
      const yy = H - (data[i].v / maxV) * H * 0.85 - H * 0.05;
      if (i === 0) ctx.moveTo(x, yy); else ctx.lineTo(x, yy);
    }
    ctx.stroke();

    const cx = ((currentYear - minY) / rangeY) * W;
    ctx.beginPath();
    ctx.strokeStyle = 'rgba(240,240,242,0.5)';
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);
    ctx.moveTo(cx, 0);
    ctx.lineTo(cx, H);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  const TIME_FILTER = (y) => ['all', ['<=', 'from', y], ['>=', 'to', y]];

  function updateMap() {
    if (!gcMap || !gcMap.isStyleLoaded()) return;

    const y = gcYear;
    const tf = TIME_FILTER(y);

    if (gcMap.getSource('borders')) {
      gcMap.setFilter('borders-fill', tf);
      gcMap.setFilter('borders-line', tf);
    }

    if (gcMap.getSource('routes')) {
      gcMap.setFilter('routes-roads', ['all', ['<=', 'from', y], ['>=', 'to', y], ['==', 'type', 'road']]);
      gcMap.setFilter('routes-roads-glow', ['all', ['<=', 'from', y], ['>=', 'to', y], ['==', 'type', 'road']]);

      const seaTypes = ['coastal', 'open sea', 'overseas', 'slowcoast', 'slowover', 'ferry'];
      const seaFilter = ['all', ['<=', 'from', y], ['>=', 'to', y], ['in', 'type', ...seaTypes]];
      gcMap.setFilter('routes-sea', seaFilter);
      gcMap.setFilter('routes-sea-glow', seaFilter);

      const riverTypes = ['river', 'upstream', 'downstream', 'fastup', 'fastdown'];
      const riverFilter = ['all', ['<=', 'from', y], ['>=', 'to', y], ['in', 'type', ...riverTypes]];
      gcMap.setFilter('routes-river', riverFilter);
      gcMap.setFilter('routes-river-glow', riverFilter);
    }

    if (gcMap.getSource('route-nodes')) {
      gcMap.setFilter('route-nodes-circles', tf);
      gcMap.setFilter('route-nodes-labels', tf);
    }

    if (gcMap.getSource('wrecks')) {
      gcMap.setFilter('wrecks-circles', tf);
    }

    if (gcMap.getSource('arcs')) {
      gcMap.setFilter('arcs-lines', tf);
    }

    if (sparklineEl && gcLeadData) {
      drawSparkline(sparklineEl, gcLeadData, y);
    }
  }

  function buildEventTicks() {
    const range = GC_TIME_MAX - GC_TIME_MIN;
    const sorted = [...HISTORICAL_EVENTS].sort((a, b) => a.year - b.year);
    const ticks = [];
    let row = 0;
    for (let i = 0; i < sorted.length; i++) {
      const ev = sorted[i];
      const pct = ((ev.year - GC_TIME_MIN) / range) * 100;
      ticks.push({ label: ev.label, pct, row });
      if (i + 1 < sorted.length) {
        const nextPct = ((sorted[i + 1].year - GC_TIME_MIN) / range) * 100;
        if (nextPct - pct < 4) { row = row === 0 ? 1 : 0; }
        else { row = (row + 1) % 2; }
      }
    }
    eventTicks = ticks;
  }

  function createAnchorImage(color, size) {
    const s = size;
    const canvas = document.createElement('canvas');
    canvas.width = s; canvas.height = s;
    const ctx = canvas.getContext('2d');
    const cx = s / 2, cy = s / 2;
    const r = s * 0.38;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = color;
    ctx.lineWidth = s * 0.09;
    // Ring at top
    ctx.beginPath();
    ctx.arc(cx, cy - r * 0.55, r * 0.28, 0, Math.PI * 2);
    ctx.stroke();
    // Vertical shaft
    ctx.beginPath();
    ctx.moveTo(cx, cy - r * 0.27);
    ctx.lineTo(cx, cy + r * 0.75);
    ctx.stroke();
    // Cross bar
    ctx.beginPath();
    ctx.moveTo(cx - r * 0.45, cy - r * 0.05);
    ctx.lineTo(cx + r * 0.45, cy - r * 0.05);
    ctx.stroke();
    // Curved flukes at bottom
    ctx.beginPath();
    ctx.moveTo(cx - r * 0.55, cy + r * 0.35);
    ctx.quadraticCurveTo(cx - r * 0.5, cy + r * 0.85, cx, cy + r * 0.75);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx + r * 0.55, cy + r * 0.35);
    ctx.quadraticCurveTo(cx + r * 0.5, cy + r * 0.85, cx, cy + r * 0.75);
    ctx.stroke();
    return ctx.getImageData(0, 0, s, s);
  }

  // ---------------------------------------------------------------------------
  // Layer toggles
  // ---------------------------------------------------------------------------

  function handleLayerToggle(layerKey, checked) {
    gcLayerVisibility = { ...gcLayerVisibility, [layerKey]: checked };

    if (!gcMap) return;
    const layerMap = {
      borders: ['borders-fill', 'borders-line'],
      routes: ['routes-roads', 'routes-sea', 'routes-river', 'routes-roads-glow', 'routes-sea-glow', 'routes-river-glow', 'route-nodes-circles', 'route-nodes-labels'],
      wrecks: ['wrecks-circles'],
      arcs: ['arcs-lines'],
    };
    const vis = checked ? 'visible' : 'none';
    for (const lid of (layerMap[layerKey] || [])) {
      if (gcMap.getLayer(lid)) gcMap.setLayoutProperty(lid, 'visibility', vis);
    }
  }

  // ---------------------------------------------------------------------------
  // Animation
  // ---------------------------------------------------------------------------

  let lastTick = 0;
  function animateTimeline(ts) {
    if (!gcPlaying) return;
    if (ts - lastTick > 40) {
      lastTick = ts;
      gcYear += 2;
      if (gcYear > GC_TIME_MAX) { gcYear = GC_TIME_MIN; }
      if (sliderEl) sliderEl.value = gcYear;
      updateMap();
    }
    gcAnimId = requestAnimationFrame(animateTimeline);
  }

  function togglePlay() {
    gcPlaying = !gcPlaying;
    if (gcPlaying) {
      animateTimeline(0);
    } else {
      if (gcAnimId !== null) cancelAnimationFrame(gcAnimId);
      gcAnimId = null;
    }
  }

  // ---------------------------------------------------------------------------
  // Fullscreen
  // ---------------------------------------------------------------------------

  function updateFsIcons() {
    fsCollapsed = !!(document.fullscreenElement || document.webkitFullscreenElement);
  }

  function toggleFullscreen() {
    if (!wrapEl) return;
    if (document.fullscreenElement || document.webkitFullscreenElement) {
      (document.exitFullscreen || document.webkitExitFullscreen).call(document);
    } else {
      (wrapEl.requestFullscreen || wrapEl.webkitRequestFullscreen).call(wrapEl);
    }
  }

  // ---------------------------------------------------------------------------
  // Map initialization effect
  // ---------------------------------------------------------------------------

  $effect(() => {
    if (!mapContainerEl) return;

    let map = null;
    let fsHandler = null;
    let fsHandlerWk = null;

    (async () => {
      const maplibregl = (await import('maplibre-gl')).default;

      map = new maplibregl.Map({
        container: mapContainerEl,
        style: {
          version: 8,
          name: 'GeoCron Satellite',
          sources: {
            'satellite': {
              type: 'raster',
              tiles: [
                'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
              ],
              tileSize: 256,
              maxzoom: 18,
              attribution: '&copy; <a href="https://www.esri.com/">Esri</a>, Maxar, Earthstar, USDA, USGS, AeroGRID, IGN'
            }
          },
          layers: [{
            id: 'background',
            type: 'background',
            paint: { 'background-color': '#060810' }
          }, {
            id: 'satellite-tiles',
            type: 'raster',
            source: 'satellite',
            paint: {
              'raster-opacity': 0.75,
              'raster-saturation': -0.35,
              'raster-brightness-min': 0.02,
              'raster-brightness-max': 0.55,
              'raster-contrast': 0.15
            }
          }]
        },
        center: [18, 37],
        zoom: 3.8,
        pitch: 20,
        minZoom: 2,
        maxZoom: 10,
        maxBounds: [[-30, 10], [60, 62]],
      });

      gcMap = map;
      map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right');

      let borders, routes, routeNodes, wrecks, arcs, leadData;
      try {
        [borders, routes, routeNodes, wrecks, arcs, leadData] = await Promise.all([
          loadJSON('/data/geo/borders.json'),
          loadJSON('/data/geo/routes.json'),
          loadJSON('/data/geo/route_nodes.json'),
          loadJSON('/data/geo/shipwrecks.json'),
          loadJSON('/data/geo/trade_arcs.json'),
          loadJSON('/data/geo/lead_sparkline.json'),
        ]);
      } catch (err) {
        console.error('GeoCron: Failed to load data', err);
        loadError = true;
        return;
      }

      gcBorders = borders;
      gcRoutes = routes;
      gcRouteNodes = routeNodes;
      gcWrecks = wrecks;
      gcArcs = arcs;
      gcLeadData = leadData;

      map.on('load', () => {
        loaded = true;

        // Borders layer
        const bordersWithColors = {
          ...borders,
          features: borders.features.map(f => ({
            ...f,
            properties: { ...f.properties, color: polityColor(f.properties.name) }
          }))
        };
        map.addSource('borders', { type: 'geojson', data: bordersWithColors });
        map.addLayer({
          id: 'borders-fill',
          type: 'fill',
          source: 'borders',
          paint: {
            'fill-color': ['get', 'color'],
            'fill-opacity': 0.22,
          },
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear]]
        });
        map.addLayer({
          id: 'borders-line',
          type: 'line',
          source: 'borders',
          paint: {
            'line-color': ['get', 'color'],
            'line-width': 1.5,
            'line-opacity': 0.5,
          },
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear]]
        });

        // Routes layers
        map.addSource('routes', { type: 'geojson', data: routes });

        const seaTypesInit = ['coastal', 'open sea', 'overseas', 'slowcoast', 'slowover', 'ferry'];
        const riverTypesInit = ['river', 'upstream', 'downstream', 'fastup', 'fastdown'];

        map.addLayer({
          id: 'routes-roads-glow',
          type: 'line',
          source: 'routes',
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear], ['==', 'type', 'road']],
          paint: {
            'line-color': '#c9944a',
            'line-width': ['interpolate', ['linear'], ['zoom'], 3, 6, 7, 12, 10, 18],
            'line-opacity': 0.12,
            'line-blur': 4,
          }
        });
        map.addLayer({
          id: 'routes-sea-glow',
          type: 'line',
          source: 'routes',
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear], ['in', 'type', ...seaTypesInit]],
          paint: {
            'line-color': '#5b8dd9',
            'line-width': ['interpolate', ['linear'], ['zoom'], 3, 5, 7, 10, 10, 16],
            'line-opacity': 0.10,
            'line-blur': 4,
          }
        });
        map.addLayer({
          id: 'routes-river-glow',
          type: 'line',
          source: 'routes',
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear], ['in', 'type', ...riverTypesInit]],
          paint: {
            'line-color': '#4fc3f7',
            'line-width': ['interpolate', ['linear'], ['zoom'], 3, 4, 7, 8, 10, 12],
            'line-opacity': 0.08,
            'line-blur': 3,
          }
        });
        map.addLayer({
          id: 'routes-roads',
          type: 'line',
          source: 'routes',
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear], ['==', 'type', 'road']],
          paint: {
            'line-color': '#c9944a',
            'line-width': ['interpolate', ['linear'], ['zoom'], 3, 1.5, 6, 2.5, 9, 4],
            'line-opacity': 0.8,
          }
        });
        map.addLayer({
          id: 'routes-sea',
          type: 'line',
          source: 'routes',
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear], ['in', 'type', ...seaTypesInit]],
          paint: {
            'line-color': '#5b8dd9',
            'line-width': ['interpolate', ['linear'], ['zoom'], 3, 1.2, 6, 2, 9, 3.5],
            'line-opacity': 0.7,
            'line-dasharray': [4, 2],
          }
        });
        map.addLayer({
          id: 'routes-river',
          type: 'line',
          source: 'routes',
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear], ['in', 'type', ...riverTypesInit]],
          paint: {
            'line-color': '#4fc3f7',
            'line-width': ['interpolate', ['linear'], ['zoom'], 3, 1.5, 6, 2.5, 9, 4],
            'line-opacity': 0.75,
            'line-dasharray': [3, 1.5],
          }
        });

        // Route nodes (cities/ports)
        map.addSource('route-nodes', { type: 'geojson', data: routeNodes });
        map.addLayer({
          id: 'route-nodes-circles',
          type: 'circle',
          source: 'route-nodes',
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear]],
          paint: {
            'circle-radius': ['interpolate', ['linear'], ['zoom'], 3, 1.5, 6, 3, 9, 5],
            'circle-color': '#c9944a',
            'circle-opacity': 0.7,
            'circle-stroke-width': 1,
            'circle-stroke-color': 'rgba(12,15,19,0.8)',
          }
        });
        map.addLayer({
          id: 'route-nodes-labels',
          type: 'symbol',
          source: 'route-nodes',
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear]],
          minzoom: 6,
          layout: {
            'text-field': ['get', 'label'],
            'text-size': ['interpolate', ['linear'], ['zoom'], 6, 9, 9, 12],
            'text-offset': [0, 1.2],
            'text-anchor': 'top',
            'text-max-width': 8,
            'text-allow-overlap': false,
          },
          paint: {
            'text-color': '#e6b86e',
            'text-halo-color': 'rgba(12,15,19,0.9)',
            'text-halo-width': 1.5,
            'text-opacity': 0.85,
          }
        });

        // Shipwrecks layer (anchor icons)
        const anchorColors = {
          'western_med': '#d94f4f',
          'eastern_med': '#5b8dd9',
          'adriatic': '#4fb5ad',
          'black_sea': '#9b6dd7',
          'default': '#e6b86e',
        };
        const anchorSize = 32;
        for (const [key, color] of Object.entries(anchorColors)) {
          map.addImage('anchor-' + key, createAnchorImage(color, anchorSize), { pixelRatio: 2 });
        }

        map.addSource('wrecks', { type: 'geojson', data: wrecks });
        map.addLayer({
          id: 'wrecks-circles',
          type: 'symbol',
          source: 'wrecks',
          layout: {
            'icon-image': [
              'match', ['get', 'region'],
              'western_med', 'anchor-western_med',
              'eastern_med', 'anchor-eastern_med',
              'adriatic', 'anchor-adriatic',
              'black_sea', 'anchor-black_sea',
              'anchor-default'
            ],
            'icon-size': ['interpolate', ['linear'], ['zoom'], 3, 0.5, 6, 0.8, 9, 1.2],
            'icon-allow-overlap': true,
            'icon-ignore-placement': true,
          },
          paint: {
            'icon-opacity': 0.85,
          },
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear]]
        });

        // Trade arcs layer
        map.addSource('arcs', { type: 'geojson', data: arcs });
        map.addLayer({
          id: 'arcs-lines',
          type: 'line',
          source: 'arcs',
          paint: {
            'line-color': '#4fb5ad',
            'line-width': 1.2,
            'line-opacity': 0.35,
          },
          filter: ['all', ['<=', 'from', gcYear], ['>=', 'to', gcYear]]
        }, 'wrecks-circles');

        // Interactions
        const popup = new maplibregl.Popup({ closeButton: true, closeOnClick: true, maxWidth: '320px' });

        map.on('click', 'wrecks-circles', (e) => {
          const f = e.features[0];
          const p = f.properties;
          let html = '<div class="popup-title">' + (p.name || 'Unknown Wreck') + '</div><div class="popup-detail">';
          html += '<b>Date:</b> ' + yearLabel(p.from) + ' – ' + yearLabel(p.to) + '<br>';
          if (p.cargo) html += '<b>Cargo:</b> ' + p.cargo + '<br>';
          if (p.provenance) html += '<b>From:</b> ' + p.provenance + '<br>';
          if (p.destination) html += '<b>To:</b> ' + p.destination + '<br>';
          if (p.region) html += '<b>Region:</b> ' + p.region.replace('_', ' ') + '<br>';
          if (p.country) html += '<b>Country:</b> ' + p.country;
          html += '</div>';
          popup.setLngLat(e.lngLat).setHTML(html).addTo(map);
        });

        function handleRouteClick(e) {
          const f = e.features[0];
          const p = f.properties;
          let html = '<div class="popup-title">' + p.source + ' → ' + p.target + '</div><div class="popup-detail">';
          html += '<b>Type:</b> ' + p.type + '<br>';
          html += '<b>Distance:</b> ' + p.km + ' km<br>';
          html += '<b>Travel time:</b> ' + p.days + ' days<br>';
          html += '<b>Cost:</b> ' + p.expense + ' denarii/kg';
          html += '</div>';
          popup.setLngLat(e.lngLat).setHTML(html).addTo(map);
        }
        map.on('click', 'routes-roads', handleRouteClick);
        map.on('click', 'routes-sea', handleRouteClick);
        map.on('click', 'routes-river', handleRouteClick);

        map.on('click', 'route-nodes-circles', (e) => {
          const f = e.features[0];
          const p = f.properties;
          let html = '<div class="popup-title">' + (p.title || p.label) + '</div><div class="popup-detail">';
          if (p.pleiades) html += '<a href="https://pleiades.stoa.org/places/' + p.pleiades + '" target="_blank" style="color:var(--accent)">Pleiades entry</a>';
          html += '</div>';
          popup.setLngLat(e.lngLat).setHTML(html).addTo(map);
        });

        map.on('click', 'borders-fill', (e) => {
          const f = e.features[0];
          const p = f.properties;
          let html = '<div class="popup-title">' + p.name + '</div><div class="popup-detail">';
          html += '<b>Period:</b> ' + yearLabel(p.from) + ' – ' + yearLabel(p.to) + '<br>';
          if (p.area) html += '<b>Area:</b> ~' + Math.round(p.area).toLocaleString() + ' km²<br>';
          if (p.wiki) html += '<a href="https://en.wikipedia.org/wiki/' + encodeURIComponent(p.wiki) + '" target="_blank" style="color:var(--accent)">Wikipedia</a>';
          html += '</div>';
          popup.setLngLat(e.lngLat).setHTML(html).addTo(map);
        });

        // Cursor changes
        for (const layerId of ['wrecks-circles', 'routes-roads', 'routes-sea', 'routes-river', 'route-nodes-circles', 'borders-fill']) {
          map.on('mouseenter', layerId, () => { map.getCanvas().style.cursor = 'pointer'; });
          map.on('mouseleave', layerId, () => { map.getCanvas().style.cursor = ''; });
        }

        // Hover tooltip
        const interactiveLayers = ['borders-fill', 'wrecks-circles', 'routes-roads', 'routes-sea', 'routes-river', 'route-nodes-circles', 'arcs-lines'];

        map.on('mousemove', (e) => {
          if (!wrapEl) return;
          const feats = map.queryRenderedFeatures(e.point, { layers: interactiveLayers });
          if (!feats || feats.length === 0) {
            hoverVisible = false;
            return;
          }

          let empireName = '';
          let detailLines = [];

          for (const f of feats) {
            const p = f.properties;
            const lid = f.layer.id;

            if (lid === 'borders-fill' && !empireName) {
              empireName = p.name || '';
            } else if (lid === 'wrecks-circles') {
              const name = p.name || 'Shipwreck';
              let sub = '';
              if (p.cargo) {
                const short = p.cargo.length > 60 ? p.cargo.substring(0, 60) + '...' : p.cargo;
                sub = short;
              }
              if (p.provenance || p.destination) {
                sub = (sub ? sub + ' · ' : '') + (p.provenance || '?') + ' → ' + (p.destination || '?');
              }
              detailLines.push({ text: name, sub });
            } else if (lid === 'route-nodes-circles') {
              detailLines.push({ text: (p.title || p.label) + ' (city/port)', sub: '' });
            } else if (lid.startsWith('routes-')) {
              detailLines.push({ text: p.source + ' → ' + p.target, sub: p.type + ', ' + p.km + ' km, ' + p.days + ' days' });
            } else if (lid === 'arcs-lines') {
              detailLines.push({ text: p.provenance + ' → ' + p.destination, sub: 'trade arc' });
            }
          }

          if (!empireName && detailLines.length === 0) {
            hoverVisible = false;
            return;
          }

          hoverEmpire = empireName;
          hoverLines = detailLines.slice(0, 3);
          hoverVisible = true;

          const rect = wrapEl.getBoundingClientRect();
          let tipX = e.point.x + 14;
          let tipY = e.point.y + 14;
          if (tipX + 200 > rect.width - 10) tipX = e.point.x - 200 - 10;
          if (tipY + 80 > rect.height - 10) tipY = e.point.y - 80 - 10;
          hoverLeft = tipX + 'px';
          hoverTop = tipY + 'px';
        });

        map.on('mouseout', () => {
          hoverVisible = false;
        });

        updateMap();
        buildEventTicks();
        if (sparklineEl && gcLeadData) drawSparkline(sparklineEl, gcLeadData, gcYear);
      });

      // Fullscreen event listeners
      fsHandler = () => {
        updateFsIcons();
        setTimeout(() => { if (gcMap) gcMap.resize(); }, 100);
      };
      fsHandlerWk = () => {
        updateFsIcons();
        setTimeout(() => { if (gcMap) gcMap.resize(); }, 100);
      };
      document.addEventListener('fullscreenchange', fsHandler);
      document.addEventListener('webkitfullscreenchange', fsHandlerWk);
    })();

    return () => {
      if (gcAnimId !== null) cancelAnimationFrame(gcAnimId);
      if (fsHandler) document.removeEventListener('fullscreenchange', fsHandler);
      if (fsHandlerWk) document.removeEventListener('webkitfullscreenchange', fsHandlerWk);
      if (map) map.remove();
      gcMap = null;
    };
  });

  // ---------------------------------------------------------------------------
  // Sync map filters when year changes
  // ---------------------------------------------------------------------------

  $effect(() => {
    // Depend on gcYear
    const _y = gcYear;
    if (gcMap && gcMap.isStyleLoaded()) {
      updateMap();
    }
  });

  // ---------------------------------------------------------------------------
  // Redraw sparkline when year or lead data changes
  // ---------------------------------------------------------------------------

  $effect(() => {
    const _y = gcYear;
    const _data = gcLeadData;
    if (sparklineEl && _data) {
      drawSparkline(sparklineEl, _data, _y);
    }
  });
</script>

<div id="geocron">
  <div id="geocron-header">
    <div class="section-label">GeoCron</div>
    <h2>The Mediterranean World Through Time</h2>
    <p>Empires, trade routes, and shipwrecks from 1200 BCE to 800 CE. Drag the timeline to explore.</p>
  </div>
  <div id="geocron-wrap" bind:this={wrapEl}>
    <div id="geocron-map" bind:this={mapContainerEl}></div>
    {#if hoverVisible}
      <div id="geocron-hover-tooltip" style="left:{hoverLeft};top:{hoverTop}">
        {#if hoverEmpire}<div class="ht-empire">{hoverEmpire}</div>{/if}
        {#if hoverLines.length > 0}
          <div class="ht-detail">
            {#each hoverLines as line (line.text)}
              <div class="ht-line"><strong>{line.text}</strong>{#if line.sub} <span class="ht-sub">{line.sub}</span>{/if}</div>
            {/each}
          </div>
        {/if}
      </div>
    {/if}

    <button id="geocron-fullscreen-btn" title="Toggle fullscreen" onclick={toggleFullscreen}>
      {#if !fsCollapsed}
        <svg viewBox="0 0 20 20" id="fs-icon-expand">
          <polyline points="6 1 1 1 1 6"/><polyline points="14 1 19 1 19 6"/>
          <polyline points="6 19 1 19 1 14"/><polyline points="14 19 19 19 19 14"/>
        </svg>
      {:else}
        <svg viewBox="0 0 20 20" id="fs-icon-collapse">
          <polyline points="1 6 6 6 6 1"/><polyline points="19 6 14 6 14 1"/>
          <polyline points="1 14 6 14 6 19"/><polyline points="19 14 14 14 14 19"/>
        </svg>
      {/if}
    </button>

    {#if !loaded && !loadError}
      <div id="geocron-loading">Loading map data&hellip;</div>
    {:else if loadError}
      <div id="geocron-loading">Failed to load map data.</div>
    {/if}

    <div id="geocron-sidebar">
      <h4>Dashboard</h4>
      <div class="sidebar-stat"><span>Visible wrecks</span><span class="val" id="stat-wrecks">{statWrecks}</span></div>
      <div class="sidebar-stat"><span>Empires</span><span class="val" id="stat-empires">{statEmpires}</span></div>
      <div class="sidebar-stat"><span>Trade routes</span><span class="val" id="stat-routes">{statRoutes}</span></div>
      <div class="sidebar-stat" style="border:none"><span>Lead emissions</span><span class="val" id="stat-lead">{statLead ?? '—'}</span></div>
      <canvas id="sparkline-canvas" bind:this={sparklineEl}></canvas>
    </div>

    <div id="geocron-layer-toggles">
      <label class="layer-toggle" class:off={!gcLayerVisibility.borders} data-layer="borders">
        <input type="checkbox" checked={gcLayerVisibility.borders} onchange={(e) => handleLayerToggle('borders', e.target.checked)}>
        <span class="dot" style="background:var(--purple)"></span>Empires
      </label>
      <label class="layer-toggle" class:off={!gcLayerVisibility.routes} data-layer="routes">
        <input type="checkbox" checked={gcLayerVisibility.routes} onchange={(e) => handleLayerToggle('routes', e.target.checked)}>
        <span class="dot" style="background:var(--accent)"></span>Routes
      </label>
      <label class="layer-toggle" class:off={!gcLayerVisibility.wrecks} data-layer="wrecks">
        <input type="checkbox" checked={gcLayerVisibility.wrecks} onchange={(e) => handleLayerToggle('wrecks', e.target.checked)}>
        <span class="dot" style="background:var(--red)"></span>Shipwrecks
      </label>
      <label class="layer-toggle" class:off={!gcLayerVisibility.arcs} data-layer="arcs">
        <input type="checkbox" checked={gcLayerVisibility.arcs} onchange={(e) => handleLayerToggle('arcs', e.target.checked)}>
        <span class="dot" style="background:var(--teal)"></span>Trade arcs
      </label>
    </div>

    <div id="geocron-legend">
      <div class="legend-title">Legend</div>
      <div class="legend-item"><span class="legend-swatch"><span class="legend-line" style="background:#c9944a;width:18px;height:2.5px;display:inline-block;border-radius:1px"></span></span> Road</div>
      <div class="legend-item"><span class="legend-swatch"><span class="legend-line dashed" style="color:#5b8dd9;width:18px;height:2px;display:inline-block"></span></span> Sea route</div>
      <div class="legend-item"><span class="legend-swatch"><span class="legend-line dashed" style="color:#4fc3f7;width:18px;height:2px;display:inline-block"></span></span> River</div>
      <div class="legend-item"><span class="legend-anchor" style="color:#d94f4f">&#9875;</span> Wreck (West)</div>
      <div class="legend-item"><span class="legend-anchor" style="color:#5b8dd9">&#9875;</span> Wreck (East)</div>
      <div class="legend-item"><span class="legend-swatch" style="width:12px;height:12px;background:rgba(155,109,215,0.25);border:1px solid rgba(155,109,215,0.5);border-radius:2px;display:inline-block"></span> Empire</div>
    </div>

    <div id="geocron-controls">
      <div id="geocron-year-display">{yearDisplay.abs} <span class="era-label">{yearDisplay.era}</span></div>
      <div id="geocron-context">{contextText}</div>
      <div id="geocron-slider-row">
        <button id="geocron-play" title="Play / Pause" onclick={togglePlay}>
          {#if gcPlaying}&#10074;&#10074;{:else}&#9654;{/if}
        </button>
        <input
          type="range"
          id="geocron-slider"
          bind:this={sliderEl}
          min="-1200"
          max="800"
          value={gcYear}
          step="1"
          oninput={(e) => {
            gcYear = parseInt(e.target.value);
            updateMap();
          }}
        >
      </div>
      <div id="geocron-event-ticks">
        {#each eventTicks as tick (tick.label)}
          <div class="event-tick" style="left:{tick.pct}%"></div>
          <div class="event-tick-label row-{tick.row}" style="left:{tick.pct}%">{tick.label}</div>
        {/each}
      </div>
    </div>
  </div>
</div>
