# Technical Summary — Experiment Reports

**AI Racing League — Go full speed with IBM Bob** · Yarará Team · Solo Entry

---

## File Reference

| File | Format | Contents |
|---|---|---|
| `experiment-list.md` | Markdown | 39 experiments · hypothesis · code change · assessment |
| `results_notes.md` | Markdown | Per-experiment telemetry observations · failure diagnosis · next step |
| `FIRSTLAP.md` | Markdown | Baseline snapshot · first successful lap record |
| `lap_data.csv.zip` | CSV (zipped) | Step-level telemetry — ~50 rows/second per run |
| `lap_summary.csv.zip` | CSV (zipped) | Per-lap summary across all 39 experiments |

---

## lap_summary.csv — Schema

```
timestamp          ISO-8601 timestamp of the run
run_id             UUID identifying a single script invocation
experiment_id      Human-readable experiment label (e.g. exp32_restore_exp17_base)
lap_id             Sequential lap number within the run (0 = warmup, 1+ = flying)
lap_status         warmup | flying | partial
sim_lap_time_s     TORCS lastLapTime (flying laps) or curLapTime at cap (partial)
max_speed_kmh      Maximum speedX recorded during the lap
final_damage       TORCS damage counter at lap end
completion_reason  race_completed | maxsteps_or_shutdown | keyboard_interrupt
```

---

## lap_data.csv — Schema

```
run_id             UUID (matches lap_summary.csv)
lap_id             Lap number (matches lap_summary.csv)
lap_status         warmup | flying | partial
step               Step counter (50 Hz)
distFromStart      metres from start line
curLapTime         TORCS current lap timer (s)
speedX             Longitudinal speed (km/h)
speedY             Lateral speed (km/h)
speedZ             Vertical speed (km/h)
steer              Steering output [−1, 1]
accel              Throttle output [0, 1]
brake              Brake output [0, 1]
gear               Gear selected [1–6]
trackPos           Lateral position [−1 = left edge, +1 = right edge]
track_min          Minimum value across all 19 track beams (m)
track_0..track_18  Individual beam distances (m) — angles −90° to +90°
wheelSpinVel_0..3  Wheel angular velocities (rad/s)
damage             TORCS damage counter
fuel               Remaining fuel
rpm                Engine RPM
angle              Car yaw relative to track axis (rad)
z                  Car height above ground (m)
```

---

## All 39 Experiments — Quick Reference

