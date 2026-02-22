#!/usr/bin/env python3
"""
Visualization pipeline for Mediterranean economic decline analysis.
Generates first-look plots, multi-proxy overlays, change-point figures,
regional decomposition, and publication-quality final figures.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "output" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
})


def load_data():
    lead = pd.read_csv(PROCESSED_DIR / "lead_emissions.csv")
    ship50 = pd.read_csv(PROCESSED_DIR / "shipwrecks_binned_50yr.csv")
    ship25 = pd.read_csv(PROCESSED_DIR / "shipwrecks_binned_25yr.csv")
    denarius = pd.read_csv(PROCESSED_DIR / "denarius_silver.csv")
    return lead, ship50, ship25, denarius


def plot_first_look_lead(lead):
    fig, ax = plt.subplots(figsize=(14, 5))
    mask = lead.lead_emissions_kt_a.notna()
    ax.plot(lead.loc[mask, "year_ce"], lead.loc[mask, "lead_emissions_kt_a"],
            color="#2c3e50", linewidth=0.6, alpha=0.85)
    ax.set_xlabel("Year")
    ax.set_ylabel("Estimated Lead Emissions (kt/yr)")
    ax.set_title("Greenland Ice Core Lead Emissions (McConnell et al. 2018)")
    ax.set_xlim(-1200, 800)
    ax.axhline(0, color="gray", linewidth=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "lead_emissions_first_look.png", dpi=150)
    plt.close()
    print("Saved lead_emissions_first_look.png")


def plot_first_look_shipwrecks(ship50):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(ship50.bin_mid, ship50.total_count,
           width=45, color="#2980b9", edgecolor="#1a5276", alpha=0.85)
    ax.set_xlabel("Year")
    ax.set_ylabel("Expected Wreck Count (equal-probability)")
    ax.set_title("Mediterranean Shipwrecks by 50-Year Bin (OxREP/Parker-Strauss)")
    ax.set_xlim(-650, 1050)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "shipwrecks_first_look.png", dpi=150)
    plt.close()
    print("Saved shipwrecks_first_look.png")


def plot_first_look_denarius(denarius):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(denarius.year_ce, denarius.silver_pct,
            "o-", color="#8e44ad", markersize=5, linewidth=1.5)
    ax.set_xlabel("Year")
    ax.set_ylabel("Silver Content (%)")
    ax.set_title("Roman Denarius Silver Content")
    ax.set_xlim(-250, 310)
    ax.set_ylim(0, 105)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "denarius_first_look.png", dpi=150)
    plt.close()
    print("Saved denarius_first_look.png")


def plot_multi_proxy_overlay(lead, ship50, denarius):
    """The 'squint test': normalize all three proxies to [0,1] and overlay."""
    fig, axes = plt.subplots(4, 1, figsize=(14, 16), sharex=True)

    # Panel A: Lead emissions
    ax = axes[0]
    mask = lead.lead_emissions_kt_a.notna()
    ax.plot(lead.loc[mask, "year_ce"], lead.loc[mask, "lead_emissions_kt_a"],
            color="#2c3e50", linewidth=0.5, alpha=0.7)
    ax.set_ylabel("Lead Emissions\n(kt/yr)")
    ax.set_title("A. Greenland Ice Core Lead Emissions", loc="left", fontweight="bold")

    # Panel B: Shipwrecks (50yr bins as step function)
    ax = axes[1]
    ax.bar(ship50.bin_mid, ship50.total_count,
           width=45, color="#2980b9", edgecolor="#1a5276", alpha=0.8)
    ax.set_ylabel("Wreck Count\n(per 50yr bin)")
    ax.set_title("B. Mediterranean Shipwrecks", loc="left", fontweight="bold")

    # Panel C: Denarius silver
    ax = axes[2]
    ax.plot(denarius.year_ce, denarius.silver_pct,
            "o-", color="#8e44ad", markersize=4, linewidth=1.5)
    ax.set_ylabel("Silver Content\n(%)")
    ax.set_ylim(0, 105)
    ax.set_title("C. Denarius Silver Content", loc="left", fontweight="bold")

    # Panel D: Normalized overlay
    ax = axes[3]

    # Bin lead into 50yr to match shipwrecks
    lead_50 = []
    for _, row in ship50.iterrows():
        bstart, bend = row.bin_start, row.bin_end
        mask_bin = (lead.year_ce >= bstart) & (lead.year_ce < bend) & lead.lead_emissions_kt_a.notna()
        if mask_bin.sum() > 0:
            lead_50.append(lead.loc[mask_bin, "lead_emissions_kt_a"].mean())
        else:
            lead_50.append(np.nan)
    lead_50 = np.array(lead_50)

    def norm01(x):
        x = np.array(x, dtype=float)
        mn, mx = np.nanmin(x), np.nanmax(x)
        if mx - mn == 0:
            return x * 0
        return (x - mn) / (mx - mn)

    ship_norm = norm01(ship50.total_count.values)
    lead_norm = norm01(lead_50)

    # Interpolate denarius to 50yr bins
    den_interp = np.interp(ship50.bin_mid, denarius.year_ce, denarius.silver_pct,
                           left=np.nan, right=np.nan)
    den_norm = norm01(den_interp)

    ax.plot(ship50.bin_mid, ship_norm, "s-", color="#2980b9",
            label="Shipwrecks", markersize=4, linewidth=1.5)
    ax.plot(ship50.bin_mid, lead_norm, "^-", color="#2c3e50",
            label="Lead Emissions", markersize=4, linewidth=1.5)
    valid_den = ~np.isnan(den_norm)
    ax.plot(ship50.bin_mid[valid_den], den_norm[valid_den], "o-", color="#8e44ad",
            label="Denarius Silver", markersize=4, linewidth=1.5)
    ax.set_ylabel("Normalized\n(0-1 scale)")
    ax.set_xlabel("Year")
    ax.set_title("D. All Proxies Normalized (the squint test)", loc="left", fontweight="bold")
    ax.legend(loc="upper right", framealpha=0.9)
    ax.set_ylim(-0.05, 1.1)

    for a in axes:
        a.set_xlim(-650, 850)
        a.axvline(0, color="gray", linewidth=0.3, linestyle="--")

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "multi_proxy_overlay.png", dpi=150)
    plt.close()
    print("Saved multi_proxy_overlay.png")


def plot_regional_decomposition(ship50):
    """Plot each Mediterranean sub-region's shipwreck density over time."""
    fig, axes = plt.subplots(3, 1, figsize=(14, 14), sharex=True)

    # Panel A: Western vs Eastern
    ax = axes[0]
    ax.bar(ship50.bin_mid - 10, ship50.western_med, width=18,
           color="#e74c3c", alpha=0.8, label="Western Med")
    ax.bar(ship50.bin_mid + 10, ship50.eastern_med, width=18,
           color="#3498db", alpha=0.8, label="Eastern Med")
    ax.set_ylabel("Wreck Count")
    ax.set_title("A. Western vs Eastern Mediterranean", loc="left", fontweight="bold")
    ax.legend()

    # Panel B: All regions stacked
    ax = axes[1]
    regions = ["western_med", "eastern_med", "adriatic", "black_sea", "atlantic"]
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]
    labels = ["Western Med", "Eastern Med", "Adriatic", "Black Sea", "Atlantic"]
    bottom = np.zeros(len(ship50))
    for region, color, label in zip(regions, colors, labels):
        vals = ship50[region].values
        ax.bar(ship50.bin_mid, vals, width=45, bottom=bottom,
               color=color, alpha=0.8, label=label)
        bottom += vals
    ax.set_ylabel("Wreck Count")
    ax.set_title("B. All Regions Stacked", loc="left", fontweight="bold")
    ax.legend(loc="upper right", fontsize=9)

    # Panel C: Western/Eastern ratio over time
    ax = axes[2]
    ratio = ship50.western_med / ship50.eastern_med.replace(0, np.nan)
    valid = ratio.notna() & np.isfinite(ratio)
    ax.plot(ship50.bin_mid[valid], ratio[valid], "o-", color="#2c3e50",
            markersize=5, linewidth=1.5)
    ax.axhline(1, color="gray", linewidth=0.5, linestyle="--")
    ax.set_ylabel("W/E Ratio")
    ax.set_xlabel("Year")
    ax.set_title("C. Western/Eastern Mediterranean Ratio", loc="left", fontweight="bold")
    ax.set_ylim(0, None)

    for a in axes:
        a.set_xlim(-650, 1050)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "regional_decomposition.png", dpi=150)
    plt.close()
    print("Saved regional_decomposition.png")


