<script>
  import 'maplibre-gl/dist/maplibre-gl.css';

  const TIME_MIN = -3400;
  const TIME_MAX = 2024;

  const POLITY_COLORS = [
    '#9b6dd7', '#7b5ea7', '#6d5baf', '#8e7cc3', '#b39ddb',
    '#5b8dd9', '#7986cb', '#64b5f6', '#4fc3f7', '#4dd0e1',
    '#4fad7a', '#66bb6a', '#81c784', '#aed581', '#c5e1a5',
    '#d94f4f', '#e57373', '#ef5350', '#f06292', '#ce93d8',
    '#c9944a', '#e6b86e', '#ffb74d', '#ffa726', '#ff8a65',
    '#26a69a', '#42a5f5', '#ab47bc', '#ec407a', '#78909c',
  ];

  let gcYear = $state(1001);
  let gcPlaying = $state(false);
  let gcAnimId = $state(null);
  let loaded = $state(false);
  let loadError = $state(false);

  let gcBorders = $state(null);

  let yearDisplay = $derived(formatYearDisplay(gcYear));

  let statPolities = $derived(computeStatPolities(gcBorders, gcYear));
  let statLargest = $derived(computeStatLargest(gcBorders, gcYear));
  let statTotalArea = $derived(computeStatTotalArea(gcBorders, gcYear));

  let gcMap = null;

  let mapContainerEl = $state(null);
  let wrapEl = $state(null);
  let sliderEl = $state(null);

  let hoverVisible = $state(false);
  let hoverLeft = $state('0px');
  let hoverTop = $state('0px');
  let hoverName = $state('');
  let hoverPeriod = $state('');
  let hoverArea = $state('');
  let fsCollapsed = $state(false);

  let playSpeed = $state(5);

  function yearLabel(y) {
    if (y < 0) return Math.abs(y) + ' BCE';
    if (y === 0) return '1 BCE';
    return y + ' CE';
  }

  function formatYearDisplay(y) {
    return { abs: Math.abs(y) || 1, era: y <= 0 ? 'BCE' : 'CE' };
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

  function computeStatPolities(borders, year) {
    if (!borders) return 0;
    let count = 0;
    for (const f of borders.features) {
      if (f.properties.from <= year && f.properties.to >= year) count++;
    }
    return count;
  }

  function computeStatLargest(borders, year) {
    if (!borders) return null;
    let best = null;
    let bestArea = 0;
    for (const f of borders.features) {
      if (f.properties.from <= year && f.properties.to >= year) {
        const a = f.properties.area || 0;
        if (a > bestArea) { bestArea = a; best = f.properties.name; }
      }
    }
    if (!best) return null;
    return { name: best, area: bestArea };
  }

  function computeStatTotalArea(borders, year) {
    if (!borders) return 0;
    let total = 0;
    for (const f of borders.features) {
      if (f.properties.from <= year && f.properties.to >= year) {
        total += (f.properties.area || 0);
      }
    }
    return total;
  }

  function formatArea(km2) {
    if (km2 >= 1_000_000) return (km2 / 1_000_000).toFixed(1) + 'M';
    if (km2 >= 1_000) return (km2 / 1_000).toFixed(0) + 'K';
    return Math.round(km2).toString();
  }

  const TIME_FILTER = (y) => ['all', ['<=', 'from', y], ['>=', 'to', y]];

  function updateMap() {
    if (!gcMap) return;
    const y = gcYear;
    const tf = TIME_FILTER(y);
    try {
      if (gcMap.getLayer('world-borders-fill')) gcMap.setFilter('world-borders-fill', tf);
      if (gcMap.getLayer('world-borders-line')) gcMap.setFilter('world-borders-line', tf);
    } catch (_) {}
  }

  let lastTick = 0;
  function animateTimeline(ts) {
    if (!gcPlaying) return;
    if (ts - lastTick > 40) {
      lastTick = ts;
      gcYear += playSpeed;
      if (gcYear > TIME_MAX) { gcYear = TIME_MIN; }
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

  $effect(() => {
    if (!mapContainerEl) return;

    let map = null;
    let fsHandler = null;
    let fsHandlerWk = null;

    (async () => {
      const maplibregl = (await import('maplibre-gl')).default;

      map = new maplibregl.Map({
        container: mapContainerEl,
        projection: { type: 'mercator' },
        style: {
          version: 8,
          name: 'Cliopatria Globe',
          sky: {
            "sky-color": "#060810",
            "horizon-color": "#0a0e16",
            "fog-color": "#060810",
            "sky-horizon-blend": 0.5,
            "horizon-fog-blend": 0.5,
            "fog-ground-blend": 0.5
          },
          sources: {
            'satellite': {
              type: 'raster',
              tiles: [
                'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
              ],
              tileSize: 256,
              maxzoom: 18,
              attribution: '&copy; <a href="https://www.esri.com/">Esri</a>'
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
              'raster-opacity': 0.65,
              'raster-saturation': -0.4,
              'raster-brightness-min': 0.02,
              'raster-brightness-max': 0.45,
              'raster-contrast': 0.1
            }
          }]
        },
        center: [20, 25],
        zoom: 1.8,
        minZoom: 1,
        maxZoom: 10,
      });

      gcMap = map;
      map.addControl(new maplibregl.NavigationControl({ showCompass: true }), 'bottom-right');

      let borders;
      try {
        borders = await loadJSON('/data/geo/world_borders.json');
      } catch (err) {
        console.error('Cliopatria: Failed to load world_borders.json', err);
        loadError = true;
        return;
      }

      gcBorders = borders;

      map.on('load', () => {
        const bordersWithColors = {
          ...borders,
          features: borders.features.map(f => ({
            ...f,
            properties: { ...f.properties, color: polityColor(f.properties.name) }
          }))
        };

        map.addSource('world-borders', { type: 'geojson', data: bordersWithColors });

        map.addLayer({
          id: 'world-borders-fill',
          type: 'fill',
          source: 'world-borders',
          paint: {
            'fill-color': ['get', 'color'],
            'fill-opacity': 0.28,
          },
          filter: TIME_FILTER(gcYear)
        });
        map.addLayer({
          id: 'world-borders-line',
          type: 'line',
          source: 'world-borders',
          paint: {
            'line-color': ['get', 'color'],
            'line-width': ['interpolate', ['linear'], ['zoom'], 1, 0.5, 4, 1.5, 8, 2.5],
            'line-opacity': 0.55,
          },
          filter: TIME_FILTER(gcYear)
        });

        const popup = new maplibregl.Popup({ closeButton: true, closeOnClick: false, maxWidth: '340px' });

        map.on('click', 'world-borders-fill', (e) => {
          e.originalEvent.stopPropagation();
          const f = e.features[0];
          const p = f.properties;
          let html = '<div class="popup-title">' + p.name + '</div><div class="popup-detail">';
          html += '<b>Period:</b> ' + yearLabel(p.from) + ' \u2013 ' + yearLabel(p.to) + '<br>';
          if (p.area) html += '<b>Area:</b> ~' + Math.round(p.area).toLocaleString() + ' km\u00B2<br>';
          if (p.wiki) html += '<a href="https://en.wikipedia.org/wiki/' + encodeURIComponent(p.wiki) + '" target="_blank" rel="noopener" style="color:var(--accent)">Wikipedia</a>';
          html += '</div>';
          popup.setLngLat(e.lngLat).setHTML(html).addTo(map);
        });

        map.on('click', (e) => {
          const feats = map.queryRenderedFeatures(e.point, { layers: ['world-borders-fill'] });
          if (!feats || feats.length === 0) popup.remove();
        });

        map.on('mouseenter', 'world-borders-fill', () => { map.getCanvas().style.cursor = 'pointer'; });
        map.on('mouseleave', 'world-borders-fill', () => { map.getCanvas().style.cursor = ''; });

        map.on('mousemove', (e) => {
          if (!wrapEl) return;
          const feats = map.queryRenderedFeatures(e.point, { layers: ['world-borders-fill'] });
          if (!feats || feats.length === 0) {
            hoverVisible = false;
            return;
          }
          const p = feats[0].properties;
          hoverName = p.name || '';
          hoverPeriod = yearLabel(p.from) + ' \u2013 ' + yearLabel(p.to);
          hoverArea = p.area ? '~' + formatArea(p.area) + ' km\u00B2' : '';
          hoverVisible = true;

          const rect = wrapEl.getBoundingClientRect();
          let tipX = e.point.x + 14;
          let tipY = e.point.y + 14;
          if (tipX + 220 > rect.width - 10) tipX = e.point.x - 220 - 10;
          if (tipY + 60 > rect.height - 10) tipY = e.point.y - 60 - 10;
          hoverLeft = tipX + 'px';
          hoverTop = tipY + 'px';
        });

        map.on('mouseout', () => { hoverVisible = false; });

        updateMap();

        map.once('idle', () => {
          updateMap();
          loaded = true;
        });
      });

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

  $effect(() => {
    const _y = gcYear;
    if (gcMap && gcMap.isStyleLoaded()) {
      updateMap();
    }
  });
</script>

<div id="cliopatria">
  <div id="cliopatria-header">
    <div class="section-label">Cliopatria</div>
    <h2>Every Civilization in History</h2>
    <p>1,876 polities across 5,400 years. Drag the timeline to explore the political geography of the world from 3400 BCE to 2024 CE.</p>
  </div>
  <div id="cliopatria-wrap" bind:this={wrapEl}>
    <div id="cliopatria-map" bind:this={mapContainerEl} class:loaded></div>

    {#if hoverVisible}
      <div class="clio-hover-tooltip" style="left:{hoverLeft};top:{hoverTop};display:block">
        <div class="ht-empire">{hoverName}</div>
        <div class="ht-detail">{hoverPeriod}</div>
        {#if hoverArea}<div class="ht-detail">{hoverArea}</div>{/if}
      </div>
    {/if}

    <button class="clio-fullscreen-btn" title="Toggle fullscreen" onclick={toggleFullscreen}>
      {#if !fsCollapsed}
        <svg viewBox="0 0 20 20">
          <polyline points="6 1 1 1 1 6"/><polyline points="14 1 19 1 19 6"/>
          <polyline points="6 19 1 19 1 14"/><polyline points="14 19 19 19 19 14"/>
        </svg>
      {:else}
        <svg viewBox="0 0 20 20">
          <polyline points="1 6 6 6 6 1"/><polyline points="19 6 14 6 14 1"/>
          <polyline points="1 14 6 14 6 19"/><polyline points="19 14 14 14 14 19"/>
        </svg>
      {/if}
    </button>

    {#if !loaded && !loadError}
      <div class="clio-loading">Loading world data&hellip;</div>
    {:else if loadError}
      <div class="clio-loading">Failed to load world data.</div>
    {/if}

    <div class="clio-sidebar">
      <h4>Dashboard</h4>
      <div class="sidebar-stat"><span>Polities</span><span class="val">{statPolities}</span></div>
      <div class="sidebar-stat">
        <span>Largest</span>
        <span class="val">{statLargest ? statLargest.name : '\u2014'}</span>
      </div>
      <div class="sidebar-stat">
        <span>Largest area</span>
        <span class="val">{statLargest ? formatArea(statLargest.area) + ' km\u00B2' : '\u2014'}</span>
      </div>
      <div class="sidebar-stat" style="border:none">
        <span>Total area</span>
        <span class="val">{formatArea(statTotalArea)} km&sup2;</span>
      </div>
    </div>

    <div class="clio-controls">
      <div class="clio-year-display">{yearDisplay.abs} <span class="era-label">{yearDisplay.era}</span></div>
      <div class="clio-slider-row">
        <button class="clio-play" title="Play / Pause" onclick={togglePlay}>
          {#if gcPlaying}&#10074;&#10074;{:else}&#9654;{/if}
        </button>
        <input
          type="range"
          class="clio-slider"
          bind:this={sliderEl}
          min={TIME_MIN}
          max={TIME_MAX}
          value={gcYear}
          step="1"
          oninput={(e) => {
            gcYear = parseInt(e.target.value);
            updateMap();
          }}
        >
      </div>
      <div class="clio-range-labels">
        <span>3400 BCE</span>
        <div class="clio-speed-control">
          <button class:active={playSpeed === 1} onclick={() => playSpeed = 1}>1x</button>
          <button class:active={playSpeed === 5} onclick={() => playSpeed = 5}>5x</button>
          <button class:active={playSpeed === 20} onclick={() => playSpeed = 20}>20x</button>
          <button class:active={playSpeed === 50} onclick={() => playSpeed = 50}>50x</button>
        </div>
        <span>2024 CE</span>
      </div>
    </div>
  </div>
  <div class="clio-source">
    Data: <a href="https://doi.org/10.5281/zenodo.14714684" target="_blank" rel="noopener">Cliopatria</a> (Bennett et al. 2025, <a href="https://www.nature.com/articles/s41597-025-04516-9" target="_blank" rel="noopener">Scientific Data</a>). CC BY 4.0. 12,406 polity records from 3400 BCE to 2024 CE.
  </div>
</div>

<style>
  #cliopatria {
    position: relative;
    width: 100%;
    max-width: 100%;
    padding: 0;
    margin: 0;
  }

  #cliopatria-header {
    text-align: center;
    padding: 3rem 2rem 1.5rem;
    max-width: 960px;
    margin: 0 auto;
  }
  #cliopatria-header .section-label { margin-bottom: 0.5rem; }
  #cliopatria-header h2 { margin-bottom: 0.5rem; }
  #cliopatria-header p { color: var(--text-muted); font-size: 0.95rem; }

  #cliopatria-wrap {
    position: relative;
    width: 100%;
    height: 85vh;
    min-height: 500px;
    max-height: 1000px;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
  }

  #cliopatria-wrap:fullscreen,
  #cliopatria-wrap:-webkit-full-screen {
    max-height: none;
    height: 100vh;
    border: none;
    background: #060810;
  }

  #cliopatria-map {
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 0.8s ease;
  }
  #cliopatria-map.loaded { opacity: 1; }

  .clio-loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-sans);
    font-size: 1rem;
    color: var(--text-muted);
    z-index: 5;
  }

  .clio-fullscreen-btn {
    position: absolute;
    top: 12px;
    right: 12px;
    z-index: 12;
    width: 34px;
    height: 34px;
    background: rgba(12,15,19,0.85);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text-muted);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(8px);
    transition: border-color 0.2s, color 0.2s;
    padding: 0;
  }
  .clio-fullscreen-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
  }
  .clio-fullscreen-btn svg {
    width: 16px;
    height: 16px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .clio-hover-tooltip {
    position: absolute;
    z-index: 20;
    pointer-events: none;
    background: rgba(12,15,19,0.92);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 11px;
    font-family: var(--font-sans);
    font-size: 12px;
    color: var(--text);
    line-height: 1.5;
    max-width: 280px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    backdrop-filter: blur(8px);
    display: none;
  }
  .clio-hover-tooltip .ht-empire {
    color: #b39ddb;
    font-weight: 600;
    font-size: 13px;
  }
  .clio-hover-tooltip .ht-detail {
    color: var(--text-muted);
    font-size: 11px;
  }

  .clio-sidebar {
    position: absolute;
    top: 12px;
    left: 12px;
    z-index: 10;
    width: 220px;
    background: rgba(12,15,19,0.88);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
    backdrop-filter: blur(10px);
    font-family: var(--font-sans);
  }
  .clio-sidebar h4 {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent);
    margin-bottom: 8px;
  }
  .clio-sidebar .sidebar-stat {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: var(--text-muted);
    padding: 3px 0;
    border-bottom: 1px solid rgba(42,48,60,0.5);
  }
  .clio-sidebar .sidebar-stat .val {
    color: var(--text-heading);
    font-weight: 600;
    font-variant-numeric: tabular-nums;
    max-width: 120px;
    text-align: right;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .clio-controls {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 10;
    background: linear-gradient(transparent, rgba(12,15,19,0.92) 30%);
    padding: 3rem 2rem 1.2rem;
  }

  .clio-year-display {
    text-align: center;
    font-family: var(--font);
    font-size: clamp(1.8rem, 3vw, 2.6rem);
    color: var(--text-heading);
    margin-bottom: 0.5rem;
    font-variant-numeric: tabular-nums;
  }
  .clio-year-display .era-label {
    font-size: 0.55em;
    color: var(--accent);
    margin-left: 0.25em;
    font-family: var(--font-sans);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .clio-slider-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    max-width: 900px;
    margin: 0 auto;
  }

  .clio-play {
    background: none;
    border: 2px solid var(--accent);
    color: var(--accent);
    width: 38px;
    height: 38px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: background 0.2s, color 0.2s;
    font-size: 16px;
  }
  .clio-play:hover {
    background: var(--accent);
    color: var(--bg);
  }

  .clio-slider {
    flex: 1;
    -webkit-appearance: none;
    appearance: none;
    height: 6px;
    border-radius: 3px;
    background: var(--border);
    outline: none;
    cursor: pointer;
  }
  .clio-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid var(--bg);
    cursor: grab;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
  }
  .clio-slider::-moz-range-thumb {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid var(--bg);
    cursor: grab;
  }

  .clio-range-labels {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 900px;
    margin: 0.4rem auto 0;
    font-family: var(--font-sans);
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding-left: 52px;
  }

  .clio-speed-control {
    display: flex;
    gap: 2px;
  }
  .clio-speed-control button {
    background: rgba(42, 48, 60, 0.6);
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-family: var(--font-sans);
    font-size: 9px;
    padding: 2px 8px;
    border-radius: 3px;
    cursor: pointer;
    transition: all 0.15s;
  }
  .clio-speed-control button:hover {
    border-color: var(--accent);
    color: var(--accent);
  }
  .clio-speed-control button.active {
    background: var(--accent);
    color: var(--bg);
    border-color: var(--accent);
  }

  .clio-source {
    text-align: center;
    padding: 1rem 2rem;
    font-family: var(--font-sans);
    font-size: 0.75rem;
    color: var(--text-muted);
  }
  .clio-source a {
    color: var(--accent);
    text-decoration: none;
  }
  .clio-source a:hover { text-decoration: underline; }

  @media (max-width: 768px) {
    #cliopatria-wrap { height: 75vh; min-height: 400px; }
    .clio-sidebar { display: none; }
    .clio-controls { padding: 2rem 1rem 1rem; }
    .clio-range-labels { padding-left: 46px; }
  }
</style>
