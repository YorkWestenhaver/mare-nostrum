#!/usr/bin/env python3
"""
Blind change-point detection on economic proxy time series.
No historical dates are fed as priors. The algorithm finds structural breaks
in the data, and only afterward do we map them to known events.
"""

import json
import pandas as pd
import numpy as np
import ruptures as rpt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLES_DIR = PROJECT_ROOT / "output" / "tables"
TABLES_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    lead = pd.read_csv(PROCESSED_DIR / "lead_emissions.csv")
    ship50 = pd.read_csv(PROCESSED_DIR / "shipwrecks_binned_50yr.csv")
    denarius = pd.read_csv(PROCESSED_DIR / "denarius_silver.csv")
    return lead, ship50, denarius


def detect_changepoints_lead(lead, n_bkps=5):
    """
    Detect change-points in the annual lead emissions series.
    Uses PELT with RBF kernel. Focus on the period -600 to 800 CE.
    """
    mask = (lead.year_ce >= -600) & (lead.year_ce <= 800) & lead.lead_emissions_kt_a.notna()
    series = lead.loc[mask].copy().reset_index(drop=True)

    signal = series.lead_emissions_kt_a.values
    years = series.year_ce.values

    # Binseg with RBF kernel, specifying number of breakpoints
    algo = rpt.Binseg(model="rbf", min_size=20).fit(signal)
    result = algo.predict(n_bkps=n_bkps)

    # Convert sample indices to years
    cp_years = []
    segments = []
    prev_idx = 0
    for idx in result:
        if idx < len(years):
            cp_year = years[idx - 1]
        else:
            cp_year = years[-1]
        seg_mean = float(np.mean(signal[prev_idx:idx]))
        seg_std = float(np.std(signal[prev_idx:idx]))
        segments.append({
            "start_idx": prev_idx,
            "end_idx": idx,
            "start_year": float(years[prev_idx]),
            "end_year": float(cp_year),
            "mean_emissions": seg_mean,
            "std_emissions": seg_std,
        })
        if idx < len(years):
            cp_years.append(float(cp_year))
        prev_idx = idx

    return cp_years, segments


def detect_changepoints_shipwrecks(ship50, column="total_count", n_bkps=4):
    """
    Detect change-points in the shipwreck binned time series.
    """
    signal = ship50[column].values
    years = ship50.bin_mid.values

    algo = rpt.Binseg(model="rbf", min_size=2).fit(signal)
    result = algo.predict(n_bkps=n_bkps)

    cp_years = []
    segments = []
    prev_idx = 0
    for idx in result:
        if idx < len(years):
            cp_year = years[idx - 1]
        else:
            cp_year = years[-1]
        seg_mean = float(np.mean(signal[prev_idx:idx]))
        segments.append({
            "start_idx": prev_idx,
            "end_idx": idx,
            "start_year": float(years[prev_idx]),
            "end_year": float(cp_year),
            "mean_count": seg_mean,
        })
        if idx < len(years):
            cp_years.append(float(cp_year))
        prev_idx = idx

    return cp_years, segments


def detect_steepest_decline_denarius(denarius):
    """
    For the denarius data (too few points for robust change-point detection),
    find the steepest decline intervals.
    """
    years = denarius.year_ce.values
    silver = denarius.silver_pct.values

    slopes = []
    for i in range(len(years) - 1):
        dy = silver[i + 1] - silver[i]
        dx = years[i + 1] - years[i]
        if dx > 0:
            slope = dy / dx
            slopes.append({
                "start_year": int(years[i]),
                "end_year": int(years[i + 1]),
                "start_silver": float(silver[i]),
                "end_silver": float(silver[i + 1]),
                "slope_pct_per_year": float(slope),
                "total_drop_pct": float(dy),
            })

    slopes_df = pd.DataFrame(slopes)
    steepest = slopes_df.nsmallest(5, "slope_pct_per_year")
    return steepest


def cross_correlation_analysis(lead, ship50):
    """
    Compute cross-correlation between lead emissions and shipwreck counts
    on a common 50-year grid.
    """
    lead_50 = []
    for _, row in ship50.iterrows():
        bstart, bend = row.bin_start, row.bin_end
        mask = (lead.year_ce >= bstart) & (lead.year_ce < bend) & lead.lead_emissions_kt_a.notna()
        if mask.sum() > 0:
            lead_50.append(float(lead.loc[mask, "lead_emissions_kt_a"].mean()))
        else:
            lead_50.append(np.nan)

    lead_50 = np.array(lead_50)
    ship_counts = ship50.total_count.values

    valid = ~np.isnan(lead_50)
    if valid.sum() < 5:
        return None

    from scipy.stats import pearsonr, spearmanr
    r_pearson, p_pearson = pearsonr(lead_50[valid], ship_counts[valid])
    r_spearman, p_spearman = spearmanr(lead_50[valid], ship_counts[valid])

    return {
        "pearson_r": float(r_pearson),
        "pearson_p": float(p_pearson),
        "spearman_r": float(r_spearman),
        "spearman_p": float(p_spearman),
    }


