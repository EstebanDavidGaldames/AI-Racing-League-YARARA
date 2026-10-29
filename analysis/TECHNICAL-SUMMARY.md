# Technical Summary — Track Analysis

**AI Racing League — Go full speed with IBM Bob** · Yarará Team · Solo Entry

---

## Tool: `find_corners.py`

`find_corners.py` is a passive analysis tool. It connects to TORCS as a normal driver
but instead of racing, it drives slowly and logs the full 19-beam sensor state at
every metre of the track.

### Inputs

- A running TORCS instance in practice mode on the Corkscrew circuit
- Optional: `-p PORT` to connect to a non-default port

### Outputs

- Console report segmented by corner (one block per identified narrowing zone)
- Two text files written to `analysis/`:

| File | Contents |
|---|---|
| `corner-map-report-corkscrew-sectores.txt` | Summary table: one row per sector, with minimum width and speed |
| `corner-map-report-corkscrew-sensores.txt` | Full raw sensor log: all 19 beam readings at each distance step |

### Algorithm

1. On each tick, records `distFromStart`, `speedX`, `trackPos`, and `track[0..18]`
2. Identifies "corner" as any consecutive stretch where the minimum of `track[7..11]`
   (the 5 forward-facing central beams) drops below a threshold
3. Groups consecutive tight steps into sectors and reports the minimum width,
   the distFromStart range, and the peak steering angle recorded

---

## Corkscrew Circuit Map — Key Zones

The following was derived from the sensor reports. All distances are `distFromStart`
in metres; widths are the minimum forward beam reading within each sector.

```
  ───────────────────────────────────────────────────────────────────────────────
  dist (m)     Sector          Min fwd (m)  Notes
  ───────────────────────────────────────────────────────────────────────────────
     0–  200   S/F straight    > 100        Long straight; full throttle
   200–  400   Left sweep      ~40–60       Gentle; 3-beam suppress fires at edges
   400–  800   Back section    > 60         Open; chicane-like layout
   800–  900   T4 right        ~18–25       Tightest single corner; radius ~20 m
               → min track sensor: 18 m (right edge closes fast)
   900– 1200   Exit + straight > 80         Speed recovery zone
  1200– 1800   Mixed curves    ~35–60       Undulating; brakes not needed
  1800– 2200   Long straight   > 100        Main acceleration zone
  2313– 2456   Corkscrew T8–9  ~15–30       Chicane: two direction changes in 143 m
               → wall is angled; dead-ahead beam misses it
               → 5-beam minimum required; multi-beam brake fix (Exp 13)
  2456– 2700   Post-chicane    > 60         Short recovery
  2700– 2830   V-corner T11    ~12–20       Sharpest geometry; reverse direction
               → track[9] underestimates; lateral beams critical
               → 50 km/h zone; outside approach in racing line
  2830– 3600   Return sweep    > 40         Gradual; sensor suppress fires on kerbs
               → reduced to 3-beam to prevent false triggers
  ───────────────────────────────────────────────────────────────────────────────
  Total length: ~3 605 m
```

---

## Sensor Array Reference

TORCS provides 19 range beams spanning −90° to +90° in 10° increments.
Index mapping (0-based):

```
Index   Angle   Role in this driver
  0     −90°    Right edge (lateral reference only)
  1     −80°
  2     −70°
  3     −60°
  4     −50°
  5     −40°
  6     −30°
  7     −20°    ┐
  8     −10°    │  5-beam brake window
  9       0°    │  (minimum used for braking trigger)
 10     +10°    │
 11     +20°    ┘
  8     −10°    ┐
  9       0°    │  3-beam throttle suppress window
 10     +10°    ┘  (narrow; avoids kerb false triggers)
 12     +30°
 13     +40°
 14     +50°
 15     +60°
 16     +70°
 17     +80°
 18     +90°    Left edge (lateral reference only)
```

The beam naming convention in TORCS is right-negative / left-positive
(same sign convention as `trackPos`).

---

## Tuning Card — Parameter Reference

`tuning-card.md` is the quick-reference for the submitted driver.
It lists every named constant in `drive_example()`, its current value,
what it physically controls, and the risk level of changing it.

Extracted key values at submission (Exp 32 configuration):

| Parameter | Value | File location |
|---|---|---|
| `target_speed` (default) | 180 km/h | `snakeoil3_v2.py` zone map |
| Zone speed — T4 | 75 km/h | Zone map |
| Zone speed — Corkscrew | 120 km/h | Zone map |
| Zone speed — V-corner | 50 km/h | Zone map |
| `brake_dist` | 100 m | Braking block |
| `ref` (brake calibration) | 180 km/h | Braking block |
| `suppress_dist` | 80 m | Throttle suppress block |
| Steering angle gain | 10 / PI | Steering block |
| Centre-tracking gain | 0.15 | Steering block |
| Turn bias coefficient | 0.03 | Steering block |
| Throttle ramp | ±0.02 / step | Throttle block |
| TCS threshold | 5 rad/s | TCS block |
| TCS cut | −0.2 | TCS block |
| Trail brake factor | 0.6 | Trail brake block |

---

<sub>Yarará Racing · AI Racing League · IBM Bob Competition</sub>
