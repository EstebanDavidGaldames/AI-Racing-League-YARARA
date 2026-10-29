# Executive Summary — Track Analysis

**AI Racing League — Go full speed with IBM Bob** · Yarará Team · Solo Entry

---

## What This Folder Contains

This folder holds the tools and outputs used to understand the Corkscrew circuit
before tuning the driver.

| File | Description |
|---|---|
| `find_corners.py` | Tool that drives a slow lap and maps every sensor reading to a track position |
| `tuning-card.md` | Quick reference card for every tunable value in the driver |
| `corner-map-report-corkscrew-sectores.txt` | Circuit divided into sectors with speed and width data |
| `corner-map-report-corkscrew-sensores.txt` | Raw sensor readings mapped to distance from start |

---

## Why This Matters

A racing driver needs to know the circuit before they can drive it fast.
`find_corners.py` is the equivalent of a slow reconnaissance lap — it logs what the
car's sensors see at every metre of the track, identifying where corners are,
how tight they are, and how close the walls are on each side.

This information was used to build the **zone speed map** in the submitted driver:
a list of track segments with a speed limit calibrated to the physical radius
of each corner. Without this data, the speed limits would have been set by trial
and error on each individual corner. With it, they were set with geometric intent.

---

## Key Findings

Three sections of the Corkscrew circuit required special treatment:

| Section | Distance | Finding | Driver response |
|---|---|---|---|
| Tight right-hander | ~850 m | Car goes off-track above 80 km/h | Speed zone: 75 km/h |
| Chicane (Corkscrew proper) | ~2313–2456 m | Angled wall not visible on forward beam | 5-beam brake; specific racing line |
| V-corner | ~2700–2830 m | Sharp direction reversal; lateral wall exposure | Speed zone: 50 km/h; outside approach |

---

## The Tuning Card

`tuning-card.md` lists every adjustable parameter in the driver, what it controls,
and what happens if you raise or lower it. It was the reference document used
throughout the 39-experiment tuning process.

---

<sub>Yarará Racing · AI Racing League · IBM Bob Competition</sub>
