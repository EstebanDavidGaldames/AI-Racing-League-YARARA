# Tuning Card — snakeoil3_v2.py

All tunable values in `drive_example()`. Current state: first successful lap of Corkscrew.

| Setting | Current Value | What It Controls | If Raised | If Lowered | Risk |
|---|---|---|---|---|---|
| `target_speed` | `100` km/h | The speed the car aims for on open road | Car goes faster on straights; may overshoot corners if braking can't compensate | Car crawls around the track safely but very slowly | **Medium** |
| Steering angle gain | `15` | How sharply the car reacts to being pointed off-road | More aggressive correction; increases weaving and risk of snap-oversteer | Slower to realign after a corner; car may drift wide | **High** |
| Centre-tracking gain | `0.10` | How firmly the car pulls back to the middle of the track | Stronger centre pull; can cause oscillation fighting the angle correction | Car drifts closer to track edges without recovering well | **Medium** |
| Throttle step up | `+0.01` per tick | How quickly the driver presses the gas each tick | Faster acceleration out of corners; more wheelspin risk | Very gradual, smooth power delivery; slower lap times | **Low** |
| Throttle step down | `−0.01` per tick | How quickly the driver lifts off the gas each tick | Engine braking increases; car slows faster when over target speed | Car takes longer to reduce speed when it should be lifting | **Low** |
| Corner speed reduction | `steer × 50` | How much the target speed drops when the car is turning | Less speed reduction in corners; higher cornering speed, more crashes | Very slow through every corner even when not needed | **High** |
| Brake trigger distance | `20` metres | How close the wall ahead must be before brakes fire | Brakes earlier; safer but slower corner entry | Brakes later; less speed shed before apex, wall contact risk | **High** |
| Brake trigger speed | `60` km/h | Minimum speed for brakes to activate | Brakes fire at lower speeds; may stall car in slow sections | Brakes never fire at moderate speed; corners become dangerous | **Medium** |
| Brake pressure | `1.0` (full) | How hard the brakes are applied when triggered | N/A — already at maximum | Softer braking; less speed shed, may not slow enough in time | **Medium** |
| Low-speed boost threshold | `10` km/h | Below this speed an extra throttle kick is applied | Boost kicks in at higher speeds; may cause unwanted lunging | Boost only helps from near-standstill; slower recovery from stalls | **Low** |
| Traction control threshold | `5` rad/s | Rear-vs-front wheel spin difference before throttle is cut | Cut fires later; more wheelspin allowed before intervention | Cut fires very easily; throttle reduced even under normal acceleration | **Medium** |
| Traction control cut | `−0.2` throttle | How much gas is removed when wheelspin is detected | Larger cut; very aggressive traction control, may feel jerky | Smaller cut; wheelspin lingers longer before grip is recovered | **Low** |
| 2nd gear threshold | `50` km/h | Speed at which the gearbox shifts up to 2nd | Later upshift; engine revs higher before changing | Earlier upshift; engine may lug (feel weak) in 2nd at low speed | **Low** |
| 3rd gear threshold | `80` km/h | Speed at which the gearbox shifts up to 3rd | Later upshift; more acceleration available before 3rd | Earlier upshift; may reduce pulling power exiting mid-speed corners | **Low** |
| 4th gear threshold | `110` km/h | Speed at which the gearbox shifts up to 4th | Later upshift; engine stays in power band longer | Earlier upshift; car may feel flat between 3rd and 4th | **Low** |
| 5th gear threshold | `140` km/h | Speed at which the gearbox shifts up to 5th | Later upshift; more top-end acceleration in 4th | Earlier upshift into 5th; minor effect at current target speed | **Low** |
| 6th gear threshold | `170` km/h | Speed at which the gearbox shifts up to 6th | Later upshift; 6th never used at current 100 km/h target | Shifts into 6th sooner; no practical effect below target speed | **Low** |