def plot_changepoints(lead, ship50, changepoints_lead, changepoints_ship):
    """Plot time series with detected change-points marked."""
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # Lead
    ax = axes[0]
    mask = lead.lead_emissions_kt_a.notna()
    ax.plot(lead.loc[mask, "year_ce"], lead.loc[mask, "lead_emissions_kt_a"],
            color="#2c3e50", linewidth=0.5, alpha=0.7)
    for cp in changepoints_lead:
        ax.axvline(cp, color="#e74c3c", linewidth=1.5, linestyle="--", alpha=0.8)
    ax.set_ylabel("Lead Emissions (kt/yr)")
    ax.set_title("A. Lead Emissions with Detected Change-Points", loc="left", fontweight="bold")

    # Shipwrecks
    ax = axes[1]
    ax.bar(ship50.bin_mid, ship50.total_count,
           width=45, color="#2980b9", edgecolor="#1a5276", alpha=0.8)
    for cp in changepoints_ship:
        ax.axvline(cp, color="#e74c3c", linewidth=1.5, linestyle="--", alpha=0.8)
    ax.set_ylabel("Wreck Count (per 50yr bin)")
    ax.set_xlabel("Year")
    ax.set_title("B. Shipwrecks with Detected Change-Points", loc="left", fontweight="bold")

    for a in axes:
        a.set_xlim(-650, 850)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "changepoints.png", dpi=150)
    plt.close()
    print("Saved changepoints.png")


