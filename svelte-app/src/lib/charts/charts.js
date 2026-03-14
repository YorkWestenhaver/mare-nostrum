// ============================================================
// ALL CHART CONFIGURATIONS
// ============================================================

import { mergeLayout, LAYOUT_BASE, OVERLAYS } from './plotly.js';
import {
  LEAD_DATA, LEAD_SEGMENTS, SEGMENT_COLORS,
  SHIPWRECKS_25, SHIPWRECKS_50,
  DENARIUS, AUREUS_DATA, SOLIDUS_DATA, DIRHAM_DATA,
  WHEAT_PRICES, CHRE_HOARDS, INSCRIPTIONS_DATA,
  POPULATION, TREE_RINGS, VOLCANIC_EVENTS, POLLEN_DATA,
  CHURCH_DATA, PAS_COINS
} from '$lib/data/datasets.js';
import { CHANGEPOINTS, HISTORICAL_EVENTS } from '$lib/data/events.js';

export const CHARTS = {

  // ============================================================
  // 1. LEAD EMISSIONS
  // ============================================================
  lead: () => {
    const x = LEAD_DATA.map(d => d.year);
    const y = LEAD_DATA.map(d => d.emissions);

    const shapes = LEAD_SEGMENTS.map((seg, i) => ({
      type: 'rect', xref: 'x', yref: 'paper',
      x0: seg.start, x1: seg.end, y0: 0, y1: 1,
      fillcolor: SEGMENT_COLORS[i], line: {width: 0}
    }));

    CHANGEPOINTS.lead.forEach(cp => {
      shapes.push({
        type: 'line', x0: cp, x1: cp, y0: 0, y1: 1,
        xref: 'x', yref: 'paper',
        line: {color: '#d94f4f', width: 1.5, dash: 'dash'}
      });
    });

    const segLines = LEAD_SEGMENTS.map(seg => ({
      type: 'scatter', mode: 'lines',
      x: [seg.start, seg.end], y: [seg.mean, seg.mean],
      line: {color: '#e6b86e', width: 2, dash: 'solid'},
      showlegend: false, hoverinfo: 'skip'
    }));

    const traces = [
      {
        type: 'scatter', mode: 'lines',
        x, y,
        line: {color: '#4fb5ad', width: 1.2},
        fill: 'tozeroy',
        fillcolor: 'rgba(79, 181, 173, 0.08)',
        name: 'Lead emissions (kt/yr)',
        hovertemplate: '%{x} CE<br>%{y:.3f} kt/yr<extra></extra>'
      },
      ...segLines
    ];

    const layout = mergeLayout({
      title: {text: 'European Lead Emissions (600 BCE \u2013 800 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [-620, 810]},
      yaxis: {title: 'Lead Emissions (kt/yr)', rangemode: 'tozero'},
      shapes,
      annotations: CHANGEPOINTS.lead.map(cp => ({
        x: cp, y: 1.02, xref: 'x', yref: 'paper',
        text: `${Math.abs(Math.round(cp))} ${cp < 0 ? 'BCE' : 'CE'}`,
        showarrow: true, arrowhead: 0, arrowcolor: '#d94f4f',
        ax: 0, ay: -25,
        font: {size: 10, color: '#d94f4f'}
      }))
    });

    return {traces, layout};
  },

  // ============================================================
  // 7. LEAD ZOOM (Augustan peak)
  // ============================================================
  leadZoom: () => {
    const filtered = LEAD_DATA.filter(d => d.year >= -100 && d.year <= 200);
    const x = filtered.map(d => d.year);
    const y = filtered.map(d => d.emissions);

    const events = [
      {year: -19, label: 'Cantabrian Wars end', color: '#4fad7a'},
      {year: 14, label: 'Death of Augustus', color: '#5b8dd9'},
      {year: 64, label: "Nero's reform", color: '#e6b86e'},
      {year: 79, label: 'Vesuvius erupts', color: '#d94f4f'},
      {year: 165, label: 'Antonine Plague', color: '#d94f4f'}
    ];

    const traces = [{
      type: 'scatter', mode: 'lines',
      x, y,
      line: {color: '#4fb5ad', width: 2},
      fill: 'tozeroy',
      fillcolor: 'rgba(79, 181, 173, 0.12)',
      name: 'Lead emissions (kt/yr)',
      hovertemplate: '%{x} CE<br>%{y:.3f} kt/yr<extra></extra>'
    }];

    const layout = mergeLayout({
      title: {text: 'Lead Emissions: The Augustan Peak (100 BCE \u2013 200 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [-110, 210]},
      yaxis: {title: 'Lead Emissions (kt/yr)', rangemode: 'tozero'},
      shapes: events.map(e => ({
        type: 'line', x0: e.year, x1: e.year, y0: 0, y1: 1,
        xref: 'x', yref: 'paper',
        line: {color: e.color, width: 1.5, dash: 'dot'}
      })),
      annotations: events.map((e, i) => ({
        x: e.year, y: 1.02 - (i % 2) * 0.1, xref: 'x', yref: 'paper',
        text: e.label, showarrow: false,
        font: {size: 9, color: e.color},
        xanchor: 'left', xshift: 4
      }))
    });

    return {traces, layout};
  },

  // ============================================================
  // 2. SHIPWRECKS (stacked area)
  // ============================================================
  shipwrecks: () => {
    const x = SHIPWRECKS_25.map(d => d.mid);
    const regions = [
      {key: 'western', name: 'Western Med', color: '#5b8dd9'},
      {key: 'eastern', name: 'Eastern Med', color: '#d94f4f'},
      {key: 'adriatic', name: 'Adriatic', color: '#4fb5ad'},
      {key: 'black_sea', name: 'Black Sea', color: '#9b6dd7'},
    ];

    const traces = regions.map(r => ({
      type: 'scatter', mode: 'lines', name: r.name,
      x, y: SHIPWRECKS_25.map(d => d[r.key]),
      stackgroup: 'one',
      line: {width: 0.5, color: r.color},
      hovertemplate: `${r.name}: %{y:.1f}<extra></extra>`
    }));

    const layout = mergeLayout({
      title: {text: 'Mediterranean Shipwreck Density (25-year bins)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [-620, 1010]},
      yaxis: {title: 'Wrecks per 25-year bin', rangemode: 'tozero'},
    });

    return {traces, layout};
  },

  // ============================================================
  // 3. REGIONAL DIVERGENCE (W vs E)
  // ============================================================
  divergence: () => {
    const x = SHIPWRECKS_50.map(d => d.mid);
    const west = SHIPWRECKS_50.map(d => d.western);
    const east = SHIPWRECKS_50.map(d => d.eastern);

    const traces = [
      {
        type: 'scatter', mode: 'lines+markers',
        x, y: west, name: 'Western Med',
        line: {color: '#5b8dd9', width: 2.5},
        marker: {size: 5},
        hovertemplate: 'Western: %{y:.1f} wrecks<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines+markers',
        x, y: east, name: 'Eastern Med',
        line: {color: '#d94f4f', width: 2.5},
        marker: {size: 5},
        hovertemplate: 'Eastern: %{y:.1f} wrecks<extra></extra>'
      }
    ];

    const layout = mergeLayout({
      title: {text: 'Western vs. Eastern Mediterranean Shipwrecks', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [-620, 1010]},
      yaxis: {title: 'Wrecks per 50-year bin', rangemode: 'tozero'},
      shapes: [
        OVERLAYS.fallOfWest,
        OVERLAYS.islamicConquest
      ],
      annotations: [
        {x: 476, y: 1.02, xref: 'x', yref: 'paper', text: 'Fall of Western Empire (476)', showarrow: false, font: {size: 10, color: '#9b6dd7'}, xanchor: 'left', xshift: 4},
        {x: 636, y: 0.92, xref: 'x', yref: 'paper', text: 'Islamic conquests (636)', showarrow: false, font: {size: 10, color: '#e6b86e'}, xanchor: 'left', xshift: 4}
      ]
    });

    return {traces, layout};
  },

  // ============================================================
  // 3b. W/E RATIO CHART
  // ============================================================
  ratio: () => {
    const x = SHIPWRECKS_50.map(d => d.mid);
    const west = SHIPWRECKS_50.map(d => d.western);
    const east = SHIPWRECKS_50.map(d => d.eastern);

    const ratioX = [];
    const ratioY = [];
    for (let i = 0; i < x.length; i++) {
      if (east[i] > 0.5) {
        ratioX.push(x[i]);
        ratioY.push(west[i] / east[i]);
      }
    }

    const traces = [{
      type: 'scatter', mode: 'lines+markers',
      x: ratioX, y: ratioY, name: 'W/E Ratio',
      line: {color: '#e6b86e', width: 2.5},
      marker: {size: 5, color: '#e6b86e'},
      fill: 'tozeroy',
      fillcolor: 'rgba(230, 184, 110, 0.08)',
      hovertemplate: '%{x} CE<br>Ratio: %{y:.2f}<extra></extra>'
    }];

    const layout = mergeLayout({
      title: {text: 'Western-to-Eastern Trade Ratio', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [-620, 1010]},
      yaxis: {title: 'West / East ratio', rangemode: 'tozero'},
      shapes: [
        {type: 'line', x0: -620, x1: 1010, y0: 1, y1: 1, line: {color: '#8b8fa3', width: 1, dash: 'dash'}}
      ],
      annotations: [
        {x: 1010, y: 1, xref: 'x', yref: 'y', text: 'Parity', showarrow: false, font: {size: 10, color: '#8b8fa3'}, xanchor: 'right', yshift: 12}
      ]
    });

    return {traces, layout};
  },

  // ============================================================
  // 4. DENARIUS SILVER CONTENT
  // ============================================================
  denarius: () => {
    const x = DENARIUS.map(d => d.year);
    const y = DENARIUS.map(d => d.silver);
    const labels = DENARIUS.map(d => d.emperor);

    const traces = [{
      type: 'scatter', mode: 'lines+markers',
      x, y,
      line: {color: '#e6b86e', width: 2.5},
      marker: {size: 7, color: '#e6b86e', line: {color: '#0c0f13', width: 1.5}},
      text: labels,
      hovertemplate: '%{text}<br>%{x} CE<br>Silver: %{y}%<extra></extra>',
      fill: 'tozeroy',
      fillcolor: 'rgba(230, 184, 110, 0.06)',
      name: 'Silver %'
    }];

    const layout = mergeLayout({
      title: {text: 'Denarius Silver Content (210 BCE \u2013 294 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [-230, 310]},
      yaxis: {title: 'Silver Content (%)', range: [0, 105]},
      shapes: [
        {type: 'rect', x0: 253, x1: 268, y0: 0, y1: 1, xref: 'x', yref: 'paper', fillcolor: 'rgba(217, 79, 79, 0.1)', line: {width: 0}},
        OVERLAYS.antoninePlague,
      ],
      annotations: [
        {x: 260, y: 18, text: 'Crisis of the<br>Third Century', showarrow: false, font: {size: 10, color: '#d94f4f'}},
        {x: 179, y: 82, text: 'Antonine<br>Plague', showarrow: false, font: {size: 10, color: '#d94f4f'}},
      ]
    });

    return {traces, layout};
  },

  // ============================================================
  // 8. GOLD COINAGE (Aureus + Solidus, dual y-axis)
  // ============================================================
  gold: () => {
    const traces = [
      {
        type: 'scatter', mode: 'lines+markers', name: 'Aureus weight (g)',
        x: AUREUS_DATA.map(d => d.year), y: AUREUS_DATA.map(d => d.weight),
        text: AUREUS_DATA.map(d => d.label),
        line: {color: '#e6b86e', width: 2.5},
        marker: {size: 7, color: '#e6b86e', line: {color: '#0c0f13', width: 1.5}},
        hovertemplate: '%{text}<br>%{x} CE<br>Weight: %{y:.2f}g<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines+markers', name: 'Solidus weight (g)',
        x: SOLIDUS_DATA.map(d => d.year), y: SOLIDUS_DATA.map(d => d.weight),
        text: SOLIDUS_DATA.map(d => d.label),
        line: {color: '#c9944a', width: 2.5, dash: 'dot'},
        marker: {size: 7, color: '#c9944a', symbol: 'diamond', line: {color: '#0c0f13', width: 1.5}},
        hovertemplate: '%{text}<br>%{x} CE<br>Weight: %{y:.2f}g<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines+markers', name: 'Solidus purity (%)',
        x: SOLIDUS_DATA.map(d => d.year), y: SOLIDUS_DATA.map(d => d.purity),
        text: SOLIDUS_DATA.map(d => d.label),
        yaxis: 'y2',
        line: {color: '#d94f4f', width: 1.5, dash: 'dash'},
        marker: {size: 5, color: '#d94f4f'},
        hovertemplate: '%{text}<br>%{x} CE<br>Purity: %{y}%<extra></extra>'
      }
    ];

    const layout = {
      ...LAYOUT_BASE,
      title: {text: 'Gold Coinage: Aureus (46 BCE\u2013284 CE) \u2192 Solidus (309\u20131092 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {...LAYOUT_BASE.xaxis, title: 'Year CE', range: [-60, 1110]},
      yaxis: {...LAYOUT_BASE.yaxis, title: 'Weight (grams)', range: [0, 9]},
      yaxis2: {
        title: 'Gold Purity (%)',
        overlaying: 'y', side: 'right',
        range: [20, 105],
        gridcolor: 'rgba(42, 48, 60, 0.2)',
        tickfont: {size: 11, color: '#d94f4f'},
        titlefont: {color: '#d94f4f'}
      },
      margin: {l: 60, r: 60, t: 40, b: 50},
      shapes: [OVERLAYS.aureusToSolidus],
      annotations: [{
        x: 309, y: 1.02, xref: 'x', yref: 'paper',
        text: 'Aureus \u2192 Solidus (309 CE)', showarrow: false,
        font: {size: 9, color: '#8b8fa3'}, xanchor: 'left', xshift: 4
      }]
    };

    return {traces, layout};
  },

  // ============================================================
  // 9. DIRHAM
  // ============================================================
  dirham: () => {
    const traces = [{
      type: 'scatter', mode: 'lines+markers',
      x: DIRHAM_DATA.map(d => d.year), y: DIRHAM_DATA.map(d => d.weight),
      text: DIRHAM_DATA.map(d => d.label),
      line: {color: '#5b8dd9', width: 2.5},
      marker: {size: 7, color: '#5b8dd9', line: {color: '#0c0f13', width: 1.5}},
      hovertemplate: '%{text}<br>%{x} CE<br>Weight: %{y:.2f}g<extra></extra>',
      fill: 'tozeroy',
      fillcolor: 'rgba(91, 141, 217, 0.06)',
      name: 'Dirham weight (g)'
    }];

    const layout = mergeLayout({
      title: {text: 'Islamic Silver Dirham (696\u2013940 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [680, 960]},
      yaxis: {title: 'Weight (grams)', range: [2.0, 3.2]}
    });

    return {traces, layout};
  },

  // ============================================================
  // 10. WHEAT PRICES
  // ============================================================
  wheat: () => {
    const traces = [{
      type: 'scatter', mode: 'lines+markers',
      x: WHEAT_PRICES.map(d => d.year), y: WHEAT_PRICES.map(d => d.price),
      text: WHEAT_PRICES.map(d => d.note),
      line: {color: '#4fad7a', width: 2.5},
      marker: {size: 7, color: '#4fad7a', line: {color: '#0c0f13', width: 1.5}},
      hovertemplate: '%{text}<br>%{x} CE<br>%{y:.0f} dr/artaba<extra></extra>',
      name: 'Wheat price'
    }];

    const layout = mergeLayout({
      title: {text: 'Egyptian Wheat Prices (45\u2013290 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [30, 300]},
      yaxis: {title: 'Drachmas per artaba', type: 'log', dtick: 1},
      shapes: [
        {type: 'rect', x0: 165, x1: 193, y0: 0, y1: 1, xref: 'x', yref: 'paper', fillcolor: 'rgba(217, 79, 79, 0.08)', line: {width: 0}},
        OVERLAYS.cyprianPlague,
      ],
      annotations: [
        {x: 179, y: 2.3, text: 'Antonine<br>Plague', showarrow: false, font: {size: 9, color: '#d94f4f'}},
        {x: 260, y: 2.8, text: 'Plague of<br>Cyprian', showarrow: false, font: {size: 9, color: '#d94f4f'}}
      ]
    });

    return {traces, layout};
  },

  // ============================================================
  // 11. COIN HOARDS (CHRE)
  // ============================================================
  hoards: () => {
    const traces = [
      {
        type: 'bar',
        x: CHRE_HOARDS.map(d => d.mid), y: CHRE_HOARDS.map(d => d.total),
        marker: {
          color: CHRE_HOARDS.map(d => d.total > 300 ? '#d94f4f' : d.total > 150 ? '#e6b86e' : '#5b8dd9'),
          line: {color: '#0c0f13', width: 0.5}
        },
        width: 22,
        hovertemplate: '%{x} CE<br>%{y} hoards (total)<extra></extra>',
        name: 'Total Hoards'
      },
      {
        type: 'scatter', mode: 'lines+markers', name: 'Western',
        x: CHRE_HOARDS.map(d => d.mid), y: CHRE_HOARDS.map(d => d.western),
        line: {color: '#5b8dd9', width: 2},
        marker: {size: 4},
        hovertemplate: '%{x} CE<br>Western: %{y}<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines+markers', name: 'Eastern',
        x: CHRE_HOARDS.map(d => d.mid), y: CHRE_HOARDS.map(d => d.eastern),
        line: {color: '#d94f4f', width: 2},
        marker: {size: 4},
        hovertemplate: '%{x} CE<br>Eastern: %{y}<extra></extra>'
      }
    ];

    const layout = mergeLayout({
      title: {text: 'CHRE Coin Hoard Frequency (200 BCE\u2013500 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE (terminal date, 25-yr bins)', range: [-210, 510]},
      yaxis: {title: 'Number of hoards', rangemode: 'tozero'},
      shapes: [OVERLAYS.thirdCenturyCrisis],
      annotations: [
        {x: 260, y: 700, text: 'Crisis of the<br>Third Century', showarrow: false, font: {size: 10, color: '#d94f4f'}}
      ]
    });

    return {traces, layout};
  },

  // ============================================================
  // 12. INSCRIPTIONS (EDH)
  // ============================================================
  inscriptions: () => {
    const traces = [
      {
        type: 'scatter', mode: 'lines', name: 'Total Inscriptions',
        x: INSCRIPTIONS_DATA.map(d => d.mid), y: INSCRIPTIONS_DATA.map(d => d.total),
        fill: 'tozeroy',
        fillcolor: 'rgba(155, 109, 215, 0.15)',
        line: {color: '#9b6dd7', width: 2},
        hovertemplate: '%{x} CE<br>Total: %{y:.1f}<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines+markers', name: 'Western',
        x: INSCRIPTIONS_DATA.map(d => d.mid), y: INSCRIPTIONS_DATA.map(d => d.western),
        line: {color: '#5b8dd9', width: 2},
        marker: {size: 4},
        hovertemplate: '%{x} CE<br>Western: %{y:.1f}<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines+markers', name: 'Eastern',
        x: INSCRIPTIONS_DATA.map(d => d.mid), y: INSCRIPTIONS_DATA.map(d => d.eastern),
        line: {color: '#d94f4f', width: 2},
        marker: {size: 4},
        hovertemplate: '%{x} CE<br>Eastern: %{y:.1f}<extra></extra>'
      }
    ];

    const layout = mergeLayout({
      title: {text: 'Latin Inscriptions \u2014 EDH (200 BCE\u2013700 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE (25-yr bins)', range: [-210, 710]},
      yaxis: {title: 'Expected inscription count', rangemode: 'tozero'},
      annotations: [
        {x: 187.5, y: 6525.6, text: 'Severan peak', showarrow: true, ax: 40, ay: -30, font: {size: 10, color: '#9b6dd7'}, arrowcolor: '#9b6dd7'},
        {x: 262.5, y: 3253.7, text: 'Diocletianic decline', showarrow: true, ax: 60, ay: -40, font: {size: 10, color: '#d94f4f'}, arrowcolor: '#d94f4f'}
      ]
    });

    return {traces, layout};
  },

  // ============================================================
  // 13. POPULATION
  // ============================================================
  population: () => {
    const traces = [
      {
        type: 'scatter', mode: 'lines',
        x: [...POPULATION.map(d => d.year), ...POPULATION.map(d => d.year).reverse()],
        y: [...POPULATION.map(d => d.hi), ...POPULATION.map(d => d.lo).reverse()],
        fill: 'toself',
        fillcolor: 'rgba(155, 109, 215, 0.12)',
        line: {color: 'transparent'},
        showlegend: false, hoverinfo: 'skip',
        name: 'Uncertainty range'
      },
      {
        type: 'scatter', mode: 'lines+markers', name: 'Population (millions)',
        x: POPULATION.map(d => d.year), y: POPULATION.map(d => d.pop),
        text: POPULATION.map(d => d.label),
        line: {color: '#9b6dd7', width: 2.5},
        marker: {size: 7, color: '#9b6dd7', line: {color: '#0c0f13', width: 1.5}},
        hovertemplate: '%{text}<br>%{x} CE<br>~%{y}M people<extra></extra>'
      }
    ];

    const layout = mergeLayout({
      title: {text: 'Roman Empire Population Estimates (200 BCE\u2013600 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [-220, 620]},
      yaxis: {title: 'Population (millions)', range: [10, 85]},
      shapes: [
        OVERLAYS.antoninePlague,
        {type: 'rect', x0: 541, x1: 600, y0: 0, y1: 1, xref: 'x', yref: 'paper', fillcolor: 'rgba(217, 79, 79, 0.06)', line: {width: 0}}
      ],
      annotations: [
        {x: 179, y: 72, text: 'Antonine Plague', showarrow: false, font: {size: 9, color: '#d94f4f'}},
        {x: 570, y: 35, text: 'Justinianic<br>Plague', showarrow: false, font: {size: 9, color: '#d94f4f'}}
      ]
    });

    return {traces, layout};
  },

  // ============================================================
  // 14. CLIMATE (tree rings + volcanic, dual y-axis)
  // ============================================================
  climate: () => {
    const trX = TREE_RINGS.map(d => d.year);
    const trY = TREE_RINGS.map(d => d.temp);

    const traces = [
      {
        type: 'scatter', mode: 'lines', name: 'Summer temperature anomaly (\u00b0C)',
        x: trX, y: trY,
        line: {color: '#d94f4f', width: 1.8},
        fill: 'tozeroy',
        fillcolor: trY.map(t => t >= 0 ? 'rgba(79, 173, 122, 0.1)' : 'rgba(91, 141, 217, 0.1)'),
        hovertemplate: '%{x} CE<br>%{y:+.1f}\u00b0C<extra></extra>'
      },
      {
        type: 'bar', name: 'Volcanic sulfur (Tg SO\u2082)',
        x: VOLCANIC_EVENTS.map(d => d.year),
        y: VOLCANIC_EVENTS.map(d => -d.sulfur / 10),
        text: VOLCANIC_EVENTS.map(d => d.label),
        marker: {color: 'rgba(155, 109, 215, 0.7)', line: {color: '#9b6dd7', width: 1}},
        width: 8,
        yaxis: 'y2',
        hovertemplate: '%{text}<br>%{x} CE<br>%{customdata} Tg SO\u2082<extra></extra>',
        customdata: VOLCANIC_EVENTS.map(d => d.sulfur)
      }
    ];

    const layout = {
      ...LAYOUT_BASE,
      title: {text: 'Climate: Tree Rings & Volcanic Eruptions (500 BCE\u20131000 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {...LAYOUT_BASE.xaxis, title: 'Year CE', range: [-520, 1020]},
      yaxis: {...LAYOUT_BASE.yaxis, title: 'Temperature anomaly (\u00b0C)', range: [-3, 1.5]},
      yaxis2: {
        title: 'Eruption magnitude',
        overlaying: 'y', side: 'right',
        range: [-5, 1],
        showgrid: false,
        tickfont: {size: 11, color: '#9b6dd7'},
        titlefont: {color: '#9b6dd7'},
        tickvals: [-4, -3, -2, -1, 0],
        ticktext: ['40', '30', '20', '10', '0']
      },
      margin: {l: 60, r: 60, t: 40, b: 50},
      shapes: [OVERLAYS.lateAntiqueLIA],
      annotations: [{
        x: 598, y: -2.0, text: 'Late Antique<br>Little Ice Age', showarrow: false,
        font: {size: 10, color: '#5b8dd9'}
      }]
    };

    return {traces, layout};
  },

  // ============================================================
  // 15. POLLEN
  // ============================================================
  pollen: () => {
    const traces = [
      {
        type: 'scatter', mode: 'lines', name: 'Arboreal (forest)',
        x: POLLEN_DATA.map(d => d.mid), y: POLLEN_DATA.map(d => d.arboreal),
        stackgroup: 'one',
        line: {width: 0.5, color: '#4fad7a'},
        fillcolor: 'rgba(79, 173, 122, 0.4)',
        hovertemplate: 'Forest: %{y}%<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines', name: 'Open land (farmland/pasture)',
        x: POLLEN_DATA.map(d => d.mid), y: POLLEN_DATA.map(d => d.open),
        stackgroup: 'one',
        line: {width: 0.5, color: '#e6b86e'},
        fillcolor: 'rgba(230, 184, 110, 0.4)',
        hovertemplate: 'Farmland: %{y}%<extra></extra>'
      }
    ];

    const layout = mergeLayout({
      title: {text: 'European Land Cover from Pollen (500 BCE\u20131100 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE (200-year bins)', range: [-600, 1200]},
      yaxis: {title: 'Percentage of pollen', range: [0, 100]},
      annotations: [
        {x: 100, y: 55, text: 'Roman deforestation<br>peak', showarrow: true, arrowhead: 0, arrowcolor: '#e6b86e', ax: 0, ay: -30, font: {size: 9, color: '#e6b86e'}},
        {x: 700, y: 40, text: 'Post-Roman<br>regrowth', showarrow: true, arrowhead: 0, arrowcolor: '#4fad7a', ax: 0, ay: -30, font: {size: 9, color: '#4fad7a'}}
      ]
    });

    return {traces, layout};
  },

  // ============================================================
  // 16. CHURCH CONSTRUCTION
  // ============================================================
  churches: () => {
    const traces = [{
      type: 'bar',
      x: CHURCH_DATA.map(d => d.mid), y: CHURCH_DATA.map(d => d.count),
      marker: {
        color: CHURCH_DATA.map(d => {
          if (d.mid < 950) return '#5b8dd9';
          if (d.mid < 1100) return '#4fad7a';
          return '#e6b86e';
        }),
        line: {color: '#0c0f13', width: 0.5}
      },
      width: 22,
      hovertemplate: '%{x} CE<br>%{y} churches<extra></extra>',
      name: 'Construction starts'
    }];

    const layout = mergeLayout({
      title: {text: 'Major Church Construction in Western Europe (700\u20131500 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE (25-year bins)', range: [690, 1510]},
      yaxis: {title: 'Construction starts per 25 years', rangemode: 'tozero'},
      annotations: [
        {x: 975, y: 32, text: 'Takeoff begins<br>~975 CE', showarrow: true, arrowhead: 0, arrowcolor: '#4fad7a', ax: -40, ay: -30, font: {size: 10, color: '#4fad7a'}},
        {x: 1212, y: 175, text: 'Peak: Gothic era', showarrow: false, font: {size: 9, color: '#e6b86e'}}
      ]
    });

    return {traces, layout};
  },

  // ============================================================
  // 17. PAS COIN LOSSES
  // ============================================================
  pas: () => {
    const maxCoins = Math.max(...PAS_COINS.map(d => d.coins));

    const traces = [{
      type: 'bar',
      x: PAS_COINS.map(d => d.mid), y: PAS_COINS.map(d => d.coins),
      text: PAS_COINS.map(d => d.label),
      marker: {
        color: PAS_COINS.map(d => {
          if (d.mid >= 410 && d.mid <= 670) return '#d94f4f';
          if (d.mid < 0) return '#8b8fa3';
          if (d.mid <= 410) return '#5b8dd9';
          return '#4fad7a';
        }),
        line: {color: '#0c0f13', width: 0.5}
      },
      width: 40,
      hovertemplate: '%{text}<br>%{x} CE<br>%{y} coin finds<extra></extra>',
      name: 'Coin finds'
    }];

    const layout = mergeLayout({
      title: {text: 'Coin Losses in Britain: PAS Data (50 BCE\u20131000 CE)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE (50-year bins)', range: [-80, 1030]},
      yaxis: {title: 'Relative coin finds', rangemode: 'tozero'},
      shapes: [OVERLAYS.angloSaxonGap],
      annotations: [{
        x: 545, y: maxCoins * 0.6, text: 'The Anglo-Saxon<br>Gap', showarrow: false,
        font: {size: 12, color: '#d94f4f'}
      }]
    });

    return {traces, layout};
  },

  // ============================================================
  // 5. MULTI-PROXY OVERLAY
  // ============================================================
  overlay: () => {
    const leadPeak = Math.max(...LEAD_DATA.map(d => d.emissions));
    const leadX = LEAD_DATA.map(d => d.year);
    const leadY = LEAD_DATA.map(d => (d.emissions / leadPeak) * 100);

    const shipPeak = Math.max(...SHIPWRECKS_50.map(d => d.total));
    const shipX = SHIPWRECKS_50.map(d => d.mid);
    const shipY = SHIPWRECKS_50.map(d => (d.total / shipPeak) * 100);

    const denPeak = Math.max(...DENARIUS.map(d => d.silver));
    const denX = DENARIUS.map(d => d.year);
    const denY = DENARIUS.map(d => (d.silver / denPeak) * 100);

    const hoardsPeak = Math.max(...CHRE_HOARDS.map(d => d.total));
    const hoardsX = CHRE_HOARDS.map(d => d.mid);
    const hoardsY = CHRE_HOARDS.map(d => (d.total / hoardsPeak) * 100);

    const inscPeak = Math.max(...INSCRIPTIONS_DATA.map(d => d.total));
    const inscX = INSCRIPTIONS_DATA.map(d => d.mid);
    const inscY = INSCRIPTIONS_DATA.map(d => (d.total / inscPeak) * 100);

    const evtShapes = HISTORICAL_EVENTS.map(e => ({
      type: 'line', x0: e.year, x1: e.year, y0: 0, y1: 1,
      xref: 'x', yref: 'paper',
      line: {color: e.color, width: 1, dash: 'dot'}, opacity: 0.4
    }));

    const evtAnnotations = HISTORICAL_EVENTS.map((e, i) => ({
      x: e.year, y: 105 - (i % 4) * 6,
      text: e.label, showarrow: false,
      font: {size: 8, color: e.color},
      xanchor: 'left', xshift: 3
    }));

    const traces = [
      {
        type: 'scatter', mode: 'lines', name: 'Lead emissions',
        x: leadX, y: leadY,
        line: {color: '#4fb5ad', width: 1.5},
        opacity: 0.8,
        hovertemplate: 'Lead: %{y:.0f}%<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines+markers', name: 'Shipwrecks (All Med)',
        x: shipX, y: shipY,
        line: {color: '#5b8dd9', width: 2.5},
        marker: {size: 4},
        hovertemplate: 'Shipwrecks: %{y:.0f}%<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines+markers', name: 'Denarius silver',
        x: denX, y: denY,
        line: {color: '#e6b86e', width: 2.5},
        marker: {size: 5},
        hovertemplate: 'Denarius: %{y:.0f}%<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines', name: 'Coin Hoards (CHRE)',
        x: hoardsX, y: hoardsY,
        line: {color: '#e6b86e', width: 2, dash: 'dash'},
        opacity: 0.7,
        hovertemplate: 'Hoards: %{y:.0f}%<extra></extra>'
      },
      {
        type: 'scatter', mode: 'lines', name: 'Inscriptions (EDH)',
        x: inscX, y: inscY,
        line: {color: '#9b6dd7', width: 2},
        opacity: 0.7,
        hovertemplate: 'Inscriptions: %{y:.0f}%<extra></extra>'
      }
    ];

    const layout = mergeLayout({
      title: {text: 'All Proxies Normalized to Peak (= 100%)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [-620, 810]},
      yaxis: {title: '% of Peak Value', range: [0, 115]},
      shapes: evtShapes,
      annotations: evtAnnotations
    });

    return {traces, layout};
  },

  // ============================================================
  // 6. CHANGE-POINT TIMELINE
  // ============================================================
  changepoints: () => {
    const allCps = [
      ...CHANGEPOINTS.lead.map(y => ({year: y, proxy: 'Lead Emissions', region: 'Europe'})),
      ...CHANGEPOINTS.ship_all.map(y => ({year: y, proxy: 'Shipwrecks', region: 'All Med'})),
      ...CHANGEPOINTS.ship_west.map(y => ({year: y, proxy: 'Shipwrecks', region: 'Western Med'})),
      ...CHANGEPOINTS.ship_east.map(y => ({year: y, proxy: 'Shipwrecks', region: 'Eastern Med'})),
    ];

    const colors = {
      'Lead Emissions': '#4fb5ad',
      'Shipwrecks': '#5b8dd9'
    };

    const traces = [{
      type: 'scatter', mode: 'markers',
      x: allCps.map(c => c.year),
      y: allCps.map(c => `${c.proxy}<br>${c.region}`),
      marker: {
        size: 14,
        color: allCps.map(c => colors[c.proxy]),
        symbol: 'diamond',
        line: {color: '#0c0f13', width: 1.5}
      },
      text: allCps.map(c => `${Math.abs(Math.round(c.year))} ${c.year < 0 ? 'BCE' : 'CE'}`),
      hovertemplate: '%{text}<br>%{y}<extra></extra>',
      showlegend: false
    }];

    const filteredEvents = HISTORICAL_EVENTS.filter(e => e.year >= -400 && e.year <= 800);

    const layout = mergeLayout({
      title: {text: 'All Detected Change-Points (Blind)', font: {size: 15, color: '#d4d4d8'}},
      xaxis: {title: 'Year CE', range: [-620, 810]},
      yaxis: {type: 'category'},
      height: 350,
      shapes: filteredEvents.map(e => ({
        type: 'line', x0: e.year, x1: e.year, y0: 0, y1: 1,
        xref: 'x', yref: 'paper',
        line: {color: e.color, width: 1, dash: 'dot'}, opacity: 0.3
      })),
      annotations: filteredEvents.map((e, i) => ({
        x: e.year, y: 1.05, xref: 'x', yref: 'paper',
        text: e.label, showarrow: false,
        font: {size: 8, color: e.color},
        textangle: -45, xanchor: 'left'
      }))
    });

    return {traces, layout};
  }
};
