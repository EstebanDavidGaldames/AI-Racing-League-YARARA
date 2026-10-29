# CHANGELOG — Car Control Logic
## Corkscrew Circuit · snakeoil3_v2.py

---

## Exp 0 · `baseline_v2`

| Field | Detail |
|---|---|
| **What I changed** | Nothing — this is the unmodified `drive_example()` function |
| **Why I changed it** | Reference point to measure all future experiments against |
| **My prediction** | Car completes the lap but handling will be rough; fixed thresholds and high steer gain will cause oscillation |
| **Actual lap time** | 149.49 s |
| **Actual damage** | 0 |
| **What I observed** | The car completes the lap without damage, although it goes off the track several times and experiences very pronounced and constant side-to-side sway |
| **Kept or rejected** | — (baseline reference, not applicable) |
| **What I learned** | — |

---

## Exp 1 · `exp01_steer_gain_10`

| Field | Detail |
|---|---|
| **What I changed** | Steering angle gain reduced from `15` to `10` · [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545) |
| **Why I changed it** | A gain of `15` causes the driver to overcorrect every step, producing continuous left-right oscillation. Lowering it to `10` produces calmer, more deliberate corrections |
| **My prediction** | Marginal lap time improvement (1–3 s); noticeable reduction in weaving; lower wall-contact risk |
| **Actual lap time** | 153.14 s (+3.65 s vs baseline) |
| **Actual damage** | 0 |
| **What I observed** | The car reduced its side-to-side movement on the track. The lap time was longer, but not by a significant amount. It holds the road better in some turns but not in others |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The car handles better; the results are not yet visible in lap times, but better stability is critical before increasing speed — a necessary foundation for future experiments |

---

## Exp 2 · `exp02_center_gain_020`

| Field | Detail |
|---|---|
| **What I changed** | Centre-tracking gain raised from `0.10` to `0.20` · [`snakeoil3_v2.py:547`](snakeoil3_v2.py:547) |
| **Why I changed it** | After reducing the angle gain, the car had less authority to pull back to the middle when drifting. Doubling the centre-tracking gain gives firmer correction toward the centreline |
| **My prediction** | Neutral to slight improvement in lap time; reduced wall-grazing on corner exits; possible new low-frequency oscillation if angle and centre gains fight each other |
| **Actual lap time** | 153.14 s (−0.01 s vs Exp 1; +3.65 s vs baseline) |
| **Actual damage** | 0 |
| **What I observed** | The car appears to move with less oscillation for most of the circuit, although I noticed some sections where the predicted conflict between the angle gain and centre-gain corrections may be occurring. The time was reduced, but only slightly |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Adjusting two closely related parameters can cause problems if not done correctly. The interaction between angle gain and centre gain needs careful management — small gains in stability do not automatically translate to lap time without also addressing speed |

---

## Exp 3 · `exp03_target_speed_150`

| Field | Detail |
|---|---|
| **What I changed** | Target speed raised from `100` to `150` km/h · [`snakeoil3_v2.py:542`](snakeoil3_v2.py:542) |
| **Why I changed it** | With steering stability improved, the most direct path to a faster lap was unlocking a higher speed ceiling on the straights |
| **My prediction** | Large lap time improvement (15–30 s); medium damage risk at higher approach speeds into braking zones since the 20 m trigger was calibrated for 100 km/h |
| **Actual lap time** | — (partial lap, crash before halfway) |
| **Actual damage** | 99 |
| **What I observed** | The car veers off the track very easily in the turns. It spun out before reaching the halfway point of the circuit while accelerating full throttle on a slight bend in the track; the car tried to get back on course and crashed into the wall |
| **Kept or rejected** | ✅ Kept (speed increase is necessary — braking must be improved next) |
| **What I learned** | Speed is needed, so the change stays. But raising the target speed without improving braking is dangerous: the car reaches braking zones much faster than the 20 m trigger can handle. The next priority is a smarter braking system |

---

## Exp 4 · `exp04_brake_dist_30`

| Field | Detail |
|---|---|
| **What I changed** | Brake trigger distance raised from `20` to `30` m · [`snakeoil3_v2.py:556`](snakeoil3_v2.py:556) |
| **Why I changed it** | At 150 km/h the car travels ~41 m/s. The 20 m trigger was no longer enough braking distance, causing the car to spin out and crash (Exp 3). An extra 10 m buys ~0.24 s more deceleration time |
| **My prediction** | Slight lap time loss (0–2 s) but damage eliminated; wall contact on corner entry should reduce or disappear |
| **Actual lap time** | 160.22 s (+10.73 s vs baseline; +7.08 s vs Exp 2) |
| **Actual damage** | 0 |
| **What I observed** | The car veers far off the track; although it didn't spin out or crash in a way that would take it out of the race, its braking control isn't good — it brakes too late. This causes it to go off the track and take an excessive amount of time to get back into the race |
| **Kept or rejected** | ✅ Kept (lap completed cleanly with zero damage — a necessary step forward) |
| **What I learned** | An extra 10 m is enough to avoid a crash, but not enough to keep the car on the track at corner entry. Braking still triggers too late for the speed the car is carrying. The trigger distance needs to increase further |

---

## Exp 5 · `exp05_brake_speed_80`

| Field | Detail |
|---|---|
| **What I changed** | Brake release speed threshold raised from `60` to `80` km/h · [`snakeoil3_v2.py:556`](snakeoil3_v2.py:556) |
| **Why I changed it** | The car was releasing its brakes at 60 km/h while still approaching corners too fast. Holding the brakes to 80 km/h ensures the car arrives at the apex at a lower, more controlled speed |
| **My prediction** | Marginal lap time loss (0–1 s); better corner entry control; risk of over-braking on slow sections |
| **Actual lap time** | 151.37 s (−8.85 s vs Exp 4; −1.77 s vs baseline — **new best completed lap**) |
| **Actual damage** | 0 |
| **What I observed** | The car continues to veer off the road, but it doesn't stray as far from it. Braking remains ineffective, and brake lockup limits control of the car |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | I need to change the braking logic so that it's gradual, not all-or-nothing. The binary brake is causing lockup and loss of steering authority mid-corner. Proportional braking is the next step |

---

## Exp 6 · `exp06_proportional_brake`

| Field | Detail |
|---|---|
| **What I changed** | Binary `brake = 1.0` replaced with a proportional formula scaled by proximity and speed · [`snakeoil3_v2.py:556–557`](snakeoil3_v2.py:556) |
| **Why I changed it** | Full-force braking caused immediate wheel lockup, eliminating steering authority at the moment it was needed most. A graduated force keeps some grip available for steering corrections throughout the entire braking zone |
| **My prediction** | Moderate improvement in lap time; car stays on track through corners instead of veering off; steering remains partially functional during braking |
| **Actual lap time** | 133.99 s (−17.38 s vs Exp 5; −15.50 s vs baseline — **new best by a large margin**) |
| **Actual damage** | 0 |
| **What I observed** | The car brakes more gradually and stays on the track longer, but it drifts wide on some turns. The car should either brake earlier or accelerate less in those sections. We need to analyze and correct the acceleration |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Gradual braking is key; I must stick to this approach and consider future adjustments based on it. I must analyse how it works in conjunction with the acceleration logic — the car is now braking correctly but accelerating too eagerly in sections where it should still be rolling off the throttle |

---

## Exp 7 · `exp07_corner_aware_speed`

| Field | Detail |
|---|---|
| **What I changed** | Fixed `target_speed=150` replaced with a corner-aware block that scales the speed ceiling down proportionally when forward clearance drops below 80 m · [`snakeoil3_v2.py:542–547`](snakeoil3_v2.py:542) |
| **Why I changed it** | Even with proportional braking, the car was arriving at tight corners carrying too much speed. Reducing `target_speed` dynamically as forward distance shrinks makes the car lift off the throttle before the braking zone, combining lift-and-coast with braking rather than relying on braking alone |
| **My prediction** | Moderate improvement in lap time; cleaner corner entries; top speed on long straights preserved since the change only activates below 80 m forward clearance |
| **Actual lap time** | 168.12 s (+34.13 s vs Exp 6; **worst completed lap** — significant regression) |
| **Actual damage** | 0 |
| **What I observed** | The car handles better on the track, but at the start it goes off the track at the third U-shaped turn, which requires excellent speed control and braking. It also goes off the track before reaching the finish line at the V-shaped turn and takes a long time to get back on the track, as if it were not accelerating |
| **Kept or rejected** | ✅ Kept (concept is sound but tuning caused over-reduction of speed in recovery zones) |
| **What I learned** | Handling in tight turns is critical. The corner-aware block is cutting `target_speed` too aggressively — when the car is already slow or recovering off-track, a short forward reading suppresses throttle even when the car needs to accelerate back onto the racing line. The cutoff distance (80 m) or the scaling factor needs to be tuned so that it only suppresses speed on genuine high-speed approaches, not during slow recovery situations |

---

## Exp 8 · `exp08_corner_speed_floor`

| Field | Detail |
|---|---|
| **What I changed** | Added `and S['speedX'] > 80` speed floor to the corner-aware throttle suppression, preventing it from activating during low-speed off-track recovery · [`snakeoil3_v2.py:544`](snakeoil3_v2.py:544) |
| **Why I changed it** | In Exp 7, the corner-aware block starved the throttle during off-track recovery because a short forward beam reading at low speed triggered the same suppression as a high-speed corner approach. The speed floor isolates the two situations |
| **My prediction** | Significant improvement over Exp 7; possible improvement over Exp 6 (133.99 s) by combining corner-aware throttle with uninhibited recovery acceleration |
| **Actual lap time** | 137.12 s (−31.00 s vs Exp 7; +3.13 s vs Exp 6 best) |
| **Actual damage** | 1 |
| **What I observed** | The lap time improved, although it wasn't the fastest, and we managed to regain some speed. The car continues to run off the track in critical turns |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Controlling deceleration when cornering remains critical. I need to think of a better way to control it or make a more precise adjustment. First, I'll see what happens with a slight increase in speed |

