"""Loading of static datasets: district boundaries, crop parameters and the
district crop mix (taken from the NISR Seasonal Agricultural Survey)."""

import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Rwanda's 30 districts grouped by province.
PROVINCES = {
    "Kigali City": ["Gasabo", "Kicukiro", "Nyarugenge"],
    "Northern": ["Burera", "Gakenke", "Gicumbi", "Musanze", "Rulindo"],
    "Southern": ["Gisagara", "Huye", "Kamonyi", "Muhanga", "Nyamagabe",
                 "Nyanza", "Nyaruguru", "Ruhango"],
    "Eastern": ["Bugesera", "Gatsibo", "Kayonza", "Kirehe", "Ngoma",
                "Nyagatare", "Rwamagana"],
    "Western": ["Karongi", "Ngororero", "Nyabihu", "Nyamasheke", "Rubavu",
                "Rusizi", "Rutsiro"],
}


def _signed_area(ring: list) -> float:
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1])) / 2


def load_geojson() -> dict:
    """District boundaries from geoBoundaries (CC BY 4.0).

    The file follows RFC 7946 (outer rings counter-clockwise), but Plotly's
    geo maps use d3, which expects outer rings clockwise and otherwise fills
    the whole globe. Rings are rewound here: outer clockwise, holes CCW."""
    with open(DATA_DIR / "rwanda_districts.geojson", encoding="utf-8") as f:
        gj = json.load(f)
    for feature in gj["features"]:
        geom = feature["geometry"]
        polygons = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        for polygon in polygons:
            for i, ring in enumerate(polygon):
                outer = i == 0
                if (_signed_area(ring) > 0) == outer:  # CCW outer or CW hole
                    ring.reverse()
    return gj


def _ring_centroid(ring: list) -> tuple[float, float, float]:
    """Area-weighted centroid of a polygon ring (shoelace formula).
    Returns (area, lon, lat)."""
    area = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]):
        cross = x0 * y1 - x1 * y0
        area += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    area /= 2
    if area == 0:
        xs, ys = zip(*ring)
        return 0.0, sum(xs) / len(xs), sum(ys) / len(ys)
    return abs(area), cx / (6 * area), cy / (6 * area)


def load_districts() -> pd.DataFrame:
    """One row per district with province and centroid coordinates, used to
    query the weather API at a representative point."""
    province_of = {d: p for p, ds in PROVINCES.items() for d in ds}
    rows = []
    for feature in load_geojson()["features"]:
        name = feature["properties"]["shapeName"]
        geom = feature["geometry"]
        polygons = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        # Use the largest outer ring so small islands don't skew the point.
        area, lon, lat = max((_ring_centroid(p[0]) for p in polygons), key=lambda c: c[0])
        rows.append({"district": name, "province": province_of.get(name, "Unknown"),
                     "lat": round(lat, 4), "lon": round(lon, 4)})
    return pd.DataFrame(rows).sort_values("district").reset_index(drop=True)


def load_crops() -> pd.DataFrame:
    """Agronomic parameters per crop (FAO-56 crop coefficients etc.)."""
    return pd.read_csv(DATA_DIR / "crops.csv")


def load_district_crops() -> pd.DataFrame:
    """Share of each district's cultivated area under each crop.

    Shares are normalised per district so that they sum to 1, which lets the
    file hold either hectares or percentages straight from the NISR tables."""
    df = pd.read_csv(DATA_DIR / "district_crops.csv")
    df["share"] = df["area"] / df.groupby("district")["area"].transform("sum")
    return df


def uses_sample_crop_data() -> bool:
    """True while district_crops.csv still holds the illustrative sample rows."""
    return (load_district_crops()["source"].str.contains("SAMPLE", case=False)).any()