| Exp | ID | Lap Time | Max Speed | Damage | Status |
|---|---|---|---|---|---|
| 0 | `baseline_v2` | 149.49 s | ~121 km/h | 0 | ✅ completed |
| 1 | `exp01_steer_gain_10` | 153.14 s | 121.2 km/h | 0 | ✅ completed |
| 2 | `exp02_center_gain_020` | 153.14 s | 114.2 km/h | 0 | ✅ completed |
| 3 | `exp03_target_speed_150` | — | 171.0 km/h | 99 | ❌ crash |
| 4 | `exp04_brake_dist_30` | 160.22 s | 170.3 km/h | 0 | ✅ completed |
| 5 | `exp05_brake_speed_80` | 151.37 s | 172.6 km/h | 0 | ✅ completed |
| 6 | `exp06_proportional_brake` | 133.99 s | 171.4 km/h | 0 | ✅ **first fast clean lap** |
| 7 | `exp07_corner_aware_speed` | 168.12 s | 170.4 km/h | 0 | ✅ regression |
| 8 | `exp08_corner_speed_floor` | 137.12 s | 171.9 km/h | 1 | ✅ recovery |
| 9 | `exp09_ceiling_160` | 133.52 s | 177.7 km/h | 2 | ✅ **new best** |
| 10 | `exp10_throttle_ramp_02` | 135.42 s | 171.3 km/h | 18 | ⚠️ damage spike |
| 11 | `exp11_center_gain_015` | 127.02 s | 171.5 km/h | 39 | ⚠️ **new best / high damage** |
| 12 | `exp12_angle_gain_8` | — | 170.9 km/h | 77 | ❌ crash |
| 13 | `exp13_multibeam_brake` | 124.09 s | 171.3 km/h | 0 | ✅ **new best · 0 damage** |
| 14 | `exp14_brake_ref_170` | 130.81 s | 171.5 km/h | 90 | ❌ regression |
| 15 | `exp15_brake_dist_80` | 134.10 s | 171.2 km/h | 24 | ⚠️ regression |
| 16 | `exp16_ceiling_180` | 132.482 s | 186.985 km/h | 0 | ✅ new best then |
| 17 | `exp17_brake_100m_quadratic` | 122.862 s | 185.9 km/h | 20 | ✅ **new best (+26.6 s vs baseline)** |
| 18 | `exp18_throttle_suppress_100m` | 132.124 s | 186.750 km/h | 41 | ❌ regression |
| 19 | `exp19_narrow_throttle_beam` | 127.522 s | 187.537 km/h | 25 | ✅ recovery |
| 20 | `exp20_ceiling_200` | 126.452 s | 205.730 km/h | 22 | ✅ marginal |
| 21 | `exp21_brake_120m` | 128.442 s | 204.516 km/h | 19 | ⚠️ regression |
| 22 | `exp22_brake_twostage` | 139.764 s | 196.724 km/h | 13 | ❌ worst completed |
| 23 | `exp23_quadratic_tcs_gate` | 126.328 s | 205.625 km/h | 33 | ✅ recovery |
| 24 | `exp24_ceiling_250` | — (crash) | 209.550 km/h | 21 | ❌ crash |
| 25 | `exp25_brake_dist_160` | ~125.2 s (cap) | 196.297 km/h | 26 | ⏱️ step cap |
| 26 | `exp26_suppress_160` | ~130.0 s (cap) | 193.718 km/h | 23 | ⏱️ step cap |
| 27 | `exp27_brake_cubic_dist` | 129.218 s | 191.325 km/h | 21 | ✅ completed |
| 28 | `exp28_unified_140` | ~128.1 s (cap) | 193.220 km/h | 27 | ⏱️ step cap |
| 29 | `exp29_throttle_ramp_03` | ~125.6 s (cap) | 198.935 km/h | 24 | ⏱️ step cap |
| 30 | `exp30_zone_brake` | 144.206 s | 195.244 km/h | 93 | ❌ rejected |
| 31 | `exp31_brake_180m` | — (cap) | 181.781 km/h | 26 | ⏱️ step cap |
| 32 | `exp32_restore_exp17_base` | **121.652 s** | **187.532 km/h** | **19** | ✅ **ALL-TIME BEST** |
| 33 | `exp33_suppress_100m` | 124.618 s | 187.314 km/h | 20 | ✅ slight regression |
| 34 | `exp34_zone_centre_gain` | 122.654 s | 186.743 km/h | 23 | ✅ near-best |
| 35 | `exp35_sensor_90deg` | 123.1 s | 180.3 km/h | 21 | ✅ diagnostic |
| 36 | `exp36_zone_speed_map` | 148.3 s | 174.8 km/h | 0 | ✅ **first 4-lap 0-damage** |
| 37 | `exp37_trail_brake` | 147.1 s | 175.9 km/h | 0 | ✅ improvement |
| 38 | `exp38_racing_line` | 143.7 s | 176.2 km/h | 0 | ✅ improvement |
| 39 | `exp39_steer_turn_bias` | 148.2 s | 175.6 km/h | 0 | ✅ initial regression |

---

## Telemetry Fix Log

Four telemetry corrections were made during the project (no driving logic affected):

| Fix | Change | Trigger |
|---|---|---|
| Fix 1 | `LAP_WRAP_THRESHOLD` 100 m → 200 m | Car at 188 km/h skipped finish line in one step |
| Fix 2 | `LAP_WRAP_THRESHOLD` 200 m → 400 m | Same problem at 204 km/h |
| Fix 3 | `maxSteps` 100k→200k · threshold 400→500 m · guard 500→1000 m | Step-cap overruns at 250 km/h target |
| Fix 4 | CSV routing to `telemetry/` · `_open_csv_new` · lap-counter deferral · flush ordering · server-end guard | Structural CSV deficiencies; lap crossing step misattributed to next lap |

---

## Key Insights from the Data

1. **The brake is more important than the throttle.** Every major lap time gain came
   from a braking improvement. The single biggest jump (Exp 6, −17 s) replaced binary
   with proportional braking.

2. **Sensor geometry matters.** The chicane crash (pre-Exp 13) was invisible to a single
   forward beam. The multi-beam minimum fixed it without changing any speed targets.

3. **The best configuration was not the most recent.** Exp 32 (the best lap) restored
   parameters from Exp 17, 15 experiments earlier. Incremental changes can obscure the
   gains of prior discoveries.

4. **Telemetry was essential.** Four separate telemetry bugs (LAP_WRAP_THRESHOLD, step cap,
   CSV routing) were caught by reading the data rather than trusting the simulator UI.

---

<sub>Yarará Racing · AI Racing League · IBM Bob Competition</sub>