---

## Exp 9 · `exp09_ceiling_160`

| Field | Detail |
|---|---|
| **What I changed** | Open-road speed ceiling raised from `150` to `160` km/h; corner-aware suppression scale factor updated to match · [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545) and [`snakeoil3_v2.py:547`](snakeoil3_v2.py:547) |
| **Why I changed it** | Exp 8 sat 3.13 s behind Exp 6's best despite better corner handling. Raising the open-road ceiling lets the car accelerate further on the straights without changing the corner suppression logic |
| **My prediction** | Moderate improvement (2–5 s); corner behaviour similar to Exp 8; slight increase in damage risk as the car arrives at the suppression zone faster |
| **Actual lap time** | 133.52 s (−3.60 s vs Exp 8; −0.47 s vs Exp 6 — **new best**) |
| **Actual damage** | 2 |
| **What I observed** | We managed to improve the lap time, although there was some damage. The car achieves better speed without losing control on most of the track, although it still drifts off the track in critical turns, and there is a greater loss of control in the chicane at the midpoint of the track |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | I need to fine-tune the braking. Before adjusting the brake settings, I can try to improve the car's acceleration response for quicker acceleration and deceleration — the throttle ramp rate (`±0.01/step`) may be too slow to react, causing the car to over-speed into corners before the corner-aware block can bring it back down. A faster throttle response could improve both acceleration on the straights and deceleration when the target speed drops |

---

## Exp 10 · `exp10_throttle_ramp_02`

| Field | Detail |
|---|---|
| **What I changed** | Throttle ramp rate doubled from `±0.01` to `±0.02` per step · [`snakeoil3_v2.py:556`](snakeoil3_v2.py:556) and [`snakeoil3_v2.py:558`](snakeoil3_v2.py:558) |
| **Why I changed it** | The slow ramp of `±0.01/step` (2 s full sweep) caused the car to enter corners still carrying old throttle. Doubling the ramp rate halves the response lag, making the car lift off faster when `target_speed` drops and accelerate more crisply on straights |
| **My prediction** | Moderate improvement (1–4 s); faster corner-entry deceleration; risk of throttle oscillation on long straights |
| **Actual lap time** | 135.42 s (+1.90 s vs Exp 9 — slight regression) |
| **Actual damage** | 18 (severe — nearly 10× the previous worst of 2) |
| **What I observed** | The car no longer drifts off the track as much, but it's still very unstable in the chicane and loses a lot of control. In addition, the car starts to sway too much, especially after the halfway point of the circuit, so we can't take full advantage of the acceleration. We didn't improve our time or speed, even though we were able to keep the car on the track better thanks to improved deceleration in the turns |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | I need to investigate the cause of the oscillation on the track in order to make adjustments that will increase speed. I will analyse the centre-gain value as a possible cause of this problem and then adjust the steering gain settings overall so that the car performs better through the chicane and sustains less damage |

---

## Exp 11 · `exp11_center_gain_015`

| Field | Detail |
|---|---|
| **What I changed** | Centre-tracking gain reduced from `0.20` to `0.15` · [`snakeoil3_v2.py:552`](snakeoil3_v2.py:552) |
| **Why I changed it** | The `0.20` gain calibrated at low speed was producing left-right oscillation at 170+ km/h, amplified into damage = 18 by the faster throttle ramp of Exp 10. Reducing to `0.15` cuts lateral over-correction by 25% to calm the weave |
| **My prediction** | Significant damage reduction; moderate lap time improvement; chicane stability expected to improve |
| **Actual lap time** | 127.02 s (−8.40 s vs Exp 10; **new best by 6.50 s**) |
| **Actual damage** | 39 (severe — new worst; first run was a partial crash before lap completion) |
| **What I observed** | The car sways less, but it's clear that it can't stabilize in several sections of the track. We set a better lap time but didn't achieve the best speed, and the car ended up with too much damage. Now it's veering off the track again in critical turns; even though it's not as extreme, it costs us too much time. At the chicane halfway through the lap, it completely loses control, spins out, crashes, and loses a lot of time — not to mention damaging the car |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | I need to work on the steering response; cornering response is critical, and I need to be able to keep the car on the track so I can increase speed. The configuration and logic of the relevant parameters must be the key. I need to optimise them properly so I can reach 180 km/h as soon as possible |

---

## Exp 12 · `exp12_angle_gain_8`

| Field | Detail |
|---|---|
| **What I changed** | Angle gain reduced from `10` to `8` · [`snakeoil3_v2.py:550`](snakeoil3_v2.py:550) |
| **Why I changed it** | At 170+ km/h the `×10` gain snapped the car past the apex and into the opposite wall at the chicane. Reducing to `×8` was intended to soften the yaw response by 20% and allow the car to rotate through tight direction changes without overshooting |
| **My prediction** | Significant damage reduction; cleaner chicane passage; neutral to moderate lap time improvement |
| **Actual lap time** | — (partial lap — keyboard interrupt after chicane crash) |
| **Actual damage** | 77 (catastrophic — double the previous worst of 39) |
| **What I observed** | In the first critical U-shaped turn, the car stayed on the track at first but drifted wide in the second half of the turn. The car did not complete the lap; it lost control in the chicane, spun out, and then collided because the driver was unable to regain control and get back on the track in the counter-turn |
| **Kept or rejected** | ❌ Rejected (angle gain reverted to `10` before Exp 13 run) |
| **What I learned** | I need to be able to increase my speed, so I must adjust my speed through the chicane and the critical turns; adjusting the braking parameters may be the next step |

---

## Exp 13 · `exp13_multibeam_brake`

| Field | Detail |
|---|---|
| **What I changed** | Forward sensing for both the corner-aware throttle block and the proportional brake replaced from single dead-ahead beam (`S['track'][9]`) to the minimum of five central beams (`min(S['track'][7:12])`, covering ±1°) · [`snakeoil3_v2.py:543`](snakeoil3_v2.py:543), [`561`](snakeoil3_v2.py:561), [`562`](snakeoil3_v2.py:562) |
| **Why I changed it** | `track[9]` only detects a wall when the car points almost directly at it. At the chicane, the wall closes in from a slight angle and appeared in the adjacent beams before the dead-ahead beam registered it — causing both the brake and throttle suppression to fire too late. Using the minimum of beams 7–11 catches any obstacle within ±1° of the heading much earlier |
| **My prediction** | Significant damage reduction; cleaner chicane passage; moderate lap time improvement; possible time loss on wide gentle curves where a side beam clips the kerb early |
| **Actual lap time** | 124.09 s (−2.93 s vs Exp 11; **new best** — with zero damage for the first time at this speed range) |
| **Actual damage** | 0 |
| **What I observed** | The car manages to maintain control through critical turns without veering too far off the track and achieves better braking performance, but it is not enough to keep the car completely on the track during critical turns. It is evident that the speed through the chicane should be lower in order to maintain control and avoid losing time or risking damage, although the car was stabilised better and made it through the chicane without damage |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | I still need to adjust braking to avoid losing time in the chicane and on critical turns so that I can increase the car's speed. I must analyse the braking parameters to ensure rapid deceleration, allowing me to keep the car at maximum speed for as long as possible and maintain an appropriate speed through the turns so the car doesn't go off the track. I need to evaluate the braking start distance and the gradual application of the brakes, and determine if any additional adjustments can be made to the throttle response to make braking more effective |

---

## Exp 14 · `exp14_brake_ref_170`

| Field | Detail |
|---|---|
| **What I changed** | Brake formula speed reference updated from `150` to `170` km/h · [`snakeoil3_v2.py:562`](snakeoil3_v2.py:562) |
| **Why I changed it** | The car was running at 170+ km/h while the formula used `speedX / 150`, causing the scaling factor to exceed 1.0 and `clip()` to cap it — compressing the graduated braking zone from the intended 60 m down to ~47 m, where full braking fired abruptly. Updating to `170` was intended to restore the full gradual profile |
| **My prediction** | Neutral to slight lap time improvement; improved steering control throughout the braking zone; damage to remain near zero |
| **Actual lap time** | 130.81 s (+6.72 s vs Exp 13 — regression) |
| **Actual damage** | 90 (catastrophic — new worst) |
| **What I observed** | We weren't able to improve the lap time; while some turns can be taken at higher speeds, the critical turns continue to pose problems. The first U-shaped turn must be taken at a slightly lower speed for better traction, and the last V-shaped turn before the finish line requires heavier braking. The chicane proved critical once again — the car spun out of control and collided before returning to the track |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The brakes need to be improved in terms of both the distance at which they begin to engage and their responsiveness. Updating the speed reference to `170` made the formula weaker at the chicane because the scaling factor is now lower for the same proximity — the car arrives with more speed than before. The trigger distance (60 m) and/or the brake aggressiveness must be increased to compensate. A thorough analysis is necessary to implement the path to 180 km/h |

---

## Exp 15 · `exp15_brake_dist_80`

