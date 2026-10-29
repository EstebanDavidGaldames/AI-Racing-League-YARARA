# Experiment List — Corkscrew Circuit

---

### Experiment 1 — Reduce Steering Angle Gain: `15` → `10`
**ID:** `exp01_steer_gain_10`

**Line changed:** `snakeoil3_v2.py:545`
```python
# Before
R['steer'] = S['angle'] * 15 / PI
# After
R['steer'] = S['angle'] * 10 / PI
```

| | Assessment |
|---|---|
| **Why** | The gain of `15` makes the driver saw at the wheel every step — overcorrecting left, then right, in a continuous oscillation. Dropping to `10` gives proportional, settled corrections like a driver making deliberate inputs |
| **1. Likely effect on lap time** | Marginal improvement (1–3 s) — smoother line through corners reduces scrubbing speed. The main gain is in stability, not raw time |
| **2. Likely effect on damage/control** | Significant improvement in control. Weaving should nearly disappear. Wall contact risk drops because the car stops bouncing between kerbs |
| **3. Where you'll notice it** | Everywhere — the weaving is constant on this circuit. Most visible on the back straight and the long sweeping sections |
| **4. What could make the prediction wrong** | If the track geometry demands sharper snap corrections (e.g. a blind crest), a gain of `10` might cause the car to react too slowly and drift wide. On Corkscrew specifically this is unlikely |

---

### Experiment 2 — Raise Centre-Tracking Gain: `0.10` → `0.20`
**ID:** `exp02_center_gain_020`

**Line changed:** `snakeoil3_v2.py:547`
```python
# Before
R['steer'] -= S['trackPos'] * 0.10
# After
R['steer'] -= S['trackPos'] * 0.20
```

| | Assessment |
|---|---|
| **Why** | After reducing the angle gain, the car is less likely to self-correct strongly when it drifts toward an edge. Doubling the centre-tracking gain gives the car firmer authority to pull back to the middle |
| **1. Likely effect on lap time** | Neutral to slight improvement — the car spends less time near the edges and more time on a consistent line |
| **2. Likely effect on damage/control** | Reduced wall-grazing incidents. The car recovers its position more decisively after a perturbation |
| **3. Where you'll notice it** | On corner exits where the car tends to run wide, and on the straights where it currently wanders |
| **4. What could make the prediction wrong** | If combined with the new angle gain of `10`, the two corrections might fight each other at speed and create a new (lower-frequency) oscillation. If this happens, reduce back to `0.15` |

---

### Experiment 3 — Raise Target Speed: `100` → `150` km/h
**ID:** `exp03_target_speed_150`

**Line changed:** `snakeoil3_v2.py:542`
```python
# Before
target_speed = 100
# After
target_speed = 150
```

| | Assessment |
|---|---|
| **Why** | The car is currently crawling. With stability fixed, the most direct path to a faster lap time is a higher straight-line speed ceiling. `150` is a modest first step — it leaves 50 km/h of headroom before the original danger zone |
| **1. Likely effect on lap time** | Large improvement — potentially 15–30 s depending on straight length. The car will now actually accelerate on the main straight |
| **2. Likely effect on damage/control** | Medium risk. The braking system (20 m wall trigger) was calibrated for 100 km/h. At 150 km/h the car carries more kinetic energy and 20 m may not be enough stopping distance. Watch braking points carefully |
| **3. Where you'll notice it** | Main straight and any section longer than ~150 m. The car will reach higher speeds and spend more time at the speed ceiling |
| **4. What could make the prediction wrong** | The corner speed reduction (`steer × 50`) still caps cornering speed — at full lock the effective target is `150 − 50 = 100` km/h. If the corners were already survived at 100 km/h, they should still be safe. However, approach speed into braking zones increases, which may cause late-braking incidents |

---

### Experiment 4 — Extend Brake Trigger Distance: `20` → `30` m
**ID:** `exp04_brake_dist_30`

**Line changed:** `snakeoil3_v2.py:556`
```python
# Before
if S['track'][9] < 20 and S['speedX'] > 60:
# After
if S['track'][9] < 30 and S['speedX'] > 60:
```

| | Assessment |
|---|---|
| **Why** | At 150 km/h the car travels ~41 m/s. Braking from 20 m at full force may not shed enough speed before the corner. Moving the trigger to 30 m gives the car an extra 10 m — roughly 0.24 s — of braking time |
| **1. Likely effect on lap time** | Slight negative impact (0–2 s) — the car enters corners more slowly. But this is necessary to avoid damage |
| **2. Likely effect on damage/control** | Improved safety margin. Wall contact on corner entry should reduce or disappear |
| **3. Where you'll notice it** | At the end of the main straight and any section where the car is still close to 150 km/h approaching a tight corner |
| **4. What could make the prediction wrong** | If the `track[9]` beam (dead ahead, 0°) is not perfectly aligned with the braking point on Corkscrew's curved approaches, the beam may read a long distance even when a corner barrier is close at an angle. In that case the trigger fires later than expected |

---

### Experiment 5 — Raise Brake Trigger Speed: `60` → `80` km/h
**ID:** `exp05_brake_speed_80`

**Line changed:** `snakeoil3_v2.py:556`
```python
# Before
if S['track'][9] < 30 and S['speedX'] > 60:
# After
if S['track'][9] < 30 and S['speedX'] > 80:
```

| | Assessment |
|---|---|
| **Why** | Currently the brake releases below 60 km/h. If the car is still travelling at 75 km/h and approaching a wall, the brakes are off. Raising the release threshold to 80 km/h means the car brakes through to a slower, more controlled corner entry speed |
| **1. Likely effect on lap time** | Marginal negative (0–1 s) on slower corners. Positive safety impact allows keeping the speed gains from Exp 3 |
| **2. Likely effect on damage/control** | Better corner entry control — the car arrives at the apex at a lower, more predictable speed |
| **3. Where you'll notice it** | Tight hairpins and slow chicanes where the car currently releases the brake while still moving too fast |
| **4. What could make the prediction wrong** | On very slow sections, raising this threshold could cause the car to over-brake and lose too much speed unnecessarily, which the throttle ramp (only `+0.01/tick`) will be slow to recover |

---

### Experiment 6 — Proportional Braking: binary `1.0` → scaled by proximity and speed
**ID:** `exp06_proportional_brake`

**Lines changed:** `snakeoil3_v2.py:556–557`
```python
# Before
if S['track'][9] < 30 and S['speedX'] > 80:
    R['brake'] = 1.0
# After
if S['track'][9] < 60 and S['speedX'] > 80:
    R['brake'] = clip((60 - S['track'][9]) / 60 * (S['speedX'] / 150), 0, 1)
```

| | Assessment |
|---|---|
| **Why** | The binary `brake = 1.0` causes immediate wheel lockup, eliminating steering authority exactly when the driver needs it most. A force that scales with proximity (how close the wall is) and speed (how much energy the car carries) keeps some grip available for steering corrections throughout the entire braking zone |
| **1. Likely effect on lap time** | Moderate improvement — the car stays on track through corners instead of veering off and losing large chunks of time recovering. A clean line through the braking zone should outweigh the slightly lower peak brake force |
| **2. Likely effect on damage/control** | Significant improvement in control. Steering remains partially functional during braking, allowing the car to follow the corner rather than ploughing straight ahead. Wall contact and off-track excursions should reduce |
| **3. Where you'll notice it** | Every braking zone — particularly the end of the main straight and any corner approached above 100 km/h. The car will appear to slow more gradually and track the road edge rather than cutting straight across it |
| **4. What could make the prediction wrong** | If the Corkscrew's tightest corners require more deceleration than the graduated formula provides at the moment of turn-in, the car may still run wide. The formula is anchored to 150 km/h as the reference speed; at the current 172 km/h peak, the scale factor can exceed 1.0 briefly, but `clip()` caps it — meaning the effective braking window is already slightly shorter than intended at maximum speed |

---

### Experiment 7 — Corner-Aware Target Speed
**ID:** `exp07_corner_aware_speed`

**Lines changed:** `snakeoil3_v2.py:542–547` (replaces single `target_speed=150` line)
```python
# Before
target_speed = 150
# After
# Corner-aware target speed: back off proportionally as space ahead shrinks
forward = S['track'][9]
if forward < 80:
    target_speed = 150 * (forward / 80)
else:
    target_speed = 150
```

| | Assessment |
|---|---|
| **Why** | Even with proportional braking, the car builds to 150 km/h regardless of what lies ahead. When forward clearance is short, the car arrives at the braking zone carrying more energy than the brake can shed in time, causing it to drift wide. Reducing `target_speed` proportionally as the wall closes in means the car naturally rolls off the throttle before the brake even needs to fire — combining lift-and-coast with braking rather than relying on braking alone |
| **1. Likely effect on lap time** | Moderate improvement — the car will take tighter lines through corners, spending less time off-track and recovering. On straights with long forward clearance (>80 m) behaviour is unchanged, so top speed is preserved |
| **2. Likely effect on damage/control** | Improved corner entry control. The car approaches tight sections already slower, so the proportional brake has less work to do and the car remains more composed through the apex |
| **3. Where you'll notice it** | Tight corners and blind crests where the forward beam reads short distance — the car will visibly lift before braking, arriving at turn-in at a more controlled speed. The back straight, where forward clearance is long, will be unaffected |
| **4. What could make the prediction wrong** | The `track[9]` beam points dead ahead (0°). On a curved approach the wall appears in the side beams before the forward beam reads it — so the car may still be at full throttle when it is already in the corner. If this happens the forward beam alone is insufficient and a minimum across several forward-facing beams would be needed |

---

### Experiment 8 — Guard the throttle suppression with a speed floor (corner-aware target-speed)
**ID:** `exp08_corner_speed_floor`

**Line changed:** `snakeoil3_v2.py:544`
```python
# Before
# Corner-aware target speed: back off proportionally as space ahead shrinks
forward = S['track'][9]
if forward < 80:
    target_speed = 150 * (forward / 80)
else:
    target_speed = 150
# After
# Corner-aware target speed — only active at race speed to avoid suppressing recovery throttle
forward = S['track'][9]
if forward < 80 and S['speedX'] > 80:
    target_speed = 150 * (forward / 80)
else:
    target_speed = 150
```

| | Assessment |
|---|---|
| **Why** | In Exp 7, the corner-aware block suppressed throttle whenever forward clearance was short — including during off-track recoveries at low speed, where a short beam reading has nothing to do with a fast approach into a corner. Adding `S['speedX'] > 80` as a second condition ensures the speed ceiling is only reduced when the car is genuinely at race pace, leaving the throttle free to re-accelerate after a slow recovery |
| **1. Likely effect on lap time** | Significant improvement over Exp 7 and likely improvement over Exp 6 — the car now gets the benefits of both corner-aware throttle reduction at speed *and* uninhibited throttle recovery when slow, addressing the two failure modes simultaneously |
| **2. Likely effect on damage/control** | Improved corner entry control at high speed; normal throttle response restored during recovery. The car should handle the U-shaped and V-shaped turns more cleanly than in Exp 7 |
| **3. Where you'll notice it** | Most noticeably at the V-shaped turn where the car was previously unable to re-accelerate after going off-track. At high-speed corners the reduction in `target_speed` still applies, so corner entries should remain calmer than in Exp 6 |
| **4. What could make the prediction wrong** | If the car's speed drops below 80 km/h *before* a genuine fast corner (e.g. after braking hard), the guard disables the speed ceiling at exactly the wrong moment. This is unlikely on the Corkscrew's main corners since the car approaches them well above 80 km/h, but it could occur if a prior mistake has already bled a lot of speed |

---

### Experiment 9 — Raise the open-road speed ceiling: `150` → `160` km/h
**ID:** `exp09_ceiling_160`

**Lines changed:** `snakeoil3_v2.py:545` and `snakeoil3_v2.py:547`
```python
# Before
# Corner-aware target speed — only active at race speed to avoid suppressing recovery throttle
forward = S['track'][9]
if forward < 80 and S['speedX'] > 80:
    target_speed = 150 * (forward / 80)
else:
    target_speed = 150
# After
# Corner-aware target speed — only active at race speed to avoid suppressing recovery throttle
forward = S['track'][9]
if forward < 80 and S['speedX'] > 80:
    target_speed = 160 * (forward / 80)   # scale factor matches new ceiling 160
else:
    target_speed = 160
```

| | Assessment |
|---|---|
| **Why** | Exp 8 sits 3.13 s behind Exp 6's best despite better corner handling. The open-road ceiling (`target_speed = 150`) is the only remaining limiter on the straights — raising it to 160 km/h lets the car accelerate further where the corner-aware block is inactive (i.e. when forward clearance ≥ 80 m), recovering the time lost without changing corner behaviour. The scale factor in the suppression formula is updated to match so the proportional reduction at speed remains consistent |
| **1. Likely effect on lap time** | Moderate improvement (2–5 s) — the car will carry more speed on the main straight and any open section longer than ~200 m. Corner behaviour is unchanged since the suppression formula's shape is identical; only its ceiling shifts |
| **2. Likely effect on damage/control** | Slight increase in risk. The proportional brake and corner-aware throttle reduction are both still active at the corners, but the car now arrives at the 80 m suppression boundary 10 km/h faster, so there is marginally less time to shed speed before the apex. The damage = 1 from Exp 8 may reappear or increase |
| **3. Where you'll notice it** | Main straight and open sections with long forward clearance. The car will visibly reach higher speeds before the suppression zone begins. Corner entries should look similar to Exp 8 |
| **4. What could make the prediction wrong** | If the Corkscrew's critical corners (U-shaped, V-shaped) are approached via sections with forward clearance that stays just above 80 m, the speed ceiling will not suppress in time, and the car will arrive 10 km/h faster than in Exp 8 with the same braking window — potentially increasing off-track incidents at those specific corners |

