# Mediterranean Economic Decline: A First-Principles Quantitative Analysis

## What This Is

A data-driven analysis of Mediterranean trade and economic activity from 1200 BCE to 800 CE, using multiple independent quantitative proxies. The analysis identifies structural breaks in the data **without historical priors**, then maps them to known events — building understanding from the ground up rather than testing any particular scholarly thesis.

## Key Finding

> Mediterranean economic activity, as measured by Greenland ice-core lead emissions, shipwreck density, denarius silver content, coin hoard frequency, and Latin inscription density, shows four distinct phases between 600 BCE and 800 CE. Industrial mining activity peaks during the early Roman Empire (1st century CE), then crashes around 174 CE coincident with the Antonine Plague — the single largest structural break in the 1,900-year record. Maritime trade, measured by shipwrecks, declines more gradually but shows a critical **regional divergence**: the Western Mediterranean drops below 10% of peak by 475 CE (the fall of the Western Empire), while the Eastern Mediterranean sustains near-peak trade through the 6th century, only collapsing below 10% around 775 CE. The Western-to-Eastern trade ratio reverses from 8:1 at the Roman peak to 1:2 by 500-650 CE. The data indicates that the Western economic collapse **precedes the Islamic conquests by approximately two centuries**, while the Eastern decline aligns more closely with them. This supports a "modified" view: plagues and the collapse of Western Roman institutions drove the primary decline, while Islamic conquests administered the final blow to what remained of Eastern Mediterranean commerce.

## Data Sources

| Dataset | Source | Records | Resolution |
|---------|--------|---------|------------|
| Lead emissions | McConnell et al. 2018, PNAS (NGRIP2 ice core) | 2,037 annual measurements | Annual, ±1-2 years |
| Shipwrecks | [OxREP Shipwrecks Database v2.1](https://oxrep.classics.ox.ac.uk/databases/shipwrecks_database/) (Strauss, Wilson & Flohr 2017; updating Parker 1992) | 1,784 wrecks | 50-year bins (equal-probability dating, Wilson 2011) |
| Denarius silver | Butcher & Ponting 2015; Walker 1976 | 33 data points | Irregular (per emperor) |
| Coin hoards | Coin Hoards of the Roman Empire (CHRE), Oxford/Ashmolean | ~4,000 hoards | 25-year bins (terminal date) |
| Latin inscriptions | Epigraphic Database Heidelberg (EDH) via SDAM/Zenodo | 81,476 inscriptions (56,280 dated) | 25-year bins (equal-probability dating) |

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
  ingest_hoards.py                 CHRE CSV → binned hoard counts with regional split
  ingest_inscriptions.py           EDH/SDAM JSON → binned inscription counts with regional split
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
- **Regional classification (hoards & inscriptions)**: Western (Britannia, Gaul, Hispania, Italia, Africa) vs. Eastern (Asia Minor, Syria, Aegyptus, Balkans, Greece) provinces, using fuzzy province-name matching

## Known Biases & Source Criticism

The shipwreck data in particular has **well-documented limitations** that are discussed in a dedicated source criticism section on the page. Key issues:

- **Unequal sinking probability**: Bilge pump invention, shift from cabotage to open-water sailing, piracy levels, and climate all altered wreck risk across periods (Wilson 2011; Hopkins 1980)
- **Barrel bias**: Post-2nd-century shift from amphorae to wooden barrels systematically undercounts late trade; Wilson concluded the decline is "at least partly explicable by a move from amphorae to wooden barrels" (Wilson 2011, p.220)
- **Discovery bias**: Italy, France, and Spain account for >70% of all wrecks; North African coast severely under-surveyed despite being a major Roman trade corridor (Parker 1992, p.548)
- **Ceramic dating uncertainty**: Most wrecks dated by cargo ceramics alone; Manning, Lorentzen & Demesticha (2022, *Antiquity*) showed radiocarbon/dendro dating can produce significantly different results
- **Inconsistency with land-based archaeology**: Port expansion at Portus and olive oil intensification in North Africa continued during the supposed 2nd–3rd century "decline" visible in the wreck graph
- **Lead proxy scope**: Reflects primarily Iberian and northern European mining, weighted by atmospheric transport to Greenland; may underrepresent Eastern Mediterranean industrial activity
- **Small-n fragility**: 1,784 wrecks across ~1,600 years and the entire Mediterranean; regional/temporal splits rest on very small numbers

## References

### Primary Data Sources
- McConnell, J.R. et al. (2018). "Lead pollution recorded in Greenland ice..." *PNAS* 115(22), 5726-5731. [doi:10.1073/pnas.1721818115](https://doi.org/10.1073/pnas.1721818115)
- Strauss, J., Wilson, A.I. & Flohr, M. (2017). OxREP Shipwrecks Database v2.1. [oxrep.classics.ox.ac.uk](https://oxrep.classics.ox.ac.uk/databases/shipwrecks_database/)
- Parker, A.J. (1992). *Ancient Shipwrecks of the Mediterranean*. BAR International Series 580.
- Butcher, K. & Ponting, M. (2015). *The Metallurgy of Roman Silver Coinage*. Cambridge.
- Walker, D.R. (1976-78). *The Metrology of the Roman Silver Coinage*. BAR.
- Büntgen, U. et al. (2011). "2500 Years of European Climate Variability." *Science* 331, 578-582. [doi:10.1126/science.1197175](https://doi.org/10.1126/science.1197175)
- Toohey, M. & Sigl, M. (2017). eVolv2k v3. *Earth System Science Data* 9, 809-831. [doi:10.5194/essd-9-809-2017](https://doi.org/10.5194/essd-9-809-2017)
- Fyfe, R.M. et al. (2015). European Pollen Database. *Quaternary Science Reviews*. [PANGAEA](https://doi.org/10.1594/PANGAEA.855674)
- CHRE — Coin Hoards of the Roman Empire. [chre.ashmus.ox.ac.uk](https://chre.ashmus.ox.ac.uk/)
- Epigraphic Database Heidelberg. [edh.ub.uni-heidelberg.de](https://edh.ub.uni-heidelberg.de/) via [SDAM/Zenodo](https://doi.org/10.5281/zenodo.4888168)
- Portable Antiquities Scheme. [finds.org.uk](https://finds.org.uk/)
- Scheidel, W. (2006). "Population and Demography." Princeton/Stanford Working Papers in Classics.

### Methodology
- Wilson, A. (2011). "Trade volumes in the Roman Mediterranean" in *Quantifying the Roman Economy* (Bowman & Wilson, eds.), Oxford.
- Manning, S.W., Lorentzen, B. & Demesticha, S. (2022). "Dating Mediterranean shipwrecks." *Antiquity*. [doi:10.15184/aqy.2022.76](https://doi.org/10.15184/aqy.2022.76)

### Scholarly Interpretations
- Pirenne, H. (1937). *Mohammed and Charlemagne*.
- Ward-Perkins, B. (2005). *The Fall of Rome and the End of Civilization*.
- McCormick, M. (2001). *Origins of the European Economy*. Cambridge.
- Harper, K. (2017). *The Fate of Rome*. Princeton.
- Wickham, C. (2005). *Framing the Early Middle Ages*. Oxford.

### Criticism of Shipwreck-as-Economic-Proxy
- Wilson, A. (2011) — see above (articulates the most substantial academic criticisms)
- Manning et al. (2022) — see above (ceramic dating problems)
- Knowles (2023). ["Please don't link ancient shipwrecks and the economy."](https://knowles06.medium.com/dont-link-ancient-shipwrecks-and-economic-activity-c887996c51d4) Popular summary of academic criticisms.
