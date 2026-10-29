# Technical Summary — Yarará Racing Driver

**AI Racing League — Go full speed with IBM Bob** · Yarará Team · Solo Entry

---

## Files

| File | Role | Base |
|---|---|---|
| `snakeoil3_v2.py` | **Submitted driver** (Yarará entry, all modifications applied) | `snakeoil3` by Chris X Edwards |
| `snakeoil3_v1.py` | Original competition code base (unmodified reference) | IBM competition materials |

---

## Driver Entry Point

The driver runs as a standalone Python 3 script. No imports beyond the standard library.

```bash
python snakeoil3_v2.py [-H host] [-p port] [-e experiment_id] [-s stage]
```

The main loop calls `drive_example(state, response)` at 50 Hz (every TORCS step),
reads sensor state from `state['S'].d`, writes control outputs to `state['R'].d`,
and logs telemetry to CSV.

---

## Control Architecture

### 1. Speed Management — Zone Speed Map

A lookup table indexed by `distFromStart` sets `target_speed` for each track segment.
Zones were calibrated from `analysis/find_corners.py` output.

```python
# Simplified structure
if 800 <= dist < 900:
    target_speed = 75      # T4 tight right — radius-constrained
elif 2313 <= dist < 2456:
    target_speed = 120     # chicane approach
elif 2700 <= dist < 2830:
    target_speed = 50      # V-corner
else:
    target_speed = 180     # open road
```

### 2. Braking — Quadratic Proportional Brake

Braking force is a continuous function of forward distance and car speed.
Uses the minimum reading across 5 central forward-facing beams
(`track[7]` through `track[11]`) to detect angled walls (e.g. chicane entry).

```python
d_min = min(S['track'][7:12])     # 5-beam minimum
speed_factor = clip(speedX / ref, 0, 1)
dist_factor  = clip(1 - d_min / brake_dist, 0, 1)
R['brake']   = speed_factor**2 * dist_factor**2
```

Key parameters:

| Parameter | Value | Notes |
|---|---|---|
| `brake_dist` | 100 m | Trigger window |
| `ref` | 180 km/h | Speed calibration reference |
| Exponent | 2 (quadratic) | Smooth ramp; no lockup |

### 3. Trail Brake

Brake force is multiplied by `1 − trail_factor × |steer|` to reduce braking
while the car is turning — preventing front-wheel lockup through corner entry.

```python
trail_factor = 0.6
R['brake'] *= (1 - trail_factor * abs(R['steer']))
```

### 4. Throttle Management

Throttle ramps at ±0.02 per step (calibrated in Exp 28).
A 3-beam narrow suppress sensor (`track[8:11]`, ~±1° arc) reduces `target_speed`
when a wall is within 80 m on the approach, lifting off before the brake zone.

```python
if min(S['track'][8:11]) < suppress_dist and speedX > suppress_floor:
    target_speed = max(suppress_min, target_speed * suppress_factor)
```

The 3-beam sensor (vs the 5-beam used for braking) prevents false triggers
on kerbs and barriers visible from curved approach sections (failure mode of Exp 18).

### 5. Steering

Three additive components:

| Component | Formula | Purpose |
|---|---|---|
| Angle correction | `angle × 10 / PI` | Aligns car nose to road direction |
| Centre tracking | `−trackPos × 0.15` | Pulls car toward track centre |
| Turn bias | `(track[10] − track[8]) × 0.03` | Anticipatory lean into corner |

The turn bias uses the asymmetry between the ±1° side beams to detect the start
of a curve and pre-steer before the yaw error builds.

### 6. Traction Control

```python
if R['brake'] < 0.05:   # TCS gate — fires only during acceleration
    wheel_diff = mean(rear_spin) - mean(front_spin)
    if wheel_diff > 5.0:
        R['accel'] -= 0.2
```

The `R['brake'] < 0.05` gate (introduced in Exp 23) prevents the TCS from cutting
throttle during braking — a failure mode that caused simultaneous throttle+brake
oscillation and was responsible for 13.4 s of lap time regression in Exp 22.

### 7. Automatic Gearbox

Rule-based sequential gearbox based on `speedX` thresholds:

| Speed | Gear |
|---|---|
| Any | 1st |
| > 50 km/h | 2nd |
| > 80 km/h | 3rd |
| > 110 km/h | 4th |
| > 140 km/h | 5th |
| > 170 km/h | 6th |

### 8. Racing Line

`target_trackPos` varies by zone. Each zone pushes the car to the outside of the
approaching corner, then to the inside of the apex, following the classic
outside-apex-outside (OAO) geometric line that minimises the arc radius driven.

```python
# Example zone entries (distFromStart ranges)
if 800 <= dist < 850:   target_tp = -0.4   # approach T4 from left (outside)
if 850 <= dist < 900:   target_tp =  0.4   # apex T4 (inside right)
if 900 <= dist < 950:   target_tp =  0.0   # exit T4 to centre
```

---

## Telemetry System

Per-step CSV (`telemetry/<EXPERIMENT_ID>_lap_data.csv`) — columns:

```
run_id, lap_id, lap_status, step,
distFromStart, curLapTime, speedX, speedY, speedZ,
steer, accel, brake, gear, trackPos,
track_min, track[0..18], wheelSpinVel[0..3],
damage, fuel, rpm, angle, z
```

Per-lap CSV (`lap_summary.csv`) — columns:

```
timestamp, run_id, experiment_id, lap_id, lap_status,
sim_lap_time_s, max_speed_kmh, final_damage, completion_reason
```

### Telemetry constants (current values)

| Constant | Value | Notes |
|---|---|---|
| `maxSteps` | 200 000 | Steps before forced shutdown (~4 000 s) |
| `LAP_WRAP_THRESHOLD` | 500 m | `distFromStart` window for finish-line detection |
| `LAP_MIN_DIST_PREV` | 1 000 m | Minimum distance before a lap crossing is counted |

---

## Experiment Genealogy of the Submitted Driver

The submitted driver (`exp39_fix_steering_gain`) inherits from:

```
Exp 0  — baseline (snakeoil3_v1 → v2 port)
  └─ Exp 6  — proportional brake
       └─ Exp 13 — 5-beam brake trigger
            └─ Exp 17 — 100 m quadratic brake (reference = 180)  ← BRAKE BASE
                 └─ Exp 19 — 3-beam throttle suppress  ← THROTTLE SENSOR
                      └─ Exp 23 — TCS gate (accel only)  ← TCS FIX
                           └─ Exp 32 — restore Exp 17 + carry Exp 19 + Exp 23
                                        ═══  121.652 s · best lap  ═══
```

---

<sub>Yarará Racing · AI Racing League · IBM Bob Competition</sub>
