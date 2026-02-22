"""
Create the final publication-quality 4-panel figure for the sick-pottery project.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import pandas as pd
import seaborn as sns

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEAD_PATH = PROJECT_ROOT / "data" / "processed" / "lead_emissions.csv"
SHIPWRECKS_PATH = PROJECT_ROOT / "data" / "processed" / "shipwrecks_binned_50yr.csv"
DENARIUS_PATH = PROJECT_ROOT / "data" / "processed" / "denarius_silver.csv"
CHANGEPOINT_PATH = PROJECT_ROOT / "output" / "tables" / "changepoint_results.json"
OUTPUT_PATH = PROJECT_ROOT / "output" / "figures" / "final_publication.png"

# Historical events: (year, label)
HISTORICAL_EVENTS = [
    (165, "Antonine Plague"),
    (249, "Plague of Cyprian"),
    (439, "Vandals take N. Africa"),
    (541, "Plague of Justinian"),
    (632, "Islamic expansion"),
]


def add_event_lines(ax, x_min, x_max, fontsize=7):
    """Add thin gray vertical lines and rotated labels for historical events in range."""
    trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
    for year, label in HISTORICAL_EVENTS:
        if x_min <= year <= x_max:
            ax.axvline(year, color="gray", linewidth=0.5, linestyle="-", alpha=0.7)
            ax.text(
                year,
                1.02,
                label,
                transform=trans,
                rotation=45,
                ha="left",
                va="bottom",
                fontsize=fontsize,
                color="gray",
            )


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load data
    lead = pd.read_csv(LEAD_PATH)
    shipwrecks = pd.read_csv(SHIPWRECKS_PATH)
    denarius = pd.read_csv(DENARIUS_PATH)
    with open(CHANGEPOINT_PATH) as f:
        cp = json.load(f)

    changepoints_lead = cp["changepoints_lead"]
    changepoints_ship_all = cp["changepoints_ship_all"]
    changepoints_ship_west = cp["changepoints_ship_west"]
    changepoints_ship_east = cp["changepoints_ship_east"]

    # Filter data to relevant ranges
    lead_sub = lead[(lead["year_ce"] >= -600) & (lead["year_ce"] <= 800)].copy()
    ship_sub = shipwrecks[
        (shipwrecks["bin_mid"] >= -600) & (shipwrecks["bin_mid"] <= 800)
    ].copy()
    denarius_sub = denarius[
        (denarius["year_ce"] >= -250) & (denarius["year_ce"] <= 310)
    ].copy()

    # Styling
    sns.set_style("white")
    plt.rcParams.update({"font.size": 10})

    fig, axes = plt.subplots(4, 1, figsize=(16, 18), sharex=False)
    fig.subplots_adjust(hspace=0.35)
    # Share x-axis for panels A, B, C
    axes[1].sharex(axes[0])
    axes[2].sharex(axes[0])

    x_shared_min, x_shared_max = -600, 850

    # --- Panel A: Lead Emissions ---
    ax_a = axes[0]
    ax_a.set_xlim(x_shared_min, x_shared_max)
    ax_a.fill_between(
        lead_sub["year_ce"],
        lead_sub["lead_emissions_kt_a"],
        0,
        color="lightgray",
        alpha=0.8,
    )
    ax_a.plot(
        lead_sub["year_ce"],
        lead_sub["lead_emissions_kt_a"],
        color="#333333",
        linewidth=1.5,
    )
    for cp_year in changepoints_lead:
        if x_shared_min <= cp_year <= x_shared_max:
            ax_a.axvline(cp_year, color="red", linestyle="--", linewidth=1)
    add_event_lines(ax_a, x_shared_min, x_shared_max, fontsize=7)
    ax_a.set_ylabel("Lead Emissions (kt/yr)", fontsize=11)
    ax_a.set_title("A. European Lead-Silver Mining (Greenland Ice Core)", fontsize=13, fontweight="bold")
    ax_a.tick_params(axis="both", labelsize=10)
    ax_a.set_ylim(bottom=0)

    # --- Panel B: All Mediterranean Shipwrecks ---
    ax_b = axes[1]
    ax_b.set_xlim(x_shared_min, x_shared_max)
    ax_b.bar(
        ship_sub["bin_mid"],
        ship_sub["total_count"],
        width=45,
        color="#555555",
        edgecolor="none",
    )
    for cp_year in changepoints_ship_all:
        if x_shared_min <= cp_year <= x_shared_max:
            ax_b.axvline(cp_year, color="red", linestyle="--", linewidth=1)
    add_event_lines(ax_b, x_shared_min, x_shared_max, fontsize=7)
    ax_b.set_ylabel("Wreck Count (50yr bin)", fontsize=11)
    ax_b.set_title("B. Mediterranean Shipwrecks (OxREP)", fontsize=13, fontweight="bold")
    ax_b.tick_params(axis="both", labelsize=10)
    ax_b.set_ylim(bottom=0)

    # --- Panel C: Western vs Eastern Mediterranean ---
    ax_c = axes[2]
    ax_c.set_xlim(x_shared_min, x_shared_max)
    width = 18
    ax_c.bar(
        ship_sub["bin_mid"] - 10,
        ship_sub["western_med"],
        width=width,
        color="red",
        alpha=0.7,
        label="Western Med",
    )
    ax_c.bar(
        ship_sub["bin_mid"] + 10,
        ship_sub["eastern_med"],
        width=width,
        color="blue",
        alpha=0.7,
        label="Eastern Med",
    )
    for cp_year in changepoints_ship_west:
        if x_shared_min <= cp_year <= x_shared_max:
            ax_c.axvline(cp_year, color="red", linestyle="--", linewidth=1)
    for cp_year in changepoints_ship_east:
        if x_shared_min <= cp_year <= x_shared_max:
            ax_c.axvline(cp_year, color="blue", linestyle="--", linewidth=1)
    add_event_lines(ax_c, x_shared_min, x_shared_max, fontsize=7)
    ax_c.set_ylabel("Wreck Count", fontsize=11)
    ax_c.set_title("C. Regional Decomposition", fontsize=13, fontweight="bold")
    ax_c.legend(loc="upper right", fontsize=9)
    ax_c.tick_params(axis="both", labelsize=10)
    ax_c.set_ylim(bottom=0)

    # --- Panel D: Denarius Silver Content ---
    ax_d = axes[3]
    x_d_min, x_d_max = -250, 310
    ax_d.set_xlim(x_d_min, x_d_max)
    ax_d.plot(
        denarius_sub["year_ce"],
        denarius_sub["silver_pct"],
        color="purple",
        linewidth=1.5,
    )
    ax_d.scatter(
        denarius_sub["year_ce"],
        denarius_sub["silver_pct"],
        color="purple",
        s=25,
        zorder=5,
    )
    add_event_lines(ax_d, x_d_min, x_d_max, fontsize=7)
    ax_d.set_ylabel("Silver (%)", fontsize=11)
    ax_d.set_xlabel("Year (CE)", fontsize=11)
    ax_d.set_title("D. Denarius Silver Content", fontsize=13, fontweight="bold")
    ax_d.tick_params(axis="both", labelsize=10)
    ax_d.set_ylim(bottom=0)

    # Add x-label only to bottom panel for shared panels (A,B,C share x)
    for ax in axes[:3]:
        ax.set_xlabel("")

    fig.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
