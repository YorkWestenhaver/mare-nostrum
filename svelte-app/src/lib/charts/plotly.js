// ============================================================
// SHARED CHART FOUNDATION
// ============================================================

export const LAYOUT_BASE = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)',
  font: {family: '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif', color: '#8b8fa3', size: 12},
  margin: {l: 60, r: 30, t: 40, b: 50},
  hovermode: 'x unified',
  xaxis: {
    gridcolor: 'rgba(42, 48, 60, 0.5)',
    zerolinecolor: 'rgba(42, 48, 60, 0.5)',
    tickfont: {size: 11}
  },
  yaxis: {
    gridcolor: 'rgba(42, 48, 60, 0.5)',
    zerolinecolor: 'rgba(42, 48, 60, 0.5)',
    tickfont: {size: 11}
  },
  legend: {
    bgcolor: 'rgba(0,0,0,0)',
    font: {size: 11}
  }
};

export const PLOTLY_CONFIG = {
  displayModeBar: true,
  modeBarButtonsToRemove: ['select2d', 'lasso2d', 'autoScale2d'],
  displaylogo: false,
  responsive: true
};

export function mergeLayout(overrides) {
  return {
    ...LAYOUT_BASE,
    ...overrides,
    xaxis: {...LAYOUT_BASE.xaxis, ...(overrides.xaxis || {})},
    yaxis: {...LAYOUT_BASE.yaxis, ...(overrides.yaxis || {})}
  };
}

// ============================================================
// REUSABLE OVERLAY SHAPES (defined once, referenced by name)
// ============================================================

export const OVERLAYS = {
  antoninePlague: {
    type: 'rect', xref: 'x', yref: 'paper',
    x0: 165, x1: 193, y0: 0, y1: 1,
    fillcolor: 'rgba(217,79,79,0.06)', line: {width: 0}
  },
  cyprianPlague: {
    type: 'rect', xref: 'x', yref: 'paper',
    x0: 249, x1: 270, y0: 0, y1: 1,
    fillcolor: 'rgba(217,79,79,0.06)', line: {width: 0}
  },
  thirdCenturyCrisis: {
    type: 'rect', xref: 'x', yref: 'paper',
    x0: 235, x1: 285, y0: 0, y1: 1,
    fillcolor: 'rgba(217,79,79,0.08)', line: {width: 0}
  },
  lateAntiqueLIA: {
    type: 'rect', xref: 'x', yref: 'paper',
    x0: 536, x1: 660, y0: 0, y1: 1,
    fillcolor: 'rgba(91,141,217,0.08)', line: {width: 0}
  },
  fallOfWest: {
    type: 'line', xref: 'x', yref: 'paper',
    x0: 476, x1: 476, y0: 0, y1: 1,
    line: {color: '#9b6dd7', width: 1.5, dash: 'dot'}
  },
  islamicConquest: {
    type: 'line', xref: 'x', yref: 'paper',
    x0: 636, x1: 636, y0: 0, y1: 1,
    line: {color: '#e6b86e', width: 1.5, dash: 'dot'}
  },
  angloSaxonGap: {
    type: 'rect', xref: 'x', yref: 'paper',
    x0: 410, x1: 680, y0: 0, y1: 1,
    fillcolor: 'rgba(217,79,79,0.06)', line: {width: 0}
  },
  aureusToSolidus: {
    type: 'line', xref: 'x', yref: 'paper',
    x0: 309, x1: 309, y0: 0, y1: 1,
    line: {color: '#8b8fa3', width: 1.5, dash: 'dash'}
  }
};

// ============================================================
// EVENT HELPER FUNCTIONS
// ============================================================

export function eventShapes(events, yMax) {
  return events.map(e => ({
    type: 'line', x0: e.year, x1: e.year, y0: 0, y1: yMax,
    line: {color: e.color, width: 1, dash: 'dot'},
    opacity: 0.5
  }));
}

export function eventAnnotations(events, yMax) {
  return events.map((e, i) => ({
    x: e.year, y: yMax * (0.95 - (i % 3) * 0.08),
    text: e.label, showarrow: false,
    font: {size: 9, color: e.color},
    xanchor: 'left', xshift: 4
  }));
}