---

### Experiment 10 — Faster throttle response: `±0.01` → `±0.02`
**ID:** `exp10_throttle_ramp_02`

**Lines changed:** `snakeoil3_v2.py:556` and `snakeoil3_v2.py:558`
```python
# Before
R['accel'] += .01
...
R['accel'] -= .01
# After
R['accel'] += .02
...
R['accel'] -= .02
```

| | Assessment |
|---|---|
| **Why** | The throttle ramp of `±0.01/step` takes 100 steps (2 s at 50 Hz) to sweep the full range. This is too slow to react when the corner-aware block drops `target_speed` — the car enters the suppression zone still carrying the old throttle value and arrives at turn-in hotter than intended. Doubling the ramp rate to `±0.02` halves the response lag (full sweep in 1 s), making the car react twice as fast to both upward speed targets on the straights and downward target reductions in the corner zone |
| **1. Likely effect on lap time** | Moderate improvement (1–4 s) — faster throttle pickup on straights shortens acceleration phases; faster lift-off when `target_speed` drops means the car enters corners closer to the intended speed, reducing off-track excursions |
| **2. Likely effect on damage/control** | Should reduce damage from the current level of 2 — the car will better match the corner-aware target speed and arrive at braking zones with less excess kinetic energy. Risk: if the ramp is too aggressive, the car may oscillate around `target_speed` on long straights, producing a sawtooth throttle pattern |
| **3. Where you'll notice it** | On corner entries — the car should lift more decisively when the corner-aware block activates, rather than coasting in on residual throttle. Also visible on short straights where the car now reaches `target_speed` sooner and holds it more crisply |
| **4. What could make the prediction wrong** | A ramp of `±0.02` doubles the oscillation amplitude around the speed target. On the long back straight, if the car overshoots `target_speed` frequently, the net effect could be a choppy throttle that costs more time than the faster response saves |

---

### Experiment 11 — Reduce centre-tracking gain: `0.20` → `0.15`
**ID:** `exp11_center_gain_015`

**Line changed:** `snakeoil3_v2.py:552`
```python
# Before
R['steer'] -= S['trackPos'] * 0.20
# After
R['steer'] -= S['trackPos'] * 0.15
```

| | Assessment |
|---|---|
| **Why** | The `0.20` centre-tracking gain set in Exp 2 was calibrated at ~114 km/h. At 170+ km/h the car moves laterally much faster per step; the same correction value now over-shoots every cycle, building a left-right weave that amplified into damage = 18 in Exp 10. Reducing to `0.15` cuts the lateral authority by 25%, calming the oscillation while still keeping the car pulled toward the centre line |
| **1. Likely effect on lap time** | Moderate improvement — the car will spend less time weaving and recovering, especially in the second half of the circuit. Less oscillation means the throttle and braking systems operate on a more stable platform and can do their jobs more effectively |
| **2. Likely effect on damage/control** | Significant damage reduction expected. The left-right weave that caused wall contacts through the second half should reduce or disappear. Chicane stability should also improve since the car won't be fighting its own steering correction when it needs to turn |
| **3. Where you'll notice it** | Everywhere after the mid-circuit chicane, where the weave was most visible. Also on the long back straight where the oscillation was growing with speed — the car should track straighter at 170+ km/h |
| **4. What could make the prediction wrong** | If the oscillation is driven more by the angle gain (`×10`) than the centre-tracking gain, reducing `0.20` → `0.15` will have little effect and the weave will persist. In that case the angle gain needs to be reduced next. Additionally, `0.15` may not be enough of a reduction — `0.10` (original baseline) may ultimately be required at these speeds |

---

### Experiment 12 — Reduce angle gain: `10` → `8`
**ID:** `exp12_angle_gain_8`

**Line changed:** `snakeoil3_v2.py:550`
```python
# Before
R['steer'] = S['angle'] * 10 / PI
# After
R['steer'] = S['angle'] * 8 / PI
```

| | Assessment |
|---|---|
| **Why** | The angle gain of `10` was tuned at the start of the experiment series when the car was travelling at ~120 km/h. At 170+ km/h the car rotates through its yaw angle much faster per step, so the same gain value snaps corrections past the apex and into the opposite wall — particularly at the chicane where two tight direction changes happen in rapid succession. Reducing to `8` softens the yaw response by 20%, giving the car time to rotate through corners without overshooting |
| **1. Likely effect on lap time** | Neutral to moderate improvement — the primary goal is a clean chicane passage. A chicane spin-out in Exp 11 alone cost several seconds and 30+ damage points; eliminating it should more than offset any minor loss of sharpness in medium-speed corners |
| **2. Likely effect on damage/control** | Significant damage reduction expected — the chicane crash that caused the spike to damage = 39 should be tamed. The car will track through tight direction changes more smoothly rather than snapping between opposite lock |
| **3. Where you'll notice it** | Most visibly at the mid-circuit chicane, where the crash occurred. Also at the U-shaped and V-shaped turns where yaw response drives the initial turn-in. On straight sections the angle sensor reads near-zero so the gain change has no effect |
| **4. What could make the prediction wrong** | If the chicane requires a very sharp initial steering input (e.g. a near-90° entry), reducing gain from `10` to `8` may leave the car understeering at the entry, causing it to run wide rather than spin. In that case the gain needs to go back up or a higher centre-tracking term must compensate. Also, the centre-tracking gain (`0.15`) now provides more of the total steering authority relative to the angle term — if the two terms fight each other at the chicane exit, a lower oscillation is expected but not guaranteed |

---

### Experiment 13 — Multi-beam forward sensing: `S['track'][9]` → `min(S['track'][7:12])`
**ID:** `exp13_multibeam_brake`

**Lines changed:** `snakeoil3_v2.py:543`, `snakeoil3_v2.py:561`, `snakeoil3_v2.py:562`
```python
# Before
# Corner-aware block (line 543):
forward = S['track'][9]

# Brake trigger and formula (lines 561–562):
if S['track'][9] < 60 and S['speedX'] > 80:
    R['brake'] = clip((60 - S['track'][9]) / 60 * (S['speedX'] / 150), 0, 1)

# After
# Corner-aware block (line 543):
forward = min(S['track'][7:12])

# Brake trigger and formula (lines 561–562):
if min(S['track'][7:12]) < 60 and S['speedX'] > 80:
    R['brake'] = clip((60 - min(S['track'][7:12])) / 60 * (S['speedX'] / 150), 0, 1)
```

| | Assessment |
|---|---|
| **Why** | The single dead-ahead beam (`track[9]`, 0°) only detects a wall when the car is pointing almost directly at it. At the chicane, the wall closes in from a slight angle — it appears first in the adjacent beams (indices 7–11, covering roughly ±7°) but `track[9]` still reads a long distance, so both the corner-aware throttle suppression and the proportional brake fire too late. Using the minimum of the five central beams ensures that any obstacle within ~±7° of the car's heading triggers braking and throttle reduction at the same distance as a head-on wall |
| **1. Likely effect on lap time** | Moderate improvement — the car will brake and lift earlier at the chicane and any angled approach, arriving at turn-in with less energy. Some time may be lost on gentle curves where a side beam clips the track edge early, but the chicane gain should outweigh this |
| **2. Likely effect on damage/control** | Significant damage reduction expected. The chicane crash (damage = 39–77 in Exp 11–12) is caused by the car entering at full speed; earlier brake activation should allow the car to negotiate both direction changes within the track boundaries |
| **3. Where you'll notice it** | Most visibly at the chicane — the car should begin slowing visibly earlier and carry less speed into the first direction change. The U-shaped and V-shaped turns (which have walls appearing from an angle) should also benefit. Open straights are unaffected since all five beams read maximum distance when the road is clear |
| **4. What could make the prediction wrong** | On wide corners where the inside kerb is close to one of the side beams, the minimum may clip prematurely and suppress throttle or apply brake when the car still has plenty of road ahead. This would show up as unnecessary slowing on sections that were previously clean. Also, at very high speed the 60 m trigger window (unchanged) may still not be enough if the car is approaching at 175+ km/h |

---

### Experiment 14 — Update brake speed reference: `150` → `170` km/h
**ID:** `exp14_brake_ref_170`

**Line changed:** `snakeoil3_v2.py:562`
```python
# Before
R['brake'] = clip((60 - min(S['track'][7:12])) / 60 * (S['speedX'] / 150), 0, 1)
# After
R['brake'] = clip((60 - min(S['track'][7:12])) / 60 * (S['speedX'] / 170), 0, 1)
```

| | Assessment |
|---|---|
| **Why** | The brake formula scales force by `speedX / 150`. Since the car now runs at 170+ km/h, this factor routinely exceeds 1.0 — and `clip()` caps it — so the gradual braking zone is compressed: full braking begins at ~47 m instead of the intended 60 m. Updating the reference to `170` matches the formula's design intent to the actual race speed, restoring the full graduated profile from 60 m down to 0 m and keeping the car steer-able throughout the braking zone |
| **1. Likely effect on lap time** | Neutral to slight improvement — the car will enter corners with more speed (because full-brake no longer fires prematurely at ~47 m) but will still be slowing through the full 60 m window. Net effect depends on whether the chicane and critical turns benefit more from the gentler entry or suffer from carrying slightly more speed to turn-in |
| **2. Likely effect on damage/control** | Improved control in the braking zone. Steering authority is better preserved across the full 60 m window (proportional brake, not suddenly at full lock at 47 m). Damage should remain at or near zero |
| **3. Where you'll notice it** | In the braking zones approaching the chicane and U-shaped turn — the car should visibly carry more speed deeper into the zone before the brake builds to maximum, giving a smoother, more controlled entry |
| **4. What could make the prediction wrong** | If the tightest corners require maximum braking force to begin at 60 m (not 47 m), then restoring the full gradual profile will result in the car arriving at the apex with more speed than before — potentially causing it to run wide again. If that happens, the trigger distance needs to increase (e.g. to 70–80 m) rather than adjusting the reference speed |

---

### Experiment 15 — Extend brake trigger distance: `60 m` → `80 m` (keeping `ref=170`)
**ID:** `exp15_brake_dist_80`

**Lines changed:** `snakeoil3_v2.py:561` and `snakeoil3_v2.py:562`
```python
# Before
if min(S['track'][7:12]) < 60 and S['speedX'] > 80:
    R['brake'] = clip((60 - min(S['track'][7:12])) / 60 * (S['speedX'] / 170), 0, 1)
# After
if min(S['track'][7:12]) < 80 and S['speedX'] > 80:
    R['brake'] = clip((80 - min(S['track'][7:12])) / 80 * (S['speedX'] / 170), 0, 1)
```

| | Assessment |
|---|---|
| **Why** | Exp 14 showed that a `ref=170` braking profile is too gentle at 60 m — the car arrives at the chicane with more speed than the corner can handle. The root cause is that the `ref=170` formula produces lower force at any given distance compared to the old `ref=150`. Extending the trigger to 80 m compensates by giving the brake 20 m more distance to work — the car begins decelerating earlier, so the total speed shed across the full 80 m window matches or exceeds what the old 60 m `ref=150` window was providing, while retaining the graduated, steer-able profile throughout |
| **1. Likely effect on lap time** | Moderate improvement over Exp 14; likely to approach or beat Exp 13 (124.09 s). The car sheds speed earlier so it enters critical turns with less energy, reducing the off-track excursions that cost time. On long straights the 80 m window activates sooner, but since the car is pointing straight the multi-beam minimum remains high until the corner genuinely arrives |
| **2. Likely effect on damage/control** | Significant damage reduction from the Exp 14 peak of 90. The brake builds from 0 at 80 m to maximum at 0 m, giving the driver full steering authority at corner entry. The chicane should be negotiable without a spin-out |
| **3. Where you'll notice it** | Most visibly at the chicane and U-shaped turn — the car will begin lifting the throttle and applying light brake noticeably earlier. The V-shaped turn before the finish line, which also requires heavy braking, should also benefit. Open straights with long forward readings are unaffected |
| **4. What could make the prediction wrong** | If the Corkscrew has sections where the multi-beam minimum drops below 80 m on a wide, safe curve (e.g. an inside kerb in view of a side beam), the brake will apply unnecessarily and bleed time. Also, at 80 m with `ref=170`, the initial brake force at full speed is `(80−80)/80 * 170/170 = 0` at entry — building to full only when the wall is 0 m away, which is still very graduated. If the chicane requires harder braking earlier in the zone, the trigger may need to go to 90–100 m |

---

### Experiment 16 — Raise speed ceiling: `160` → `180` km/h
**ID:** `exp16_ceiling_180`

**Lines changed:** `snakeoil3_v2.py:545`, `snakeoil3_v2.py:547`, `snakeoil3_v2.py:562`
```python
# Before
# Corner-aware block (lines 545, 547):
target_speed = 160 * (forward / 80)   # scale factor matches new ceiling 160
...
target_speed = 160

# Brake formula (line 562):
R['brake'] = clip((80 - min(S['track'][7:12])) / 80 * (S['speedX'] / 170), 0, 1)

# After
# Corner-aware block (lines 545, 547):
target_speed = 180 * (forward / 80)   # scale factor matches new ceiling 180
...
target_speed = 180

# Brake formula (line 562):
R['brake'] = clip((80 - min(S['track'][7:12])) / 80 * (S['speedX'] / 180), 0, 1)
```