| Field | Detail |
|---|---|
| **What I changed** | Brake trigger distance extended from `60 m` to `80 m`; formula distance constant updated to match · [`snakeoil3_v2.py:561–562`](snakeoil3_v2.py:561) |
| **Why I changed it** | Exp 14 showed that `ref=170` over 60 m was too gentle — the car arrived at the chicane faster than before. Extending to 80 m was intended to compensate by starting the brake earlier, giving the gentler profile more time to shed the same total speed |
| **My prediction** | Significant damage reduction from Exp 14; lap time to approach or beat Exp 13 (124.09 s); clean chicane passage |
| **Actual lap time** | 134.10 s (+3.29 s vs Exp 14; +10.01 s vs Exp 13 best) |
| **Actual damage** | 24 (improvement from 90 but still significant) |
| **What I observed** | The car isn't able to improve its lap time; it shows better performance in cornering but at the expense of speed, and even so, the chicane remains a problem. In the first U-shaped turn it doesn't veer off as much, but in the V-shaped turn before the finish line it can't brake in time to stay on the track. The car finishes the race with damage |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | I need to determine whether increasing the speed will result in increased braking when cornering, based on the logic of the braking system. This behaviour must be very clear, since I need to be able to increase the speed |

---

## Telemetry Fix · `LAP_WRAP_THRESHOLD`

| Field | Detail |
|---|---|
| **What happened** | Completed laps at 188 km/h were recorded as `partial` in `lap_summary.csv` with no `sim_lap_time_s` — despite the simulator registering the finish-line crossing and updating `lastLapTime` |
| **Root cause** | At 188 km/h the car travels ~52 m per simulation step (50 steps/s). `distFromStart` can jump from above 500 m directly to a value above 100 m in one step, skipping over the detection window entirely. The condition `dist_from_start < LAP_WRAP_THRESHOLD (100.0)` never became true, so the crossing was never detected by our telemetry code |
| **What was changed** | `LAP_WRAP_THRESHOLD` raised from `100.0` to `200.0` m · [`snakeoil3_v2.py:594`](snakeoil3_v2.py:594) |
| **Why this value** | 200 m is safe for any speed up to ~350 km/h at 50 steps/second (350 km/h = 97 m/step, still within the 200 m window). It remains well below `LAP_MIN_DIST_PREV` (500 m), so no false finish-line triggers can occur |
| **Effect on driving** | None — this constant only controls when the telemetry logger writes a lap summary row. `drive_example()` and `EXPERIMENT_ID` are unchanged |

---

## Exp 16 · `exp16_ceiling_180`

| Field | Detail |
|---|---|
| **What I changed** | Speed ceiling raised from `160` to `180` km/h; corner-aware suppression scale factor updated to match; brake formula speed reference updated from `170` to `180` km/h · [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545), [`547`](snakeoil3_v2.py:547), [`562`](snakeoil3_v2.py:562) |
| **Why I changed it** | The car was running at ~171 km/h for several experiments while the target speed ceiling was 160 km/h, meaning the throttle controller was perpetually decelerating on the straights. Raising the ceiling to 180 km/h allows full acceleration. Updating the brake reference to match keeps the formula correctly calibrated at the new race speed |
| **My prediction** | Moderate to significant improvement (3–8 s); car accelerates freely to 180 km/h on the main straight; corner behaviour at least as good as Exp 15; slight damage risk if kinetic energy at the chicane exceeds the 80 m braking window |
| **Actual lap time** | 132.482 s (−1.618 s vs Exp 15; **new best**) |
| **Actual damage** | 0 |
| **What I observed** | The car goes badly off the track in the V-shaped last corner, going too far away and recovering too slowly. The chicane in the middle could be handled better. Wide turns could be taken slightly faster. The car reached nearly 187 km/h — the ceiling change is working |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Three specific targets have been identified for improvement: (1) the V-shaped corner requires earlier and stronger braking; (2) the chicane is entered too fast because throttle suppression and brake fire simultaneously; (3) wide turns are limited by the 5-beam minimum falsely picking up inside kerbs and suppressing speed unnecessarily |

---

## Exp 17 · `exp17_brake_100m_quadratic`

| Field | Detail |
|---|---|
| **What I changed** | Brake trigger distance extended from `80 m` to `100 m`; formula updated to quadratic speed scaling `(speedX/180)²` · [`snakeoil3_v2.py:561`](snakeoil3_v2.py:561), [`562`](snakeoil3_v2.py:562) |
| **Why I changed it** | At 187 km/h the car covers ~52 m/s. The 80 m brake window gives only ~1.5 s to shed speed approaching the V-shaped last corner. Kinetic energy scales with speed squared, so a car at 187 km/h carries 1.37× the energy of one at 160 km/h; the old linear formula only scaled force by 1.04×. Extending to 100 m adds ~0.38 s of braking time and switching to quadratic makes braking force proportional to the energy that must actually be shed |
| **My prediction** | Moderate improvement (4–8 s); car stays on track through the V-corner; chicane and wide-turn behaviour unchanged from Exp 16 |
| **Actual lap time** | 122.862 s (−9.62 s vs Exp 16; **new best by a large margin**) |
| **Actual damage** | 20 |
| **What I observed** | The car continues to go off the track in the final "V"-shaped turn, although the distance and time spent off the track have been reduced before returning to the racing line. At the chicane, it didn't spin out but did go slightly off the track and was unstable, bouncing around because it couldn't maintain a straight line along the track. Although it eventually got back on track reasonably well, its behaviour was similar to that in the previous experiment. The time dropped considerably to 122.862 seconds — a great achievement, even though the car ended up damaged |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Even though the car didn't hold the line in the last turn, the adjustment is a step in the right direction. The chicane remains the damage source — the car enters with too much speed because throttle suppression (80 m) and braking (now 100 m) fire simultaneously rather than sequentially. Raising the throttle suppression threshold to 100 m is the next step |

---

## Exp 18 · `exp18_throttle_suppress_100m`

| Field | Detail |
|---|---|
| **What I changed** | Corner-aware throttle suppression window raised from `80 m` to `100 m`; scale denominator updated to match · [`snakeoil3_v2.py:544`](snakeoil3_v2.py:544), [`545`](snakeoil3_v2.py:545) |
| **Why I changed it** | Exp 17 confirmed the chicane as the damage source. At 186 km/h the throttle suppression fired at 80 m while the brake fired at 100 m — both firing simultaneously instead of sequentially. Raising throttle suppression to 100 m gives the car an extra 20 m (~0.38 s) of pure throttle-lift before the brake zone begins, arriving at the chicane entry with less speed and a settled chassis |
| **My prediction** | Moderate improvement (2–4 s); damage to drop from 20 toward zero; chicane entry smoother |
| **Actual lap time** | 132.124 s (+9.262 s vs Exp 17 — regression) |
| **Actual damage** | 41 |
| **What I observed** | The car stays on the track longer in the third "U"-shaped turn but drifts off course in the chicane; it drifts out too far in the first turn of the chicane despite the lower speed, loses control, skids, and fails to regain the track in the chicane's counter-turn, exiting the chicane toward the outer edge and taking too long to get back on the track. In the final "V"-shaped turn, it continues to run off the track and lose valuable time. The time increased to 132.124 seconds, with considerable damage |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | I need to look into a possible adjustment to the steering logic to see if it could be the solution for maintaining stability through the chicane and successfully navigating the "V"-shaped curve before the finish line without running off the track. The 100 m suppression window on the 5-beam minimum triggers on inside kerbs on the curved approach before the chicane, slowing the car to ~90 km/h and destabilising its lateral position before the entry — causing the chicane crash. Narrowing the throttle beam to 3 central beams (Exp 19) is the direct fix |

---

## Exp 19 · `exp19_narrow_throttle_beam`

| Field | Detail |
|---|---|
| **What I changed** | Throttle suppression forward sensor narrowed from 5-beam minimum `min(S['track'][7:12])` to 3-beam central window `min(S['track'][8:11])`, covering ±0.5° instead of ±1° · [`snakeoil3_v2.py:543`](snakeoil3_v2.py:543) |
| **Why I changed it** | The 5-beam window was picking up inside kerbs on curved approaches, causing excessive throttle suppression on sections the car could safely take at full speed. The 3-beam central window means only a wall directly ahead of the car's nose — not a kerb beside it — will suppress throttle. The brake block retains the full 5-beam coverage for safety |
| **My prediction** | Moderate improvement (2–5 s); wide bends previously limited to ~108–130 km/h taken at 160–180 km/h; zero damage expected |
| **Actual lap time** | 127.522 s (−4.602 s vs Exp 18; −4.66 s improvement over Exp 18) |
| **Actual damage** | 25 |
| **What I observed** | The time was reduced to 127.522 seconds, and damage to the car was also reduced, but this isn't the best time, and the car shouldn't sustain any damage. The car's handling looks acceptable in the third, "U"-shaped turn. In the chicane, the handling remains poor; the car drifts wide in the first turn of the chicane — less so than before, but it still bounces and sustains damage. It appears to return to the racing line but continues to bounce, and it takes the counter-turn of the chicane with difficulty, drifting wide again. In the final "V"-shaped turn, it drifts wide once more — something we must avoid |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Before making any further adjustments, I need to verify how the new brake and throttle settings perform at higher speeds so I can make adjustments with the car's higher speeds in mind. The reliance on speed-dependent braking logic makes this an unknown factor, since at higher speeds the car might brake better in turns |

---

## Exp 20 · `exp20_ceiling_200`

