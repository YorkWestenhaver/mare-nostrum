#!/usr/bin/env python3
"""
Prepare world_borders.json for the Cliopatria World Civilizations map.

Reads the full Cliopatria GeoJSON (~186 MB, 14,945 features, 3400 BCE - 2024 CE)
and produces a browser-friendly version with FULL polygon detail.

Processing:
  - Filters out composite polities (names starting with '(')
  - Rounds coordinates to 2 decimal places (~1.1 km precision)
  - Strips fields not needed for display
  - NO polygon simplification — every coordinate point is preserved

Output: svelte-app/static/data/geo/world_borders.json (~38 MB, gzips to ~10 MB)
"""

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
GEO_OUT = BASE / "svelte-app" / "static" / "data" / "geo"
GEO_OUT.mkdir(parents=True, exist_ok=True)

COORD_PRECISION = 2


def round_coords(obj, precision):
    if isinstance(obj, list):
        if obj and isinstance(obj[0], (int, float)):
            return [round(x, precision) for x in obj]
        return [round_coords(item, precision) for item in obj]
    return obj


def process():
    clio_dir = RAW / "cliopatria" / "extracted"
    inner = list(clio_dir.glob("Seshat-*"))
    if not inner:
        print("ERROR: Cliopatria extracted directory not found")
        sys.exit(1)

    geojson_path = inner[0] / "cliopatria.geojson"
    print(f"Reading {geojson_path} ...")
    with open(geojson_path) as f:
        data = json.load(f)

    total = len(data["features"])
    print(f"  Total features: {total}")

    features_out = []
    skipped_composite = 0
    skipped_no_geom = 0
    skipped_no_year = 0

    for feat in data["features"]:
        props = feat["properties"]
        name = props.get("Name", "")

        if name.startswith("("):
            skipped_composite += 1
            continue

        from_year = props.get("FromYear")
        to_year = props.get("ToYear")
        if from_year is None or to_year is None:
            skipped_no_year += 1
            continue

        geom = feat.get("geometry")
        if not geom:
            skipped_no_geom += 1
            continue

        geom["coordinates"] = round_coords(geom["coordinates"], COORD_PRECISION)

        features_out.append({
            "type": "Feature",
            "properties": {
                "name": name,
                "from": int(from_year),
                "to": int(to_year),
                "area": round(props.get("Area", 0), 0),
                "wiki": props.get("Wikipedia", ""),
            },
            "geometry": geom,
        })

    print(f"  Kept: {len(features_out)}")
    print(f"  Skipped composite: {skipped_composite}")
    print(f"  Skipped no geometry: {skipped_no_geom}")
    print(f"  Skipped no year: {skipped_no_year}")

    result = {"type": "FeatureCollection", "features": features_out}
    out_path = GEO_OUT / "world_borders.json"
    with open(out_path, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"\n  Wrote {len(features_out)} features to {out_path}")
    print(f"  File size: {size_mb:.1f} MB")


if __name__ == "__main__":
    process()
