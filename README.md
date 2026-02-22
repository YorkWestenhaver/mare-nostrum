# Mediterranean Economic Decline: A First-Principles Quantitative Analysis

## What This Is

A data-driven analysis of Mediterranean trade and economic activity from 1200 BCE to 800 CE, using three independent quantitative proxies. The analysis identifies structural breaks in the data **without historical priors**, then maps them to known events — building understanding from the ground up rather than testing any particular scholarly thesis.

## Key Finding

> Mediterranean economic activity, as measured by Greenland ice-core lead emissions, shipwreck density, and denarius silver content, shows four distinct phases between 600 BCE and 800 CE. Industrial mining activity peaks during the early Roman Empire (1st century CE), then crashes around 174 CE coincident with the Antonine Plague — the single largest structural break in the 1,900-year record. Maritime trade, measured by shipwrecks, declines more gradually but shows a critical **regional divergence**: the Western Mediterranean drops below 10% of peak by 475 CE (the fall of the Western Empire), while the Eastern Mediterranean sustains near-peak trade through the 6th century, only collapsing below 10% around 775 CE. The Western-to-Eastern trade ratio reverses from 8:1 at the Roman peak to 1:2 by 500-650 CE. The data indicates that the Western economic collapse **precedes the Islamic conquests by approximately two centuries**, while the Eastern decline aligns more closely with them. This supports a "modified" view: plagues and the collapse of Western Roman institutions drove the primary decline, while Islamic conquests administered the final blow to what remained of Eastern Mediterranean commerce.

## Data Sources

| Dataset | Source | Records | Resolution |
|---------|--------|---------|------------|
| Lead emissions | McConnell et al. 2018, PNAS (NGRIP2 ice core) | 2,037 annual measurements | Annual, ±1-2 years |
| Shipwrecks | Oxford Roman Economy Project (Parker-Strauss) | 1,784 wrecks | 50-year bins (equal-probability dating) |
| Denarius silver | Butcher & Ponting 2015; Walker 1976 | 33 data points | Irregular (per emperor) |

## Detected Change-Points (Blind — No Historical Priors)

| Proxy | Region | Break Year | Segment Before → After |
|-------|--------|------------|----------------------|
| Lead | All Europe | ~336 BCE | 0.38 → 0.68 kt/yr |
| Lead | All Europe | ~10 BCE | 0.68 → 0.91 kt/yr |
| Lead | All Europe | **~174 CE** | **0.91 → 0.33 kt/yr (largest break)** |
| Lead | All Europe | ~674 CE | 0.33 → 0.66 kt/yr |
| Lead | All Europe | ~766 CE | 0.66 → 1.77 kt/yr |
| Shipwrecks | All Med | ~125 CE | 103.2 → 65.4 per bin |
| Shipwrecks | All Med | ~375 CE | 65.4 → 12.9 per bin |
| Shipwrecks | Western Med | ~375 CE | 46.2 → 4.4 per bin |
| Shipwrecks | **Eastern Med** | **~625 CE** | 8.7 → 3.1 per bin |

## Scholarly Comparison

| Scholar | Verdict |
|---------|---------|
| **Pirenne** (1937): Islamic conquest caused western trade collapse | **Not supported** — Western collapse precedes Islam by ~200 years |
| **Ward-Perkins** (2005): Real material decline, pre-Islamic | **Strongly supported** |
| **McCormick** (2001): Trade transformed, didn't die | **Partially supported** — transformation in East, collapse in West |
| **Harper** (2017): Plagues drove economic decline | **Strongly supported** — timing aligns with structural breaks |
| **Wickham** (2005): Structural simplification was inevitable | **Modified support** — yes, but regionally uneven |

## Project Structure

```
data/raw/                          Original data files
data/processed/                    Cleaned CSVs and parquet files
src/
  ingest_lead.py                   McConnell xlsx → CSV
  ingest_shipwrecks.py             OxREP Excel → CSV with equal-probability dating
  ingest_denarius.py               Literature values → CSV
  classify_regions.py              Regional classification (name-based for 860+ wrecks)
  analyze.py                       Change-point detection (ruptures PELT/Binseg)
  visualize.py                     First-look and multi-proxy plots
  final_figure.py                  Publication-quality 4-panel figure
output/
  figures/
    multi_proxy_overlay.png        The "squint test" — all proxies normalized
    changepoints.png               Blind change-point detection results
    regional_decomposition.png     Western vs Eastern Mediterranean
    historical_overlay.png         Data + historical events
    final_publication.png          Publication-ready 4-panel figure
  tables/
    changepoint_results.json       Full change-point detection output
    changepoint_summary.csv        Break dates by proxy and region
    changepoint_event_mapping.csv  Break dates mapped to nearest events
    narrative.md                   Plain-language data narrative
    scholarly_comparison.md        Comparison to Pirenne et al.
```

## Methodology

- **Equal-probability dating**: Shipwrecks with date ranges contribute fractional counts to each year in the range, avoiding midpoint distortion (Wilson 2011)
- **Change-point detection**: Binary segmentation with RBF kernel (`ruptures` library), no historical dates as priors
- **Regional classification**: 1,713 of 1,784 wrecks classified into Western Med, Eastern Med, Adriatic, Black Sea, or Atlantic using Country, Region, and name-based heuristics

## Known Biases

- **Barrel bias**: Post-2nd-century shift from amphorae to barrels undercounts late trade in wreck data
- **Discovery bias**: More wrecks found in French/Italian waters; North African coast under-surveyed
- **Lead proxy scope**: Reflects primarily Iberian and northern European mining, weighted by atmospheric transport to Greenland

## References

- McConnell, J.R. et al. (2018). "Lead pollution recorded in Greenland ice..." *PNAS* 115(22), 5726-5731.
- Parker, A.J. (1992). *Ancient Shipwrecks of the Mediterranean*. BAR International Series 580.
- Strauss, J. (2013). OxREP Shipwrecks Database. oxrep.classics.ox.ac.uk
- Butcher, K. & Ponting, M. (2015). *The Metallurgy of Roman Silver Coinage*. Cambridge.
- Walker, D.R. (1976-78). *The Metrology of the Roman Silver Coinage*. BAR.
- Pirenne, H. (1937). *Mohammed and Charlemagne*.
- Ward-Perkins, B. (2005). *The Fall of Rome and the End of Civilization*.
- McCormick, M. (2001). *Origins of the European Economy*. Cambridge.
- Harper, K. (2017). *The Fate of Rome*. Princeton.
- Wickham, C. (2005). *Framing the Early Middle Ages*. Oxford.