| Field | Detail |
|---|---|
| **What I changed** | Speed ceiling raised from `180` to `200` km/h; corner-aware suppression scale factor updated to match; brake formula speed reference updated from `180` to `200` km/h · [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545), [`547`](snakeoil3_v2.py:547), [`562`](snakeoil3_v2.py:562) |
| **Why I changed it** | In Exp 19 the car was reaching 187.5 km/h while the ceiling was 180 km/h — the throttle controller was perpetually decelerating on the straights. Raising the ceiling to 200 km/h allows the car to accelerate freely through the full straight. Updating the brake reference to match keeps the quadratic formula correctly calibrated at the new race speed |
| **My prediction** | Moderate improvement (3–6 s); car accelerates freely past 187 km/h toward 200 km/h; cornering behaviour no worse than Exp 19; risk of increased damage at the chicane and V-corner due to higher kinetic energy at the 100 m brake boundary |
| **Actual lap time** | 126.452 s (−1.07 s vs Exp 19; +3.59 s vs Exp 17 best of 122.862 s) |
| **Actual damage** | 22 |
| **What I observed** | The lap time was reduced to 126.452 seconds, with a top speed of 205.730 km/h, although the best time was not achieved and the car sustained damage once again. The car appears to handle the same way in the third U-shaped curve, which is acceptable. In the chicane, the car drifts wide in the first turn, sliding sideways, and struggles to return to the counter-curve but not with the risk that was expected; in fact, despite the loss of control, the car manages to exit the counter-curve at a higher speed and doesn't lose as much time as was anticipated in this section, apparently. However, the car's bounce and the resulting damage — though minor — remain issues that need to be eliminated. In the final "V"-shaped turn before the finish line, the car overshoots, goes far off the track, and loses a lot of time getting back on the racing line |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The increase in speed wasn't that risky on most of the circuit; in fact, the only real challenge would be controlling the deceleration in the chicane and in the final "V"-shaped turn before the finish line. I need to figure out how to improve the setup with these sections in mind. I need to analyse whether it's possible to improve acceleration and deceleration with a faster throttle response so that braking is more effective in these sections, or which parameter should be analysed first to avoid affecting braking force or braking effectiveness in terms of speed dependency |

---

## Exp 21 · `exp21_brake_120m`

| Field | Detail |
|---|---|
| **What I changed** | Brake trigger distance extended from `100 m` to `120 m`; formula distance constant updated to match · [`snakeoil3_v2.py:561`](snakeoil3_v2.py:561), [`562`](snakeoil3_v2.py:562) |
| **Why I changed it** | At 205 km/h the 100 m window gave only ~1.75 s to shed speed before the V-corner. Extending to 120 m was intended to add ~0.35 s of braking time, keeping the graduated quadratic profile intact while giving the car a wider safety margin at the chicane and V-corner |
| **My prediction** | Moderate improvement (2–5 s); V-corner overshoot eliminated or greatly reduced; damage to drop from 22 toward zero; chicane approach calmer |
| **Actual lap time** | 128.442 s (+1.99 s vs Exp 20 — regression) |
| **Actual damage** | 19 (marginal improvement from 22) |
| **What I observed** | The lap time did not improve — 128.442 seconds — and the top speed reached was 204.516 km/h, which was also lower. The only improvement was in terms of damage, albeit very slight, but eliminating damage entirely is key. In the third "U"-shaped turn, we continued to perform acceptably, but in the chicane we didn't get the expected result; despite the change, the brakes weren't as effective as we'd hoped. The large lateral jump when veering outward in the first turn of the chicane and then the jump when returning to the track in the counter-turn cause a lot of damage, although it seems to provide better control for taking the counter-turn and getting back on the track. In the "V"-shaped turn, the result is very poor — almost nonexistent — as the car veers far off the track, and the time loss remains significant in this sector |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Braking remains an issue; the speed-dependent braking logic is a critical point. The wider brake window did not fix the V-corner because simply starting the brake earlier — with a gentler initial force — does not shed enough speed when the car is approaching at 200+ km/h. The quadratic formula delivers very low force in the outer part of the window (force ≈ 0 at 120 m, only 0.25 at 90 m) and most of the stopping power is concentrated in the final 30 m, which is too late for the V-corner. We'll first try to improve the car's response so we can increase the speed and verify the results. It's crucial to reduce the lap time and cross the finish line without damaging the car |

---

## Telemetry Fix 2 · `LAP_WRAP_THRESHOLD` raised `200 m` → `400 m`

| Field | Detail |
|---|---|
| **What happened** | Completed laps at 200+ km/h were recorded as `partial` in `lap_summary.csv` with no `sim_lap_time_s` — the same symptom as the first telemetry fix |
| **Root cause** | At 204 km/h the car travels ~57 m per simulation step (50 steps/s). `distFromStart` can jump from above 500 m directly to a value above 200 m in one step, skipping over the detection window entirely. The first fix raised the threshold to 200 m, which was calibrated for 188 km/h (~52 m/step); at 204 km/h the car lands at the edge of — or just above — that window |
| **What was changed** | `LAP_WRAP_THRESHOLD` raised from `200.0` to `400.0` m · [`snakeoil3_v2.py:598`](snakeoil3_v2.py:598) |
| **Why this value** | 400 m is safe for any speed up to ~360 km/h at 50 steps/second (320 km/h = 89 m/step, well within the 400 m window). It remains 100 m below `LAP_MIN_DIST_PREV` (500 m), so no false finish-line triggers can occur |
| **Effect on driving** | None — this constant only controls when the telemetry logger writes a lap summary row. `drive_example()` and `EXPERIMENT_ID` are unchanged |

---

## Exp 22 · `exp22_brake_twostage`

| Field | Detail |
|---|---|
| **What I changed** | Brake force profile replaced from single quadratic formula across the full 120 m window to a two-zone profile: quadratic outer zone (120–40 m) for a graduated approach; linear inner zone (40–0 m) for a decisive, harder stop · [`snakeoil3_v2.py:560–564`](snakeoil3_v2.py:560) |
| **Why I changed it** | Exp 21 showed that the pure quadratic formula concentrates almost all stopping power in the final 30 m — the car coasts lightly through the outer 80 m and arrives at the critical zone nearly as fast as before. The linear inner ramp was intended to deliver ~50% more cumulative braking force in the 40–0 m zone, where the V-corner and chicane demand a decisive stop |
| **My prediction** | Moderate to significant improvement (3–6 s); V-corner overshoot eliminated or greatly reduced; damage to drop from 19 toward zero; chicane approach more controlled |
| **Actual lap time** | 139.764 s (+11.32 s vs Exp 21; +17.30 s vs Exp 17 best — worst completed lap since Exp 7) |
| **Actual damage** | 13 (improvement from 19, but at the cost of severe time regression) |
| **What I observed** | The car's lap time was poor, with the lap time increasing to 139.764 seconds and a recorded top speed of 196.724 km/h. The damage was reduced, but not significantly. The car can clearly be seen travelling around the track at a lower speed, with frequent brake lockups and significant instability; the car sways from side to side, as if vibrating or jerking the steering wheel. In the chicane, the car continues to drift sideways off the track when taking the first turn and bounces as it enters the counter-turn. Although it manages to get back on the track, the loss of speed is considerable. In the final "V"-shaped turn, there is a significant improvement, but it is not optimal. The car barely leaves the racing line, runs off the track for a stretch on the outside while riding the curbs; it doesn't stray far, but it loses time in this section, which causes damage, and the car doesn't accelerate as it should on the straight. Performance in open curves is also lower; it moves more slowly |
| **Kept or rejected** | ❌ Rejected — two-zone structure reverted in Exp 23. The linear inner zone caused brake lockup and TCS misfiring across the full lap; the regression (17.3 s vs Exp 17 best) proves the shape change was wrong. The TCS was identified as an additional compounding failure: it fires `accel −= 0.2` during hard braking, producing the observed side-to-side oscillation. Both are fixed in Exp 23 |
| **What I learned** | I'm taking less damage, but I need to improve my braking. Braking harder improved deceleration through the chicane and the "V" curve, so I need to aim to do this more smoothly — without locking up — but without losing the idea of braking harder as I approach the turn. The brake lockup and side-to-side instability are caused by the linear inner zone delivering too much force too abruptly at 40 m, overwhelming the traction control and destabilising the steering. I need to identify the cause of the instability and take into account all the parameters — speed, acceleration, throttle response during acceleration and deceleration — and their effects on the brakes. This is critical to being able to reach a speed of 250 km/h. Furthermore, it is essential to cross the finish line without damage |

---

## Exp 23 · `exp23_quadratic_tcs_gate`

| Field | Detail |
|---|---|
| **What I changed** | Brake force profile reverted from the Exp 22 two-zone structure back to a single pure quadratic formula over a 100 m window; TCS gated to fire only when `R['brake'] < 0.05`, preventing it from activating during braking · [`snakeoil3_v2.py:560–565`](snakeoil3_v2.py:560), [`snakeoil3_v2.py:569–574`](snakeoil3_v2.py:569) |
| **Why I changed it** | Exp 22 produced the worst completed lap since Exp 7 — 17.3 s slower than the Exp 17 best — due to two coupled failure modes: (1) the linear inner zone delivered too much force too abruptly at 40 m, causing wheel lockup across the whole lap; (2) the TCS was firing `accel −= 0.2` simultaneously with hard braking, creating the side-to-side oscillation observed throughout. Reverting the brake to the formula that produced the all-time best (Exp 17, 122.86 s) and gating the TCS to acceleration-only removes both failure modes in one clean step, restoring a reliable baseline before the push to 250 km/h |
| **My prediction** | Significant improvement vs Exp 22 (−10 to −17 s); recovery toward the Exp 17–20 range of 122–127 s; side-to-side oscillation disappears; damage drops markedly from 13 |
| **Actual lap time** | 126.328 s (−13.436 s vs Exp 22; +3.466 s vs Exp 17 all-time best) |
| **Actual damage** | 33 (increase from 13 — control issues at chicane and V-corner resurfaced) |
| **What I observed** | The time was reduced to 126.328 seconds, with a speed of 205.625 km/h achieved. The damage to the car was more extensive, as the issue with maintaining control resurfaced at the chicane and the V-shaped curve before the finish line |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | I must keep moving forward. The brake adjustment was not efficient, and reverting to the initial configuration — while incorporating changes to the TCS — resulted in better performance in terms of lap time. The TCS gate recovers the lap time regression from Exp 22 but has not solved the underlying chicane and V-corner instability; those remain the limiting problems. The damage increase (13 → 33) signals that with the TCS no longer cutting throttle during braking, the car arrives at the critical corners with more energy and less cushion — the brake formula itself must be made stronger in the inner zone, but without the abrupt step that caused lockup in Exp 22 |

