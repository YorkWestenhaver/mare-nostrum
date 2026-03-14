#!/usr/bin/env python3
"""
Prepare GeoJSON files for the GeoCron visualization.

Reads:
  - Cliopatria geojson (historical political borders, 3400 BCE - 2024 CE)
  - ORBIS gorbit CSV files (Roman transportation network)
  - Shipwrecks CSV (existing processed data)

Writes to data/geo/:
  - borders.json    – Mediterranean political entities filtered & simplified
  - routes.json     – ORBIS trade routes as GeoJSON LineStrings
  - shipwrecks.json – Shipwreck points with date ranges and cargo info
"""

import json
import csv
import os
import math
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"
GEO_OUT = BASE / "data" / "geo"
GEO_OUT.mkdir(parents=True, exist_ok=True)

MED_BBOX = {"lat_min": 20, "lat_max": 55, "lon_min": -15, "lon_max": 50}
TIME_MIN = -1200
TIME_MAX = 800


def centroid_of_polygon(coords):
    """Approximate centroid from the first ring of a polygon."""
    ring = coords[0] if coords else []
    if not ring:
        return None, None
    lons = [p[0] for p in ring]
    lats = [p[1] for p in ring]
    return sum(lons) / len(lons), sum(lats) / len(lats)


def centroid_of_geometry(geom):
    gtype = geom.get("type", "")
    coords = geom.get("coordinates", [])
    if gtype == "Polygon":
        return centroid_of_polygon(coords)
    elif gtype == "MultiPolygon":
        all_lons, all_lats = [], []
        for poly in coords:
            ring = poly[0] if poly else []
            all_lons.extend(p[0] for p in ring)
            all_lats.extend(p[1] for p in ring)
        if all_lons:
            return sum(all_lons) / len(all_lons), sum(all_lats) / len(all_lats)
    return None, None


def simplify_ring(ring, tolerance=0.15):
    """Ramer-Douglas-Peucker simplification."""
    if len(ring) <= 4:
        return ring

    def rdp(points, eps):
        if len(points) <= 2:
            return points
        dmax = 0
        idx = 0
        start, end = points[0], points[-1]
        for i in range(1, len(points) - 1):
            d = point_line_distance(points[i], start, end)
            if d > dmax:
                dmax = d
                idx = i
        if dmax > eps:
            left = rdp(points[:idx + 1], eps)
            right = rdp(points[idx:], eps)
            return left[:-1] + right
        else:
            return [start, end]

    result = rdp(ring, tolerance)
    if len(result) < 4:
        return ring
    return result


def point_line_distance(point, start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    if dx == 0 and dy == 0:
        return math.hypot(point[0] - start[0], point[1] - start[1])
    t = max(0, min(1, ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / (dx * dx + dy * dy)))
    proj_x = start[0] + t * dx
    proj_y = start[1] + t * dy
    return math.hypot(point[0] - proj_x, point[1] - proj_y)


def simplify_geometry(geom, tolerance=0.15):
    gtype = geom.get("type", "")
    coords = geom.get("coordinates", [])
    if gtype == "Polygon":
        new_coords = [simplify_ring(ring, tolerance) for ring in coords]
        return {"type": gtype, "coordinates": new_coords}
    elif gtype == "MultiPolygon":
        new_polys = []
        for poly in coords:
            new_polys.append([simplify_ring(ring, tolerance) for ring in poly])
        return {"type": gtype, "coordinates": new_polys}
    return geom


def in_med_bbox(lon, lat):
    return (MED_BBOX["lat_min"] <= lat <= MED_BBOX["lat_max"]
            and MED_BBOX["lon_min"] <= lon <= MED_BBOX["lon_max"])


# ── 1. Process Cliopatria borders ──────────────────────────────────────────────

def process_borders():
    print("Processing Cliopatria borders...")
    clio_dir = RAW / "cliopatria" / "extracted"
    inner = list(clio_dir.glob("Seshat-*"))
    if not inner:
        print("  ERROR: Cliopatria extracted directory not found")
        return
    geojson_path = inner[0] / "cliopatria.geojson"
    with open(geojson_path) as f:
        data = json.load(f)

    features_out = []
    for feat in data["features"]:
        props = feat["properties"]
        from_year = props.get("FromYear")
        to_year = props.get("ToYear")
        if from_year is None or to_year is None:
            continue
        if to_year < TIME_MIN or from_year > TIME_MAX:
            continue

        geom = feat.get("geometry")
        if not geom:
            continue
        lon, lat = centroid_of_geometry(geom)
        if lon is None or not in_med_bbox(lon, lat):
            continue

        features_out.append({
            "type": "Feature",
            "properties": {
                "name": props.get("Name", "Unknown"),
                "from": int(from_year),
                "to": int(to_year),
                "type": props.get("Type", ""),
                "wiki": props.get("Wikipedia", ""),
                "area": round(props.get("Area", 0), 1),
            },
            "geometry": geom
        })

    def round_coords(obj):
        """Recursively round all coordinate numbers to 2 decimal places."""
        if isinstance(obj, list):
            if obj and isinstance(obj[0], (int, float)):
                return [round(x, 2) for x in obj]
            return [round_coords(item) for item in obj]
        return obj

    for feat in features_out:
        geom = feat["geometry"]
        geom["coordinates"] = round_coords(geom["coordinates"])

    result = {"type": "FeatureCollection", "features": features_out}
    out_path = GEO_OUT / "borders.json"
    with open(out_path, "w") as f:
        json.dump(result, f, separators=(",", ":"))
    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"  Wrote {len(features_out)} features to borders.json ({size_mb:.1f} MB)")


