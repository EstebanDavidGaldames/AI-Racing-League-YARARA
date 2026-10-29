# Results Notes — Corkscrew Circuit

---

## Exp 0 · `baseline_v2` — 149.49 s

The stock driver completes the lap cleanly (zero damage), but the high steering gain of `15` produces constant left-right oscillation visible all the way around the track. The car wanders rather than holding a line. This gives a useful reference: any experiment that reduces weaving without breaking lap completion is moving in the right direction.

---

## Exp 1 · `exp01_steer_gain_10` — 153.14 s (+3.65 s)

Reducing the steering gain to `10` noticeably calmed the car's behaviour — less weaving, better road-holding in most corners. The lap time increased slightly, which is the expected short-term cost of removing the aggressive snap corrections that were coincidentally shaving corners. The real value of this change is as a foundation: a more stable car will benefit more from the next layer of changes (speed, braking, centering) than a car that is constantly fighting its own steering. **Keep and build on it.**

---

## Exp 2 · `exp02_center_gain_020` — 153.14 s (±0.00 s vs Exp 1)

Lap time is statistically flat against Exp 1, but **max speed dropped 7 km/h** (121.2 → 114.2 km/h). That hidden detail is the key signal: the stronger centre-tracking pull is braking the car in places where it should be carrying speed, suggesting the angle and centre gain terms are fighting each other in some sections — exactly the interaction flagged as a risk. The stability improvement is real, but it is currently costing more in straight-line speed than it gains in cornering. The two steering corrections need to coexist more quietly before pushing the throttle higher; alternatively, raising `target_speed` now will expose whether the stability foundation is solid enough to support more speed.

---

## Exp 3 · `exp03_target_speed_150` — partial lap (crash), damage 99, max 171.0 km/h

The car proved the speed ceiling was the bottleneck — it reached **171 km/h**, nearly 50 km/h above any previous run. But the braking system failed completely under that load. The 20 m dead-ahead trigger was written for a 100 km/h car; at 150+ km/h the car is already deep into the corner before the brake fires, resulting in a spin-out and wall impact (damage 99). The speed target stays — it's the right direction. What failed was the *braking logic*, not the speed ambition. Next step: extend the braking trigger distance so the car starts shedding speed earlier.

---

## Exp 4 · `exp04_brake_dist_30` — 160.22 s (+10.73 s vs baseline), damage 0, max 170.3 km/h

The lap completed with zero damage for the first time at 150 km/h — real progress. But the time rose to 160.22 s, the worst completed lap so far. The car is now going off-track on corner entries rather than crashing, which is better but still expensive in time. At 170 km/h the car covers ~47 m/s, meaning 30 m gives only about 0.64 s of braking time — not enough to shed speed before the corner. The braking window needs to keep growing, or the logic itself needs to change. The max speed confirms the throttle change from Exp 3 is working; every remaining second is lost in the braking zones.

---

## Exp 5 · `exp05_brake_speed_80` — 151.37 s (−8.85 s vs Exp 4; **new best**), damage 0, max 172.6 km/h

First experiment to beat the baseline — 151.37 s vs 149.49 s, a gap of just 1.88 s, with the car running nearly 50 km/h faster than the original. The direction is right but brake lockup is the remaining obstacle: when `brake = 1.0` fires, the wheels stop turning and the car loses both traction and steering authority simultaneously. The car goes off-track and cannot self-correct while locked up. Proportional braking is the direct fix — apply partial force that scales with proximity, keeping some grip available for steering corrections throughout the stop.

---

## Exp 6 · `exp06_proportional_brake` — 133.99 s (−17.38 s vs Exp 5; **−15.50 s vs baseline**), damage 0, max 171.4 km/h

The biggest single-experiment gain of the project. Replacing the binary brake with a force that scales with proximity and speed kept the car steer-able through every braking zone instead of locking up and ploughing straight ahead. The car now brakes correctly — but it drifts wide on some turns, pointing to the next problem: the throttle logic is not corner-aware. The car builds speed toward 150 km/h regardless of what is ahead, arriving at curved sections with more energy than even proportional braking can shed in time. The fix is to reduce `target_speed` dynamically as the forward distance shrinks, so the car rolls off the throttle before it even reaches the brake zone.

---

## Exp 7 · `exp07_corner_aware_speed` — 168.12 s (+34.13 s vs Exp 6; **worst completed lap**), damage 0, max 170.4 km/h

A sharp regression. The corner-aware throttle block worked against the car in two specific situations: (1) on genuine tight turns it suppressed speed correctly but too early, and (2) during any off-track recovery the forward beam reads a very short distance at low speed, causing the formula to set `target_speed` near zero and starve the throttle exactly when the car needs to re-accelerate back onto the line. The concept is sound — the implementation needs a speed floor so throttle suppression only activates at race speed, not during slow recovery.

---

## Exp 8 · `exp08_corner_speed_floor` — 137.12 s (−31.00 s vs Exp 7), damage 1, max 171.9 km/h