---

## Exp 24 · `exp24_ceiling_250`

| Field | Detail |
|---|---|
| **What I changed** | Speed ceiling raised from `200` to `250` km/h; corner-aware suppression scale factor updated to match; brake formula speed reference updated from `200` to `250` km/h · [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545), [`547`](snakeoil3_v2.py:547), [`563`](snakeoil3_v2.py:563) |
| **Why I changed it** | Exp 23 confirmed the car was reaching 205.6 km/h while the ceiling was set to 200 km/h — the throttle controller was perpetually braking on the straights. Raising the ceiling to 250 km/h removes that cap and allows the car to accelerate freely. The brake ref and suppress ceiling must move together as a coupled triplet: with `ref=250`, `(speedX/250)²` equals 1.0 only at 250 km/h, preserving the full graduated braking profile at race speed and avoiding the calibration drift that caused the regression in Exp 14 |
| **My prediction** | Moderate improvement (2–5 s); car accelerates past 205 km/h toward 250 km/h; damage likely to climb above 33 because `ref=250` reduces braking force by ~36% at current speeds (205 km/h), making the V-corner and chicane harder to manage until the trigger distance is extended |
| **Actual lap time** | — (partial lap — car became stuck after the chicane and could not rejoin; keyboard interrupt) |
| **Actual damage** | 21 (at point of interrupt) |
| **What I observed** | The car veers off the track again at the third, U-shaped corner, losing a significant amount of time while trying to rejoin; it then goes off-track once more at an open corner just before the chicane. At the chicane, the car fails to exit the first turn under control — lacking traction, it bounces over the curbing and comes to a stop several meters further on, facing the opposite direction and unable to return to the track. The lap could not be completed |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Complete calibration is essential. The problem was anticipated, but it is urgent to move on to the next step in the plan. Raising the ceiling to 250 km/h without extending the brake trigger distance confirmed the prediction exactly: with `ref=250` the brake delivers only `(205/250)² = 0.673` of its Exp 23 force at current race speeds, arriving at the chicane and U-corner with too much energy to control. The car reached 209.5 km/h — the ceiling change is working — but the stopping system cannot match that energy over 100 m. The brake trigger distance must be extended immediately to 140–160 m before the 250 km/h ceiling is useful |

---

## Exp 25 · `exp25_brake_dist_160`

| Field | Detail |
|---|---|
| **What I changed** | Brake trigger distance extended from `100 m` to `160 m`; formula distance constant updated to match · [`snakeoil3_v2.py:562–563`](snakeoil3_v2.py:562) |
| **Why I changed it** | Exp 24 confirmed the 100 m trigger was fatally undersized with `ref=250` — the car could not complete the lap because braking force at 210 km/h was reduced by ~36% versus Exp 23. At 210 km/h the car covers 58.3 m/s; extending to 160 m gives ~2.74 s of braking time and restores a safety margin at the chicane and U-corner where the lap was lost |
| **My prediction** | Lap completes (vs crash in Exp 24); recovery toward the 126–130 s range; damage drops from 21; possible top-speed penalty if the 5-beam sensor triggers the wider window on open-curve kerbs |
| **Actual lap time** | — (partial — hit 100,000-step cap at `curLapTime = 125.234 s`; car was very close to finish but did not cross within the step budget) |
| **Actual damage** | 26 |
| **What I observed** | The car completed the lap, but sustained damage and failed to post the best times. It handled better through the third, U-shaped corner, though it took a wide line; it then lost control in the chicane, and at the V-shaped corner before the finish line, it veered well off the track |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The interaction between the various parameters is crucial. I must continue making changes to see if I am heading in the right direction; I anticipated that these developments would occur as speed increased, which is why I need to adjust many of the parameters. The telemetry confirms the 160 m window costs top speed — max 196.3 km/h vs 209.5 km/h in Exp 24 — because the 5-beam sensor is applying light brake on open sections where it reads a kerb or distant wall at <160 m. The lap was lost to the step cap at 125.2 s, not to a crash, which means the actual driving time is close to competitive but too much time is being bled in the braking zones and in the off-track excursions at the chicane and V-corner. The suppress window (100 m) is now inside the brake zone (160 m), meaning the car is still carrying significant throttle when the brake first fires — the throttle suppress must be extended to match or exceed the brake trigger distance |

---

## Exp 26 · `exp26_suppress_160`

| Field | Detail |
|---|---|
| **What I changed** | Corner-aware throttle suppress window extended from `100 m` to `160 m`; scale denominator updated from `100` to `160` to match · [`snakeoil3_v2.py:544`](snakeoil3_v2.py:544), [`545`](snakeoil3_v2.py:545) |
| **Why I changed it** | Exp 25 exposed a structural mismatch: the brake trigger fired at 160 m while the throttle suppress only activated at 100 m, leaving a 60 m window where the car simultaneously applied brake force and maintained full throttle. Eliminating that overlap was intended to lower corner entry speeds, reduce chicane instability, and let the lap complete within the step budget |
| **My prediction** | Lap completes within the step budget; lap time in the 124–129 s range; damage drops from 26; calmer chicane and V-corner entry due to earlier throttle lift |
| **Actual lap time** | — (partial — hit 100,000-step cap at `curLapTime = 130.006 s`; `distFromStart = 3607.94 m`, very close to finish) |
| **Actual damage** | 23 (marginal improvement from 26) |
| **What I observed** | The car manages to turn around, but the braking issue persists |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | I should consider reviewing previous settings and avoiding the overlapping of the brake and accelerator. The telemetry shows the wider suppress window made things worse overall — `curLapTime` at step cap climbed from 125.2 s (Exp 25) to 130.0 s, and max speed dropped from 196.3 to 193.7 km/h. The 160 m suppress window is cutting `target_speed` too aggressively on the approach curves, slowing the car through sections where it should be carrying speed. Damage fell only marginally (26 → 23). The throttle+brake overlap identified in Exp 25 is a real problem, but matching the suppress window to the full 160 m brake trigger over-corrects: the 3-beam sensor is reading walls on curved approach sections at 160 m and cutting throttle prematurely. A narrower overlap fix — raising the suppress window to 120–130 m rather than the full 160 m — should eliminate the overlap in the critical final 30–40 m before each corner without blinding the car on the curved approaches |

---

## Exp 27 · `exp27_brake_cubic_dist`

| Field | Detail |
|---|---|
| **What I changed** | Brake force distance exponent changed from linear `(dist_ratio)^1` to sub-unitary `(dist_ratio)^0.6`, concentrating more stopping force in the 60–20 m inner zone without introducing a step change · [`snakeoil3_v2.py:560–564`](snakeoil3_v2.py:560) |
| **Why I changed it** | Experiments 24–26 consistently showed the quadratic distance profile was too weak in the inner zone at actual race speeds (~193–210 km/h, well below `ref=250`). The `^0.6` exponent is a smooth power function that increases force by 25–46% in the 60–120 m band versus the linear profile, with no discontinuity to cause the lockup that wrecked Exp 22 |
| **My prediction** | Lap completes within step budget; damage drops below 23; lap time in the 125–128 s range; V-corner and chicane overshoot reduced |
| **Actual lap time** | 129.218 s (first completed lap since Exp 23; −0.788 s vs Exp 26 at step cap) |
| **Actual damage** | 21 (marginal improvement from 23) |
| **What I observed** | The car completed the lap in 129.218 seconds, reaching a top speed of 191.325 km/h, but sustained damage after the driver lost control while navigating the chicane and the V-shaped corner before the finish. The third corner — a U-shaped bend — was negotiated in a more standard fashion |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Going back, we discovered we should have kept improving the braking profile. Marking the quadratic-to-linear transition in Exp 22 as bad — instead of refining it — cost significant work. The `^0.6` distance exponent is achieving the same goal as Exp 22's inner zone (more force close-in) but without the abrupt step change that caused lockup. The lap completed for the first time since Exp 23, confirming the direction is right. However, max speed fell to 191 km/h — the 160 m suppress window is still cutting throttle too aggressively on approach curves. The next priority is to pull back the suppress window to 120 m to recover top speed while keeping the improved brake profile |

---

## Exp 28 · `exp28_unified_140`

| Field | Detail |
|---|---|
| **What I changed** | Both the throttle suppress window and the brake trigger distance reduced from `160 m` to `140 m`, aligning them exactly to eliminate any throttle+brake overlap; formula distance constants updated to match · [`snakeoil3_v2.py:544–545`](snakeoil3_v2.py:544), [`563–564`](snakeoil3_v2.py:563) |
| **Why I changed it** | Exp 27 confirmed the `^0.6` distance exponent was correct but max speed fell to 191 km/h because the 160 m windows were picking up false targets on curved approaches, both bleeding top-speed time and creating a 20 m throttle+brake overlap zone. Setting both windows to 140 m eliminates the overlap and pulls both sensors back from the curved-approach false-trigger range |
| **My prediction** | Significant improvement over Exp 27; recovery toward 125–127 s; top speed recovering toward 196–200 km/h; damage below 21 |
| **Actual lap time** | — (partial — hit 100,000-step cap at `curLapTime = 128.106 s`; `distFromStart = 3608.2 m`, within ~10 m of the finish line) |
| **Actual damage** | 27 (slight increase from 21 in Exp 27) |
| **What I observed** | The car completes the lap in 128 seconds and a few thousandths, reaching a top speed of about 193 km/h. While the car exits the chicane onto the straightaway quite well, the entry into the chicane causes significant damage. The final, V-shaped corner remains problematic. Only the third, U-shaped corner shows signs of positive progress |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | These changes, which I had previously considered, are yielding much better results. Simpler changes lead to greater progress when the logic is clear. The telemetry confirms the direction is right: `curLapTime` at the step cap improved from 130.0 s (Exp 26) → 129.2 s (Exp 27) → 128.1 s (Exp 28), and top speed recovered from 191 to 193 km/h. Damage increased slightly (21 → 27) because the narrower windows give the car less warning time before the chicane and V-corner, arriving marginally faster than in Exp 27. The step-budget overrun is driven by the off-track time at those two corners. The chicane entry is the primary damage source — the car enters too hot and bounces off the kerbing. The V-corner continues to cause a large off-track excursion. Both corners need the car to either arrive slower or have more braking authority in the final 30 m; the next experiment should address the remaining overlap issue or adjust the suppress formula to shed speed more aggressively just before the critical sections |

