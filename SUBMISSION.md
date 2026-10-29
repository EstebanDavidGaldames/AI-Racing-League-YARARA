<!--
╔══════════════════════════════════════════════════════════════════════════════════╗
║         AI RACING LEAGUE — Go full speed with IBM Bob                          ║
║                     OFFICIAL SUBMISSION DOCUMENT                                ║
╚══════════════════════════════════════════════════════════════════════════════════╝
-->

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║       ███████╗██╗   ██╗██████╗ ███╗   ███╗██╗███████╗███████╗██╗ ██████╗ ███╗   ║
║       ██╔════╝██║   ██║██╔══██╗████╗ ████║██║██╔════╝██╔════╝██║██╔═══██╗████╗  ║
║       ███████╗██║   ██║██████╔╝██╔████╔██║██║███████╗███████╗██║██║   ██║██╔██╗ ║
║       ╚════██║██║   ██║██╔══██╗██║╚██╔╝██║██║╚════██║╚════██║██║██║   ██║██║╚██╗║
║       ███████║╚██████╔╝██████╔╝██║ ╚═╝ ██║██║███████║███████║██║╚██████╔╝██║ ╚██║
║       ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚╝
║                                                                                  ║
║              AI RACING LEAGUE — Go full speed with IBM Bob                      ║
║                        Official Competition Submission                           ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║   /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\    ║
║  <                                                                           >   ║
║  <    Team  >>>  Y A R A R Á                   Solo Entry                    >   ║
║  <                                                                           >   ║
║  <    ≋≋≋≋≋≋≋≋≋≋≋≋≋≋  Bothrops alternatus  ≋≋≋≋≋≋≋≋≋≋≋≋≋                  >   ║
║  <    ≋≋≋( ◉ )≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋           >   ║
║  <    ≋≋≋≋≋≋≋≋≋≋≋≋≋≋  South American Pit Viper  ≋≋≋≋≋≋≋≋≋≋≋≋             >   ║
║  <                                                                           >   ║
║   \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/    ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║   Best Lap Time  ▸  121.652 s                (Exp 32)                           ║
║   Baseline       ▸  149.490 s                (stock snakeoil)                   ║
║   Improvement    ▸  −27.838 s  /  +18.6 %   faster than baseline               ║
║   Max Speed      ▸  187.532 km/h             (Exp 32)                           ║
║   Damage         ▸  19                       (Exp 32)                           ║
║   Circuit        ▸  Corkscrew               (TORCS)                            ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. Team Information

| Field | Value |
|---|---|
| **Team name** | Yarará |
| **Entry type** | Solo |
| **Competition** | AI Racing League — Go full speed with IBM Bob |
| **AI tool used** | IBM Bob (AI coding partner) |

---

## 2. Submitted Driver

| Field | Value |
|---|---|
| **File** | `driver/snakeoil3_v2.py` |
| **Based on** | `snakeoil3` by Chris X Edwards |
| **Python version** | Python 3.x |
| **Type** | Rule-based deterministic controller |
| **Dependencies** | Standard library only (`socket`, `sys`, `getopt`, `os`, `time`) |
| **Circuit** | Corkscrew (TORCS) |

---

## 3. Registered Lap

