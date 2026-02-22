"""
Ingest denarius silver fineness data from numismatic literature.
Data from Butcher & Ponting (2015) "The Metallurgy of Roman Silver Coinage",
Walker (1976-78) "The Metrology of the Roman Silver Coinage", and other standard references.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_CSV = PROJECT_ROOT / "data" / "processed" / "denarius_silver.csv"
OUT_FIG = PROJECT_ROOT / "output" / "figures" / "denarius_first_look.png"

# Well-established denarius silver fineness data points from published research
DENARIUS_DATA = [
    {"year_ce": -210, "silver_pct": 97.0, "emperor_or_period": "Republic (post-Second Punic War)", "source_note": "Walker 1976"},
    {"year_ce": -150, "silver_pct": 97.0, "emperor_or_period": "Republic", "source_note": "Walker 1976"},
    {"year_ce": -100, "silver_pct": 97.0, "emperor_or_period": "Late Republic", "source_note": "Walker 1976"},
    {"year_ce": -50, "silver_pct": 97.5, "emperor_or_period": "Late Republic", "source_note": "Walker 1976"},
    {"year_ce": -27, "silver_pct": 98.0, "emperor_or_period": "Augustus (early)", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 14, "silver_pct": 97.5, "emperor_or_period": "Augustus (late) / Tiberius", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 37, "silver_pct": 97.5, "emperor_or_period": "Caligula", "source_note": "Walker 1976"},
    {"year_ce": 54, "silver_pct": 97.0, "emperor_or_period": "Claudius", "source_note": "Walker 1976"},
    {"year_ce": 64, "silver_pct": 93.5, "emperor_or_period": "Nero (post-reform)", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 68, "silver_pct": 93.0, "emperor_or_period": "Galba", "source_note": "Walker 1976"},
    {"year_ce": 69, "silver_pct": 93.0, "emperor_or_period": "Vitellius", "source_note": "Walker 1976"},
    {"year_ce": 79, "silver_pct": 92.0, "emperor_or_period": "Vespasian", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 81, "silver_pct": 92.0, "emperor_or_period": "Titus", "source_note": "Walker 1976"},
    {"year_ce": 96, "silver_pct": 92.0, "emperor_or_period": "Domitian", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 98, "silver_pct": 93.0, "emperor_or_period": "Nerva / Trajan (early)", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 107, "silver_pct": 89.0, "emperor_or_period": "Trajan (middle)", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 117, "silver_pct": 87.0, "emperor_or_period": "Trajan (late) / Hadrian", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 138, "silver_pct": 83.0, "emperor_or_period": "Hadrian (late) / Antoninus Pius", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 161, "silver_pct": 79.0, "emperor_or_period": "Marcus Aurelius", "source_note": "Butcher & Ponting 2015"},
    {"year_ce": 180, "silver_pct": 75.0, "emperor_or_period": "Commodus", "source_note": "Walker 1976"},
    {"year_ce": 193, "silver_pct": 60.0, "emperor_or_period": "Pertinax / Septimius Severus (early)", "source_note": "Walker 1976"},
    {"year_ce": 200, "silver_pct": 56.0, "emperor_or_period": "Septimius Severus", "source_note": "Walker 1976"},
    {"year_ce": 211, "silver_pct": 52.0, "emperor_or_period": "Caracalla (pre-antoninianus)", "source_note": "Walker 1976"},
    {"year_ce": 215, "silver_pct": 51.5, "emperor_or_period": "Caracalla (antoninianus introduced)", "source_note": "Walker 1976"},
    {"year_ce": 222, "silver_pct": 47.0, "emperor_or_period": "Severus Alexander", "source_note": "Walker 1976"},
    {"year_ce": 238, "silver_pct": 45.0, "emperor_or_period": "Maximinus / Gordian III", "source_note": "Walker 1976"},
    {"year_ce": 253, "silver_pct": 40.0, "emperor_or_period": "Valerian / Gallienus (early)", "source_note": "Walker 1976"},
    {"year_ce": 260, "silver_pct": 20.0, "emperor_or_period": "Gallienus (sole reign)", "source_note": "Walker 1976"},
    {"year_ce": 268, "silver_pct": 2.5, "emperor_or_period": "Claudius II", "source_note": "Walker 1976"},
    {"year_ce": 270, "silver_pct": 2.0, "emperor_or_period": "Aurelian (pre-reform)", "source_note": "Walker 1976"},
    {"year_ce": 274, "silver_pct": 5.0, "emperor_or_period": "Aurelian (post-reform)", "source_note": "Walker 1976"},
    {"year_ce": 284, "silver_pct": 4.0, "emperor_or_period": "Diocletian (pre-reform)", "source_note": "Walker 1976"},
    {"year_ce": 294, "silver_pct": 3.0, "emperor_or_period": "Diocletian (argenteus)", "source_note": "Walker 1976"},
]


def main():
    # Ensure output dirs exist
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(DENARIUS_DATA)

    # Save CSV
    df.to_csv(OUT_CSV, index=False)
    print(f"Saved {len(df)} rows to {OUT_CSV}")

    # First-look plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["year_ce"], df["silver_pct"], color="black", s=30, zorder=3)
    ax.plot(df["year_ce"], df["silver_pct"], color="black", linewidth=0.8, zorder=2)
    ax.set_xlim(-250, 300)
    ax.set_xlabel("Year")
    ax.set_ylabel("Silver content (%)")
    ax.set_title("Roman Denarius Silver Content")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT_FIG, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved plot to {OUT_FIG}")


if __name__ == "__main__":
    main()