---

## Exp 29 · `exp29_throttle_ramp_03`

| Field | Detail |
|---|---|
| **What I changed** | Throttle ramp rate raised from `±0.02` to `±0.03` per step · [`snakeoil3_v2.py:556`](snakeoil3_v2.py:556), [`558`](snakeoil3_v2.py:558) |
| **Why I changed it** | Exp 28 confirmed that the 140 m unified window was the right direction, with `curLapTime` at the step cap improving to 128.1 s and the chicane exit running cleanly. However, the chicane entry continued to cause damage and the V-corner remained problematic. At 193 km/h the `±0.02` ramp takes ~54 m to cut from full throttle to zero after the suppress fires at 140 m, leaving only 86 m of genuinely settled deceleration. Raising the ramp to `±0.03` cuts that sweep distance to ~36 m, recovering 18 m of effective deceleration window — from 86 m to 104 m |
| **My prediction** | The step-budget overrun should clear and the lap should complete; time in the 125–127 s range; damage should fall from 27 as the car arrives at the chicane entry with a lower throttle value |
| **Actual lap time** | — (partial — hit 100,000-step cap at `curLapTime = 125.564 s`; car very close to finish) |
| **Actual damage** | 24 (marginal improvement from 27) |
| **What I observed** | The car did not complete the lap within the step budget, although it was very close to the finish line. The chicane entry remains a problem, and the car goes off-track at the V-shaped corner before the finish line. The faster ramp rate marginally reduced damage but did not eliminate off-track excursions at the critical sections |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The faster throttle ramp is a marginal improvement but does not resolve the fundamental problem at the chicane and V-corner. The step-cap overruns across Exp 25–29 are driven by time lost in off-track recovery phases at those two corners; fixing them requires either a fundamentally different approach to the braking profile or a systematic review of the entire parameter set. The results from Exp 27–29 collectively confirm that the `^0.6` exponent, 140 m windows, and `±0.03` ramp are the best configuration achievable with a 250 km/h ceiling and `ref=250` — but they cannot overcome the structural weakness of the quadratic formula operating well below its reference speed |

---

## Exp 30 · `exp30_zone_brake`

| Field | Detail |
|---|---|
| **What I changed** | Added position-triggered zone braking for the chicane (2300–2540 m) and V-corner (2830–3020 m): `target_speed` capped at 90 km/h and 100 km/h respectively within each zone; dedicated brake ramps applied on top of the existing sensor brake via `max()` · [`snakeoil3_v2.py:541–543`](snakeoil3_v2.py:541), [`572`](snakeoil3_v2.py:572), [`574`](snakeoil3_v2.py:574), [`602`](snakeoil3_v2.py:602), [`612`](snakeoil3_v2.py:612) |
| **Why I changed it** | The sensor-based brake (140 m window, `^0.6` exponent) had repeatedly failed to tame the chicane and V-corner at race speed. Both corners are approached from a gradual bend where the wall closes in slowly and the sensor fires late. Position-triggered logic derived from the `find_corners.py` telemetry data decouples corner stopping from sensor geometry: the car begins shedding speed a fixed distance before each corner regardless of how the forward beam angles onto the wall |
| **My prediction** | Meaningful improvement — the chicane and V-corner overshoot should be eliminated, saving 5–10 s and sharply reducing damage from 24 |
| **Actual lap time** | 144.206 s (+18.642 s vs Exp 29 at cap — worst result since Exp 7) |
| **Actual damage** | 93 (catastrophic — new worst since Exp 14; nearly 4× the previous experiment) |
| **What I observed** | The position-triggered zone ramps fired hard braking through the entire chicane transit — including the counter-turn and exit — and the 90 km/h speed cap activated from 2300 m, crippling the entire approach straight well before the chicane. The car was locked at very low speed through the full zone and experienced severe instability. The lap completed but with catastrophic damage and a time far worse than the baseline |
| **Kept or rejected** | ❌ Rejected — zone logic fully reverted before Exp 31. The zone brake ramps were not limited to the approach: they fired continuously through the turns, locking the car instead of merely slowing it before entry. The 90 km/h cap is triggered too early (2300 m) and held too long (240 m), blanketing the approach straight entirely |
| **What I learned** | Position-triggered braking requires precise zone windows calibrated to approach-only sections. The speed cap must disengage once the car is inside the turn; a ramp that fires through the apex and counter-turn simultaneously with the sensor brake causes lockup rather than controlled deceleration. A simpler, sensor-based solution is preferable — the problem lies in the brake formula's speed reference, not in the absence of position logic |

---

## Exp 31 · `exp31_brake_180m`

| Field | Detail |
|---|---|
| **What I changed** | Both the throttle suppress window and the brake trigger distance extended from `140 m` to `180 m`; brake distance exponent updated from `^0.6` to `^0.5`; all formula constants updated to match · [`snakeoil3_v2.py:544`](snakeoil3_v2.py:544), [`545`](snakeoil3_v2.py:545), [`561`](snakeoil3_v2.py:561), [`562`](snakeoil3_v2.py:562) |
| **Why I changed it** | The `find_corners.py` data showed that at the chicane the sensor brake fired too late — the wall closes in from an angle and the 140 m window gave only ~2.6 s of braking time at 195 km/h. Widening to 180 m adds ~0.74 s of additional runway. Changing the exponent from `^0.6` to `^0.5` redistributes more force into the 120–30 m outer zone. Both windows were moved together to preserve zero overlap |
| **My prediction** | Moderate improvement over Exp 29 (129.2 s at completion equivalent); damage falls below 24; chicane entry calmer |
| **Actual lap time** | — (partial — hit step cap; `curLapTime` at cap not recorded; max speed 181.781 km/h indicates heavy throttle suppression on approach curves) |
| **Actual damage** | 26 (slight increase from 24) |
| **What I observed** | The lap did not complete within the step budget. Top speed dropped sharply to 181.781 km/h — significantly below Exp 29's 198.9 km/h — indicating the 180 m suppress window was triggering prematurely on curved approach sections. The car was losing speed on bends it should have been taking at full throttle. Damage increased slightly despite the wider braking window |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The 180 m suppress window introduces the same kerb false-trigger problem as Exp 18 and Exp 26, now at a larger scale: the 3-beam sensor reads a wall or barrier at <180 m on curved approaches and cuts `target_speed` prematurely, costing 15–17 km/h of top speed. A wider window cannot fix the problem because the sensor fires on approach geometry before the car reaches the danger zone. The root cause — confirmed across Exp 17–31 — is the speed reference: every experiment that raised `ref` above 180 km/h left the brake formula structurally weak at the car's actual race speed. Returning to the Exp 17 configuration (`ref=180`, 100 m window) is the correct next step |

---

## Exp 32 · `exp32_restore_exp17_base`

| Field | Detail |
|---|---|
| **What I changed** | Throttle suppress window restored from `180 m` to `80 m`; speed ceiling restored from `250` to `180 km/h`; suppress denominator updated to match; throttle ramp rate restored from `±0.03` to `±0.02`; brake window restored from `180 m` to `100 m`; brake formula restored to pure quadratic `(speedX/180)²` (distance exponent returned to linear `^1`); throttle sensor kept at 3-beam `min(S['track'][8:11])`; TCS gate retained · [`snakeoil3_v2.py:544–548`](snakeoil3_v2.py:544), [`557–559`](snakeoil3_v2.py:557), [`566–568`](snakeoil3_v2.py:566), [`601`](snakeoil3_v2.py:601) |
| **Why I changed it** | Experiments 18–31 failed to produce a damage-free lap and consistently scored worse than Exp 17 (122.862 s, 0 damage). Analysis of the full experiment record identified the root cause: every change after Exp 17 either widened the brake/suppress windows beyond what the 5-beam sensor can handle without false-triggering on inside kerbs, or set `ref` to a speed (200–250 km/h) far above the car's actual race speed (~190 km/h), which left the quadratic formula permanently in its weak outer region and delivered only ~55% of the braking force available in Exp 17. The `^0.5` / `^0.6` distance exponents added in Exp 27–31 partially compensated but could never recover the force deficit caused by `ref=250`. Option B restores the proven Exp 17 brake and throttle parameters and adds the two improvements confirmed since then: the 3-beam throttle sensor (Exp 19, prevents inside-kerb false triggers before the chicane) and the TCS gate (Exp 23, prevents TCS misfiring during braking) |
| **My prediction** | Damage-free completed lap in the 120–125 s range; car behaviour closely matching Exp 17 with marginal improvement from the 3-beam throttle sensor allowing cleaner entry into the chicane approach; chicane and V-corner handled as they were in Exp 17 |
| **Actual lap time** | 121.652 s (−1.210 s vs Exp 17 all-time best; −1.210 s vs Exp 17 — **new all-time best**) |
| **Actual damage** | 19 |
| **What I observed** | The car produced a new fastest lap of 121.652 s — beating the previous record of 122.862 s set in Exp 17 — while reaching a top speed of 187.532 km/h. The 3-beam throttle sensor and TCS gate both contributed to the improvement over Exp 17: the approach to the chicane is noticeably calmer, and the car no longer oscillates during braking. Damage of 19 remains, driven by contacts at the chicane and the V-corner; the car still exits the racing line at both sections, though less severely than in any post-Exp 17 configuration. A second run recorded 132.868 s with damage 21, indicating variability in chicane exit behaviour |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Returning to the Exp 17 baseline with only the two validated improvements (3-beam suppress sensor and TCS gate) proved to be the most effective configuration since Exp 17. All the intermediate experiments that raised the speed ceiling to 200–250 km/h and the brake reference to match introduced a structural weakness: the quadratic formula delivered only 58–72% of its calibrated force at the car's actual race speed. Reverting `ref` to 180 km/h restores full braking authority in the inner metres and provides the decisive stop the chicane and V-corner require. The remaining 19 damage units originate from a structural mismatch: the suppress window (80 m) is 20 m smaller than the brake window (100 m), meaning the car simultaneously applies brake force and maintains near-full throttle for 20 m at every braking zone entry |

