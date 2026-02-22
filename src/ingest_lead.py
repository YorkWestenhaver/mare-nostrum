"""
Ingest lead emissions data from McConnell et al. 2018 (PNAS).
Reads both sheets from the xlsx file, merges, and outputs clean CSV + first-look plot.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "pnas.1721818115.sd01.xlsx"
OUT_CSV = PROJECT_ROOT / "data" / "processed" / "lead_emissions.csv"
OUT_FIG = PROJECT_ROOT / "output" / "figures" / "lead_emissions_first_look.png"

# Headers in rows 6-7 (0-indexed 5-6), data starts at row 8 (0-indexed 7)
HEADER_ROWS = [5, 6]
DATA_START_ROW = 7
MISSING_VALUE = -0.999


def _flatten_col(col):
    """Flatten multi-level column to string for matching."""
    if isinstance(col, tuple):
        return " ".join(str(c).strip() for c in col if c).strip()
    return str(col).strip()


def _find_col(df, candidates):
    """Find first matching column name (handles multi-index)."""
    cols = [c for c in df.columns]
    flat = [_flatten_col(c) for c in cols]
    for cand in candidates:
        for i, f in enumerate(flat):
            if cand.lower() in f.lower():
                return cols[i]
    return None


def read_sheet(sheet_name: str) -> pd.DataFrame:
    """Read one sheet with correct header/data rows."""
    df = pd.read_excel(
        RAW_PATH,
        sheet_name=sheet_name,
        header=HEADER_ROWS,
    )
    return df


def main():
    # Ensure output dirs exist
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)

    # Read both sheets
    fig2 = read_sheet("Fig. 2")
    fig3 = read_sheet("Fig. 3")

    # Resolve column names (handle multi-index)
    year_col = _find_col(fig2, ["Year Before 1950", "year"])
    lead_col = _find_col(fig2, ["Lead", "pg/g"])
    flux_col = _find_col(fig3, ["non background Lead Flux", "Lead Flux"])
    emissions_col = _find_col(fig3, ["11-y median", "Lead Emissions", "kt/a"])

    if year_col is None:
        raise ValueError("Could not find 'Year Before 1950' column")
    if lead_col is None:
        raise ValueError("Could not find 'Lead' column in Fig. 2")
    if flux_col is None:
        raise ValueError("Could not find 'non background Lead Flux' column")
    if emissions_col is None:
        raise ValueError("Could not find '11-y median filtered estimated Lead Emissions' column")

    # Build merged dataframe
    year_bp = fig2[year_col].astype(float)
    year_ce = 1950 - year_bp

    df = pd.DataFrame(
        {
            "year_ce": year_ce,
            "lead_concentration_pg_g": fig2[lead_col].replace(MISSING_VALUE, np.nan),
            "lead_flux_ug_m2_a": fig3[flux_col].replace(MISSING_VALUE, np.nan),
            "lead_emissions_kt_a": fig3[emissions_col].replace(MISSING_VALUE, np.nan),
        }
    )

    # Drop rows where year_ce is NaN (from invalid year_bp)
    df = df.dropna(subset=["year_ce"])

    # Save CSV
    df.to_csv(OUT_CSV, index=False)
    print(f"Saved {len(df)} rows to {OUT_CSV}")

    # First-look plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["year_ce"], df["lead_emissions_kt_a"], color="black", linewidth=0.8)
    ax.set_xlim(-1200, 800)
    ax.set_xlabel("Year")
    ax.set_ylabel("Lead emissions (kt/a)")
    ax.set_title("Greenland Ice Core Lead Emissions (McConnell et al. 2018)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_FIG, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved plot to {OUT_FIG}")


if __name__ == "__main__":
    main()
