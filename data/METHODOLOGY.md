# Met Open Access Data: Processing Methodology

## Source

**The Metropolitan Museum of Art Open Access dataset**
- URL: https://github.com/metmuseum/openaccess
- License: CC0 (Creative Commons Zero)
- Raw file: `data/raw/met-artifact-data/MetObjects.csv`
- ~485,000 objects spanning 5,000+ years of human material culture
- 54 metadata columns per object including dates, department, classification, culture, geography, medium

## Pipeline

```
raw CSV (317 MB) → parquet (49 MB) → aggregated web JSON (~380 KB total)
```

### Step 1: Parquet conversion

The raw CSV is loaded, column types are cleaned (booleans, integers, nullable strings), and saved as `met_objects.parquet`. This is a full-fidelity copy of the original data in a columnar format that loads in ~1 second vs ~4 seconds for the CSV, and compresses to ~15% of the original size.

### Step 2: Temporal aggregation with dual-kernel uncertainty quantification

#### The problem

Museum objects are dated with varying precision. Some have exact dates ("37 BCE"), others have ranges ("5th century BCE", i.e. 500–400 BCE), and some have very broad ranges ("1st millennium BCE", i.e. 1000–1 BCE). When we bin these objects into 25-year periods to create time series, we need a principled way to handle this uncertainty rather than simply picking the midpoint or arbitrarily assigning objects to bins.

#### The statistical framework

For each object, we model the true creation date as a random variable over the interval `[Object Begin Date, Object End Date]`. For a given 25-year bin, each object _i_ contributes a probability `p_i` of truly belonging to that bin. Since the object either belongs or doesn't, `X_i ~ Bernoulli(p_i)`:

```
E[X_i] = p_i
Var[X_i] = p_i × (1 - p_i)
```

Across all _N_ objects overlapping a bin (independent):

```
E[Total] = Σ p_i                    (the "expected count")
Var[Total] = Σ p_i × (1 - p_i)     (independence)
95% CI = E ± 1.96 × √Var           (lower bound clamped to 0)
```

The key question is _how to compute p_i_ — this is where the two kernels differ.

#### Kernel 1: Uniform (maximum-entropy, conservative)

```
p_i = overlap(bin, [b_i, e_i]) / span_i
```

Assumes equal probability across the entire date range. This is the maximum-entropy assumption — it adds no information beyond "the object is somewhere in this range." It produces the flattest possible distribution of probability across bins.

**When it's appropriate:** When we have no reason to believe any part of the range is more likely than any other. This is the conservative default.

#### Kernel 2: Truncated Gaussian (expert-judgment model)

```
μ_i = (b_i + e_i) / 2              (center of range)
σ_i = span_i / 4                   (~95% of mass within range)
p_i = [Φ((bin_hi - μ)/σ) - Φ((bin_lo - μ)/σ)] / Z
```

where `Z = Φ((e_i - μ)/σ) - Φ((b_i - μ)/σ)` normalizes the truncated distribution.

Assumes the center of the date range is the most likely creation date, with decreasing probability toward the edges. This models how art-historical dating actually works: when a curator writes "5th century BCE," they usually mean "stylistically most consistent with the middle of this period, but could be earlier or later."

**When it's appropriate:** When date ranges represent expert assessments centered on a best estimate with diminishing confidence outward.

#### Comparison of kernel behavior

| Object dating | Span | Kernel | Central bin p | Edge bin p | Effect |
|---|---|---|---|---|---|
| Exact year | 0–1 yr | Both | 1.00 | — | Identical: full count, zero uncertainty |
| "475–450 BCE" | 25 yr | Both | 1.00 | — | Identical: fits in one bin |
| "500–400 BCE" | 100 yr | Uniform | 0.25 | 0.25 | Flat across 4 bins |
| | | Gaussian | 0.40 | 0.06 | Peaked at center, tapers at edges |
| "1000–500 BCE" | 500 yr | Uniform | 0.05 | 0.05 | Flat across 20 bins |
| | | Gaussian | 0.15 | 0.01 | Strongly peaked, nearly zero at edges |

**Net effect on time series:**
- The Gaussian kernel produces sharper peaks and deeper valleys than uniform.
- Periods where objects cluster around similar midpoints appear more prominent with Gaussian.
- Both kernels produce identical results for precisely-dated objects (the majority of the dataset).
- CIs tend to be slightly tighter with Gaussian for bins near range centers (higher p → more certainty about placement) and slightly wider at range edges.

### Step 3: Survivorship bias correction — Composite Material Culture Index

#### The problem

Raw artifact counts across classifications are dominated by materials with high archaeological survival rates. Ceramics are nearly indestructible; metals get reused; textiles rot; wood burns. The Met's collection of ~21,000 ancient vases vs. ~900 coins doesn't mean vases were 23× more commonly produced — it means ceramics survive far better and were aggressively collected.