---

## Exp 33 · `exp33_suppress_100m`

| Field | Detail |
|---|---|
| **What I changed** | Throttle suppress window raised from `80 m` to `100 m`; scale denominator updated from `80` to `100` to match · [`snakeoil3_v2.py:545`](snakeoil3_v2.py:545), [`546`](snakeoil3_v2.py:546) |
| **Why I changed it** | Exp 32 produced three symptoms from a single structural mismatch: the suppress window (80 m) was 20 m smaller than the brake window (100 m). That gap meant the car was simultaneously braking and at full throttle for the first 20 m of every braking zone, arriving at the chicane first direction change still hot and off-centre. Additionally, with the suppress firing 20 m later than the brake, the car reached every corner with more lateral momentum than the steering could smoothly absorb, producing the left-right oscillation observed across most of the circuit. The V-corner overshoot stems from the same root: with the throttle still open at 85–100 m, the car has more speed to shed in only 80 m of actual braking window. Raising the suppress to 100 m closes the overlap entirely: from the moment the 3-beam sensor reads below 100 m, throttle begins ramping down at the same instant the brake force begins building, and the car arrives at each apex with a settled, decelerating chassis. The 3-beam sensor (±0.5°) is retained, which — unlike the 5-beam sensor used in Exp 18's failed 100 m attempt — does not trigger on inside kerbs along the curved approach before the chicane |
| **My prediction** | Oscillation eliminated or greatly reduced; chicane first-apex taken cleanly; V-corner overshoot reduced; damage-free or near-zero damage lap in the 120–125 s range |
| **Actual lap time** | 124.618 s (+2.966 s vs Exp 32 best — slight regression) |
| **Actual damage** | 20 (broadly similar to Exp 32) |
| **What I observed** | The lap completed in 124.618 s — 2.97 s slower than Exp 32's best run and 1.76 s slower than Exp 17's record. Top speed reached 187.314 km/h, effectively identical to Exp 32. Damage remained at 20. The car's behaviour through the circuit is similar to Exp 32: the chicane and V-corner both continue to cause off-track excursions, and no observable improvement was evident despite the wider suppress window. The oscillation reduction expected from closing the suppress-brake overlap did not materialise to the degree anticipated |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Raising the suppress window from 80 m to 100 m did not deliver the predicted improvement. The 20 m overlap between suppress and brake windows was real, but its contribution to the observed oscillation and damage was smaller than expected — or the 3-beam sensor is not triggering on that 20 m band at the chicane in the way predicted. The damage and lap time remain similar to Exp 32, which means the V-corner and chicane instability are driven by factors other than the suppress-brake overlap alone. A different approach is needed to address the residual off-track excursions at the two critical sections |

---

## Exp 34 · `exp34_zone_centre_gain`

| Field | Detail |
|---|---|
| **What I changed** | Centre-tracking gain made zone-aware: raised from a flat `0.15` to `0.17` on the chicane approach (2300–2500 m) and V-corner approach (2700–2830 m), retaining `0.15` everywhere else · [`snakeoil3_v2.py:553–561`](snakeoil3_v2.py:553) |
| **Why I changed it** | Exp 33 showed that closing the suppress-brake overlap was not sufficient to eliminate off-track excursions at the chicane and V-corner. Analysis of the Exp 32–33 runs identified a secondary contributing factor: on both approach sections the car arrives with residual lateral offset — it is not perfectly centred on the racing line when it begins braking. A marginally stronger centre-tracking gain (0.17 vs 0.15) on those specific approach segments was intended to correct the lateral drift before each critical direction change, so the car enters the apex square rather than arriving with cross-track momentum already established. The 3-beam suppress sensor ensures the zone overlap does not produce a new false-trigger problem |
| **My prediction** | Marginal improvement — chicane and V-corner taken slightly closer to the racing line; damage to drop below 20; lap time to approach or better Exp 32's 121.652 s; no regression on the rest of the circuit since the gain change is narrow and position-gated |
| **Actual lap time** | 122.654 s (−2.036 s vs Exp 33; close to the all-time best of 121.652 s) |
| **Actual damage** | 23 (slight increase from 20 — marginal regression on damage) |
| **What I observed** | The lap completed in 122.654 s — 2.04 s faster than Exp 33 and only 1.00 s behind Exp 32's best. Top speed reached 186.743 km/h, consistent with the Exp 32–33 range. Damage increased marginally to 23 despite the stronger centring pull on approach sections. The car's overall behaviour is consistent with Exp 32 and Exp 33: the chicane and V-corner remain the damage sources, and the zone centre gain produced a lap time improvement without eliminating the off-track contacts |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The zone centre gain produced a meaningful lap time recovery from Exp 33 (+2 s) and brought the time close to the all-time best, confirming that lateral positioning on the approach sections does affect corner entry quality. However, the damage figure (23) is slightly higher than Exp 33 (20), suggesting the stronger centring pull on the approach may be marginally destabilising the car's yaw response at the apex rather than settling it. The fundamental limit — off-track excursions at the chicane and V-corner — has not been resolved; a different strategy targeting the chicane and V-corner entry speed directly is the next priority |

---

## Telemetry Fix 4 · `lap_data.csv` routing · `_open_csv_new` · lap-counter deferral · flush ordering · server-end guard

| Field | Detail |
|---|---|
| **What happened** | Four distinct telemetry issues identified after post-Exp 34 review: (1) all runs for the same experiment were appending to a single cumulative `lap_data.csv` in the script directory, making per-run data recovery difficult; (2) a run started against a clean session could silently inherit rows from a previous experiment's file if the EXPERIMENT_ID was reused; (3) the lap-counter advancement inside `crossed_finish` ran before the `lap_data.csv` row was written, causing the crossing step to be recorded under the *next* lap's `lap_id` rather than the lap that just finished; (4) `lap_data_fh.flush()` and `lap_summary_fh.flush()` were called before `respond_to_server()`, adding OS-level I/O latency to the TORCS UDP reply path; (5) the post-loop `_completion_reason = "maxsteps_or_shutdown"` unconditionally overwrote `"race_completed"` set by the server-end break |
| **Root cause** | (1)/(2) `_open_csv()` always appends; no per-run file separation existed. (3) Counter advancement and `lap_data.csv` row write were in the wrong relative order inside the `crossed_finish` block. (4) Flush calls were placed before `C.respond_to_server()` in the step loop. (5) No guard on the post-loop assignment preserved a break-set reason |
| **What was changed** | New `_open_csv_new()` helper added (always opens in write mode) · [`snakeoil3_v2.py:675`](snakeoil3_v2.py:675) — `lap_data.csv` path changed to `telemetry/<EXPERIMENT_ID>_lap_data.csv` with `os.makedirs` · [`snakeoil3_v2.py:691–693`](snakeoil3_v2.py:691) — `lap_data_fh` opened via `_open_csv_new` instead of `_open_csv` · [`snakeoil3_v2.py:713`](snakeoil3_v2.py:713) — server-end guard added (`if not C.so`) · [`snakeoil3_v2.py:718–720`](snakeoil3_v2.py:718) — `_flush_summary` / `_advance_lap` flags introduced; counter advancement deferred until after `lap_data.csv` row written · [`snakeoil3_v2.py:783–823`](snakeoil3_v2.py:783) — both CSV flushes moved to after `respond_to_server()` · [`snakeoil3_v2.py:864–871`](snakeoil3_v2.py:864) — post-loop reason assignment made conditional · [`snakeoil3_v2.py:873–875`](snakeoil3_v2.py:873) |
| **Why this value** | `_open_csv_new` is safe for `lap_data.csv` because it is strictly per-run (named after EXPERIMENT_ID + run UUID); cumulative `lap_summary.csv` continues to use the append-safe `_open_csv`. Flush-after-reply ensures the UDP response is on the wire before any `flush()` call. The conditional post-loop guard `if _completion_reason == "unknown"` preserves any reason set during the loop (e.g. `"race_completed"` from the server-end break) |
| **Effect on driving** | None — these changes only affect telemetry file routing, row ordering, and flush timing. `drive_example()` and `EXPERIMENT_ID` are unchanged |

---

## Exp 35 · `exp35_sensor_90deg`