# ── 2. Process ORBIS routes ───────────────────────────────────────────────────

def process_routes():
    print("Processing ORBIS routes...")

    nodes = {}
    nodes_path = RAW / "orbis" / "gorbit-nodes.csv"
    with open(nodes_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            nid = row["id"].strip().strip('"')
            nodes[nid] = {
                "label": row["label"].strip().strip('"'),
                "x": float(row["x"]),
                "y": float(row["y"]),
                "rank": int(row.get("rank", 0)),
            }

    sites = {}
    sites_path = RAW / "orbis" / "gorbit-sites.csv"
    with open(sites_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["id"].strip().strip('"')
            sites[sid] = {
                "title": row["title"].strip().strip('"'),
                "lat": float(row["latitude"]),
                "lon": float(row["longitude"]),
                "pleiades": row.get("pleiades", "").strip().strip('"'),
            }

    # Regional time ranges for Roman control/route viability.
    # Based on when Rome built/controlled infrastructure in each area.
    # Format: (lon_min, lon_max, lat_min, lat_max, from_year, to_year)
    REGION_TIMES = [
        # Italy core — earliest Roman roads (Via Appia 312 BCE)
        (7, 19, 36, 46,   -350, 600),
        # Sicily, Sardinia, Corsica — after First Punic War
        (8, 16, 36, 42,   -240, 550),
        # Iberia — after Second Punic War, lost to Visigoths ~420
        (-10, 4, 35, 44,  -200, 420),
        # Southern Gaul — conquest ~120 BCE
        (-2, 8, 42, 46,   -120, 470),
        # Northern Gaul, Belgica, Germania Inferior
        (-5, 10, 46, 54,  -50, 460),
        # Britannia
        (-6, 2, 50, 58,   43, 410),
        # Greece, Macedonia — conquest 146 BCE
        (19, 30, 35, 42,  -200, 600),
        # Asia Minor/Anatolia — province of Asia 133 BCE
        (26, 42, 36, 42,  -130, 650),
        # Syria, Levant — Pompey 64 BCE
        (34, 42, 30, 37,  -64, 640),
        # Egypt — annexed 30 BCE
        (24, 36, 22, 32,  -30, 640),
        # North Africa (Tunisia, Libya) — after Punic Wars
        (7, 25, 30, 38,   -146, 550),
        # Mauretania (Morocco, western Algeria) — annexed 40 CE
        (-8, 7, 30, 37,   40, 430),
        # Dacia, Moesia, Pannonia — Danube provinces
        (16, 30, 42, 48,  -15, 450),
        # Black Sea coast
        (30, 42, 40, 46,  -65, 600),
    ]

    # Sea routes and rivers were available earlier (pre-Roman trade) and
    # persisted longer (Byzantine/Arab continuation). Expand ranges.
    TYPE_OFFSETS = {
        "road": (0, 0),
        "river": (-200, 100),
        "coastal": (-300, 150),
        "open sea": (-400, 200),
    }

    def route_time_range(x1, y1, x2, y2, route_type):
        """Determine from/to years for a route based on endpoint locations."""
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        best_from, best_to = -100, 500  # default: generic Roman era
        for lon_min, lon_max, lat_min, lat_max, rfrom, rto in REGION_TIMES:
            if lon_min <= mx <= lon_max and lat_min <= my <= lat_max:
                best_from = rfrom
                best_to = rto
                break
        off = TYPE_OFFSETS.get(route_type, (0, 0))
        return best_from + off[0], best_to + off[1]

    edge_features = []
    node_features = []
    node_time_ranges = {}  # track per-node earliest from / latest to
    edges_path = RAW / "orbis" / "gorbit-edges.csv"
    with open(edges_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row["source"].strip().strip('"')
            tgt = row["target"].strip().strip('"')
            if src not in nodes or tgt not in nodes:
                continue

            s = nodes[src]
            t = nodes[tgt]
            route_type = row["type"].strip().strip('"')
            km = float(row["km"])
            days = float(row["days"])
            expense = float(row["expense"])

            rfrom, rto = route_time_range(s["x"], s["y"], t["x"], t["y"], route_type)

            for nid in (src, tgt):
                if nid not in node_time_ranges:
                    node_time_ranges[nid] = [rfrom, rto]
                else:
                    node_time_ranges[nid][0] = min(node_time_ranges[nid][0], rfrom)
                    node_time_ranges[nid][1] = max(node_time_ranges[nid][1], rto)

            edge_features.append({
                "type": "Feature",
                "properties": {
                    "source": s["label"],
                    "target": t["label"],
                    "type": route_type,
                    "from": rfrom,
                    "to": rto,
                    "km": round(km, 1),
                    "days": round(days, 2),
                    "expense": round(expense, 2),
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[s["x"], s["y"]], [t["x"], t["y"]]]
                }
            })

    seen_nodes = set()
    for nid, n in nodes.items():
        if nid in seen_nodes:
            continue
        seen_nodes.add(nid)
        site_info = sites.get(nid, {})
        tr = node_time_ranges.get(nid, [-100, 500])
        node_features.append({
            "type": "Feature",
            "properties": {
                "id": nid,
                "label": n["label"],
                "rank": n["rank"],
                "title": site_info.get("title", n["label"]),
                "pleiades": site_info.get("pleiades", ""),
                "from": tr[0],
                "to": tr[1],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [n["x"], n["y"]]
            }
        })

    routes_out = {
        "type": "FeatureCollection",
        "features": edge_features
    }
    nodes_out = {
        "type": "FeatureCollection",
        "features": node_features
    }

    with open(GEO_OUT / "routes.json", "w") as f:
        json.dump(routes_out, f, separators=(",", ":"))
    with open(GEO_OUT / "route_nodes.json", "w") as f:
        json.dump(nodes_out, f, separators=(",", ":"))

    print(f"  Wrote {len(edge_features)} edges to routes.json")
    print(f"  Wrote {len(node_features)} nodes to route_nodes.json")


# ── 3. Process shipwrecks ────────────────────────────────────────────────────

PLACE_COORDS = {
    "egypt": (31.2, 30.0), "aegean": (25.5, 37.5), "rhodes": (28.2, 36.4),
    "cos": (27.0, 36.9), "rome": (12.5, 41.9), "cosa": (11.3, 42.4),
    "carthage": (10.2, 36.8), "spain": (-3.7, 37.0), "iberia": (-3.7, 37.0),
    "gaul": (2.3, 43.3), "france": (2.3, 43.3), "sicily": (14.0, 37.5),
    "syria": (36.3, 34.0), "palestine": (34.8, 31.8), "africa": (10.2, 36.8),
    "north africa": (10.2, 36.8), "crete": (24.9, 35.2), "cyprus": (33.4, 35.1),
    "anatolia": (32.0, 39.0), "turkey": (32.0, 39.0),
    "greece": (23.7, 38.0), "athens": (23.7, 37.97),
    "corinth": (22.9, 37.9), "apulia": (16.5, 41.0), "brindisi": (17.9, 40.6),
    "campania": (14.3, 40.8), "dalmatia": (16.5, 43.5), "baetica": (-5.0, 37.4),
    "tarraconensis": (1.0, 41.0), "lusitania": (-8.0, 39.0),
    "southern gaul": (3.9, 43.3), "gallia narbonensis": (3.0, 43.2),
    "massalia": (5.4, 43.3), "marseilles": (5.4, 43.3),
    "constantinople": (29.0, 41.0), "antioch": (36.2, 36.2),
    "alexandria": (29.9, 31.2), "tripoli": (13.2, 32.9),
    "leptis magna": (14.3, 32.6), "tyrrhenian": (12.0, 40.0),
    "northern italy": (12.0, 44.5), "italy": (12.5, 42.5),
    "britain": (-1.0, 51.5), "sardinia": (9.1, 39.2), "corsica": (9.0, 42.0),
    "luna": (10.1, 44.1), "chios": (26.1, 38.4), "cnidus": (27.4, 36.7),
    "adriatic": (16.0, 42.5), "proconnesus": (27.6, 40.7), "euboea": (23.9, 38.5),
    "neapolis": (10.15, 36.85), "nabeul": (10.73, 36.45), "llobregat": (2.0, 41.3),
    "pisa": (10.4, 43.7), "levant": (35.5, 33.9), "india": (78.0, 20.0),
    "black sea": (34.0, 43.0), "pergamum": (27.2, 39.1), "caesarea": (34.9, 32.5),
    "mesembria": (27.75, 42.67), "ganos": (27.4, 40.9), "claros": (27.2, 38.0),
}


def lookup_coord(name):
    if not name:
        return None
    key = name.strip().lower().rstrip("?").strip()
    if key in PLACE_COORDS:
        return PLACE_COORDS[key]
    parts = [p.strip().rstrip("?").strip() for p in key.replace("/", ",").split(",")]
    for part in parts:
        if part in PLACE_COORDS:
            return PLACE_COORDS[part]
    for k, v in PLACE_COORDS.items():
        if k in key or key in k:
            return v
    for part in parts:
        for k, v in PLACE_COORDS.items():
            if k in part or part in k:
                return v
    return None


def process_shipwrecks():
    print("Processing shipwrecks...")
    csv_path = PROCESSED / "shipwrecks_clean.csv"
    points = []
    arcs = []

    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat_s = row.get("latitude", "").strip()
            lon_s = row.get("longitude", "").strip()
            if not lat_s or not lon_s:
                continue
            try:
                lat = float(lat_s)
                lon = float(lon_s)
            except ValueError:
                continue

            try:
                date_start = float(row.get("date_start") or 0)
                date_end = float(row.get("date_end") or 0)
            except ValueError:
                continue
            cargo = row.get("cargo_types", "").strip()
            prov = row.get("provenance", "").strip()
            dest = row.get("destination", "").strip()
            name = row.get("name", "").strip()
            region = row.get("region", "").strip()

            points.append({
                "type": "Feature",
                "properties": {
                    "name": name or f"Wreck #{row.get('wreck_id', '?')}",
                    "from": int(date_start),
                    "to": int(date_end),
                    "cargo": cargo[:200] if cargo else "",
                    "provenance": prov,
                    "destination": dest,
                    "region": region,
                    "country": row.get("country", "").strip(),
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [round(lon, 4), round(lat, 4)]
                }
            })

            prov_coord = lookup_coord(prov)
            dest_coord = lookup_coord(dest)
            if prov_coord and dest_coord:
                arcs.append({
                    "type": "Feature",
                    "properties": {
                        "wreck": name or f"Wreck #{row.get('wreck_id', '?')}",
                        "from": int(date_start),
                        "to": int(date_end),
                        "provenance": prov,
                        "destination": dest,
                        "region": region,
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [round(prov_coord[0], 2), round(prov_coord[1], 2)],
                            [round(lon, 4), round(lat, 4)],
                            [round(dest_coord[0], 2), round(dest_coord[1], 2)],
                        ]
                    }
                })

    wrecks_out = {"type": "FeatureCollection", "features": points}
    arcs_out = {"type": "FeatureCollection", "features": arcs}

    with open(GEO_OUT / "shipwrecks.json", "w") as f:
        json.dump(wrecks_out, f, separators=(",", ":"))
    with open(GEO_OUT / "trade_arcs.json", "w") as f:
        json.dump(arcs_out, f, separators=(",", ":"))

    print(f"  Wrote {len(points)} wreck points to shipwrecks.json")
    print(f"  Wrote {len(arcs)} trade arcs to trade_arcs.json")


# ── 4. Process lead emissions for sparkline ──────────────────────────────────

def process_lead_sparkline():
    print("Processing lead emissions sparkline...")
    csv_path = PROCESSED / "lead_emissions.csv"
    data = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                year = float(row["year_ce"])
                val = float(row["lead_emissions_kt_a"])
            except (ValueError, KeyError):
                continue
            if TIME_MIN <= year <= TIME_MAX:
                data.append({"y": round(year), "v": round(val, 3)})

    with open(GEO_OUT / "lead_sparkline.json", "w") as f:
        json.dump(data, f, separators=(",", ":"))
    print(f"  Wrote {len(data)} points to lead_sparkline.json")


if __name__ == "__main__":
    process_borders()
    process_routes()
    process_shipwrecks()
    process_lead_sparkline()
    print("\nDone! Files in", GEO_OUT)
