# FIRSTLAP — Corkscrew Circuit: First Successful Lap

This document records the two changes made to `snakeoil3_v1.py` that enabled the car to complete
a full lap of the Corkscrew circuit without damage, along with a snapshot of all driving
characteristics at that point as a baseline for future tuning.

---

## Changes Made

### Change 1 — Reduced Target Speed: 300 → 100 km/h

**File:** `snakeoil3_v1.py`, line 537  
**Code before:**
```python
target_speed=300
```
**Code after:**
```python
target_speed=100
```

**In driving terms:**  
The original driver had been instructed to go flat-out at 300 km/h everywhere on the circuit —
straights, chicanes, and hairpins alike. On a road course like Corkscrew, no amount of steering
skill can keep a car on track when it is arriving at tight corners at motorway speeds with no
braking. Reducing the target to 100 km/h tells the driver to cruise at a safe, manageable pace.
The throttle logic already contains a built-in corner speed reducer: the faster the car is
steering, the more the effective target drops (by up to 50 km/h at full lock). At 100 km/h
this means the car targets as low as ~50 km/h through the tightest bends, which is within
safe cornering limits.

---

### Change 2 — Added Emergency Braking on Corner Approach

**File:** `snakeoil3_v1.py`, lines 550–554  
**Code added (no lines were removed or modified):**
```python
# Brake if a wall is closing in fast ahead
if S['track'][9] < 20 and S['speedX'] > 60:
    R['brake'] = 1.0
else:
    R['brake'] = 0.0
```

**In driving terms:**  
The original driver never touched the brake pedal at all. The only way the car slowed down was
by lifting off the throttle, which bleeds speed far too slowly (only 0.01 throttle per tick,
50 ticks per second) to make a significant difference before a corner. The new braking rule
gives the driver a simple instinct: **look straight ahead; if the track edge is less than
20 metres away and the car is still going faster than 60 km/h, stamp on the brakes fully**.
Below 60 km/h the brake is released — the car is already slow enough to steer through safely
without risk of stalling. This mimics the most fundamental motorsport driving technique:
brake hard and in a straight line before the corner, then carry the remaining speed through.

---

## Known Issues at This Baseline

These are behaviours that exist in the current working state and are candidates for the next
round of tuning:

| Issue | Cause | Driving Description |
|---|---|---|
| **Constant side-to-side weaving** | Steering angle gain is `15` — too sensitive | The driver overreacts to every small deviation, sawing at the wheel continuously instead of making smooth, measured corrections |
| **Sluggish corner exit acceleration** | Gear shifts happen too early (2nd at 50 km/h, etc.) | The engine is being asked to pull in too tall a gear before it has built up torque — the car feels lazy out of corners |
| **Slow overall lap time** | Target speed of 100 km/h is conservative | The car is not using the full potential of the straights |

---

## Driver Characteristics Snapshot — Baseline for Future Changes

The table below records every tunable parameter in `drive_example()` as it stands after the
first successful lap. Use this as the reference point before making any further modifications.

### Speed & Throttle

| Parameter | Current Value | Notes |
|---|---|---|
| Target speed | `100` km/h | Ceiling the driver aims for on straights |
| Throttle step up | `+0.01` per tick | How quickly the driver presses the gas |
| Throttle step down | `−0.01` per tick | How quickly the driver lifts off |
| Low-speed boost | `+1/(speedX+0.1)` when `speedX < 10` | Prevents stalling from rest |
| Corner speed reduction | `target − (steer × 50)` | Implicit: reduces target by up to 50 km/h at full lock |

### Braking

| Parameter | Current Value | Notes |
|---|---|---|
| Brake trigger distance | `< 20 metres` (front radar) | Brakes fire when wall ahead is within 20 m |
| Brake trigger speed | `> 60` km/h | Brakes only fire above this speed |
| Brake pressure | `1.0` (full) | No modulation — on or off |
| Brake release | `0.0` otherwise | Brake fully released when condition is not met |

### Steering

| Parameter | Current Value | Notes |
|---|---|---|
| Angle correction gain | `× 15 / PI` (~4.77) | How aggressively the car aligns its nose to the road |
| Centre-tracking gain | `× 0.10` | How firmly the car returns to the middle of the track |

### Traction Control

| Parameter | Current Value | Notes |
|---|---|---|
| Rear vs. front wheel spin threshold | `> 5` rad/s difference | Triggers throttle cut if rear wheels spin faster than fronts |
| Throttle cut on wheelspin | `−0.2` | Significant cut to recover grip |

### Automatic Gearbox

| Speed threshold | Gear selected |
|---|---|
| Any speed | 1st |
| > 50 km/h | 2nd |
| > 80 km/h | 3rd |
| > 110 km/h | 4th |
| > 140 km/h | 5th |
| > 170 km/h | 6th |

---

*Next recommended change: reduce the steering angle gain from `15` to `10` to eliminate the
side-to-side weaving, as this affects both stability and the effectiveness of the braking trigger.*
