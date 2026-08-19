# SABA — site prototype

Two pages, no build step, no dependencies.

    index.html      homepage — mirrors the section structure of sabaworld.com,
                    with a scroll-driven globe on "Major satellite distribution"
    coverage.html   interactive coverage tool: pick a market, see which of the
                    18 orbital slots reach it and at what elevation

## Run
    python3 -m http.server 8940
    open http://127.0.0.1:8940/

## Files
    data/fleet.json       satellites + markets. EDIT HERE to revise the fleet;
                          both pages read from it.
    data/world.json       coastlines (Natural Earth 110m, public domain)
    coverage.py           independent reference model; regenerates coverage.geojson
    verify.js             cross-checks the browser against coverage.py (10/10 markets)

## What the numbers mean
Elevation angle is computed from orbital longitude alone — pure geostationary
geometry, no proprietary operator data. A slot counts as reachable above 10°
elevation, below which rain fade and ground obstruction make service unreliable.

The homepage globe shades each point by how many of the 18 slots reach it, from a
1° grid computed once at load. The counts under each region are computed, never
written by hand.

**These are line-of-sight footprints, not beam footprints.** Real beams are shaped
and narrower: the map will show a satellite as reachable from a location its actual
beam does not serve. Layering true EIRP contours needs datasheets (KMZ/GeoJSON)
from the operators.

## Data caveat
The fleet list is reproduced as published on sabaworld.com/satellite. Several
entries appear dated — worth verifying before this goes public.