def plot_historical_overlay(lead, ship50, changepoints_lead, changepoints_ship):
    """Final publication figure with historical events overlaid."""
    events = [
        (-264, "Punic Wars begin"),
        (-146, "Carthage destroyed"),
        (-31, "Actium / Augustus"),
        (9, "Teutoburg"),
        (64, "Nero reform"),
        (165, "Antonine Plague"),
        (235, "Crisis of 3rd C."),
        (249, "Plague of Cyprian"),
        (410, "Sack of Rome"),
        (439, "Vandals take N. Africa"),
        (476, "Fall of W. Rome"),
        (541, "Plague of Justinian"),
        (632, "Islamic expansion begins"),
        (711, "Umayyads take Spain"),
        (750, "Melle mines reopen"),
    ]

    fig, axes = plt.subplots(3, 1, figsize=(16, 14), sharex=True)

    # Lead
    ax = axes[0]
    mask = lead.lead_emissions_kt_a.notna()
    ax.fill_between(lead.loc[mask, "year_ce"], 0,
                    lead.loc[mask, "lead_emissions_kt_a"],
                    color="#2c3e50", alpha=0.3)
    ax.plot(lead.loc[mask, "year_ce"], lead.loc[mask, "lead_emissions_kt_a"],
            color="#2c3e50", linewidth=0.6)
    for cp in changepoints_lead:
        ax.axvline(cp, color="#e74c3c", linewidth=1.2, linestyle="--", alpha=0.7)
    ax.set_ylabel("Lead Emissions (kt/yr)")
    ax.set_title("A. European Lead-Silver Mining Activity", loc="left", fontweight="bold")

    # Shipwrecks
    ax = axes[1]
    ax.bar(ship50.bin_mid, ship50.total_count,
           width=45, color="#2980b9", edgecolor="#1a5276", alpha=0.8)
    for cp in changepoints_ship:
        ax.axvline(cp, color="#e74c3c", linewidth=1.2, linestyle="--", alpha=0.7)
    ax.set_ylabel("Wreck Count (50yr bin)")
    ax.set_title("B. Mediterranean Shipwrecks", loc="left", fontweight="bold")

    # Regional
    ax = axes[2]
    ax.bar(ship50.bin_mid - 10, ship50.western_med, width=18,
           color="#e74c3c", alpha=0.7, label="Western Med")
    ax.bar(ship50.bin_mid + 10, ship50.eastern_med, width=18,
           color="#3498db", alpha=0.7, label="Eastern Med")
    ax.set_ylabel("Wreck Count")
    ax.set_xlabel("Year")
    ax.set_title("C. Regional Decomposition", loc="left", fontweight="bold")
    ax.legend(loc="upper right")

    for ax in axes:
        ax.set_xlim(-650, 850)
        for year, label in events:
            ax.axvline(year, color="#bdc3c7", linewidth=0.4, alpha=0.6)
        ylim = ax.get_ylim()
        for year, label in events:
            if -650 < year < 850:
                ax.text(year, ylim[1] * 0.95, label, rotation=90,
                        va="top", ha="right", fontsize=7, color="#7f8c8d", alpha=0.8)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "historical_overlay.png", dpi=200)
    plt.close()
    print("Saved historical_overlay.png")


if __name__ == "__main__":
    lead, ship50, ship25, denarius = load_data()
    plot_first_look_lead(lead)
    plot_first_look_shipwrecks(ship50)
    plot_first_look_denarius(denarius)
    plot_multi_proxy_overlay(lead, ship50, denarius)
    plot_regional_decomposition(ship50)
    print("\nFirst-look plots complete. Run analyze.py for change-point detection.")