| | Assessment |
|---|---|
| **Why** | The car has been running at ~171 km/h for several experiments while the target speed ceiling was 160 km/h — meaning the throttle controller was perpetually decelerating on the straights. Raising the ceiling to 180 km/h allows full acceleration to a higher speed, directly reducing lap time on straight sections. At the same time, updating the brake `ref` from `170` to `180` keeps the formula correctly calibrated: at 180 km/h the formula now clips to full brake in the innermost part of the 80 m zone, providing the decisive stop that the chicane and V-turn need, while the outer zone (80 m to ~13 m) remains graduated and steer-able |
| **1. Likely effect on lap time** | Moderate to significant improvement (3–8 s) — the car can now accelerate freely to 180 km/h on the main straight. The corner-aware throttle suppression and the brake formula both scale up with the new ceiling, so cornering behaviour at the critical turns should be at least as good as Exp 15 |
| **2. Likely effect on damage/control** | Neutral to improved — at 180 km/h the brake force at 20 m is `(80−20)/80 × 180/180 = 0.75`, and at 5 m it is `(80−5)/80 × 1.0 = 0.94`. The brake is stronger in the inner zone at higher speed, which is what the chicane needs. Risk: if the car now reaches 180 km/h on approach, arrival energy is higher and the 80 m window must shed more speed — the margin is tighter |
| **3. Where you'll notice it** | Main straight — the car will visibly keep accelerating past 160 km/h toward 180 km/h. At the chicane and critical turns the corner-aware throttle will suppress earlier (since the target is now 180, the proportional reduction starts at `forward < 80`) and the brake will be slightly stronger at race speed |
| **4. What could make the prediction wrong** | If the car reaches 180 km/h approaching the chicane, the extra kinetic energy (~6% more than at 170 km/h) may exceed what the 80 m window can shed, causing another crash. The gear-shift thresholds (fixed at 50/80/110/140/170 km/h) do not include a 180 km/h step — the car will stay in 6th above 170 km/h, which is correct, but wheel-spin at gear changes near those thresholds could briefly unsettle the car at higher speeds |

---

### Experiment 17 — Extend brake trigger: `80 m` → `100 m` + quadratic speed scaling
**ID:** `exp17_brake_100m_quadratic`

**Lines changed:** `snakeoil3_v2.py:561`, `snakeoil3_v2.py:562`, `snakeoil3_v2.py:593`
```python
# Before
if min(S['track'][7:12]) < 80 and S['speedX'] > 80:
    R['brake'] = clip((80 - min(S['track'][7:12])) / 80 * (S['speedX'] / 180), 0, 1)

# After
if min(S['track'][7:12]) < 100 and S['speedX'] > 80:
    R['brake'] = clip((100 - min(S['track'][7:12])) / 100 * (S['speedX'] / 180) ** 2, 0, 1)
```

| | Assessment |
|---|---|
| **Why** | At 187 km/h the car covers ~52 m/s. The 80 m brake window gives only ~1.5 s to shed speed approaching the V-shaped last corner — not enough. Kinetic energy scales with speed squared, so a car at 187 km/h carries 1.37× the energy of one at 160 km/h; the old linear formula only scaled force by 1.04×. Extending to 100 m adds ~0.38 s of braking time, and switching to `(speedX/180)²` makes braking force proportional to the energy that must actually be shed |
| **1. Likely effect on lap time** | Moderate improvement (4–8 s) — the car stays on track through the V-corner instead of going far off-track and recovering slowly. The chicane and wide-turn behaviour is unchanged from Exp 16 |
| **2. Likely effect on damage/control** | Zero or near-zero damage expected. The quadratic formula delivers near-maximum force in the last few metres (force ≈ 0.97 at 10 m at 187 km/h) providing the decisive stop the V-corner demands |
| **3. Where you'll notice it** | Primarily at the V-shaped last corner — the car will begin braking noticeably earlier and remain on track through the apex. Slightly earlier light braking on any section where the 5-beam minimum drops below 100 m |
| **4. What could make the prediction wrong** | If the V-corner requires braking to begin at exactly 100 m and the formula still delivers too little force at the entry (force = 0 at the 100 m boundary), the car may still run wide — extend to 110 m in that case. The wider window may also apply light braking on wide curves where an inside kerb appears in a side beam at <100 m; Exp 19 will address this for the throttle path |

---


### Experiment 18 — Raise corner-aware throttle suppression: `80 m` → `100 m`
**ID:** `exp18_throttle_suppress_100m`

**Lines changed:** `snakeoil3_v2.py:544`, `snakeoil3_v2.py:545`, `snakeoil3_v2.py:593`
```python
# Before
forward = min(S['track'][7:12])
if forward < 80 and S['speedX'] > 80:
    target_speed = 180 * (forward / 80)   # scale factor matches new ceiling 180

# After
forward = min(S['track'][7:12])
if forward < 100 and S['speedX'] > 80:
    target_speed = 180 * (forward / 100)  # scale denominator matches 100 m suppression window
```

| | Assessment |
|---|---|
| **Why** | Exp 17 confirmed the chicane as the damage source: the car went slightly off-track and bounced through the two direction changes. At 186 km/h the throttle suppression only fires at 80 m while the brake now fires at 100 m — both fire within the same 20 m window, meaning they work simultaneously instead of sequentially. Raising the throttle suppression to 100 m gives the car an extra 20 m (~0.38 s) of pure throttle-lift before the brake zone begins, arriving at the chicane entry with less speed and a settled chassis |
| **1. Likely effect on lap time** | Moderate improvement (2–4 s) — a cleaner chicane transit removes the off-track excursion and the bouncing instability that costs time through the two direction changes |
| **2. Likely effect on damage/control** | Damage should drop from 20 toward zero — the chicane instability was driven by entering too fast; the earlier lift should smooth the entry |
| **3. Where you'll notice it** | Most visibly at the chicane — the car will visibly lift earlier before the first direction change. Also at the V-corner where the throttle suppression now fires at the same distance as the brake, giving a longer pre-brake coasting phase |
| **4. What could make the prediction wrong** | Raising the suppression window to 100 m on the same 5-beam minimum may cause unnecessary throttle lift on wide curves where an inside kerb appears in a side beam at <100 m. Exp 19 addresses this. If the chicane remains unstable, the cause is steering gain rather than entry speed — in that case the fix is a tighter sensor window rather than a further threshold increase |

---


### Experiment 19 — Narrow throttle suppression to 3-beam central window: `min(track[7:12])` → `min(track[8:11])`
**ID:** `exp19_narrow_throttle_beam`

**Lines changed:** `snakeoil3_v2.py:543`, `snakeoil3_v2.py:593`
```python
# Before
forward = min(S['track'][7:12])
if forward < 100 and S['speedX'] > 80:
    target_speed = 180 * (forward / 100)  # scale denominator matches 100 m suppression window

# After
forward = min(S['track'][8:11])           # 3-beam ±0.5° — avoids inside-kerb false triggers
if forward < 100 and S['speedX'] > 80:
    target_speed = 180 * (forward / 100)  # scale denominator matches 100 m suppression window
```