The speed floor fixed the main failure mode of Exp 7 — the car can re-accelerate cleanly after an off-track excursion. But it sits 3.13 s behind Exp 6's best, and damage = 1 appeared for the first time since the crash experiments. The car is still going wide on critical turns, meaning the corner-aware suppression window needs refinement rather than removal. The gap to Exp 6 is small enough that a moderate speed increase on the open straights (where the corner-aware block is inactive) should recover it without reintroducing the turn problems.

---

## Exp 9 · `exp09_ceiling_160` — 133.52 s (−3.60 s vs Exp 8; **new best**), damage 2, max 177.7 km/h

New best by a slim 0.47 s over Exp 6, with the car now reaching 177.7 km/h — 55 km/h above the baseline. The margin is thin and damage climbed to 2, both pointing to the same root cause: the throttle ramp of `±0.01/step` (100 steps = 2 s to sweep full range at 50 Hz) is too sluggish to react when the corner-aware block drops `target_speed`. The car enters the suppression zone still carrying old throttle, arriving hotter than intended. Doubling the ramp rate halves that lag and should let both acceleration and deceleration track the target speed more tightly.

---

## Exp 10 · `exp10_throttle_ramp_02` — 135.42 s (+1.90 s vs Exp 9), damage 18, max 171.3 km/h

Damage jumped from 2 to 18 — a 9× spike — while lap time barely moved. The faster ramp didn't cause the oscillation; it amplified one that was already there. At 170+ km/h the car moves laterally much faster than at the 114 km/h of Exp 2 when the `0.20` centre-gain was set. Each over-correction now arrives harder and faster, building a left-right weave that becomes wall contacts through the second half. The throttle ramp change is kept but the steering must be addressed first — reducing the centre-tracking gain is the immediate priority.

---

## Exp 11 · `exp11_center_gain_015` — 127.02 s (−8.40 s vs Exp 10; **new best**), damage 39, max 171.5 km/h

The biggest lap time leap yet — 22.5 s faster than the baseline — but also the worst damage total, and the first run didn't even complete the lap. The car is fast enough; it just can't handle the chicane. Reducing centre-gain from `0.20` to `0.15` calmed the straight-line weave but made no difference at the chicane, where the dominant problem is yaw response, not lateral drift. The angle gain (`×10`) is the remaining lever: at 170+ km/h, a yaw correction that felt right at 100 km/h is now snapping the car past the apex and into the opposite wall. Reducing it is the next logical step.

---

## Exp 12 · `exp12_angle_gain_8` — partial (crash), damage 77, max 170.9 km/h

Reducing the angle gain made things dramatically worse — damage tripled and the lap didn't complete. This is a clear diagnostic: the problem at the chicane is not over-aggressive steering but insufficient speed reduction before entry. A lower gain means less steering authority, so the car ran wide on chicane entry, overcorrected on the counter-turn, and hit the wall harder. The angle gain is not the lever. The chicane wall doesn't appear in the dead-ahead `track[9]` beam until the car is already in it — the brake fires too late. The fix is to use the minimum of several central forward-facing beams so that a wall arriving at any angle within ~±7° of forward triggers the brake (and throttle suppression) early enough.

---

## Exp 13 · `exp13_multibeam_brake` — 124.09 s (−2.93 s vs Exp 11; **new best**), damage 0, max 171.3 km/h

Best result so far and the first clean lap at this speed range — zero damage, 25.4 s faster than the baseline. Multi-beam sensing solved the chicane crash by detecting the angled wall in the adjacent beams before the dead-ahead beam registered it. The car still goes slightly wide on critical turns, pointing to one remaining braking inefficiency: the formula uses `speedX / 150` as its scaling factor, but the car is running at 170+ km/h. This means the factor exceeds 1.0 and `clip()` caps it, compressing the gradual zone — full braking kicks in earlier than the geometry intends. Correcting the reference to `170` restores the full proportional profile at current race speeds.

---

## Exp 14 · `exp14_brake_ref_170` — 130.81 s (+6.72 s vs Exp 13), damage 90, max 171.5 km/h

A clear counter-result. Raising the reference from `150` to `170` made the braking force gentler at any given distance — which was the intent — but at the chicane the car now arrives faster than before because the brake no longer provides the hard stop it needs. Exp 13's `ref=150` was accidentally correct: the over-scaling (factor > 1.0 → clip to full brake at ~47 m) was providing exactly the hard stop the chicane demands. The `ref=170` change removed that safety margin. The fix is to extend the trigger distance to 80 m: the brake starts earlier, giving the gentler `ref=170` profile more time and distance to shed the same amount of speed as before — without losing the graduated, steer-able quality.

---

## Exp 15 · `exp15_brake_dist_80` — 134.10 s (+10.01 s vs Exp 13 best), damage 24, max 171.2 km/h

Damage improved from 90 to 24 but the lap time moved further away from Exp 13. The three-experiment sequence since Exp 13 reveals a consistent pattern: any change that makes the brake gentler at a given distance causes the chicane to be approached too fast. Exp 13's `ref=150` at 60 m was accidentally providing maximum braking in the final ~13 m because the formula clipped — and that hard stop in the last few metres is what the chicane demands. Rather than continuing to tune the brake shape, the more productive path is to raise the speed ceiling: at 180 km/h the current brake formula will automatically produce more force, and the corner-aware throttle suppression (which scales with the same speed ceiling) will start cutting throttle earlier, addressing both entry speed and braking simultaneously.