def main():
    lead, ship50, denarius = load_data()

    print("=" * 60)
    print("BLIND CHANGE-POINT DETECTION")
    print("No historical priors. Let the data speak.")
    print("=" * 60)

    # 1. Lead emissions change-points
    print("\n--- Lead Emissions (annual, -600 to 800 CE) ---")
    cp_lead, seg_lead = detect_changepoints_lead(lead, n_bkps=5)
    print(f"Detected break years: {[f'{y:.0f}' for y in cp_lead]}")
    print("\nSegment means:")
    for s in seg_lead:
        print(f"  {s['start_year']:.0f} to {s['end_year']:.0f}: "
              f"mean={s['mean_emissions']:.3f} kt/yr (sd={s['std_emissions']:.3f})")

    # 2. Shipwrecks (all Med)
    print("\n--- Shipwrecks: All Mediterranean (50yr bins) ---")
    cp_ship_all, seg_ship_all = detect_changepoints_shipwrecks(ship50, "total_count", n_bkps=3)
    print(f"Detected break years: {[f'{y:.0f}' for y in cp_ship_all]}")
    for s in seg_ship_all:
        print(f"  {s['start_year']:.0f} to {s['end_year']:.0f}: mean={s['mean_count']:.1f}")

    # 3. Shipwrecks (Western Med only)
    print("\n--- Shipwrecks: Western Mediterranean ---")
    cp_ship_west, seg_ship_west = detect_changepoints_shipwrecks(ship50, "western_med", n_bkps=3)
    print(f"Detected break years: {[f'{y:.0f}' for y in cp_ship_west]}")
    for s in seg_ship_west:
        print(f"  {s['start_year']:.0f} to {s['end_year']:.0f}: mean={s['mean_count']:.1f}")

    # 4. Shipwrecks (Eastern Med only)
    print("\n--- Shipwrecks: Eastern Mediterranean ---")
    cp_ship_east, seg_ship_east = detect_changepoints_shipwrecks(ship50, "eastern_med", n_bkps=3)
    print(f"Detected break years: {[f'{y:.0f}' for y in cp_ship_east]}")
    for s in seg_ship_east:
        print(f"  {s['start_year']:.0f} to {s['end_year']:.0f}: mean={s['mean_count']:.1f}")

    # 5. Denarius steepest decline
    print("\n--- Denarius Silver: Steepest Decline Intervals ---")
    steepest = detect_steepest_decline_denarius(denarius)
    print(steepest.to_string(index=False))

    # 6. Cross-correlation
    print("\n--- Cross-Correlation: Lead vs Shipwrecks (50yr bins) ---")
    xcorr = cross_correlation_analysis(lead, ship50)
    if xcorr:
        print(f"  Pearson r = {xcorr['pearson_r']:.3f} (p = {xcorr['pearson_p']:.4f})")
        print(f"  Spearman r = {xcorr['spearman_r']:.3f} (p = {xcorr['spearman_p']:.4f})")

    # Save results
    results = {
        "changepoints_lead": cp_lead,
        "segments_lead": seg_lead,
        "changepoints_ship_all": cp_ship_all,
        "segments_ship_all": seg_ship_all,
        "changepoints_ship_west": cp_ship_west,
        "segments_ship_west": seg_ship_west,
        "changepoints_ship_east": cp_ship_east,
        "segments_ship_east": seg_ship_east,
        "denarius_steepest_decline": steepest.to_dict("records"),
        "cross_correlation": xcorr,
    }

    results_path = TABLES_DIR / "changepoint_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved results to {results_path}")

    # Also save a summary table
    summary_rows = []
    for cp in cp_lead:
        summary_rows.append({"proxy": "lead_emissions", "break_year": cp, "region": "all"})
    for cp in cp_ship_all:
        summary_rows.append({"proxy": "shipwrecks", "break_year": cp, "region": "all_med"})
    for cp in cp_ship_west:
        summary_rows.append({"proxy": "shipwrecks", "break_year": cp, "region": "western_med"})
    for cp in cp_ship_east:
        summary_rows.append({"proxy": "shipwrecks", "break_year": cp, "region": "eastern_med"})

    summary = pd.DataFrame(summary_rows)
    summary = summary.sort_values("break_year").reset_index(drop=True)
    summary_path = TABLES_DIR / "changepoint_summary.csv"
    summary.to_csv(summary_path, index=False)
    print(f"Saved summary to {summary_path}")

    return results


if __name__ == "__main__":
    results = main()
