# Executive Summary — Experiment Reports

**AI Racing League — Go full speed with IBM Bob** · Yarará Team · Solo Entry

---

## What This Folder Contains

This folder holds the complete experimental record of the Yarará entry — all data
collected and all observations written during the tuning process.

| File | Description |
|---|---|
| `experiment-list.md` | All 39 experiments: the change made, the reasoning, and the predicted outcome |
| `results_notes.md` | What actually happened in each experiment: lap time, damage, observations, next step |
| `FIRSTLAP.md` | The milestone document for the first completed lap on Corkscrew |
| `lap_data.csv.rar` | Step-level telemetry — one row per 1/50th second, per run |
| `lap_summary.csv.rar` | One row per completed (or attempted) lap across all 39 experiments |

---

## Story in Numbers

Starting from a stock driver that completed the Corkscrew circuit in **149.49 seconds**,
39 experiments were run over several weeks. Each experiment changed one thing,
measured the result, and informed the next decision.

| Metric | Baseline | Best Result | Improvement |
|---|---|---|---|
| Lap time | 149.49 s | **121.65 s** (Exp 32) | −27.8 s |
| Top speed | ~121 km/h | 187.5 km/h (Exp 32) | +66.5 km/h |
| First clean lap at speed | — | Exp 13 (124.1 s, 0 damage) | — |
| First 4-lap damage-free run | — | Exp 36 (148.3 s steady) | — |

The best single lap came from Experiment 32 — not the most recent experiment,
but the most robust configuration: the Exp 17 brake profile combined with the
3-beam throttle sensor (Exp 19) and the TCS gate (Exp 23).

---

## What the Data Shows

The `lap_data.csv` files capture every sensor reading and every control output
for every step of every run. They were used to diagnose why experiments failed —
for example, detecting that the car was going off-track at a specific corner
even when the lap completed without a crash.

The `lap_summary.csv` file gives a quick view of how each experiment performed:
lap time, maximum speed, damage accumulated, and whether the run completed normally.

---

<sub>Yarará Racing · AI Racing League · IBM Bob Competition</sub>