---

## Telemetry Fix · `LAP_WRAP_THRESHOLD` raised `100 m` → `200 m`

At 188 km/h Exp 16 laps were completing but not being recorded — `lap_summary.csv` showed `partial` with no time. The finish-line detector checks `distFromStart < 100 m`, but at ~52 m/step the car crosses the line and lands above 100 m in the same step, so the condition never fires. Raising `LAP_WRAP_THRESHOLD` to 200 m makes the window large enough for any speed up to ~350 km/h. No driving behaviour is affected — the fix is purely in the telemetry logging constant on line 594.

---

## Exp 16 · `exp16_ceiling_180` — 132.482 s, damage 0, max 186.985 km/h

New best. Raising the speed ceiling to 180 km/h allowed the car to accelerate freely on the main straight, reaching nearly 187 km/h. Three specific problems were identified from observation: (1) the V-shaped last corner — car goes badly off-track and recovers slowly, costing several seconds; (2) the chicane in the middle — throttle and brake fire simultaneously, causing a messy entry; (3) wide turns — the 5-beam minimum falsely triggers the throttle suppression on inside kerbs, limiting speed on safe curves to ~108–112 km/h. These are the three targets for Exp 17–19.

---

## Exp 17 · `exp17_brake_100m_quadratic` — 122.862 s (−9.62 s vs Exp 16; **new best**), damage 20, max 185.9 km/h

New best by a significant margin — 26.6 s faster than the baseline. Extending the brake window to 100 m and switching to a quadratic force formula kept the car much closer to the track through the V-corner: it still went slightly off but recovered far faster than in Exp 16, confirming the direction is right. Damage of 20 appeared, coming from the chicane: the car went slightly off-track there and bounced around in an unstable manner — it couldn't hold a straight line through the two direction changes. This is the exact behaviour targeted by Exp 18 (raise the throttle suppression threshold to 100 m so the car lifts off earlier before the chicane entry, decoupling throttle lift from brake application). The V-corner still needs more work too, but the gain here is real and the change is kept.

---

## Exp 18 · `exp18_throttle_suppress_100m` — 132.124 s (+9.262 s vs Exp 17), damage 41, max 186.750 km/h

A clear regression — 9.26 s slower than Exp 17 and damage doubled from 20 to 41. Raising the throttle suppression window to 100 m on the same 5-beam minimum backfired: the ±1° side beams were clipping the inside kerb on the curved approach *before* the chicane at ~80–100 m, dropping `target_speed` to ~90 km/h on a section the car could safely take at 160+ km/h. This slowed the car but also pulled it off-centre laterally, so it entered the chicane's first direction change at the wrong position and spun wide. The V-corner continued to cause problems as well. The root cause is the 5-beam window, not the 100 m distance — Exp 19's 3-beam central window is the direct fix.

---

## Exp 19 · `exp19_narrow_throttle_beam` — 127.522 s (−4.602 s vs Exp 18), damage 25, max 187.537 km/h

Partial recovery from the Exp 18 regression — 4.6 s faster and damage down from 41 to 25. Narrowing the throttle sensor from 5 beams to 3 beams prevented the inside-kerb false triggers that were destabilising the approach to the chicane. The car's handling in the third U-shaped turn looks acceptable. However, the chicane remains problematic: the car drifts wide in the first direction change — less than before, but still bounces and takes damage — and struggles through the counter-turn, drifting wide again. The V-corner also still loses the car off the track. The improvement confirms the beam-narrowing direction is correct, but both the chicane and V-corner still need further work. The speed-dependent braking behaviour at higher speeds must be verified before making additional adjustments, since the quadratic formula may perform differently as the car continues to gain speed.

---


## Exp 20 · `exp20_ceiling_200` — 126.452 s (−1.07 s vs Exp 19), damage 22, max 205.730 km/h

A step forward — the ceiling change is confirmed working (205.7 km/h vs the old 187.5 km/h cap) — but the time gain is smaller than the speed gain suggests. The V-corner is the reason: the car overshoots badly and loses most of the advantage gained on the straight. The chicane is less dangerous than feared at this speed; the car drifts wide and bounces but exits the counter-curve faster than expected, so the net time loss there is modest. The damage of 22 comes from those contacts rather than a full spin-out. The straight speed ceiling has now been pushed as far as it usefully can go with the current braking window — the next lever is extending the brake trigger distance so the car begins shedding speed earlier at 205+ km/h, directly targeting the V-corner overshoot and giving the chicane approach a wider safety margin.

---

## Exp 21 · `exp21_brake_120m` — 128.442 s (+1.99 s vs Exp 20), damage 19, max 204.516 km/h

