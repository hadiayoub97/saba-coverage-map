# SABA — orbital fleet coverage map

Interactive coverage tool built on the fleet listed at https://www.sabaworld.com/satellite
(18 satellites, 10 operators). Pick a market; see which slots it can reach and how high
above the horizon each sits.

## Run
    python3 -m http.server 8940
    open http://127.0.0.1:8940/

## Files
    index.html            the whole app — no dependencies, no build step
    data/fleet.json       satellites + markets. EDIT HERE to revise the fleet.
    data/world.json       coastlines (Natural Earth 110m, public domain)
    coverage.py           independent reference model; regenerates coverage.geojson
    verify.js             cross-checks the browser against coverage.py (10/10 markets)
    shot.js               screenshots

## What the numbers mean
Elevation angle is computed from orbital longitude alone — pure geostationary geometry,
no proprietary operator data. A slot counts as reachable above 10° elevation, below which
rain fade and ground obstruction make service unreliable.

**These are line-of-sight footprints, not beam footprints.** Real beams are shaped and
narrower: the map will show a satellite as reachable from a location its actual beam does
not serve. Layering true EIRP contours needs datasheets (KMZ/GeoJSON) from the operators.

## Data caveat
The fleet list is reproduced as published. Several entries appear dated — worth verifying
before this goes public.
