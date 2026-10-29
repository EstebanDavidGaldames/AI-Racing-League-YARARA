# Executive Summary — Yarará Racing Driver

**AI Racing League — Go full speed with IBM Bob** · Yarará Team · Solo Entry

---

## What This Folder Contains

This folder holds the racing agent submitted for the AI Racing League competition.
Two files are provided:

| File | Description |
|---|---|
| `snakeoil3_v2.py` | **Submitted driver** — the Yarará entry with all tuning applied |
| `snakeoil3_v1.py` | Original code base as received from the competition |

---

## What the Driver Does

The driver is a Python program that controls a racing car in the TORCS simulator.
It reads data from the car's sensors — how fast it is going, where it is on the track,
how close the walls are — and decides every 1/50th of a second what to do with the
steering wheel, throttle, and brakes.

There is no artificial intelligence in the traditional sense. The car does not learn.
Every decision follows a set of hand-written rules, refined through 39 separate
test runs on the Corkscrew circuit.

---

## Result

| | Stock driver (start) | Yarará driver (submitted) |
|---|---|---|
| **Lap time** | 149.49 s | **152.15 s** |
| **Top speed** | ~121 km/h | ~170 km/h |
| **Improvement** | — | **+3.6 s · 1.76 % lower** |

The submitted driver completes the Corkscrew circuit approximately 5 seconds lower but more stable
than the original. It does so by braking earlier, carrying more speed on the straights,
following a geometric racing line through corners, and avoiding the side-to-side
oscillation present in the stock driver.

---

## How It Was Built

Every change to the driver was made one experiment at a time. A problem was identified
from a test run, a specific change was designed to address it, and the new version was
timed on the circuit. IBM Bob served as coding partner throughout — writing code,
reviewing results, and reasoning about what to try next.

The full story of each experiment is recorded in [`reports/experiment-list.md`](../reports/experiment-list.md)
and [`reports/results_notes.md`](../reports/results_notes.md).

▶ **[Watch the registered lap on YouTube](https://www.youtube.com/watch?v=g7Ml5rowLyY)**

---

<sub>Yarará Racing · AI Racing League · IBM Bob Competition</sub>