A regression — slower than Exp 20 and barely any damage improvement. The wider brake window exposed a structural weakness in the quadratic formula: at 120 m from the wall, force = 0; at 90 m, force ≈ 0.25; at 60 m, force ≈ 0.56. Most of the deceleration is still concentrated in the final 30 m, which is the same stopping zone as before — the car just coasts lightly for an extra 20 m first. That early coasting bleeds top-speed time on the straight and reduces corner entry speed only marginally. The V-corner requires a hard, decisive stop in the 60–30 m zone; the chicane requires a controlled, sustained scrub of speed across the full window. Neither problem is solved by simply making the window wider. The next lever must be the braking force shape itself — or the throttle response that precedes it — not the trigger distance.

---

## Telemetry Fix 2 · `LAP_WRAP_THRESHOLD` raised `200 m` → `400 m`

At 204 km/h Exp 22 laps are completing but not recording — the same problem as at 188 km/h in the first telemetry fix. The 200 m window is no longer large enough at this speed (~57 m/step). Raising the threshold to 400 m covers any speed up to ~360 km/h without risk of false triggers (still 100 m below the `LAP_MIN_DIST_PREV = 500 m` guard). No driving behaviour changes.

---

## Exp 22 · `exp22_brake_twostage` — 139.764 s (+11.32 s vs Exp 21), damage 13, max 196.724 km/h

The worst completed lap since Exp 7 — 17.3 s off the Exp 17 best, despite a small damage improvement. The two-zone design was correct in principle: the V-corner is noticeably better (car barely leaves the racing line). But the linear inner zone starting at 0.667 force at 40 m was far too abrupt at 200 km/h — it caused brake lockup across the whole lap, not just at the critical corners. Lockup does three things simultaneously: it removes steering authority, activates the traction control which cuts throttle, and creates the side-to-side oscillation that was observed. The car effectively braked itself into instability everywhere the inner zone fired, including on open curves where the 5-beam minimum briefly reads <40 m on an inside kerb. The direction — harder braking in the inner zone — is confirmed correct by the V-corner improvement. The problem is the abruptness of the 0.667 handover, not the concept. The fix is to lower the handover point (e.g. 20–25 m) so the linear ramp only fires very close to the wall where it is genuinely needed, and the quadratic formula handles everything from 120 m down to that point.

---

## Exp 23 · `exp23_quadratic_tcs_gate` — 126.328 s (−13.436 s vs Exp 22), damage 33, max 205.625 km/h

Two failure modes from Exp 22 were fixed in one step: the brake reverted to the proven 100 m pure quadratic, and the TCS was gated to fire only during acceleration (`R['brake'] < 0.05`). The lap time recovered sharply — 13.4 s faster than Exp 22 and within 3.5 s of the all-time best. The TCS gate is the key gain: without it cutting throttle simultaneously during braking, the side-to-side oscillation that plagued Exp 22 is gone and the car can carry full speed through the straights. However, the damage figure climbed from 13 to 33 — the chicane and V-corner instability returned, now worse than in Exp 20–21. The reason is physics: with the TCS no longer acting as an accidental speed governor during braking, the car arrives at both critical corners with more energy than the 100 m quadratic can shed cleanly. The TCS gate was the right fix; the brake formula and/or trigger distance must now grow to match the energy the car is carrying at 205 km/h.

---


## Exp 24 · `exp24_ceiling_250` — partial (crash), damage 21, max 209.550 km/h

The ceiling change worked exactly as the physics predicted — the car accelerated to 209.5 km/h, confirming the straight is long enough to benefit from a 250 km/h target. But the lap could not be completed: the U-corner and the open bend before the chicane cost time with off-track excursions, and the chicane itself ended the run — the car bounced over the curbing on the first direction change, came to rest facing the wrong way, and could not rejoin. The root cause is the exact calibration shift that was anticipated: raising `ref` from 200 to 250 reduces braking force at 210 km/h from `(210/200)² ≈ 1.10` (clipping) to `(210/250)² = 0.706` — a 36% reduction. The 100 m trigger window was already marginal at 205 km/h in Exp 23; with 36% less force it cannot shed enough energy at the U-corner or chicane entry. The ceiling is correct; the brake trigger distance must grow immediately to compensate.

---


## Exp 25 · `exp25_brake_dist_160` — partial (maxsteps, 125.2 s), damage 26, max 196.297 km/h

Two runs, both hitting the 100,000-step cap: the car reached `curLapTime ≈ 125.2 s` at step 100,000 but never crossed the finish line within the budget. This is not a crash — it's a time overrun driven by the off-track excursions at the chicane and V-corner. The direction is correct: extending the trigger to 160 m restored lap-ability after Exp 24's catastrophic failure, and damage held at 26 both times. But the 160 m window introduced a new structural problem: the 5-beam sensor reads distant kerbs and barriers on open sections and applies a small but continuous brake drag, which explains why max speed dropped to 196 km/h from 209.5 km/h in Exp 24. More critically, the suppress window remained at 100 m — putting it 60 m inside the brake trigger. For the first 60 m of every braking zone, the car is simultaneously on full throttle and beginning to brake, working against itself. The throttle suppress window must be extended to 160 m immediately to eliminate that overlap, using the 3-beam narrow sensor to protect against the kerb false-triggers that wrecked Exp 18.