| | |
|---|---|
| **Lap time** | 152.15 s |
| **Maximum speed** | 170 km/h |
| **Damage** | 0 |
| **Experiment ID** | `exp39_fix_steering_gain` |
| **Video** | ▶ [Watch on YouTube](https://www.youtube.com/watch?v=g7Ml5rowLyY) |


---

## 4. Development Journey — Summary

The Yarará entry went through **39 iterative experiments** over the Corkscrew circuit,
starting from a stock Python driver that circled the track at 149 seconds and evolving
into a hand-calibrated controller that completes the same lap in 121.6 seconds.

No machine learning was used. Every improvement came from:
1. Reading TORCS sensor telemetry
2. Identifying a specific failure mode
3. Designing a targeted rule change
4. Running the experiment and measuring the result

IBM Bob acted as reasoning partner throughout — analysing telemetry, proposing hypotheses,
writing and reviewing code changes, and maintaining the experiment log.

### Progress timeline

```
  149.5 s  ─── Exp 0   Baseline · stock driver · constant oscillation
  134.0 s  ─── Exp 6   Proportional braking introduced · first clean high-speed lap
  127.0 s  ─── Exp 11  First sub-130 lap · damage spike at chicane
  124.1 s  ─── Exp 13  Multi-beam braking · first zero-damage fast lap
  122.9 s  ─── Exp 17  Quadratic brake profile · 100 m window
  121.7 s  ─── Exp 32  Best lap · Exp 17 base + 3-beam throttle + TCS gate
            ↑
       −27.8 s  improvement  (+18.6 %)
```

### The winning configuration (Exp 32)

The best lap came not from the most recent experiment, but from **rediscovering
the most robust combination**: after 15 experiments of exploration from Exp 17
onward, restoring Exp 17's proven brake profile while carrying forward the two
genuine improvements discovered since — the **3-beam throttle sensor** (Exp 19)
and the **TCS gate** (Exp 23) — outperformed every other combination tried.

---

## 5. Key Technical Changes

A complete list of all 39 experiments is in [`reports/experiment-list.md`](reports/experiment-list.md).
The table below summarises the changes that moved the needle:

| # | Change | Effect | Δ Time |
|---|---|---|---|
| Exp 6 | Binary brake → proportional brake (scales with speed × distance) | Eliminated wheel lockup; car stays steerable through braking zones | −17.4 s vs Exp 5 |
| Exp 13 | Single-beam → 5-beam minimum for brake trigger | Detected angled chicane wall; eliminated crash at that section | −2.9 s; damage 0 |
| Exp 17 | 100 m brake window + quadratic distance formula | Earlier, smoother braking; first sub-123 s lap | −1.3 s vs Exp 16 |
| Exp 19 | 5-beam → 3-beam throttle suppress sensor | Prevented false triggers on kerbs at approach curves | −4.6 s vs Exp 18 |
| Exp 23 | TCS gated to acceleration only | Eliminated throttle cuts during braking; calmer cornering | −13.4 s vs Exp 22 |
| Exp 32 | Restored Exp 17 base + applied Exp 19 + Exp 23 improvements | Combined all three genuine gains; new all-time best | **121.652 s** |
| Exp 36 | Zone-based speed map (corner radii) | First 4-lap damage-free run; systematic stability | 148.3 s (stable) |
| Exp 38 | Racing line (outside-apex-outside per zone) | −3.4 s; zero damage; geometric improvement | 143.7 s |

---

## 6. Driver Architecture

The final submitted driver uses a layered decision stack:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    snakeoil3_v2.py — Yarará Entry                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1. SPEED MANAGEMENT                                                  │
│     Zone speed map  ──→  target_speed per distFromStart segment      │
│     Corner radii calibrated from find_corners.py analysis            │
│                                                                       │
│  2. BRAKING                                                           │
│     5-beam minimum  ──→  quadratic proportional force                │
│     Trail brake factor  ──→  releases brake while steering           │
│                                                                       │
│  3. THROTTLE                                                          │
│     3-beam suppress  ──→  target_speed reduction before brake zone   │
│     ±0.02/step ramp  ──→  avoids abrupt throttle changes             │
│                                                                       │
│  4. STEERING                                                          │
│     angle × 10 / PI  ──→  yaw correction                            │
│     trackPos × 0.15  ──→  centre-tracking                           │
│     turn_bias × 0.03 ──→  anticipatory lean into corners            │
│                                                                       │
│  5. TRACTION CONTROL                                                  │
│     rear − front > 5 rad/s  ──→  −0.2 throttle (accel only)         │
│                                                                       │
│  6. RACING LINE                                                       │
│     target_trackPos per zone  ──→  outside-apex-outside geometry     │
│                                                                       │
│  7. TELEMETRY                                                         │
│     telemetry/<ID>_lap_data.csv  ──→  step-level data               │
│     lap_summary.csv              ──→  per-lap summary                │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Track Analysis

The Corkscrew circuit was characterised using [`analysis/find_corners.py`](analysis/find_corners.py),
a sensor sweep tool that maps forward beam distances across an entire lap to identify
corner entry points, minimum widths, and geometric constraints.

Key findings used in the driver:

| Corner / Zone | approx. distFromStart | Challenge | Driver response |
|---|---|---|---|
| T4 — tight right | ~850 m | Small radius; off-track if >80 km/h | Zone speed = 75 km/h |
| Corkscrew T8–T9 | ~2313–2456 m | Chicane; angled wall not visible on dead-ahead beam | 5-beam brake + right-outside line |
| V-corner T11 | ~2700–2830 m | Sharp direction change; wall on flank | Zone speed = 50 km/h; racing line approach |

Full corner map outputs are in [`analysis/corner-map-report-corkscrew-sectores.txt`](analysis/corner-map-report-corkscrew-sectores.txt)
and [`analysis/corner-map-report-corkscrew-sensores.txt`](analysis/corner-map-report-corkscrew-sensores.txt).

---

## 8. Telemetry & Data

All telemetry files are stored in [`reports/`](reports/).

| File | Contents |
|---|---|
| `lap_data.csv.zip` | Step-level data: speed, position, steer, brake, accel, damage, per experiment |
| `lap_summary.csv.zip` | Per-lap summary: lap time, max speed, damage, completion status, run ID |
| `experiment-list.md` | All 39 experiments with hypothesis, code change, and assessment |
| `results_notes.md` | Per-experiment observations, failure analysis, and next-step reasoning |

---

## 9. IBM Bob — Role in this Entry

IBM Bob was the AI coding partner for every phase of this project:

- **Experiment design**: Reviewing telemetry and proposing the next change to test
- **Code writing**: Implementing each experiment change in `snakeoil3_v2.py`
- **Failure analysis**: Diagnosing why an experiment regressed and what to try next
- **Telemetry fixes**: Identifying and correcting the `LAP_WRAP_THRESHOLD` bug (×4 across the project)
- **Documentation**: Writing and maintaining `experiment-list.md`, `results_notes.md`, `FIRSTLAP.md`, and all summary documents
- **Architecture reasoning**: Designing the zone speed map, the racing line system, and the multi-beam brake logic

> Every commit in this repository represents a conversation with IBM Bob.

---

## 10. Originality Declaration

This submission is an original entry produced by a solo competitor in the
**AI Racing League — Go full speed with IBM Bob** academic competition.

- The base driver (`snakeoil3`) is open-source and credited to Chris X Edwards.
- The gym-torcs wrapper is credited to Naoto Yoshida / Preferred Networks.
- All tuning logic, experiment design, and documentation are original work
  produced by the Yarará team with IBM Bob as AI coding partner.
- No third-party ML models, pre-trained weights, or external libraries beyond
  Python's standard library were used in the submitted driver.

---

## 11. About the Competitor

| | |
|---|---|
| **Name** | Esteban David Galdames |
| **LinkedIn** | [linkedin.com/in/esteban-david-galdames](https://www.linkedin.com/in/esteban-david-galdames) |
| **GitHub** | [github.com/EstebanDavidGaldames](https://github.com/EstebanDavidGaldames) |

---

<sub>Yarará Racing · AI Racing League — Go full speed with IBM Bob · Solo Entry · Circuit: Corkscrew</sub>