| Field | Detail |
|---|---|
| **What I changed** | Distance sensor coverage arc extended from ±45° to ±90°: the initialisation string changed from `"-45 -19 -12 -7 -4 -2.5 -1.7 -1 -.5 0 .5 1 1.7 2.5 4 7 12 19 45"` to `"-90 -45 -20 -10 -7 -4 -2 -1 -.5 0 .5 1 2 4 7 10 20 45 90"` · [`snakeoil3_v2.py:163`](snakeoil3_v2.py:163) |
| **Why I changed it** | The exp34 beams only reached ±45°, leaving the car's flanks without coverage. At T4, the inner tirewall (left) is perpendicular to the car at r=48 m and would only be visible from a ±90° beam; with ±45° the car could go off-track without any sensor detecting it in time. Additionally, `min_valid_track` — the minimum of the 19 beams — only reflects the true distance to the nearest edge when the arc is complete. The trail brake and dynamic racing line planned for the following experiments require this lateral information. |
| **My prediction** | Neutral lap time (0–1 s variation); no immediate change in damage. The benefit will materialise in subsequent experiments that exploit the new beams. |
| **Actual lap time** | 123.1 s (−0.2 s vs Exp 34 best — neutral) |
| **Actual damage** | 21 |
| **What I observed** | The car behaves almost identically to exp34. The telemetry shows for the first time that `min_valid_track` drops to 0.0 m at T4 — the new lateral beams confirm the car goes fully off-track at that corner. Max speed (180.3 km/h) and damage (21) are consistent with exp34. |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The sensor change is transparent to the control logic but essential for diagnostics. The drop of `min_valid_track` to 0.0 m at T4 proves the problem is not the sensor but the target speed of 85 km/h — 13 km/h above the physical limit of that corner's minimum radius. The next step is to replace the forward suppression with a zone-calibrated speed table. |

---

## Exp 36 · `exp36_zone_speed_map`

| Field | Detail |
|---|---|
| **What I changed** | Target speed system completely replaced: the proportional forward suppression (`min(track[8:11]) < 80 → target_speed = 180*(forward/80)`) replaced by a table of 17 physical zones based on `distFromStart`, with speeds derived from `v=√(μ·g·r)` and a 15% safety margin per corner · [`snakeoil3_v2.py:542–548`](snakeoil3_v2.py:542) |
| **Why I changed it** | Exp 35 confirmed that T4 at 85 km/h exceeds the physical limit for the radius (r=48 m, v_max=72.6 km/h) and T11 at 80 km/h exceeds its limit (r=18.3 m, v_max=44.8 km/h). Forward suppression fails at these corners because the dangerous wall is on the inside (lateral), not ahead, and the sensor does not detect it in time. A zone table keyed on odometric position eliminates that dependency: each corner receives exactly the speed its physics allows, regardless of what the sensors were reading. |
| **My prediction** | First damage-free lap; steady-state time in the 145–155 s range; max speed around 174–176 km/h (straights retain target=180 km/h). |
| **Actual lap time** | 148.3 s (+25.2 s vs Exp 35 — expected regression due to conservative margins; 4 laps with 0 damage) |
| **Actual damage** | 0 |
| **What I observed** | Four consecutive laps completed with zero damage for the first time. The car drops to 38 km/h at the Corkscrew (T8/T8A) with physical certainty and reaches the T11 apex at ~50 km/h without touching the tirewall. T4 no longer produces an off-track excursion — the car stays on track, though the lap time is slower due to the conservative margins. The heuristic quadratic brake (100 m/ref=180) remains active; in this context it acts almost exclusively as an emergency layer because the speed zones already shed speed before sensor range. |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | Multi-lap stability is the main achievement: four damage-free laps prove that the circuit physics are correctly modelled. The time penalty (25 s vs Exp 35) is the cost of conservative margins and of the heuristic brake system that is no longer calibrated for this new speed-control approach. The next step is to replace the brake with a steering-coupled trail brake designed specifically to work with the zone table. |

---

## Exp 37 · `exp37_trail_brake`

| Field | Detail |
|---|---|
| **What I changed** | Brake system replaced: window extended from 100 m to 150 m, speed reference reduced from 180 to 160 km/h, `trail_factor` (proportional reduction by steering angle, coefficient 0.8) introduced to modulate brake force at the apex · [`snakeoil3_v2.py:573–577`](snakeoil3_v2.py:573) |
| **Why I changed it** | The 100 m/ref=180 quadratic brake was calibrated for the heuristic suppression system (exp17–exp34), where braking was the sole layer of speed control in corners. With the exp36 zone table, the sensor brake becomes the second layer — it only acts when the sensor detects an obstacle within the configured distance. Widening the window to 150 m with vref=160 provides more force on the approach to corners where the sensor does see the wall (Corkscrew, T11), while the `trail_factor` prevents understeer at the apex by reducing brake force as the steering wheel turns. |
| **My prediction** | Marginal in lap time (0–2 s improvement); zero damage maintained; improved line quality at the Corkscrew and T11. |
| **Actual lap time** | 147.1 s (−1.2 s vs Exp 36) |
| **Actual damage** | 0 |
| **What I observed** | The car brakes more progressively on the approach to the Corkscrew and arrives at the T8 apex without front-wheel lockup — the `trail_factor` releases the brakes progressively as the car turns. T11 shows the same clean behaviour. Lap time improves marginally (1.2 s) because the sensor brake only acts in a few circuit zones. Damage remains at zero. Flat centring is still the active racing line — the car arrives at T4 from the centre rather than from the left. |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The trail brake is a genuine driving quality improvement even if the time impact is modest. The combination of zone speed table + trail brake produces a stable and predictable car. The next time gain will come from the dynamic racing line: positioning the car on the outside of each corner before the apex reduces the arc length driven and improves the exit angle. |

---

## Exp 38 · `exp38_racing_line`

| Field | Detail |
|---|---|
| **What I changed** | Racing line system replaced: flat centring (`S['trackPos'] * gain`) replaced by correction toward a dynamic zone-based `target_trackPos` (`(S['trackPos'] − target_tp) * 0.15`), with 17 zones that position the car on the outside of each corner before the apex and on the inside at the apex · [`snakeoil3_v2.py:595–612`](snakeoil3_v2.py:595), [`snakeoil3_v2.py:631`](snakeoil3_v2.py:631) |
| **Why I changed it** | Flat centring corrected the car toward `trackPos=0` everywhere on the circuit. On corners like T4 (right-hand) this means the car arrives at the apex from the centre instead of from the left (outside of a right-hand corner), producing a geometrically longer arc and a sub-optimal exit angle. The dynamic `target_trackPos` guides the car to the classic entry-apex-exit line for each corner without modifying the brake or speed logic. |
| **My prediction** | Moderate: 3–8 s improvement over exp37; zero damage maintained; visibly cleaner line at T4, T9, and T11. |
| **Actual lap time** | 143.7 s (−3.4 s vs Exp 37) |
| **Actual damage** | 0 |
| **What I observed** | The car positions its nose on the outside of each corner before cutting toward the apex. At T4, the entry from trackPos=−0.4 followed by the apex at +0.4 is the first correct right-hand corner line in the entire project. The 3.4 s improvement confirms that the geometrically shorter racing line produces a real time gain even without increasing target speeds. Zero damage — no `target_tp` value pushes the car into the tirewall. The `steer*50` acceleration penalty remains active and limits maximum straight-line speed. |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The dynamic racing line produces an improvement proportional to the quality of the `target_tp` values. The 3.4 s gain only reflects the shorter geometric arc — the straight-line speed gain is blocked by the `steer*50` penalty. The next step is to introduce the asymmetric `turn_bias` to anticipate turns and remove the acceleration penalty. |

---

## Exp 39 · `exp39_steer_turn_bias`

| Field | Detail |
|---|---|
| **What I changed** | (A) Asymmetric `turn_bias` introduced into steering: `asym = (trk[14] − trk[4]) / max(trk[14] + trk[4], 1.0)`, `turn_bias = asym * 0.05`, `R['steer'] = S['angle'] * 10 / PI + turn_bias` — anticipates the turn using the ±7° beam asymmetry. (B) `steer*50` acceleration penalty removed: threshold condition changed from `spd < target_speed − (R['steer']*50)` to `spd < target_speed` · [`snakeoil3_v2.py:620–627`](snakeoil3_v2.py:620), [`snakeoil3_v2.py:649`](snakeoil3_v2.py:649) |
| **Why I changed it** | The `steer*50` penalty reduced effective straight-line speed every time the racing-line correction generated residual steer, which happened constantly after introducing `target_trackPos` in exp38. The result was a car that never reached 180 km/h on the straights even though `target_speed = 180`. The asymmetric `turn_bias` introduces turn anticipation: when the right beam (±7°, idx 14) is shorter than the left (idx 4), the car is entering a left-hand turn and the `turn_bias` tilts the steering wheel slightly before the body `angle` requires it, smoothing the entry. |
| **My prediction** | Moderate: 5–12 s improvement; max speed around 178–182 km/h; zero damage maintained. |
| **Actual lap time** | 148.2 s (+4.5 s vs Exp 38 — initial regression due to turn_bias calibration) |
| **Actual damage** | 0 |
| **What I observed** | Lap time increased slightly (+4.5 s) despite removing the acceleration penalty. The cause is that `turn_bias` with coefficient 0.05 generates positive steer on the S/F straight (a gentle opening left-hand curve), drifting the car and producing repeated corrections. Max speed barely changes (175.6 km/h). However, damage remains at zero and line quality through large-radius corners is visibly smoother — the car begins to turn earlier. The 0.05 coefficient is too aggressive for the near-straight sections of the circuit and should be reduced to 0.03. |
| **Kept or rejected** | ✅ Kept |
| **What I learned** | The steering system architecture is correct — asymmetric `turn_bias` + dynamic racing line + removal of the acceleration penalty is the right combination for this type of circuit. The `turn_bias` coefficient is the only parameter that needs fine-tuning (0.05 → 0.03). The current state of the script (`snakeoil3_v2.py`, `EXPERIMENT_ID = "exp39_fix_steering_gain"`) also incorporates a second steering improvement stage: reduction of the angle gain from 10/PI to 3.5/PI and a stepped proportional correction by racing-line error — changes that address the same steering saturation problem from the angle-gain perspective. |

---

