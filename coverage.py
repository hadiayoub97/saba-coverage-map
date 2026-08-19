"""
Derive real coverage geometry for SABA's listed fleet from orbital longitude alone.
No proprietary operator data required -- this is pure geostationary geometry.
"""
import math, json

RE, H = 6378.137, 35786.0
K = RE / (RE + H)
MIN_EL = 10.0  # deg; below this, rain fade and obstruction make service unreliable

# from sabaworld.com/satellite
FLEET = [
    ("Astra 19.2E",        19.2,  "Ku"), ("Hot Bird 13D",     13.0,  "Ku"),
    ("Eutelsat 7 West A",  -7.0,  "Ku"), ("Eutelsat 8 West B", -8.0,  "Ku"),
    ("Yahsat 1A",          52.5,  "Ku"), ("Galaxy 19",        -97.0, "Ku"),
    ("Intelsat 20",        68.5,  "Ku"), ("AsiaSat 5",        100.5, "C"),
    ("AsiaSat 7",         105.5,  "C"),  ("Eutelsat 16A",      16.0,  "Ku"),
    ("Eutelsat 5 West A",  -5.0,  "C"),  ("SES-5",             5.0,   "Ka/Ku"),
    ("Africasat-1a",       46.0,  "C"),  ("Optus D2",          152.0, "Ku"),
    ("Hellas Sat 2",       39.0,  "Ku"), ("Thor 6",           -0.8,  "Ku"),
    ("Eutelsat 3D",         3.1,  "Ku"), ("Telstar 12",       -15.0, "Ku"),
]

def elevation(lat, lon, sat_lon):
    p, d = math.radians(lat), math.radians(lon - sat_lon)
    g = math.acos(max(-1, min(1, math.cos(p) * math.cos(d))))
    if math.sin(g) == 0: return 90.0
    return math.degrees(math.atan2(math.cos(g) - K, math.sin(g)))

# angular radius of the min-elevation circle
def gamma_max(el_deg):
    t = math.tan(math.radians(el_deg))
    R, ph = math.hypot(1, t), math.atan(t)
    return math.degrees(math.acos(max(-1, min(1, K / R))) - ph)

GM = gamma_max(MIN_EL)

def footprint(sat_lon, n=180):
    """Circle of angular radius GM around the sub-satellite point, as lon/lat ring."""
    ring = []
    for i in range(n + 1):
        az = 2 * math.pi * i / n
        g = math.radians(GM)
        lat = math.asin(math.sin(g) * math.cos(az))                 # sub-sat lat = 0
        lon = math.atan2(math.sin(az) * math.sin(g), math.cos(g))
        ring.append([round(math.degrees(lon) + sat_lon, 3), round(math.degrees(lat), 3)])
    return ring

MARKETS = {
    "Beirut": (33.89, 35.50),   "Kuwait City": (29.38, 47.98), "Cairo": (30.04, 31.24),
    "Dubai": (25.20, 55.27),    "Riyadh": (24.71, 46.68),      "London": (51.51, -0.13),
    "Lagos": (6.52, 3.38),      "Singapore": (1.35, 103.82),   "Sydney": (-33.87, 151.21),
    "New York": (40.71, -74.01),
}

feats, rows = [], []
for name, lon, band in FLEET:
    feats.append({"type":"Feature",
                  "properties":{"satellite":name,"lon":lon,"band":band,"min_elevation":MIN_EL},
                  "geometry":{"type":"Polygon","coordinates":[footprint(lon)]}})
    rows.append((name, lon, band, {m: round(elevation(*c, lon), 1) for m, c in MARKETS.items()}))

json.dump({"type":"FeatureCollection","features":feats},
          open("coverage.geojson","w"))

print(f"min-elevation {MIN_EL}deg -> footprint angular radius {GM:.2f}deg")
print(f"wrote coverage.geojson: {len(feats)} footprints\n")

hdr = f"{'satellite':20}{'lon':>7} {'band':6}" + "".join(f"{m[:9]:>10}" for m in MARKETS)
print(hdr); print("-" * len(hdr))
for name, lon, band, els in rows:
    cells = "".join(f"{(str(v) if v >= MIN_EL else '  --'):>10}" for v in els.values())
    print(f"{name:20}{lon:>7.1f} {band:6}" + cells)

print("\nper-market: how many of SABA's 18 birds are usable (elev >= 10deg)")
for m in MARKETS:
    n = sum(1 for _,_,_,els in rows if els[m] >= MIN_EL)
    print(f"  {m:14} {n:2}/18  {'#' * n}")