---


## Exp 26 · `exp26_suppress_160` — partial (maxsteps, 130.0 s), damage 23, max 193.718 km/h

Extending the suppress window to 160 m made things measurably worse: `curLapTime` at the step cap rose from 125.2 s to 130.0 s, and max speed fell another 2.6 km/h to 193.7 km/h. The 3-beam sensor is picking up walls through curved approach sections at 160 m and cutting `target_speed` on bends where the car should be at full speed — the same kerb false-trigger problem that wrecked Exp 18, now at a larger scale. Damage only improved marginally (26 → 23), confirming that the throttle+brake overlap was not the primary damage source. The suppress window is now too wide and must be pulled back. The real remaining problem is the brake force profile itself: the quadratic distance term produces too little force in the 60–20 m zone where the V-corner and chicane demand a decisive stop. A steeper distance exponent — specifically a sub-unitary power on the distance ratio that front-loads force into the inner zone without a step change — is the correct next lever.

---


## Exp 27 · `exp27_brake_cubic_dist` — 129.218 s, damage 21, max 191.325 km/h

The lap completed for the first time since Exp 23 — the `^0.6` distance exponent confirmed that concentrating more brake force in the 60–20 m inner zone without a step change is the right approach. Damage fell modestly from 23 to 21, and the chicane and V-corner remain the damage sources, now with less severity. However, max speed dropped to 191 km/h — 14 km/h below Exp 23 — because the 160 m suppress window is cutting `target_speed` on approach curves where the 3-beam sensor reads a distant wall at <160 m. Every suppressed bend bleeds 1–2 km/h and a fraction of a second. The `^0.6` brake shape is the correct direction and should be kept; the suppress window must shrink. The key lesson from this run and the entire Exp 24–27 arc: the Exp 22 two-zone brake was rejected too hastily. Its goal — harder braking in the inner zone — was sound; only the implementation (an abrupt linear step at 40 m) was wrong. The `^0.6` continuous power profile achieves the same goal without lockup, effectively re-validating the Exp 22 concept with a smoother execution.

---

## Telemetry Fix 3 · `maxSteps` doubled `100 000` → `200 000` · `LAP_WRAP_THRESHOLD` raised `400 m` → `500 m` · `LAP_MIN_DIST_PREV` raised `500 m` → `1 000 m`

Three coupled constants changed together; no driving logic affected.

**`maxSteps` (`Client.__init__`, line 135)** — Experiments 25, 26, 28 and 29 all hit the 100 000-step cap before crossing the finish line. The clean-lap budget is only ~8 750 steps (warmup ~45 s + flying lap ~130 s = ~175 s × 50 Hz). Off-track recovery phases at near-zero speed, however, can consume thousands of steps while advancing the car only a few metres. Exp 28's notes confirm the car was ~10 m from the finish at the cap — proof the budget was exhausted by crawl-recovery time, not by the lap itself. Doubling to 200 000 steps (4 000 s of simulated time) absorbs any realistic recovery phase with no impact on lap-time measurement, which comes from TORCS's own `lastLapTime`, not from step count.

**`LAP_WRAP_THRESHOLD` (`TELEMETRY CONFIGURATION`, line 598)** — The finish-line detector fires when `distFromStart < LAP_WRAP_THRESHOLD`. At 250 km/h the car covers ~69 m per step. The previous 400 m window gave only ~5.8 consecutive steps in which to catch the crossing. Raising to 500 m gives ~7.2 steps — a comfortable margin at the current ceiling. This follows the same pattern as Telemetry Fix 1 (100 → 200 m at ~188 km/h) and Telemetry Fix 2 (200 → 400 m at ~204 km/h); this time the raise is pre-emptive rather than reactive.

**`LAP_MIN_DIST_PREV` (`TELEMETRY CONFIGURATION`, line 601)** — This guard prevents a false crossing when the car is already near the start line. It must exceed `LAP_WRAP_THRESHOLD` by a margin large enough that no normally-placed car can satisfy both conditions simultaneously. With `LAP_WRAP_THRESHOLD` raised to 500 m the old guard of 500 m would have zero separation. Raising to 1 000 m restores a 500 m gap and is safe for the ~3 600 m Corkscrew (a car must have traversed at least 1 000 m before a crossing is counted).

**`lap_summary.csv` reconstruction** — The six partial rows for experiments 24–26 and 28–29 already existed in the file but had a blank `sim_lap_time_s` column, because the logger has no value for a lap that never crosses the line. The `curLapTime` from the final step of each run in `lap_data.csv` was back-filled into that field:

| Experiment | Run | `curLapTime` at cap | Note |
|---|---|---|---|
| exp24_ceiling_250 | 968b3d76 | 158.726 s | `keyboard_interrupt` — car crashed, user stopped session |
| exp25_brake_dist_160 | ae18ce47 | 125.234 s | `maxsteps_or_shutdown` |
| exp25_brake_dist_160 | a0c19229 | 125.454 s | `maxsteps_or_shutdown` |
| exp26_suppress_160 | 36608e28 | 130.006 s | `maxsteps_or_shutdown` |
| exp28_unified_140 | 5d12696c | 128.106 s | `maxsteps_or_shutdown` — car was ~10 m from finish |
| exp29_throttle_ramp_03 | c93660f6 | 125.564 s | `maxsteps_or_shutdown` |

---


## Exp 28 · `exp28_unified_140` — partial (maxsteps, ~128.1 s), damage 27, max 193.220 km/h

The 140 m unified window is a step in the right direction: `curLapTime` at the step cap improved again (128.1 s vs 129.2 s in Exp 27) and top speed recovered from 191 to 193 km/h. The car was within ~10 m of the finish at the step limit — essentially a complete lap timed at ~128 s. Damage rose slightly from 21 to 27, which pinpoints the remaining problem precisely: pulling both windows back to 140 m gave the car less runway to decelerate, so it arrives at the chicane entry marginally faster than in Exp 27. The chicane *exit* is now clean — the `^0.6` profile gives the car enough authority to stop and turn — but the *entry* is still too hot. The V-corner continues to force a large off-track excursion. Both problems are throttle-response lag: at 193 km/h, `±0.02/step` takes 1.0 s and 54 m to cut from full throttle to zero. The suppress fires at 140 m, but 54 m of the window is consumed before accel even reaches zero — leaving only 86 m of genuinely settled braking. Raising the ramp to `±0.03` cuts the response lag to 0.67 s / 36 m, giving 104 m of effective deceleration — a direct fix for the chicane entry problem.

---



## Exp 29 · `exp29_throttle_ramp_03` — partial (maxsteps, 125.6 s), damage 24, max 198.935 km/h

A marginal improvement that did not resolve the core problem. The faster `±0.03` ramp was designed to recover 18 m of effective deceleration window by cutting throttle more crisply once the 140 m suppress fires — and the telemetry supports that it worked as intended: the chicane exit was clean, max speed rose to 198.9 km/h, and damage fell slightly from 27 to 24. But the step-cap overrun persisted (`curLapTime = 125.564 s` at step 100,000), and the car was still losing time in off-track excursions at the chicane entry and V-corner. The arc from Exp 25 through Exp 29 — five consecutive step-cap overruns — tells a consistent story: the 250 km/h ceiling with `ref=250` delivers only ~64% of calibrated braking force at the car's actual race speed, and no combination of window widths, distance exponents, or throttle ramp rates can close that structural gap. The right fix is not incremental — it is to revisit the speed reference itself.

---

## Exp 30 · `exp30_zone_brake` — 144.206 s (+18.6 s vs Exp 29 at cap), damage 93, max 195.244 km/h — **REJECTED**

The worst result since Exp 7 and a categorical failure. The position-triggered zone ramps — designed to slow the car before the chicane and V-corner — instead fired hard braking continuously through the entire chicane transit, including the counter-turn and exit. The 90 km/h speed cap activated from 2300 m (110 m before the chicane entry, C9 at ~2411 m) and remained active until 2540 m, blanketing the final 110 m of the approach straight and the first half of the chicane simultaneously. The result was a car that was both too slow on the approach and unable to rotate through the direction changes, because full-force braking was still active when it needed to steer. Damage of 93 is the worst total since Exp 14 and the highest ever for a completed lap. The concept — address the chicane and V-corner with earlier, stronger deceleration — is sound; but position-triggered logic requires zone boundaries calibrated to approach-only sections, with the braking ramp released before the apex. An approach-only zone that deactivates at the turn-in point would avoid the problem. Alternatively, a structural solution that restores `ref=180` eliminates the force deficit without any position logic at all.

---

## Exp 31 · `exp31_brake_180m` — partial (maxsteps), damage 26, max 181.781 km/h

A step backwards. Widening both windows to 180 m with a `^0.5` exponent produced the lowest top speed of the entire 250 km/h era — 181.8 km/h, down from 198.9 km/h in Exp 29. The loss confirms a recurring pattern: every time the suppress window has been extended beyond ~140 m on the 3-beam sensor, the car loses 10–17 km/h of top speed because the sensor reads a wall or distant barrier on approach curves at that distance range and cuts `target_speed` prematurely. At 180 m that effect is more severe than at 160 m (Exp 26), and the damage did not improve despite the wider braking window. The `^0.5` exponent provides slightly more force in the outer zone than `^0.6`, but neither can compensate when the car enters the braking zone already 15–17 km/h below intended speed because the suppress has been running for the past 40–60 m. The data from Exp 17 through Exp 31 now form a clear pattern: the only configuration that produced a sub-125 s, zero-damage lap is Exp 17 (`ref=180`, 100 m window, standard linear distance term). Every departure from that configuration — raising `ref`, widening windows, changing exponents — has either degraded lap time, increased damage, or both.

---

## Exp 32 · `exp32_restore_exp17_base` — 121.652 s (−1.210 s vs Exp 17; **new all-time best**), damage 19, max 187.532 km/h