If you sum raw counts across all classifications, the "total" essentially tells you "when were Attic vases made" rather than providing a balanced picture of material culture activity.

#### The solution

We compute an **equal-weight composite index** that normalizes each classification independently and then averages:

1. **Select diagnostic classifications** (N = 10): Vases, Ceramics, Glass, Sculpture, Bronzes, Coins, Jewelry, Gold and Silver, Terracottas, Metalwork. These represent distinct material categories with different survival properties.

2. **Normalize each class** to [0, 1] by dividing by its own peak count across all bins. This removes the absolute magnitude difference — whether a class has 5,000 or 50 objects at its peak, it contributes equally.

3. **Average across classes** for each bin:
   ```
   composite(bin) = (1/N) × Σ normalized_count_c(bin)
   ```

4. **Propagate confidence intervals** under independence:
   ```
   Var[composite] = (1/N²) × Σ (var_c / peak_c²)
   CI = composite ± 1.96 × √Var
   ```

The composite index ranges from 0 (no class has any activity) to 1 (all classes simultaneously at their respective peaks). A value of 0.35 means that on average, each material type is at 35% of its peak production level in that period.

#### Properties

- Each material type gets an equal "vote" regardless of survival rate or collection bias.
- A period where every material type shows moderate activity scores higher than a period where one type dominates but others are absent.
- CIs reflect both the dating uncertainty of individual objects and the agreement/disagreement across material types.
- Both uniform and Gaussian composite variants are computed.

### Assumptions and limitations

1. **Kernel choice is a modeling decision.** The uniform kernel is conservative (maximum entropy); the Gaussian kernel is more realistic for expert-assessed date ranges. Neither is "correct" — they bracket the likely truth. The website should present both or allow toggling.

2. **Independence assumption.** Objects are treated as independent. In practice, groups from the same excavation may have correlated dating uncertainty, making true CIs somewhat wider.

3. **Collection bias persists in per-class data.** The composite index corrects for cross-class survival bias but not within-class collection bias. The Met collected Attic vases more aggressively than provincial Roman pottery; both fall under "Vases" but the former dominates.

4. **Equal weighting is arbitrary.** Giving each of 10 classifications equal vote in the composite is a choice. Different weightings (e.g., by economic significance) would produce different indices. Equal weight is the default because it requires no subjective judgment.

5. **Date field semantics.** `Object Begin Date` and `Object End Date` represent the museum's cataloging estimates. These are expert assessments, not measurements, and their precision varies by department and object type.

## Output format

Each per-bin record in the web JSON files contains:

| Field | Type | Description |
|---|---|---|
| `mid` | number | Midpoint of the 25-year bin (e.g., -487.5 = 500–475 BCE) |
| `count` | number | Uniform kernel: expected object count (Σ p_i) |
| `lo` | number | Uniform kernel: lower bound of 95% CI |
| `hi` | number | Uniform kernel: upper bound of 95% CI |
| `count_g` | number | Gaussian kernel: expected object count |
| `lo_g` | number | Gaussian kernel: lower bound of 95% CI |
| `hi_g` | number | Gaussian kernel: upper bound of 95% CI |
| `n_objects` | integer | Number of distinct objects whose date range overlaps this bin |

`n_objects` is always ≥ `count`. The difference tells you how many objects are "shared" with other bins due to imprecise dating. When `n_objects` >> `count`, most objects in the bin are broadly dated.

The composite index file has a different structure:

| Field | Type | Description |
|---|---|---|
| `mid` | number | Bin midpoint |
| `index` | number | Composite value [0, 1] — average normalized activity across all classes |
| `lo` | number | Lower bound of 95% CI |
| `hi` | number | Upper bound of 95% CI |

## Files produced

| File | Size | Description |
|---|---|---|
| `met_objects.parquet` | 49 MB | Full dataset, all 54 columns, cleaned types |
| `met_timeline_25yr.json` | 11 KB | Overall artifact count per 25-year bin (1000 BCE – 1500 CE) |
| `met_by_department.json` | 72 KB | 8 key Met departments |
| `met_by_classification.json` | 130 KB | 16 material/object type categories |
| `met_by_culture.json` | 72 KB | 12 ancient culture labels |
| `met_greek_roman_detail.json` | 86 KB | Greek & Roman dept, sub-classifications |
| `met_composite_index.json` | 11 KB | Equal-weight composite of 10 material classes, both kernels |

## Reproducibility

```bash
# Process everything (academic datasets + Met):
python data/process.py

# Met only (uses cached parquet):
python data/process.py --met-only

# Rebuild Met parquet from raw CSV + print date analysis:
python data/process.py --met-only --force --analyze

# Academic datasets only (no pandas/numpy needed):
python data/process.py --skip-met
```

Scripts: `data/process.py` (entry point), `data/process_all.py`, `data/process_met.py`