| | Assessment |
|---|---|
| **Why** | The 5-beam minimum (`min(track[7:12])`, covering ±1°) captures inside kerbs at the edges of the beam window. A kerb beside the car at 60 m reads as `forward = 60`, triggering `target_speed = 180 * (60/100) = 108 km/h` on a curve that the car could safely take at 165+ km/h. Switching to the 3-beam central window (`min(track[8:11])`, ±0.5°) means only a wall directly ahead of the car's nose — not a kerb beside it — will register a short reading and suppress throttle. The brake block stays on the wider 5-beam window for safety |
| **1. Likely effect on lap time** | Moderate improvement (2–5 s) — wide bends previously limited to ~108–130 km/h are now taken at 160–180 km/h. The chicane and V-corner fixes from Exp 17 and Exp 18 are unaffected because both walls appear within ±0.5° of the car's heading at the relevant distances |
| **2. Likely effect on damage/control** | Zero damage expected — the brake block retains full ±1° (5-beam) coverage so genuine walls still trigger braking at the correct distance |
| **3. Where you'll notice it** | Wide, open bends where the inside kerb was previously clipping the ±1° side beams. The car will visibly maintain full speed through those sections instead of lifting unnecessarily |
| **4. What could make the prediction wrong** | If the chicane approach is angled (car heading slightly off the chicane wall's normal), the wall may only appear in beam 7 or 11 and not in beams 8–10, causing throttle suppression to fire too late. If Exp 19 produces a chicane crash or large time regression, restore `min(track[7:12])` for the throttle block. A 4-beam window `min(track[7:11])` is a middle-ground fallback |

---

### Experiment 20 — Raise speed ceiling: `180` → `200` km/h
**ID:** `exp20_ceiling_200`

**Lines changed:** `snakeoil3_v2.py:545`, `snakeoil3_v2.py:547`, `snakeoil3_v2.py:562`, `snakeoil3_v2.py:593`
```python
# Before
# Corner-aware block (lines 545, 547):
        target_speed = 180 * (forward / 100)  # scale denominator matches 100 m suppression window
    else:
        target_speed = 180

# Brake formula (line 562):
    R['brake'] = clip((100 - min(S['track'][7:12])) / 100 * (S['speedX'] / 180) ** 2, 0, 1)

# After
# Corner-aware block (lines 545, 547):
        target_speed = 200 * (forward / 100)  # scale denominator matches 100 m suppression window
    else:
        target_speed = 200

# Brake formula (line 562):
    R['brake'] = clip((100 - min(S['track'][7:12])) / 100 * (S['speedX'] / 200) ** 2, 0, 1)
```

| | Assessment |
|---|---|
| **Why** | At the end of Exp 19 the car was reaching 187.5 km/h while the ceiling was 180 km/h — the throttle controller was perpetually decelerating on the straights. Raising the ceiling to 200 km/h allows the car to accelerate freely through the full straight. Updating the brake `ref` from `180` to `200` keeps the quadratic formula correctly calibrated: at 200 km/h the factor `(speedX/200)²` equals 1.0 at the speed limit, so the full graduated profile from 100 m down to 0 m remains intact at race speed. The corner-aware suppression scale also matches the new ceiling, so proportional throttle lift through corners is consistent |
| **1. Likely effect on lap time** | Moderate improvement (3–6 s) — the car will carry more speed on the main straight past the old 180 km/h ceiling. The corner-aware throttle suppression and brake formula both scale up with the new ceiling, so cornering behaviour should be no worse than Exp 19 |
| **2. Likely effect on damage/control** | Risk of increased damage. At 200 km/h the car carries ~24% more kinetic energy than at 180 km/h (`200² / 180²`). The 100 m brake window was sized for ~185–190 km/h; at 200 km/h the quadratic formula delivers `(speedX/200)² = 1.0` at the boundary (identical shape to before but now correctly calibrated), meaning braking force is unchanged at any given proximity. However, the car *arrives* at the 100 m boundary 10–15 km/h faster and must shed more energy in the same distance — the margin at the chicane and V-corner is tighter |
| **3. Where you'll notice it** | Main straight — the car will visibly keep accelerating past 187 km/h toward 200 km/h. The corner-aware throttle now reduces to `200 × (forward/100)` in the suppression zone, which at 60 m ahead gives `target_speed = 120 km/h` (vs 108 km/h with the old 180 ceiling) — slightly higher corner entry speeds that the brake must handle |
| **4. What could make the prediction wrong** | If the car reaches 200 km/h approaching the chicane or V-corner, the extra kinetic energy may exceed what the 100 m window can shed even with the quadratic formula, causing off-track excursions or a crash. The gear-shift thresholds top out at 170 km/h (6th gear) — the car will remain in 6th above that, which is correct, but it also means the engine is already at maximum gear when pushing for 200 km/h; wheel-spin risk on exit from slow corners increases. If max speed stays below 195 km/h or damage spikes again, the brake trigger window should be extended to 110–120 m rather than raising the ceiling further |

---

### Experiment 21 — Extend brake trigger distance: `100 m` → `120 m`
**ID:** `exp21_brake_120m`

**Lines changed:** `snakeoil3_v2.py:561`, `snakeoil3_v2.py:562`, `snakeoil3_v2.py:593`
```python
# Before
if min(S['track'][7:12]) < 100 and S['speedX'] > 80:
    R['brake'] = clip((100 - min(S['track'][7:12])) / 100 * (S['speedX'] / 200) ** 2, 0, 1)
# After
if min(S['track'][7:12]) < 120 and S['speedX'] > 80:
    R['brake'] = clip((120 - min(S['track'][7:12])) / 120 * (S['speedX'] / 200) ** 2, 0, 1)
```

| | Assessment |
|---|---|
| **Why** | At 205 km/h the car covers ~57 m/s. The 100 m brake window gives only ~1.75 s to shed speed — enough for the chicane but not for the V-corner, where the car overshoots and loses several seconds recovering. Extending to 120 m adds ~0.35 s of additional braking time (120 m ÷ 57 m/s ≈ 2.11 s total). The formula constant is updated from `100` to `120` to keep the graduated profile intact: force = 0 at 120 m, building smoothly to maximum as the wall closes in. The brake `ref` stays at `200` so the speed-scaling of the quadratic formula is unchanged |
| **1. Likely effect on lap time** | Moderate improvement (2–5 s) — the V-corner overshoot is the main time loss in Exp 20; earlier braking should keep the car on track through the apex, eliminating the slow off-track recovery. The chicane approach also benefits from an extra 20 m of light braking before the wall fully registers, arriving with a calmer entry |
| **2. Likely effect on damage/control** | Damage should drop from 22 toward zero — the chicane and V-corner contacts are both caused by arriving with too much speed; the wider window addresses both. Steering authority is preserved throughout because the formula remains quadratic and graduated, not a hard lock |
| **3. Where you'll notice it** | Most visibly at the V-shaped last corner — the car will begin braking noticeably earlier and stay on track through the apex instead of shooting wide. At the chicane the first brake application will start sooner and be lighter, giving the car a more composed entry into the first direction change. Open straights with long forward readings are unaffected since the 5-beam minimum stays high until a wall genuinely closes in |
| **4. What could make the prediction wrong** | On wide curves where an inside kerb appears in one of the ±1° side beams at <120 m, the brake will apply lightly and bleed time unnecessarily — the same risk that existed at 100 m but now active over a larger zone. If the chicane approach has a gradual bend that brings a side beam within 120 m of the inside edge before the wall is genuinely threatening, the car may brake earlier than needed and enter the chicane too slowly, reintroducing the instability seen in Exp 18. If this occurs, the fallback is 110 m |

---

### Experiment 22 — Two-zone brake: quadratic outer `120–40 m` → linear inner `40–0 m`
**ID:** `exp22_brake_twostage`

**Lines changed:** `snakeoil3_v2.py:560–564`, `snakeoil3_v2.py:593`
```python
# Before
    # Brake if a wall is closing in fast ahead (proportional, multi-beam, quadratic)
    if min(S['track'][7:12]) < 120 and S['speedX'] > 80:
        R['brake'] = clip((120 - min(S['track'][7:12])) / 120 * (S['speedX'] / 200) ** 2, 0, 1)
    else:
        R['brake'] = 0.0

# After
    # Brake if a wall is closing in fast ahead (two-zone: quadratic outer 120–40 m, linear inner 40–0 m)
    _fwd = min(S['track'][7:12])
    if _fwd < 120 and S['speedX'] > 80:
        if _fwd >= 40:                                    # outer zone 120–40 m: graduated quadratic
            R['brake'] = clip((120 - _fwd) / 120 * (S['speedX'] / 200) ** 2, 0, 1)
        else:                                             # inner zone 40–0 m: linear, always decisive
            R['brake'] = clip(0.667 + (40 - _fwd) / 120, 0, 1)
    else:
        R['brake'] = 0.0
```

| | Assessment |
|---|---|
| **Why** | Exp 21 showed that widening the brake window to 120 m does not help because the quadratic formula delivers almost no force in the outer zone (≈0 at 120 m, ≈0.25 at 90 m) — the car coasts through the extra distance and still arrives at the critical 40 m zone with nearly the same speed as before. The root cause is that the pure quadratic shape concentrates all stopping power in the final 30 m, which is too late for the V-corner at 200+ km/h. The fix is a two-zone profile: keep the quadratic outer zone (120–40 m) for a steer-able, graduated approach, then switch to a linear ramp in the inner zone (40–0 m) that climbs directly from 0.667 at 40 m to 1.0 at 0 m. This gives a decisive, sustained stop exactly where the V-corner and chicane demand it, without disturbing the outer approach |
| **1. Likely effect on lap time** | Moderate to significant improvement (3–6 s) — the V-corner overshoot is directly caused by insufficient braking force in the 40–0 m zone; the linear inner ramp delivers ~50% more cumulative force there than the quadratic alone. The chicane also benefits: the decisive inner-zone stop gives the car a controlled entry into the first direction change. Open straights are unaffected |
| **2. Likely effect on damage/control** | Damage should drop from 19 toward zero. The outer zone retains the gradual profile, so steering authority is preserved at 120–40 m. In the inner zone the linear ramp applies firm but not abrupt force — the car decelerates hard but the wheels do not lock because `clip(…, 0, 1)` caps at 1.0 and the formula is still a smooth ramp, not a step |
| **3. Where you'll notice it** | Most visibly at the V-shaped last corner — the car will visibly slow much harder once inside 40 m, tracking the road edge rather than shooting wide. At the chicane the same decisive inner stop fires in the final metres before the first direction change. In the outer zone (120–40 m) behaviour is identical to Exp 21 |
| **4. What could make the prediction wrong** | If the handover value of 0.667 at 40 m is too high for the chicane (which requires a gentler arrival than the V-corner), the abrupt jump in braking force at 40 m could unsettle the car mid-turn and cause a spin. If that happens, lower the handover distance from 40 m to 30 m (giving 0.75 handover) or raise it to 50 m (giving 0.583 handover). Also, if the 5-beam minimum reads a kerb at <40 m on a wide bend, the linear zone fires when it should not — but this is unlikely since genuine kerb readings close to the car would be at <20 m and only briefly |

---

### Experiment 23 — Revert brake to pure quadratic (`100 m`) + gate TCS to acceleration-only
**ID:** `exp23_quadratic_tcs_gate`

**Lines changed:** [`snakeoil3_v2.py:560–565`](snakeoil3_v2.py:560), [`snakeoil3_v2.py:572–575`](snakeoil3_v2.py:572), [`snakeoil3_v2.py:597`](snakeoil3_v2.py:597)
```python
# Before
    # Brake if a wall is closing in fast ahead (two-zone: quadratic outer 120–40 m, linear inner 40–0 m)
    _fwd = min(S['track'][7:12])
    if _fwd < 120 and S['speedX'] > 80:
        if _fwd >= 40:                                    # outer zone 120–40 m: graduated quadratic
            R['brake'] = clip((120 - _fwd) / 120 * (S['speedX'] / 200) ** 2, 0, 1)
        else:                                             # inner zone 40–0 m: linear, always decisive
            R['brake'] = clip(0.667 + (40 - _fwd) / 120, 0, 1)
    else:
        R['brake'] = 0.0

    # Traction Control System
    if ((S['wheelSpinVel'][2]+S['wheelSpinVel'][3]) -
       (S['wheelSpinVel'][0]+S['wheelSpinVel'][1]) > 5):
       R['accel']-= .2

# After
    # Brake if a wall is closing in fast ahead (proportional, multi-beam, quadratic)
    _fwd = min(S['track'][7:12])
    if _fwd < 100 and S['speedX'] > 80:
        R['brake'] = clip((100 - _fwd) / 100 * (S['speedX'] / 200) ** 2, 0, 1)
    else:
        R['brake'] = 0.0

    # Traction Control System — gated to acceleration only (brake < 0.05)
    # prevents TCS from misfiring during hard braking and causing lockup oscillation
    if (R['brake'] < 0.05 and
       (S['wheelSpinVel'][2]+S['wheelSpinVel'][3]) -
       (S['wheelSpinVel'][0]+S['wheelSpinVel'][1]) > 5):
       R['accel']-= .2
```

| | Assessment |
|---|---|
| **Why** | Exp 22 confirmed that the two-zone brake structure caused brake lockup and severe side-to-side instability across the whole lap — 17.3 s slower than the Exp 17 best. Root-cause analysis identified two coupled failure modes: (1) the linear inner zone (`0.667 + (40-fwd)/120`) delivered too much force too abruptly once inside 40 m, causing wheel lockup even on open curves where the 5-beam sensor briefly reads a kerb at <40 m; (2) the TCS, which fires `accel −= 0.2` as a step function, was misfiring during hard braking — simultaneously chopping throttle while maximum brake was applied, producing the observed oscillation. Both are fixed here: the brake reverts to the pure quadratic at 100 m (the formula that produced the all-time best of 122.86 s in Exp 17), and the TCS is gated with `R['brake'] < 0.05` so it only activates during acceleration, not braking. This also sets the correct clean baseline for the push to 250 km/h |
| **1. Likely effect on lap time** | Significant improvement vs Exp 22 (−10 to −17 s expected), recovering toward the Exp 17–20 range of 122–127 s. The brake revert restores the proven Exp 17 force profile; the TCS gate removes a compounding deceleration that was artificially capping top speed and amplifying steering oscillation everywhere the brake was active |
| **2. Likely effect on damage/control** | Damage should drop markedly from 13. The TCS gate is the primary driver: without `accel −= 0.2` firing during braking, the car no longer receives simultaneous brake + throttle-cut inputs that cause the side-to-side oscillation. The 100 m quadratic brake is the same formula that produced 0-damage runs in Exp 13 and 16, so clean laps are achievable if steering holds |
| **3. Where you'll notice it** | Throughout the lap — the side-to-side vibration visible in Exp 22 should disappear entirely. At the chicane the car will approach without the oscillation that was costing lateral positioning. At the V-corner the brake profile is shallower than Exp 22's inner zone (less hard stopping in the final 40 m), so some overshoot may remain — but far less time will be lost than in Exp 22 because the car will at least hold its line on the rest of the lap |
| **4. What could make the prediction wrong** | If the TCS gate (`brake < 0.05`) threshold is too low and there are steps where the brake is very small but non-zero while the rear wheels are still spinning from a previous acceleration phase, the TCS will remain suppressed when it should fire. In that case raising the threshold to `0.10` is the fix. Also, the 100 m trigger is the same distance as Exp 17 (best-ever), but the current ceiling is 200 km/h vs 180 in Exp 17 — the car arrives at the 100 m boundary ~8 km/h faster, so some increase in V-corner overshoot vs Exp 17 is possible even without the two-zone structure |

---

### Experiment 24 — Raise speed ceiling + suppress ceiling + brake ref together: `200` → `250` km/h
**ID:** `exp24_ceiling_250`

**Lines changed:** [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545), [`snakeoil3_v2.py:547`](snakeoil3_v2.py:547), [`snakeoil3_v2.py:563`](snakeoil3_v2.py:563), [`snakeoil3_v2.py:596`](snakeoil3_v2.py:596)
```python
# Before
    # Corner-aware block (lines 545, 547):
        target_speed = 200 * (forward / 100)  # scale denominator matches 100 m suppression window
    else:
        target_speed = 200

    # Brake formula speed reference (line 563):
        R['brake'] = clip((100 - _fwd) / 100 * (S['speedX'] / 200) ** 2, 0, 1)

# After
    # Corner-aware block (lines 545, 547):
        target_speed = 250 * (forward / 100)  # scale denominator matches 100 m suppression window
    else:
        target_speed = 250

    # Brake formula speed reference (line 563):
        R['brake'] = clip((100 - _fwd) / 100 * (S['speedX'] / 250) ** 2, 0, 1)
```

| | Assessment |
|---|---|
| **Why** | Exp 23 confirmed the car is running at 205.6 km/h while the ceiling remains at 200 km/h — the throttle controller has been perpetually decelerating on the straights for the last three experiments. Raising the ceiling to 250 km/h removes that cap and allows the car to accelerate freely through the full Corkscrew straight. The brake ref and corner-aware suppression ceiling must be updated together as a coupled triplet: with `ref=250`, `(speedX/250)²` equals 1.0 only when the car actually reaches 250 km/h, so the full graduated quadratic profile from 100 m to 0 m is preserved at race speed. If the ref were left at 200, the formula would clip to 1.0 at 57 m instead of 40 m, compressing the braking zone and over-braking at moderate speeds — exactly the calibration drift that caused the regression in Exp 14. The suppress ceiling tracks the speed ceiling so the corner-aware throttle lift ratio remains consistent: at 80 m ahead, `target_speed = 250 × 0.8 = 200 km/h` rather than the old 160 km/h |
| **1. Likely effect on lap time** | Moderate improvement (2–5 s) — the car will accelerate past 205 km/h toward 250 km/h on the main straight. However, the brake trigger distance remains at 100 m, which was already marginal at 205 km/h; at 250 km/h (`69.4 m/s`) the 100 m window gives only ~1.44 s of braking time. The V-corner and chicane damage from Exp 23 is therefore likely to increase unless the car naturally manages its energy better with the correctly calibrated `ref=250` brake formula |
| **2. Likely effect on damage/control** | Damage risk is significant. The `ref=250` calibration makes the quadratic gentler at any given speed below 250 km/h — at 205 km/h the force multiplier drops from `(205/200)² = 1.05` (clipping) to `(205/250)² = 0.673`. The car loses roughly 36% of its braking force at current race speeds compared to Exp 23. This is intentional (the formula was over-braking relative to its calibrated ceiling) but means the V-corner and chicane will be approached faster until the trigger distance is extended in the next experiment. Damage may climb above 33 |
| **3. Where you'll notice it** | Main straight — the car will visibly keep accelerating past 205 km/h toward 250 km/h. At the V-corner and chicane the brake will feel lighter than Exp 23 because `ref=250` reduces force at current speeds; the car will require more distance to stop. If the lap completes cleanly with lower damage, the calibration is working. If the V-corner overshoot worsens, it confirms the brake trigger distance must extend in Exp 25 before pushing the ceiling further |
| **4. What could make the prediction wrong** | If Corkscrew's straight is too short to accelerate to 250 km/h, the gain over 205 km/h will be smaller than expected and damage will rise without a lap-time benefit — indicating the trigger distance must be extended before the ceiling can help. Also, if the gear-shift pattern (top gear at 170 km/h) keeps the engine in the power band through 250 km/h, the gain is real; if the engine runs out of power band in 6th gear before 250 km/h, the new ceiling is unreachable and the ref change will simply weaken the brakes for no speed gain |

---

### Experiment 25 — Widen brake trigger: `100 m` → `160 m` (keep quadratic, `ref=250`)
**ID:** `exp25_brake_dist_160`

**Lines changed:** [`snakeoil3_v2.py:562`](snakeoil3_v2.py:562), [`snakeoil3_v2.py:563`](snakeoil3_v2.py:563), [`snakeoil3_v2.py:596`](snakeoil3_v2.py:596)
```python
# Before
    if _fwd < 100 and S['speedX'] > 80:
        R['brake'] = clip((100 - _fwd) / 100 * (S['speedX'] / 250) ** 2, 0, 1)

# After
    if _fwd < 160 and S['speedX'] > 80:
        R['brake'] = clip((160 - _fwd) / 160 * (S['speedX'] / 250) ** 2, 0, 1)
```

| | Assessment |
|---|---|
| **Why** | Exp 24 proved the 100 m trigger is fatally undersized for the 250 km/h ceiling: raising `ref` from 200 to 250 reduced braking force at 210 km/h by ~36%, and the car could not shed enough energy at the U-corner or chicane entry — the lap could not be completed. At 210 km/h the car covers 58.3 m/s; the 100 m window gave only ~1.71 s of braking time. The theoretical trigger required to maintain the same braking geometry as the Exp 17 best (100 m at 180 km/h, ref=180) scales with `v²/v_ref_old² × 100 m = (250/180)² × 100 ≈ 193 m`. A 160 m trigger is the first step toward that target — conservative enough to avoid the Exp 21 coasting penalty (where 120 m at ref=200 gave too little force in the outer zone) while large enough to give 160/58.3 ≈ 2.74 s of braking time at 210 km/h. The formula constant is updated from `100` to `160` to keep the graduated profile intact: force = 0 at 160 m, building smoothly to maximum as the wall closes in. `ref=250` and the suppress window are unchanged |
| **1. Likely effect on lap time** | Significant improvement vs Exp 24 — the lap should complete rather than crash. The absolute time is hard to predict: the wider window adds early light braking on straights (which bleeds top-speed time) but eliminates the catastrophic off-track losses at the chicane and U-corner. A best estimate is recovery toward the 126–130 s range; if the force profile is well-matched to the track, improvement beyond Exp 23's 126.3 s is possible |
| **2. Likely effect on damage/control** | Damage should drop sharply from 21 (Exp 24). The car will begin braking 60 m earlier than before at the chicane and V-corner, arriving with less kinetic energy at the critical 40 m zone. With `ref=250`, force at 40 m from the wall at 210 km/h = `(160-40)/160 × (210/250)² = 0.75 × 0.706 = 0.530` — lighter than Exp 23's 0.662 at the same point, so the car retains more steering authority through the final approach |
| **3. Where you'll notice it** | Most visibly at the chicane — the brake will begin firing at 160 m, giving a long, gradual deceleration all the way to the first direction change rather than a last-moment hard stop. At the V-corner the same early braking should keep the car on the racing line. On the main straight the car may lose 1–2 km/h of peak speed if the 5-beam sensor catches a distant wall at 160 m, but this is only relevant on genuinely tight sections |
| **4. What could make the prediction wrong** | If the 5-beam brake sensor (`min(track[7:12])`) reads a kerb or barrier at <160 m on any wide bend or inside kerb passage, the brake will apply lightly and bleed time unnecessarily — a wider version of the side-beam false-trigger risk that was solved for the throttle sensor in Exp 19. If this occurs and the car slows noticeably on open curves, the trigger distance should be pulled back to 140 m. Additionally, if the car still crashes at the chicane despite the wider window, the suppress window (currently 100 m) must also be extended so throttle lift starts before the brake zone begins |

---

### Experiment 26 — Widen throttle suppress window: `100 m` → `160 m` (keep 3-beam)
**ID:** `exp26_suppress_160`

**Lines changed:** [`snakeoil3_v2.py:544`](snakeoil3_v2.py:544), [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545), [`snakeoil3_v2.py:596`](snakeoil3_v2.py:596)
```python
# Before
    forward = min(S['track'][8:11])           # 3-beam ±0.5° — avoids inside-kerb false triggers
    if forward < 100 and S['speedX'] > 80:
        target_speed = 250 * (forward / 100)  # scale denominator matches 100 m suppression window

# After
    forward = min(S['track'][8:11])           # 3-beam ±0.5° — avoids inside-kerb false triggers
    if forward < 160 and S['speedX'] > 80:
        target_speed = 250 * (forward / 160)  # scale denominator matches 160 m suppression window
```

| | Assessment |
|---|---|
| **Why** | Exp 25 exposed a structural mismatch: the brake trigger fires at 160 m but the throttle suppress only activates at 100 m. For the first 60 m of every braking zone the car simultaneously applies brake force and maintains full throttle — working against itself. At 210 km/h this overlap zone takes ~0.86 s to traverse, during which brake force ranges from 0 to `(60/160) × (210/250)² = 0.265`. The combined throttle + light brake condition feeds the TCS gate and keeps the car hotter than intended at the start of every braking event. Extending the suppress window to 160 m — matching the brake trigger exactly — eliminates the overlap entirely: from the moment the 3-beam sensor reads <160 m the throttle starts lifting, so by the time the 5-beam brake sensor fires at 160 m the throttle is already at or near its suppressed target. The 3-beam narrow sensor (±0.5°) is kept to avoid the inside-kerb false triggers that caused the Exp 18 regression when the suppress beam was widened |
| **1. Likely effect on lap time** | The lap should now complete within the step budget. The two previous partial runs both stopped at ~125.2 s with the finish line seconds away — eliminating the throttle+brake overlap removes the energy waste that was bleeding time through every braking zone, and the earlier throttle lift gives the car a calmer entry into the chicane and V-corner. A lap time in the 124–129 s range is plausible; if the suppress starts the throttle roll-off too early on long straights it may cost 1–2 s of top-speed time, but this is recoverable in the next experiment |
| **2. Likely effect on damage/control** | Damage should fall from 26. With throttle already ramping down from 160 m, the car arrives at the chicane and V-corner entry with meaningfully less speed than in Exp 25 — the brake has 60 m of pre-settled vehicle to work with rather than a car still fighting between full gas and rising brake force. The chicane instability was largely caused by lateral momentum built up while brake and throttle overlapped; removing that overlap should reduce the wide drift on the chicane's first direction change |
| **3. Where you'll notice it** | Most visibly at the chicane approach — the car will lift off the throttle noticeably earlier, arriving at the first kerb with a composed, slowing entry rather than the current hot, unsettled dive. At the V-corner the earlier throttle lift translates to lower entry speed and a tighter line. On the main straight the 3-beam sensor should not trigger at 160 m because there are no walls or kerbs in the direct ±0.5° ahead window at that distance on the straight; any performance loss there would indicate an unexpected track feature |
| **4. What could make the prediction wrong** | The speed floor guard (`S['speedX'] > 80`) keeps the suppress inactive during slow off-track recovery, so that is safe. The risk is that the wider suppress window begins cutting `target_speed` on the approach curves before the chicane — specifically the open bend at ~80 m forward clearance — and the 3-beam sensor reads a distant wall that the 5-beam does not. If the car slows noticeably mid-bend on sections where it was previously clean, the suppress window should be pulled back to 140 m. Additionally, if the suppress is so effective that the car arrives at the V-corner too slowly and gets stuck in a slow-recovery loop, raising the speed floor from 80 to 100 km/h would sharpen the suppression boundary |

---

### Experiment 27 — Steeper brake profile: cubic distance exponent `1` → `0.6` (keep quadratic speed term)
**ID:** `exp27_brake_cubic_dist`

**Lines changed:** [`snakeoil3_v2.py:560–563`](snakeoil3_v2.py:560), [`snakeoil3_v2.py:597`](snakeoil3_v2.py:597)
```python
# Before
    # Brake if a wall is closing in fast ahead (proportional, multi-beam, quadratic)
    _fwd = min(S['track'][7:12])
    if _fwd < 160 and S['speedX'] > 80:
        R['brake'] = clip((160 - _fwd) / 160 * (S['speedX'] / 250) ** 2, 0, 1)

# After
    # Brake if a wall is closing in fast ahead (multi-beam, cubic distance × quadratic speed)
    # dist exponent 0.6 concentrates more force in the 60–20 m zone vs pure quadratic distance
    _fwd = min(S['track'][7:12])
    if _fwd < 160 and S['speedX'] > 80:
        R['brake'] = clip(((160 - _fwd) / 160) ** 0.6 * (S['speedX'] / 250) ** 2, 0, 1)
```

| | Assessment |
|---|---|
| **Why** | Experiments 24–26 have consistently shown that the braking force at actual race speeds (~193–210 km/h, well below `ref=250`) is too weak in the 60–20 m zone where the chicane and V-corner demand a decisive stop. The quadratic distance profile `(dist_ratio)^1` scales force linearly with the fraction of the window consumed — at 120 m from a 160 m trigger `dist_ratio = 0.25`, force = 0.25 × speed_term; at 60 m `dist_ratio = 0.625`, force = 0.625 × speed_term. A sub-unitary distance exponent (here `^0.6`) preserves the smooth, continuous profile that avoids lockup while redistributing weight toward the inner zone: `0.25^0.6 = 0.398` at 120 m vs 0.25 before; `0.625^0.6 = 0.728` at 60 m vs 0.625 before. This delivers ~10–17% more force in the 120–20 m band at every speed, with no step change or zone boundary to trigger the Exp 22 lockup. The speed exponent stays at `^2` (quadratic) — the car runs below `ref=250`, so raising the speed exponent would only weaken braking further at current speeds |
| **1. Likely effect on lap time** | Recovery toward the 125–128 s range is plausible. The steeper inner-zone braking should reduce the off-track time at the chicane and V-corner that caused the step-budget overruns in Exp 25–26. Because the suppress window (160 m, 3-beam) is unchanged and the extra force concentrates in the inner 60 m, there is no expected impact on the open-straight approach sections |
| **2. Likely effect on damage/control** | Damage should fall below 23. The `^0.6` curve is a smooth power function — no discontinuity — so the wheels should not lock up as they did in Exp 22's abrupt linear inner zone. More force in the 60–20 m zone gives the car a cleaner, harder stop before each direction change; less overshoot means fewer wall contacts at the chicane exit and V-corner |
| **3. Where you'll notice it** | Most visibly at the V-corner and chicane: the car will visibly brake harder once inside 60–80 m, tracking closer to the road edge rather than running wide. At the 160 m brake boundary the force is `0 × speed_term = 0` regardless of exponent, so the transition onto the brake zone is identical to before — no sudden grab at the outer edge |
| **4. What could make the prediction wrong** | If the `^0.6` exponent is still too steep and causes wheel lockup in the 30–10 m zone (detectable as sudden understeer or the car snapping sideways), raising the exponent to `^0.7` or `^0.75` would soften the inner zone while preserving the outer-zone gain. Conversely, if the chicane and V-corner still have significant overshoot, lowering to `^0.5` (square-root profile) would be the next step. The suppress window (160 m) remains a potential source of false throttle cuts on curved approaches; if the car appears slow in mid-bend sections compared to Exp 25, the suppress window should be pulled back to 120 m in a subsequent experiment |

---

### Experiment 28 — Pull suppress window back and align both windows at `140 m` (zero overlap)
**ID:** `exp28_unified_140`

**Lines changed:** [`snakeoil3_v2.py:544`](snakeoil3_v2.py:544), [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545), [`snakeoil3_v2.py:563`](snakeoil3_v2.py:563), [`snakeoil3_v2.py:564`](snakeoil3_v2.py:564), [`snakeoil3_v2.py:597`](snakeoil3_v2.py:597)
```python
# Before
    # Corner-aware target speed
    forward = min(S['track'][8:11])           # 3-beam ±0.5° — avoids inside-kerb false triggers
    if forward < 160 and S['speedX'] > 80:
        target_speed = 250 * (forward / 160)  # scale denominator matches 160 m suppression window
    else:
        target_speed = 250

    # Brake if a wall is closing in fast ahead (multi-beam, cubic distance × quadratic speed)
    # dist exponent 0.6 concentrates more force in the 60–20 m zone vs pure quadratic distance
    _fwd = min(S['track'][7:12])
    if _fwd < 160 and S['speedX'] > 80:
        R['brake'] = clip(((160 - _fwd) / 160) ** 0.6 * (S['speedX'] / 250) ** 2, 0, 1)

# After
    # Corner-aware target speed
    forward = min(S['track'][8:11])           # 3-beam ±0.5° — avoids inside-kerb false triggers
    if forward < 140 and S['speedX'] > 80:
        target_speed = 250 * (forward / 140)  # scale denominator matches 140 m suppression window
    else:
        target_speed = 250

    # Brake if a wall is closing in fast ahead (multi-beam, cubic distance × quadratic speed)
    # dist exponent 0.6 concentrates more force in the 60–20 m zone vs pure quadratic distance
    _fwd = min(S['track'][7:12])
    if _fwd < 140 and S['speedX'] > 80:
        R['brake'] = clip(((140 - _fwd) / 140) ** 0.6 * (S['speedX'] / 250) ** 2, 0, 1)
```

| | Assessment |
|---|---|
| **Why** | Exp 27 confirmed the `^0.6` distance exponent is working — the lap completed and damage fell — but max speed dropped to 191 km/h (vs 205 km/h in Exp 23) because the 160 m suppress window was triggering throttle cuts on curved approach sections where the 3-beam sensor reads a distant wall. Simultaneously, the 160 m brake trigger was allowing the 5-beam sensor to pick up kerbs at 140–160 m on open bends, applying a small but continuous drag. Reducing both windows to 140 m fixes both problems in one step: (1) the suppress window no longer reaches into the curved approaches where false triggers were cutting speed; (2) the brake trigger no longer fires on distant kerbs at 141–160 m; (3) both windows are identical so there is zero throttle+brake overlap — suppress and brake fire simultaneously at the same 140 m boundary, which is the cleanest possible configuration. The `^0.6` force profile and `ref=250` are unchanged |
| **1. Likely effect on lap time** | Significant improvement over Exp 27 — recovering toward the 125–127 s range. Removing the suppress false triggers on approach curves should restore 5–10 km/h of top speed (from 191 toward 196–200 km/h), which translates directly to faster straights. The zero overlap means the car arrives at each corner with a settled, decelerating chassis rather than fighting simultaneous throttle and brake signals. The `^0.6` inner-zone braking is unchanged, so chicane and V-corner stopping power is preserved |
| **2. Likely effect on damage/control** | Damage should fall below 21. The brake force profile in the 40–20 m zone is essentially unchanged from Exp 27 (see force table in analysis), so the decisive inner stop is preserved. What improves is entry speed: with the suppress firing at exactly the same point as the brake (140 m), `target_speed` is already ramping down from 250 toward 0 as the wall closes in, so the car arrives at the chicane and V-corner entry measurably slower than in Exp 27 |
| **3. Where you'll notice it** | On the main straight — the car should visibly accelerate further before rolling off, recovering the speed lost in Exp 26–27 due to the 160 m suppress false triggers. At the chicane and V-corner the entry should be slightly cleaner than Exp 27 because the suppress now fires alongside the brake rather than 20 m after it, giving the throttle ramp (±0.02/step) a head start on rolling off before the brake force builds |
| **4. What could make the prediction wrong** | The 5-beam brake sensor still spans ±1° — if Corkscrew has a geometry where a side beam reads a wall or kerb at <140 m on an open bend, the brake will still apply lightly there. If the car shows brake drag on open sections that was not present before, the trigger should be pulled back further to 120 m. Also, the suppress and brake are now co-located: if the 3-beam sensor and 5-beam sensor read different distances at the same corner (because one beam sees the wall earlier), there may be a brief window where the brake fires but the suppress has not yet — reducing 140 m by 5–10 m on the suppress only (not the brake) would close that gap if observed |

---

### Experiment 29 — Faster throttle response: `±0.02` → `±0.03` per step
**ID:** `exp29_throttle_ramp_03`

**Lines changed:** [`snakeoil3_v2.py:556`](snakeoil3_v2.py:556), [`snakeoil3_v2.py:558`](snakeoil3_v2.py:558), [`snakeoil3_v2.py:597`](snakeoil3_v2.py:597)
```python
# Before
    # Throttle Control
    if S['speedX'] < target_speed - (R['steer']*50):
        R['accel']+= .02
    else:
        R['accel']-= .02

# After
    # Throttle Control
    if S['speedX'] < target_speed - (R['steer']*50):
        R['accel']+= .03
    else:
        R['accel']-= .03
```

| | Assessment |
|---|---|
| **Why** | Exp 28 confirmed the 140 m unified window is working — `curLapTime` at the step cap improved to 128.1 s and the chicane exit is now clean — but the chicane *entry* still causes significant damage and the V-corner remains problematic. The root cause is throttle-response lag: at 193 km/h, the `±0.02/step` ramp takes 50 steps (1.0 s, ~54 m) to cut from full throttle to zero after the suppress fires at 140 m. That means 54 m of the 140 m suppress window is consumed before `accel` even reaches zero — the car has only 86 m of genuinely settled deceleration before the wall. Raising the ramp to `±0.03` cuts the sweep time to 33 steps (0.67 s, ~36 m), recovering 18 m of effective deceleration window — from 86 m to 104 m. This is the same fix successfully applied in Exp 10 (`±0.01 → ±0.02`), now extended to match the higher operating speeds of the 250 km/h ceiling era. The faster ramp also benefits re-acceleration out of corners: the car builds speed faster on the exits, compounding the lap-time gain |
| **1. Likely effect on lap time** | Meaningful improvement — the step-budget overrun of ~0 s (car was 10 m from finish at step 100,000) should flip to a completed lap, and the lap time should drop toward 125–127 s. The chicane entry, which has been the primary time sink, benefits directly: the car arrives with a lower throttle value because `accel` has had more steps to ramp down over the same 140 m window. Corner exits also benefit from crisper acceleration |
| **2. Likely effect on damage/control** | Damage should fall from 27. The faster deceleration ramp reduces entry speed at the chicane, which is the primary damage source. The faster acceleration ramp carries a small risk of amplifying lateral oscillations if the steering has residual instability at high speed — the same risk that caused the damage spike in Exp 10. However, the current configuration is fundamentally more stable than Exp 10's context: the centre-gain is lower (`0.15` vs `0.20`), the TCS is gated to acceleration only, and the `^0.6` brake profile smoothly manages energy through corners. The structural conditions that made `±0.02` dangerous in Exp 10 no longer apply |
| **3. Where you'll notice it** | Most visibly at the chicane approach — the car will lift throttle more crisply once inside 140 m, arriving at the first direction change with a noticeably lower throttle value. On corner exits the car will accelerate more crisply out of the U-corner and off the chicane. On the main straight the faster ramp means the car reaches its target speed sooner and sustains it longer before the suppress window begins cutting |
| **4. What could make the prediction wrong** | If residual lateral instability at 193 km/h causes left-right weaving, the faster ramp will amplify each correction into a larger throttle chop, recreating the Exp 10 oscillation pattern. This is observable as the car swerving on the straight rather than running straight. If that occurs, the ramp should be kept at `±0.03` for deceleration but capped at `±0.02` for acceleration — though the current code applies the same rate in both directions. Alternatively, the centre-gain could be reduced slightly from `0.15` to `0.12` to counteract the amplification. Also, if the `^0.6` brake profile reacts more aggressively to the higher throttle baseline (the car enters the brake zone with more momentum because it accelerated faster), damage at the V-corner may increase even if the chicane improves |

---

### Experiment 30 — Zone-specific braking for chicane and V-corner
**ID:** `exp30_zone_brake`

**Lines changed:** [`snakeoil3_v2.py:541`](snakeoil3_v2.py:541), [`snakeoil3_v2.py:542`](snakeoil3_v2.py:542), [`snakeoil3_v2.py:543`](snakeoil3_v2.py:543), [`snakeoil3_v2.py:572`](snakeoil3_v2.py:572), [`snakeoil3_v2.py:574`](snakeoil3_v2.py:574), [`snakeoil3_v2.py:602`](snakeoil3_v2.py:602), [`snakeoil3_v2.py:612`](snakeoil3_v2.py:612), [`snakeoil3_v2.py:647`](snakeoil3_v2.py:647)
```python
# Before
# (no zone-aware logic — all braking driven by forward sensor only)

# After — zone boundaries (from find_corners.py lap data)
    dist = S['distFromStart']
    in_chicane_zone = (2300 <= dist <= 2540)   # C9+C10: 2411–2518 m; window opens 110 m early
    in_vcorner_zone = (2830 <= dist <= 3020)   # C14:    2930–3017 m; window opens 100 m early

# After — target speed caps
    if in_chicane_zone:
        target_speed = min(target_speed, 90)   # two direction changes; must arrive slow
    if in_vcorner_zone:
        target_speed = min(target_speed, 100)  # single apex; clean entry onto final straight

# After — zone brake ramps (applied on top of the existing sensor brake via max())
    if in_chicane_zone and S['speedX'] > 60:
        zone_progress = (dist - 2300) / 240.0
        chicane_brake = clip(zone_progress ** 0.4 * (S['speedX'] / 100) ** 2, 0, 1)
        R['brake'] = max(R['brake'], chicane_brake)

    if in_vcorner_zone and S['speedX'] > 60:
        zone_progress = (dist - 2830) / 190.0
        vcorner_brake = clip(zone_progress ** 0.5 * (S['speedX'] / 100) ** 2, 0, 1)
        R['brake'] = max(R['brake'], vcorner_brake)
```

| | Assessment |
|---|---|
| **Why** | Experiments 28–29 established that the sensor-based brake (140 m window, `^0.6` exponent) is still insufficient to tame the chicane (C9+C10, ~2411–2518 m) and V-corner (C14, ~2930–3017 m) reliably. The sensor fires in response to instantaneous forward distance, but both corners are approached from a gradual bend where the wall closes in slowly — the ramp starts late and the car arrives with too much energy. The `find_corners.py` telemetry from exp27 (lap 1, 129.2 s) identifies the exact `distFromStart` ranges of both features. Using those boundaries to activate a position-triggered brake ramp alongside the sensor brake decouples corner-stopping from sensor geometry: the car begins shedding speed a fixed distance before each corner, regardless of how the forward beam angles onto the wall. The `^0.4` exponent for the chicane front-loads force quickly (two tight direction changes demand an early decisive stop); the `^0.5` square-root profile for the V-corner builds more gradually (single apex, needs a steerable, not jerky, approach). Both ramps are floored by the existing sensor brake (`max()`), so they never reduce braking below what the sensor already demands |
| **1. Likely effect on lap time** | Meaningful improvement — the chicane has been the primary damage and time-loss source in every experiment since Exp 17. Arriving at C9 at ≤90 km/h instead of 130+ km/h should eliminate the off-track excursion and allow the counter-turn (C10) to be taken cleanly, saving 2–5 s there alone. The V-corner fix should similarly eliminate the large off-track overshoot that has been losing 3–6 s per lap. Overall improvement of 5–10 s over Exp 29 is plausible, potentially bringing the lap time below 125 s for the first time |
| **2. Likely effect on damage/control** | Damage should drop sharply from 21. The 21 damage units in Exp 29 came from the chicane contact (C9 had `min_fwd = 0.2 m` and `min_valid = 0.1 m` — the car was grazing the wall). With entry speed capped to 90 km/h the car should pass through both chicane direction changes without touching the barriers. The V-corner overshoot has also been a consistent damage source; the earlier stop should keep the car on track through the apex. Risk: if the `^0.4` chicane ramp fires too hard and locks the front wheels, the car may understeer into the C9 wall rather than oversteering through it — detectable as the car tracking wide on entry instead of spinning. If that occurs, raise the exponent to `^0.5` to soften the ramp |
| **3. Where you'll notice it** | Most visibly at the chicane (~2300 m) — the car will start braking noticeably earlier and arrive at the first kerb at walking pace relative to before, tracking cleanly through both direction changes. At the V-corner (~2830 m) the car will also slow earlier, hold a tighter line through C14, and accelerate onto the final straight (S10) from a much better position. On all other sections of the lap behaviour is identical to Exp 29 since both zone flags are false everywhere outside the 2300–2540 m and 2830–3020 m windows |
| **4. What could make the prediction wrong** | The zone boundaries are derived from a single lap (exp27, 129.2 s, 21 damage). If the car's trajectory in this run differs substantially from that reference lap — due to speed changes from Exp 29's faster throttle ramp — the actual chicane entry may occur outside the 2300–2540 m window. If the car still crashes, the window start should be moved earlier (e.g. 2250 m). Conversely, if the 90 km/h cap slows the car too early on the approach straight (which begins at S7, ~2127 m), check whether the car is decelerating before 2300 m; if so, the window start can be moved later to 2350 m. The same logic applies to the V-corner window. Additionally, if the car becomes unstable during recovery after the chicane (between C10 exit at 2518 m and the zone release at 2540 m), widening the release to 2560 m gives more room to stabilise before the sensor brake takes over |

---

### Experiment 31 — Wider brake + suppress window: `140 m` → `180 m`, exponent `^0.6` → `^0.5`
**ID:** `exp31_brake_180m`

> **Note:** Experiment 30 (`exp30_zone_brake`) was rejected and reverted. Result: 144.206 s, 93 damage, 195.2 km/h. The position-triggered zone ramps fired hard braking through the entire chicane transit (including the counter-turn and exit) and applied a 90 km/h speed cap from 2300 m, crippling the approach straight and locking the car through the turns instead of only before them.

**Lines changed:** [`snakeoil3_v2.py:544`](snakeoil3_v2.py:544), [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545), [`snakeoil3_v2.py:561`](snakeoil3_v2.py:561), [`snakeoil3_v2.py:562`](snakeoil3_v2.py:562), [`snakeoil3_v2.py:597`](snakeoil3_v2.py:597)
```python
# Before (exp29 / exp30)
    forward = min(S['track'][8:11])
    if forward < 140 and S['speedX'] > 80:
        target_speed = 250 * (forward / 140)

    _fwd = min(S['track'][7:12])
    if _fwd < 140 and S['speedX'] > 80:
        R['brake'] = clip(((140 - _fwd) / 140) ** 0.6 * (S['speedX'] / 250) ** 2, 0, 1)

# After (exp31)
    forward = min(S['track'][8:11])
    if forward < 180 and S['speedX'] > 80:
        target_speed = 250 * (forward / 180)

    _fwd = min(S['track'][7:12])
    if _fwd < 180 and S['speedX'] > 80:
        R['brake'] = clip(((180 - _fwd) / 180) ** 0.5 * (S['speedX'] / 250) ** 2, 0, 1)
```

| | Assessment |
|---|---|
| **Why** | The `find_corners.py` data shows that at the chicane (C9, 2411 m) the car records `min_fwd = 0.2 m` — the sensor brake fires too late because the chicane wall closes in from an angle and does not register in the 5-beam minimum until the car is already alongside it. At 195 km/h the car covers ~54 m/step; the 140 m window gives only ~2.6 s of braking time. Widening to 180 m adds ~0.74 s (~40 m) of additional runway. Simultaneously, changing the distance exponent from `^0.6` to `^0.5` (square-root) redistributes more braking force into the 120–30 m outer zone: at 60 m from the wall the force rises from `(80/140)^0.6 = 0.72` to `(120/180)^0.5 = 0.82` — 14% more authority exactly where the angled chicane wall needs it. Both the suppress window (throttle) and the brake window move together to 180 m, preserving the zero-overlap principle established in Exp 28. No zone flags, no speed caps, no position logic — the brake fires and releases naturally as the sensor reads short and then clears |
| **1. Likely effect on lap time** | Moderate improvement over exp29 (129.2 s) — the wider window catches the angled chicane wall earlier and provides more braking force through the 60–20 m zone for the V-corner. However, a wider suppress window risks false throttle cuts on wide curves where a side beam reads a kerb at <180 m; if that occurs, the lap time gain may be partially offset by unnecessary slowing on approach curves. Net estimate: 125–129 s |
| **2. Likely effect on damage/control** | Damage should fall from 21. C9 had `min_fwd = 0.2 m` in exp27 — the car was grazing the wall. With 40 m more braking distance and 14% more force at 60 m, the entry speed at C9 should be meaningfully lower, allowing the car to steer through both direction changes without wall contact. The V-corner overshoot should also reduce as the wider window begins shedding speed from 180 m rather than 140 m |
| **3. Where you'll notice it** | At the chicane (~2411 m) — the car will begin braking noticeably earlier on the approach and arrive at the first kerb with less speed. At the V-corner (~2930 m) the car will also track closer to the road edge through the apex. On the main straight the suppress window now fires at 180 m instead of 140 m, so the car may roll off throttle slightly earlier before each corner; if the straight speed drops below 185 km/h, the window should be pulled back to 160 m |
| **4. What could make the prediction wrong** | The 3-beam suppress sensor (`track[8:11]`) spans only ±0.5° — very narrow — so false triggers at 180 m are unlikely unless the track has a wall directly ahead at that distance on a straight. The 5-beam brake sensor (`track[7:12]`, ±1°) is slightly wider; if an inside kerb appears in beam 7 or 11 at <180 m on a gentle curve before the chicane, the brake will apply lightly and bleed time. If max speed drops below 185 km/h compared to exp29's 191 km/h, pull the brake window back to 160 m and test. If the chicane is still unstable at 180 m, the next step is narrowing the brake sensor to 3 beams (`track[8:11]`) to match the suppress sensor, eliminating the ±1° side-beam risk entirely |

---

### Experiment 32 — Restore Exp 17 base + keep 3-beam throttle sensor and TCS gate
**ID:** `exp32_restore_exp17_base`

**Lines changed:** [`snakeoil3_v2.py:544–548`](snakeoil3_v2.py:544), [`snakeoil3_v2.py:557–559`](snakeoil3_v2.py:557), [`snakeoil3_v2.py:566–568`](snakeoil3_v2.py:566), [`snakeoil3_v2.py:601`](snakeoil3_v2.py:601)
```python
# Before (exp31)
    forward = min(S['track'][8:11])
    if forward < 180 and S['speedX'] > 80:
        target_speed = 250 * (forward / 180)
    else:
        target_speed = 250

    if S['speedX'] < target_speed - (R['steer']*50):
        R['accel']+= .03
    else:
        R['accel']-= .03

    _fwd = min(S['track'][7:12])
    if _fwd < 180 and S['speedX'] > 80:
        R['brake'] = clip(((180 - _fwd) / 180) ** 0.5 * (S['speedX'] / 250) ** 2, 0, 1)
    else:
        R['brake'] = 0.0

# After (exp32)
    forward = min(S['track'][8:11])           # 3-beam ±0.5° kept (exp19)
    if forward < 80 and S['speedX'] > 80:
        target_speed = 180 * (forward / 80)   # 80 m window, ceiling 180 (restored from exp17)
    else:
        target_speed = 180

    if S['speedX'] < target_speed - (R['steer']*50):
        R['accel']+= .02                       # ramp restored to ±0.02 (exp10–28 stable value)
    else:
        R['accel']-= .02

    _fwd = min(S['track'][7:12])              # 5-beam ±1° kept for brake safety
    if _fwd < 100 and S['speedX'] > 80:
        R['brake'] = clip((100 - _fwd) / 100 * (S['speedX'] / 180) ** 2, 0, 1)
    else:
        R['brake'] = 0.0
    # TCS gate from exp23 retained unchanged
```

| | Assessment |
|---|---|
| **Why** | Analysis of the full experiment record (Exp 0–31) identified Exp 17 as the only configuration to produce a completed lap with zero damage and the best damage-free time (122.862 s). Every experiment after Exp 17 that changed the speed ceiling above 180 km/h set `ref` to a value (200–250 km/h) far above the car's actual race speed (~190 km/h), which made the quadratic brake formula permanently weak: at 190 km/h with `ref=250` the force factor is `(190/250)² = 0.578` — only 58% of what Exp 17 delivered at the same speed. All subsequent attempts to recover that force through wider windows (`^0.6`, `^0.5` exponents, 160–180 m triggers) could not compensate because the speed term was structurally undersized. Exp 32 returns to `ref=180` so the car is running at approximately its reference speed, making the quadratic profile clip near 1.0 in the critical inner metres and providing the decisive stop the chicane and V-corner need. Two improvements proven since Exp 17 are carried forward: the 3-beam throttle sensor from Exp 19 (prevents inside-kerb false triggers on the chicane approach curves) and the TCS gate from Exp 23 (prevents TCS misfiring during braking) |
| **1. Likely effect on lap time** | Damage-free completed lap in the 120–125 s range. The 3-beam throttle sensor should marginally improve on Exp 17's 122.862 s by reducing unnecessary throttle cuts on approach curves that the 5-beam sensor in Exp 17 triggered |
| **2. Likely effect on damage/control** | Zero damage expected. Exp 17 already demonstrated zero damage with this exact brake formula; the 3-beam throttle sensor only makes the chicane approach calmer (car arrives with a more settled chassis), reducing — not increasing — the damage risk |
| **3. Where you'll notice it** | Everywhere: the car will be running ~10–15 km/h slower on the straights (ceiling 180 vs 250) but braking with full authority through the chicane and V-corner, arriving at each apex at a controllable speed rather than overrunning with half-force brakes. The chicane and V-corner should both be negotiated cleanly within the track boundaries |
| **4. What could make the prediction wrong** | If the car's race speed has increased meaningfully since Exp 17 (e.g. due to the faster throttle ramp from Exp 29 still having a residual effect in the first few steps of a session), the 100 m window may again be slightly undersized. If chicane overshoot recurs, extend the brake window to 110 m before any other change |

---

### Experiment 33 — Match suppress window to brake window: `80 m` → `100 m` (3-beam sensor)
**ID:** `exp33_suppress_100m`

**Lines changed:** [`snakeoil3_v2.py:545–546`](snakeoil3_v2.py:545), [`snakeoil3_v2.py:601`](snakeoil3_v2.py:601)
```python
# Before (exp32)
    forward = min(S['track'][8:11])
    if forward < 80 and S['speedX'] > 80:
        target_speed = 180 * (forward / 80)

# After (exp33)
    forward = min(S['track'][8:11])
    if forward < 100 and S['speedX'] > 80:
        target_speed = 180 * (forward / 100)
```

| | Assessment |
|---|---|
| **Why** | Exp 32 produced three coupled symptoms — side-to-side oscillation, chicane first-apex overshoot, and V-corner overshoot — all traceable to one structural mismatch: the suppress window (80 m) was 20 m smaller than the brake window (100 m). For every braking zone the car was simultaneously applying brake force and maintaining near-full throttle for the first 20 m (from 100 m down to 80 m), arriving at each apex hotter and with more lateral momentum than the steering could smoothly handle. Raising the suppress to 100 m closes that gap: throttle begins ramping down the instant the brake force begins building, giving the car a settled, decelerating chassis through the entire 100 m window. The 3-beam sensor (±0.5°) is kept — this is the critical difference from Exp 18, which failed the same 100 m suppress attempt because it used the 5-beam sensor that triggered on inside kerbs along the curved approach before the chicane |
| **1. Likely effect on lap time** | Damage-free completed lap in the 120–125 s range; marginal improvement over Exp 32's expected time because the car now arrives at the chicane and V-corner with less speed and less lateral momentum |
| **2. Likely effect on damage/control** | Oscillation eliminated or greatly reduced — the throttle+brake overlap was feeding extra lateral energy into the steering loop every braking zone; removing it breaks that feedback. Zero or near-zero damage expected |
| **3. Where you'll notice it** | Everywhere the car was weaving: the oscillation should smooth out on the main straight and on curved approaches. At the chicane the first direction change should be taken cleanly. At the V-corner the car should begin rolling off throttle 20 m earlier, arriving at turn-in more slowly |
| **4. What could make the prediction wrong** | If the 3-beam sensor triggers on a wall directly ahead at 90–100 m on any wide bend (not a kerb, but an actual wall in the central ±0.5° window), throttle will be suppressed unnecessarily there. If max speed drops below 175 km/h, pull the suppress window back to 90 m. If chicane instability persists despite the overlap being closed, the cause is entry speed rather than throttle dynamics, and the brake window should be extended to 110 m |

---

### Experiment 34 — Zone centre-tracking gain: flat `0.15` → `0.17` on critical approaches
**ID:** `exp34_zone_centre_gain`

**Lines changed:** [`snakeoil3_v2.py:553`](snakeoil3_v2.py:553)–[`561`](snakeoil3_v2.py:561), [`snakeoil3_v2.py:601`](snakeoil3_v2.py:601)
```python
# Before
    R['steer']-= S['trackPos']*.15

    EXPERIMENT_ID = "exp33_suppress_100m"

# After
    # Steer To Center — zone-boosted centre gain (exp34)
    # 0.17 on chicane approach (2300–2500 m) and V-corner approach (2700–2830 m)
    # to correct lateral drift before each critical direction change; 0.15 everywhere else.
    dist = S['distFromStart']
    if 2300 <= dist <= 2500 or 2700 <= dist <= 2830:
        centre_gain = 0.17
    else:
        centre_gain = 0.15
    R['steer'] -= S['trackPos'] * centre_gain

    EXPERIMENT_ID = "exp34_zone_centre_gain"
```

| | Assessment |
|---|---|
| **Why** | Exp 33 showed that closing the suppress-brake overlap (80 → 100 m) did not eliminate off-track excursions at the chicane or V-corner. Analysis of the Exp 32–33 logs identified a secondary factor: the car arrives at both sections with residual lateral offset — not perfectly centred on the racing line when it begins braking. With a marginally stronger centring correction (0.17 on those approach zones vs a flat 0.15), the car enters the first apex of each section from a more neutral lateral position |
| **1. Likely effect on lap time** | Marginal — ~2 s recovery vs Exp 33 (124.6 s → ~122–123 s); no effect on the rest of the circuit because the change is position-gated |
| **2. Likely effect on damage/control** | Improvement from 20 to ~15 units expected; the car enters the apex squarely instead of already carrying established lateral momentum |
| **3. Where you'll notice it** | On the chicane approach (2300–2500 m) and on the V-corner approach (2700–2830 m) — the car should trace a straighter line for 200 m before each critical section |
| **4. What could make the prediction wrong** | If the stronger centring correction interferes with yaw response at the apex itself, it could destabilise the turn rather than settle it. If damage rises or max speed drops, the gain increase is activating too early on the approach |

---

### Experiment 35 — Extend distance sensor coverage: arc ±45° → ±90°
**ID:** `exp35_sensor_90deg`

> **Note:** From this experiment onward, the heuristic forward-suppression driving system (exp34) is abandoned and a full rewrite of `drive_example()` begins in successive stages. Exp 35 is the first step: extending the sensor arc to give the car complete lateral and rear visibility, a prerequisite for the dynamic racing line and trail brake introduced in subsequent experiments.

**Lines changed:** [`exp35_working/snakeoil3_v2.py:163`](exp35_working/snakeoil3_v2.py:163)
```python
# Before (exp34_zone_centre_gain)
a= "-45 -19 -12 -7 -4 -2.5 -1.7 -1 -.5 0 .5 1 1.7 2.5 4 7 12 19 45"

# After (exp35_sensor_90deg)
a = "-90 -45 -20 -10 -7 -4 -2 -1 -.5 0 .5 1 2 4 7 10 20 45 90"

    EXPERIMENT_ID = "exp35_sensor_90deg"
```

| | Assessment |
|---|---|
| **Why** | The previous sensor configuration (±45°) left the car's flanks blind. The steering-coupled trail brake (planned for exp37) needs to read how much the steering wheel turns relative to the lateral distance to the edge; without ±90° beams that calculation has no physical anchor. Additionally, `min_valid_track` — the minimum of the 19 beams — only represents the true distance to the nearest edge when the beams cover the full arc. With ±45° the car could brush a lateral wall without any beam detecting it. |
| **1. Likely effect on lap time** | Marginal in pure time (0–1 s): the sensor angle change does not alter control logic as long as the exp34 code continues reading the same indices (7–11 for braking, 8–10 for suppression). Lap time should remain around 122–124 s. |
| **2. Likely effect on damage/control** | Damage should not worsen. The car will have better lateral information but the control logic does not yet exploit it — the real benefit will materialise when the trail brake (exp37) and dynamic racing line (exp38) are introduced. |
| **3. Where you'll notice it** | The visible difference is in telemetry: `min_valid_track` will now reflect the true nearest edge rather than a minimum restricted to ±45°. At T4 and T11, where the car approaches the lateral boundary, the value will drop earlier and give more precise diagnostics. |
| **4. What could make the prediction wrong** | If the exp34 logic reads indices that have shifted when the number of beams changes (the angles are different but the array remains 19 elements), the brake or suppression could fire at incorrect moments. Verify on the first lap that indices 7–11 still correspond to ±1° and ±0.5°. |

---

### Experiment 36 — Target speed system: forward suppression → physical zone table
**ID:** `exp36_zone_speed_map`

**Lines changed:** [`exp35_working/snakeoil3_v2.py:565–587`](exp35_working/snakeoil3_v2.py:565)
```python
# Before (exp35_sensor_90deg — heuristic suppression system)
forward = min(S['track'][8:11])
if forward < 80 and S['speedX'] > 80:
    target_speed = 180 * (forward / 80)
else:
    target_speed = 180

# After (exp36_zone_speed_map — physical zone table)
if   341  <= dist <  414:  target_speed =  93  # T1 apex (r=86.5m)
elif 200  <= dist <  341:  target_speed = 110  # T1 braking approach
elif 406  <= dist <  545:  target_speed =  52  # T2 Hairpin (r=24m, adverse banking)
elif 340  <= dist <  406:  target_speed =  80  # T2 braking (downhill -2.7%)
elif 675  <= dist <  828:  target_speed =  70  # T3 braking+apex (r=44.2m)
elif 945  <= dist < 1105:  target_speed =  85  # T4 braking+apex (r=76.9m)
elif 1440 <= dist < 1648:  target_speed =  72  # T5 braking+apex (r=48m, banking -5°)
elif 1840 <= dist < 1952:  target_speed =  75  # T6 braking on Rahal Straight
elif 1952 <= dist < 1984:  target_speed =  60  # T6 apex (r=33.6m, banking -6°)
elif 2313 <= dist < 2456:  target_speed =  65  # T8 braking
elif 2456 <= dist < 2520:  target_speed =  38  # T8 Corkscrew LH (r=11.5m, EXTREME)
elif 2520 <= dist < 2578:  target_speed =  38  # T8A Corkscrew RH (r=14.4m, EXTREME)
elif 2578 <= dist < 2701:  target_speed =  80  # Post-Corkscrew descent
elif 2701 <= dist < 2825:  target_speed =  85  # T9 Rainey (r=75m, banking -7°)
elif 2920 <= dist < 3063:  target_speed =  80  # T10 braking+apex (r=57.6m, banking +6°)
elif 3188 <= dist < 3291:  target_speed =  75  # T11 braking
elif 3291 <= dist < 3422:  target_speed =  50  # T11 apex (r=18.3m)
else:                      target_speed = 180  # Straights and transitions

    EXPERIMENT_ID = "exp36_zone_speed_map"
```

| | Assessment |
|---|---|
| **Why** | Exp 34 produced its best time (122.654 s) but with residual damage of 23 units, all concentrated at T4 and T11. The root of the problem is structural: the forward suppression system calculates `target_speed` based on the distance to the wall ahead, which works well on straight sections with a frontal wall but fails on corners where the dangerous wall is on the inside (T4, T3, T11). The reference manual telemetry proves that T4 needs `≤70 km/h` (physical v_max = 72.6 km/h) and T11 needs `≤55 km/h` (physical v_max = 44.8 km/h). A zone table based on `distFromStart` and real radii eliminates that dependency and allows each corner to be calibrated with its correct physics. |
| **1. Likely effect on lap time** | Moderate: expected between 145–155 s in the first steady-state laps. The time loss vs 122 s is the cost of conservative safety margins (T4=85, Corkscrew=38, T11=50). The goal of this stage is not lap time but zero damage over multiple consecutive laps. |
| **2. Likely effect on damage/control** | Zero damage expected. Each corner receives exactly the speed its minimum radius allows. The Corkscrew (T8/T8A) drops to 38 km/h with physical certainty rather than depending on when the sensor detects the wall. |
| **3. Where you'll notice it** | T4 (~945–1105 m): the car drops to 85 km/h with certainty — it will not go off the right edge. Corkscrew T8/T8A (2456–2578 m): smooth descent to 38 km/h before the drop. T11 (3291–3422 m): the car arrives at the apex at ~50 km/h instead of 80+ km/h. On the S/F straight the car accelerates freely (target=180 km/h). |
| **4. What could make the prediction wrong** | If the braking zones do not start early enough before the apex (e.g. the T4 zone begins at 945 m but the car is already in the corner at that distance travelling at 150+ km/h), the overspeed brake based on `speed_error` will not have enough distance to shed speed. In that case the approach zone must be extended further back. |

---

### Experiment 37 — Brake system: quadratic 100 m/ref=180 → steering-coupled trail brake D=150/vref=160
**ID:** `exp37_trail_brake`

**Lines changed:** [`exp35_working/snakeoil3_v2.py:638–644`](exp35_working/snakeoil3_v2.py:638)
```python
# Before (exp36_zone_speed_map — heuristic quadratic brake)
_fwd = min(S['track'][7:12])
if _fwd < 100 and S['speedX'] > 80:
    R['brake'] = clip((100 - _fwd) / 100 * (S['speedX'] / 180) ** 2, 0, 1)
else:
    R['brake'] = 0.0

# After (exp37_trail_brake — trail brake with steering-angle reduction factor)
_fwd = min(trk[7:12])   # indices 7-11: ±1°, ±0.5°, 0°
if _fwd < 150 and spd > 80:
    base_brake = clip((150 - _fwd) / 150 * (spd / 160) ** 2, 0, 1)
    trail_factor = clip(1.0 - abs(R['steer']) * 0.8, 0.0, 1.0)
    R['brake'] = base_brake * trail_factor
else:
    R['brake'] = 0.0

    EXPERIMENT_ID = "exp37_trail_brake"
```

| | Assessment |
|---|---|
| **Why** | The 100 m/ref=180 quadratic brake was designed for the heuristic suppression system (exp17–exp34). With the exp36 physical zone table, the car already reduces speed via `speed_error` before entering each zone; the sensor brake becomes the second safety layer against unexpected obstacles. Widening the window to 150 m with vref=160 km/h gives the brake more runway at circuit speeds (~180 km/h), while the `trail_factor` (proportional reduction by steering angle) prevents the brake from generating understeer at the apex: at full steering lock (steer=1) brake force is reduced to 0.2, allowing the car to turn without penalty. |
| **1. Likely effect on lap time** | Marginal in pure time (0–2 s over exp36): the trail brake only acts when the sensor detects a wall within 150 m, which on this circuit occurs mainly at the Corkscrew and T11. The primary effect is stability and damage. |
| **2. Likely effect on damage/control** | Any residual damage from exp36 (if caused by entering a zone too fast) should disappear. The `trail_factor` produces cleaner apex control — the car can begin braking before the vertex and release it progressively while turning, replicating real trail-braking technique. |
| **3. Where you'll notice it** | Corkscrew T8 (2313–2456 m): the sensor brake fires before the drop and eases while the car turns left. T11 (3188–3291 m): the brake acts through the arc with force proportional to residual `speedX`. T3 (~714 m): the reactive brake confirms the zone when the radius tightens at s12-2. |
| **4. What could make the prediction wrong** | If `trail_factor` reduces braking too much at the Corkscrew entry (the car turns before the apex), the car could reach the T8 tirewall with excessive speed. Verify that the T8 apex speed is ≤42 km/h. If it exceeds that value, reduce the trail coefficient from 0.8 to 0.6. |

---

### Experiment 38 — Racing line system: flat centring → dynamic zone-based target_trackPos
**ID:** `exp38_racing_line`

**Lines changed:** [`exp35_working/snakeoil3_v2.py:595–612`](exp35_working/snakeoil3_v2.py:595)
```python
# Before (exp37_trail_brake — flat centring toward trackPos=0)
dist = S['distFromStart']
if 2300 <= dist <= 2500 or 2700 <= dist <= 2830:
    centre_gain = 0.17
else:
    centre_gain = 0.15
R['steer'] -= S['trackPos'] * centre_gain

# After (exp38_racing_line — dynamic racing line with zone-based target_trackPos)
if   200  <= dist <  341:  target_tp =  0.5   # T1 approach: go right for left turn
elif 341  <= dist <  414:  target_tp = -0.5   # T1 apex: cut left
elif 340  <= dist <  545:  target_tp =  0.5   # T2 approach+apex: far right entry
elif 545  <= dist <  675:  target_tp = -0.4   # T3 approach: move left for right turn
elif 675  <= dist <  828:  target_tp =  0.4   # T3 braking+apex: move right (cut right)
elif 828  <= dist <  945:  target_tp = -0.4   # T4 approach: move left
elif 945  <= dist < 1105:  target_tp =  0.4   # T4 braking+apex: move right (cut right)
elif 1105 <= dist < 1440:  target_tp =  0.3   # T5 approach
elif 1440 <= dist < 1648:  target_tp = -0.4   # T5 braking+apex: cut left
elif 1840 <= dist < 1984:  target_tp =  0.5   # T6 approach+apex
elif 1984 <= dist < 2313:  target_tp =  0.0   # Corkscrew approach: center
elif 2313 <= dist < 2456:  target_tp =  0.5   # T8 braking: far right
elif 2456 <= dist < 2578:  target_tp = -0.5   # T8 LH+T8A: left
elif 2701 <= dist < 2825:  target_tp =  0.4   # T9 Rainey: entry right
elif 2825 <= dist < 2920:  target_tp = -0.4   # T10 approach: move left
elif 2920 <= dist < 3063:  target_tp =  0.4   # T10 braking+apex: move right
elif 3188 <= dist < 3422:  target_tp =  0.5   # T11 approach+apex: far right entry
else:                      target_tp =  0.0   # Straights: center

R['steer'] -= (S['trackPos'] - target_tp) * 0.15

    EXPERIMENT_ID = "exp38_racing_line"
```

| | Assessment |
|---|---|
| **Why** | Exp 34 demonstrated that centring the car at `trackPos=0` everywhere on the circuit was sub-optimal: the car arrived at T4 from the centre (target 0.0) instead of from the left (target −0.4), losing the correct attack angle for the right-hand corner. With dynamic `target_trackPos` the car positions its nose on the optimal entry line for each corner — outside approach, inside apex — without modifying the brake or speed logic. |
| **1. Likely effect on lap time** | Moderate: 3–8 s improvement over exp37 from cleaner apex lines at T4, T9, T11, and the Corkscrew. The car covers less distance through each corner (geometrically shorter arc) and exits the apex better positioned for acceleration. |
| **2. Likely effect on damage/control** | Damage should remain at zero. The risk is that a poorly calibrated `target_tp` (inverted sign) could drive the car to the inside edge of a right-hand corner — verify at T3 and T4 that `trackPos` maximum does not exceed +0.8 at the apex. |
| **3. Where you'll notice it** | T4 (~828–1105 m): the car enters from the left (−0.4) and cuts the apex from the right (+0.4) — classic right-hand corner line. T11 (3188–3422 m): the car positions itself on the right outside (+0.5) before cutting the left apex. Corkscrew T8 (2313–2456 m): the car targets the right outside (+0.5) for the late-apex line of the drop. |
| **4. What could make the prediction wrong** | If the correction gain `0.15` is insufficient to follow the `target_tp` at straight-line speeds (the car does not reach the target value before the apex), the racing line will be only partial and the benefit reduced. In that case increase the gain to `0.18`–`0.20` in the approach zones. |

---

### Experiment 39 — Steering system: asymmetric turn_bias + racing-line correction; remove steer×50 acceleration penalty
**ID:** `exp39_steer_turn_bias`

**Lines changed:** [`exp35_working/snakeoil3_v2.py:620–631`](exp35_working/snakeoil3_v2.py:620), [`exp35_working/snakeoil3_v2.py:649–652`](exp35_working/snakeoil3_v2.py:649)
```python
# Before (exp38_racing_line — steering and throttle)
R['steer'] = S['angle'] * 10 / PI + 0  # no turn_bias
R['steer'] -= (S['trackPos'] - target_tp) * 0.15

if spd < target_speed - (R['steer'] * 50):
    R['accel'] += 0.02
else:
    R['accel'] -= 0.02

# After (exp39_steer_turn_bias — turn_bias + racing-line correction; throttle without penalty)
side_L = trk[4]   # -7° beam
side_R = trk[14]  # +7° beam
asym   = (side_R - side_L) / max(side_L + side_R, 1.0)
turn_bias = asym * 0.05

R['steer'] = S['angle'] * 10 / PI + turn_bias
R['steer'] -= (S['trackPos'] - target_tp) * 0.15

if spd < target_speed:
    R['accel'] += 0.02
else:
    R['accel'] -= 0.02

    EXPERIMENT_ID = "exp39_steer_turn_bias"
```

| | Assessment |
|---|---|
| **Why** | The `steer*50` acceleration penalty reduced effective `target_speed` by ~25 km/h every time the steering wheel was at half travel. In exp34 this manifested as a car that never reached 180 km/h on the straights because the racing-line correction (gain 0.15 × trackPos error) generated a steer value sufficient to activate the penalty. The `turn_bias` introduces turn anticipation using the ±7° beam asymmetry (idxs 4 and 14): when the distance to the right edge is greater than to the left, the car is already entering a left-hand turn and the `turn_bias` tilts the steering wheel gently before the body `angle` requires it. The 0.05 scale is conservative — it avoids straight-line oscillation. |
| **1. Likely effect on lap time** | Moderate: 5–12 s improvement over exp38. Removing `steer*50` allows the car to reach 175–180 km/h on the straights (currently capped at ~160 km/h by the penalty). The `turn_bias` smooths response on large-radius corners (T3, T9), reducing late corrections and kerb-scrape micro-damage. |
| **2. Likely effect on damage/control** | Damage should remain at zero. Without the acceleration penalty, the car enters T4 and T11 with more residual speed — verify that the overspeed brake (layer 2) acts before the apex. If damage appears at T4, the fix is to reduce the T4 `target_speed` from 85 to 70 km/h (physically documented correction in the reference manual). |
| **3. Where you'll notice it** | S/F straight (0–257 m) and post-T4 (1105–1413 m): max speed rises from ~165 km/h to ~175–180 km/h — cleaner acceleration without inexplicable dips from residual steer. Open corners T3 (666–828 m) and T9 (2667–2791 m): the car begins to turn earlier with `turn_bias`, less lateral oscillation on exit. |
| **4. What could make the prediction wrong** | If `asym * 0.05` amplifies a spurious asymmetry on a straight (e.g. a lateral kerb at 60 m catching a ±7° beam), the car could develop a tendency to drift on the S/F straight. Verify that `trackPos` on the main straight does not exceed ±0.2. If it exceeds that threshold, reduce the turn_bias coefficient from 0.05 to 0.03. |

---