The best lap time in the project so far — beating Exp 17's 122.862 s by 1.21 s. Restoring the Exp 17 brake and throttle parameters while carrying forward the two improvements confirmed since that experiment — the 3-beam throttle sensor (Exp 19) and the TCS gate (Exp 23) — proved more effective than any configuration tried in the intervening fourteen experiments. The 3-beam sensor prevents premature throttle cuts on chicane approach curves, and the TCS gate eliminates the simultaneous throttle reduction that caused side-to-side oscillation during braking. Together they produce a calmer, more settled approach to both critical sections. Damage of 19 remains, indicating the car is still contacting the barriers at the chicane and V-corner. A second run recorded 132.868 s with damage 21, reflecting variability in how the car handles the chicane on a given run. The structural mismatch between the 80 m suppress window and the 100 m brake window — where the car simultaneously applies brake force and near-full throttle for 20 m — is the most likely remaining contributor to the off-track contacts.

---

## Exp 33 · `exp33_suppress_100m` — 124.618 s (+2.97 s vs Exp 32 best), damage 20, max 187.314 km/h

A slight regression from Exp 32's best run, despite a theoretically sound fix. Closing the 20 m suppress-brake overlap by raising the suppress window from 80 m to 100 m did not produce the improvement in oscillation or damage that was predicted. The lap time increased by ~3 s and damage remained at 20 — effectively unchanged. The top speed of 187.314 km/h is nearly identical to Exp 32's 187.532 km/h, confirming the 3-beam sensor is not triggering on kerbs at 100 m (the Exp 18 failure mode). The result suggests that the 20 m overlap — while real — is not the dominant driver of the remaining damage and instability at the chicane and V-corner. Both sections continue to produce off-track excursions regardless of whether the car's throttle is partially open or fully closed at the 100 m mark. A different intervention is needed: either a change to the lateral positioning of the car on the approach, or a direct increase in braking force in the critical inner metres.

---

## Exp 34 · `exp34_zone_centre_gain` — 122.654 s (−2.036 s vs Exp 33), damage 23, max 186.743 km/h

A meaningful lap time recovery from Exp 33 — 2.04 s faster and within 1.0 s of the all-time best — confirming that lateral positioning on the approach sections influences corner entry quality. Boosting the centre-tracking gain from 0.15 to 0.17 on the chicane approach (2300–2500 m) and V-corner approach (2700–2830 m) pulled the car closer to the centreline before each critical direction change, allowing it to enter the apex from a more neutral lateral position. However, damage increased from 20 to 23, suggesting the slightly stronger centring correction is marginally destabilising the car's yaw balance at the apex rather than purely settling it. The lap time and max speed (186.743 km/h) are consistent with the Exp 32–33 range, confirming the zone centre gain is not adversely affecting the rest of the circuit. The chicane and V-corner remain the limiting factors; the zone gain addresses lateral positioning but not entry speed — a further reduction in approach speed at those two sections remains the next challenge.


---

## Telemetry Fix 4 · `lap_data.csv` routed to `telemetry/` · `_open_csv_new` · lap-counter deferral · flush-after-reply · server-end guard

Five structural deficiencies in the CSV-writing section were corrected together; no driving logic changed.

**`lap_data.csv` routing and `_open_csv_new` (lines 675–685, 691–693, 713)** — Previously all runs for a given experiment appended to a single `lap_data.csv` file in the script directory, making it impossible to isolate the row set for a single run without filtering by `run_id`. A new `_open_csv_new()` helper (opens in write mode, always creates a fresh file) was added; `lap_data.csv` is now written to `telemetry/<EXPERIMENT_ID>_lap_data.csv`, one file per invocation. The `telemetry/` sub-directory is created automatically via `os.makedirs(..., exist_ok=True)`. The cumulative `lap_summary.csv` retains the append-safe `_open_csv()` path unchanged.

**Server-end guard (lines 718–720)** — TORCS signals a race completion by closing the socket (`C.so` becomes falsy). Previously this case fell through to the standard break path with `_completion_reason = "unknown"`, which was then overwritten unconditionally by the post-loop assignment. A `if not C.so` guard now sets `_completion_reason = "race_completed"` and breaks immediately, giving the completion reason a precise label.

**Lap-counter deferral via `_flush_summary` / `_advance_lap` flags (lines 783–823)** — In the backup, lap-counter advancement (`lap_id += 1`, `lap_status = "flying"`, etc.) occurred inside the `crossed_finish` block *before* the `lap_data.csv` row for that step was written. This meant the crossing step was recorded under the new lap's `lap_id` rather than the lap that just finished. The fix introduces two boolean flags: `_advance_lap` is set `True` when a crossing is detected and the summary row written, but the counters are incremented only after the `lap_data.csv` row — ensuring the crossing step is permanently attributed to the lap that completed.

**Flush-after-reply ordering (lines 864–871)** — `lap_data_fh.flush()` and `lap_summary_fh.flush()` were previously called before `C.respond_to_server()`, adding OS-level syscall latency to the TORCS UDP reply path. Both flush calls are now placed after `respond_to_server()` so the UDP packet is on the wire before any kernel I/O occurs. `writerow()` itself is a pure userspace buffer append and remains before the reply, which is correct.

