#!/usr/bin/env python3
"""
Ingest OxREP/Parker-Strauss shipwreck database.
Reads Excel data, applies equal-probability dating, regional classification,
and outputs cleaned CSV, binned time series, and a first-look plot.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "oxrep_shipwrecks"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "output" / "figures"

# Bin boundaries: -600 (600 BCE) to 1000 CE
BIN_START_YEAR = -600
BIN_END_YEAR = 1000
BIN_50YR = 50
BIN_25YR = 25


def load_shipwrecks() -> pd.DataFrame:
    """Load shipwreck data from OxREP Excel file."""
    xlsx_path = RAW_DIR / "StraussShipwrecks.xlsx"
    if not xlsx_path.exists():
        raise FileNotFoundError(f"OxREP data not found at {xlsx_path}")
    return pd.read_excel(xlsx_path, sheet_name="Shipwrecks")


def parse_wreck(row: pd.Series) -> dict:
    """Extract key fields from a wreck row."""
    # Dates: already BCE-negative in source; ensure int
    date_start = row.get("Earliest date")
    date_end = row.get("Latest date")
    if pd.isna(date_start):
        date_start = None
    else:
        date_start = int(float(date_start))
    if pd.isna(date_end):
        date_end = None
    else:
        date_end = int(float(date_end))

    # Cargo types: combine relevant columns
    cargo_parts = []
    if row.get("Amphorae") == True:
        cargo_parts.append("amphorae")
    if row.get("Marble") == True:
        cargo_parts.append("marble")
    if row.get("Columns etc") == True:
        cargo_parts.append("columns")
    if row.get("Sarcophagi") == True:
        cargo_parts.append("sarcophagi")
    if row.get("Blocks") == True:
        cargo_parts.append("blocks")
    if pd.notna(row.get("Marble type")) and str(row.get("Marble type")).strip():
        cargo_parts.append(f"marble:{row['Marble type']}")
    if pd.notna(row.get("Other cargo")) and str(row.get("Other cargo")).strip():
        cargo_parts.append(str(row.get("Other cargo")))
    if pd.notna(row.get("Amphora type")) and str(row.get("Amphora type")).strip():
        cargo_parts.append(f"amphora_type:{row['Amphora type']}")
    cargo_types = "; ".join(cargo_parts) if cargo_parts else ""

    return {
        "wreck_id": row.get("Wreck ID"),
        "strauss_id": row.get("Strauss ID"),
        "name": row.get("Name"),
        "parker_number": row.get("Parker Number"),
        "country": row.get("Country"),
        "sea_area": row.get("Sea area"),
        "region_db": row.get("Region"),
        "latitude": row.get("Latitude"),
        "longitude": row.get("Longitude"),
        "date_start": date_start,
        "date_end": date_end,
        "cargo_types": cargo_types,
        "provenance": row.get("Place of origin"),
        "destination": row.get("Place of destination"),
    }


def classify_region(country: str, sea_area: str) -> str:
    """
    Classify wreck into region based on country and sea_area.
    Returns one of: western_med, eastern_med, adriatic, black_sea, atlantic, other
    """
    if pd.isna(country):
        country = ""
    if pd.isna(sea_area):
        sea_area = ""
    country = str(country).strip()
    sea_area = str(sea_area).strip()

    # Black Sea (explicit)
    if "Black Sea" in sea_area:
        return "black_sea"
    if country in ("Bulgaria", "Romania"):
        return "black_sea"

    # Adriatic
    adriatic_countries = ("Croatia", "Albania", "Montenegro")
    adriatic_sea = "Adriatic"
    if country in adriatic_countries or adriatic_sea in sea_area:
        return "adriatic"
    # East Italian coast = Adriatic (Italy + Adriatic sea)
    if country == "Italy" and adriatic_sea in sea_area:
        return "adriatic"

    # Atlantic/Channel
    atlantic_countries = ("Britain", "United Kingdom", "UK", "Belgium", "Netherlands")
    if country in atlantic_countries:
        return "atlantic"
    # Atlantic France: France + Atlantic/Channel waters
    if country == "France" and any(
        x in sea_area for x in ("Atlantic", "Channel", "English Channel")
    ):
        return "atlantic"

    # Western Med
    western_countries = (
        "Spain",
        "France",
        "Minorca",
        "Malta",  # Central but often grouped west
        "Tunisia",
        "Algeria",
        "Morocco",
        "Libya",  # Whole Libya for simplicity (west of Tunisia)
    )
    western_sea = (
        "Western Mediterranean",
        "West Mediterranean",
        "Tyrrhenian Sea",
        "Central Mediterranean",
    )
    if country in western_countries:
        return "western_med"
    if country == "Italy" or country == "Italy - Sicily":
        # Western/central Italy (non-Adriatic)
        if adriatic_sea not in sea_area:
            return "western_med"
        return "adriatic"

    # Eastern Med
    eastern_countries = (
        "Greece",
        "Turkey",
        "Cyprus",
        "Syria",
        "Lebanon",
        "Israel",
        "Egypt",
        "Sudan",
    )
    eastern_sea = (
        "Eastern Mediterranean",
        "Aegean",
        "Southern Aegean",
        "Northern Aegean",
        "Ionian",
        "Red Sea",
    )
    if country in eastern_countries:
        return "eastern_med"
    if any(s in sea_area for s in eastern_sea):
        return "eastern_med"

    # India, International waters, ZZ-Non-Mediterranean
    return "other"


def apply_equal_probability_dating(
    df: pd.DataFrame, bin_years: int
) -> pd.DataFrame:
    """
    For each wreck with [date_start, date_end], contribute weight 1/span to each year.
    Bin into bin_years-year bins from BIN_START_YEAR to BIN_END_YEAR.
    Returns DataFrame with columns: bin_start, bin_end, bin_mid, total_count,
    western_med, eastern_med, adriatic, black_sea, atlantic.
    """
    bin_edges = list(range(BIN_START_YEAR, BIN_END_YEAR + 1, bin_years))
    if bin_edges[-1] != BIN_END_YEAR:
        bin_edges.append(BIN_END_YEAR)

    # Accumulate weights per year, per region
    year_min = BIN_START_YEAR
    year_max = BIN_END_YEAR
    n_years = year_max - year_min + 1
    year_weights = np.zeros(n_years)
    region_weights = {
        "western_med": np.zeros(n_years),
        "eastern_med": np.zeros(n_years),
        "adriatic": np.zeros(n_years),
        "black_sea": np.zeros(n_years),
        "atlantic": np.zeros(n_years),
    }

    for _, row in df.iterrows():
        date_start = row["date_start"]
        date_end = row["date_end"]
        region = row["region"]

        if pd.isna(date_start) or pd.isna(date_end):
            continue
        date_start = int(float(date_start))
        date_end = int(float(date_end))
        span = date_end - date_start
        if span <= 0:
            span = 1  # avoid div by zero
        weight = 1.0 / span

        # Clip to our year range
        start_clip = max(date_start, year_min)
        end_clip = min(date_end, year_max)
        if start_clip > end_clip:
            continue

        for y in range(start_clip, end_clip + 1):
            idx = y - year_min
            if 0 <= idx < n_years:
                year_weights[idx] += weight
                if region in region_weights:
                    region_weights[region][idx] += weight

    # Bin the year-level weights
    bins_out = []
    for i in range(len(bin_edges) - 1):
        b_start = bin_edges[i]
        b_end = bin_edges[i + 1]
        b_mid = (b_start + b_end) / 2

        # Sum weights for years in this bin
        y_start_idx = max(0, b_start - year_min)
        y_end_idx = min(n_years, b_end - year_min)
        total = float(np.sum(year_weights[y_start_idx:y_end_idx]))
        w_med = float(np.sum(region_weights["western_med"][y_start_idx:y_end_idx]))
        e_med = float(np.sum(region_weights["eastern_med"][y_start_idx:y_end_idx]))
        adr = float(np.sum(region_weights["adriatic"][y_start_idx:y_end_idx]))
        blk = float(np.sum(region_weights["black_sea"][y_start_idx:y_end_idx]))
        atl = float(np.sum(region_weights["atlantic"][y_start_idx:y_end_idx]))

        bins_out.append(
            {
                "bin_start": b_start,
                "bin_end": b_end,
                "bin_mid": b_mid,
                "total_count": total,
                "western_med": w_med,
                "eastern_med": e_med,
                "adriatic": adr,
                "black_sea": blk,
                "atlantic": atl,
            }
        )

    return pd.DataFrame(bins_out)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading OxREP shipwreck data...")
    raw = load_shipwrecks()

    # Parse and clean
    records = []
    for _, row in raw.iterrows():
        rec = parse_wreck(row)
        rec["region"] = classify_region(rec["country"], rec["sea_area"])
        records.append(rec)

    df = pd.DataFrame(records)

    # Filter to wrecks with valid dates for binning (optional: keep all in clean)
    df_dated = df[
        df["date_start"].notna()
        & df["date_end"].notna()
        & (df["date_start"] <= df["date_end"])
    ].copy()

    n_wrecks = len(df)
    n_dated = len(df_dated)
    print(f"Parsed {n_wrecks} wrecks ({n_dated} with valid date range)")

    if n_dated > 0:
        date_min = int(df_dated["date_start"].min())
        date_max = int(df_dated["date_end"].max())
        print(f"Year range: {date_min} to {date_max}")

    # Output clean CSV
    out_clean = PROCESSED_DIR / "shipwrecks_clean.csv"
    df.to_csv(out_clean, index=False)
    print(f"Wrote {out_clean}")

    # Equal-probability binning
    binned_50 = apply_equal_probability_dating(df_dated, BIN_50YR)
    binned_25 = apply_equal_probability_dating(df_dated, BIN_25YR)

    out_50 = PROCESSED_DIR / "shipwrecks_binned_50yr.csv"
    out_25 = PROCESSED_DIR / "shipwrecks_binned_25yr.csv"
    binned_50.to_csv(out_50, index=False)
    binned_25.to_csv(out_25, index=False)
    print(f"Wrote {out_50}")
    print(f"Wrote {out_25}")

    # First-look plot
    fig, ax = plt.subplots(figsize=(12, 6))
    x = binned_50["bin_mid"]
    y = binned_50["total_count"]
    ax.bar(x, y, width=BIN_50YR * 0.85, align="center", color="steelblue", edgecolor="navy", alpha=0.8)
    ax.set_xlabel("Year (CE/BCE)")
    ax.set_ylabel("Expected wreck count per bin")
    ax.set_title("Mediterranean Shipwrecks by 50-Year Bin (OxREP/Parker-Strauss)")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_xlim(BIN_START_YEAR - 25, BIN_END_YEAR + 25)
    fig.tight_layout()
    plot_path = FIGURES_DIR / "shipwrecks_first_look.png"
    fig.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Wrote {plot_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