**Conditional post-loop reason (line 875)** — The post-loop statement `_completion_reason = "maxsteps_or_shutdown"` was unconditional, silently overwriting `"race_completed"` set by the server-end guard. The assignment is now guarded: `if _completion_reason == "unknown": _completion_reason = "maxsteps_or_shutdown"`. No driving behaviour is affected by any of these changes.

---

## Exp 35 · `exp35_sensor_90deg` — 123.1 s (−0.2 s vs Exp 34 best), damage 21, max 180.3 km/h

The change from a ±45° to a ±90° sensor arc does not appreciably alter driving behaviour because the exp34 logic continues reading the same internal indices (7–11 for braking, 8–10 for suppression); lap time remains almost identical (−0.2 s). The real benefit of the change shows up in telemetry: `min_valid_track` now reflects the true nearest edge across the full arc, and at T4 the value drops consistently to 0.0 m — confirming that the car goes systematically off-track at that corner even though the brake does not detect it because the dangerous wall is on the flank, not ahead. The residual damage of 21 persists because the wider sensors do not modify the speed at T4 (still 85 km/h, 13 km/h above the physical limit for that radius). The next step is to replace the target speed system to calibrate T4 and T11 using their real radii.

---

## Exp 36 · `exp36_zone_speed_map` — 148.3 s (+25.2 s vs Exp 35), damage 0, max 174.8 km/h

First damage-free steady-state lap of the project — the car completes four consecutive laps with zero damage, lap times converging to 148–149 s. Replacing forward suppression with a physical zone table eliminates the off-track excursions at T4 (target_speed drops to 85 km/h, sufficient to contain the car) and at T11 (target_speed 50 km/h). Max speed falls from 180 to 174 km/h because the long straights now also have approach zones where the car begins to brake earlier; the time penalty is the price of stability. The car still carries the original heuristic quadratic brake (100 m/ref=180) that was calibrated for forward suppression and is conservative for fast corners in this new context. The next step is to introduce the steering-coupled trail brake.

---

## Exp 37 · `exp37_trail_brake` — 147.1 s (−1.2 s vs Exp 36), damage 0, max 175.9 km/h

The 1.2 s improvement is modest because the trail brake is the second safety layer — on a circuit with conservative target speeds, the sensor brake rarely needs to intervene. The benefit shows up in line quality: the `trail_factor` reduces brake force as the steering wheel turns, allowing braking to begin earlier before the corner without generating the understeer that full-force braking produced at the apex. At Corkscrew T8 this is especially visible: the car brakes from 150 m out and the `trail_factor` progressively releases it while turning, preventing front-wheel lockup through the left-hand corner. Damage remains at zero. The racing line system is still the flat centring (target=0) inherited from exp34 — the car arrives at T4 from the centre rather than from the left, losing the ideal attack angle. The next step is to introduce the dynamic `target_trackPos`.

---

## Exp 38 · `exp38_racing_line` — 143.7 s (−3.4 s vs Exp 37), damage 0, max 176.2 km/h

Three and a half seconds of improvement with zero damage: the dynamic `target_trackPos` makes the car trace each corner from the outside toward the inside, reducing the geometric arc length driven and improving the exit angle. The most pronounced improvement occurs at T4 (entry from −0.4, apex at +0.4): the car no longer arrives at the right-hand corner from the centre of the track but from the left, executing a classic line that reduces the lateral speed required at the vertex. At the Corkscrew (2313–2456 m) the right-outside positioning (+0.5) allows the car to begin braking from the ideal line. Damage remains at zero — the `target_tp` values are well calibrated and no zone pushes the car into the tirewall. Steering is still `angle*10/PI` with no turn anticipation, producing reactive corrections instead of preventive ones; and the `steer*50` acceleration penalty limits straight-line speed. The next step is to introduce the `turn_bias` and remove that penalty.

---

## Exp 39 · `exp39_steer_turn_bias` — 148.2 s (+4.5 s vs Exp 38 — initial regression), damage 0, max 175.6 km/h

The introduction of `turn_bias` and the removal of the `steer*50` penalty initially produce a slight time regression (+4.5 s) with zero damage. The regression is not a failure: it reflects that `turn_bias` needs calibration — with coefficient 0.05 the turn anticipation generates a slightly positive steer on the S/F straight (a gentle opening left-hand bend), drifting the car to the right side of the straight and forcing corrections. Max speed drops slightly (175.6 vs 176.2 km/h), indicating the `turn_bias` is acting even on near-straight sections where it should not. However, the system is conceptually correct: the ±7° beam asymmetry is a valid physical signal of the surrounding geometry. The next step is to reduce the `turn_bias` coefficient from 0.05 to 0.03 — the value that appears in the current code ([`snakeoil3_v2.py:669`](snakeoil3_v2.py:669)) — and add the second stage of the steering system: reduction of the angle gain from 10/PI to 3.5/PI with proportional correction by racing-line error.

---

