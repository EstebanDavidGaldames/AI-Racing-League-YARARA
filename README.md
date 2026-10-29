<!--
╔══════════════════════════════════════════════════════════════════════════════════╗
║         AI RACING LEAGUE — Go full speed with IBM Bob                          ║
║                     Academic Competition                                        ║
╚══════════════════════════════════════════════════════════════════════════════════╝
-->

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   ██╗   ██╗ █████╗ ██████╗  █████╗ ██████╗  █████╗                             ║
║   ╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗                            ║
║    ╚████╔╝ ███████║██████╔╝███████║██████╔╝███████║                            ║
║     ╚██╔╝  ██╔══██║██╔══██╗██╔══██║██╔══██╗██╔══██║                            ║
║      ██║   ██║  ██║██║  ██║██║  ██║██║  ██║██║  ██║                            ║
║      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  Á                        ║
║                                                                                  ║
║                    AI RACING LEAGUE — Go full speed with IBM Bob                ║
║                            Academic Competition Entry                            ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║   Team  >>>  Y A R A R Á   (Solo Entry)                                         ║
║                                                                                  ║
║    /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\       ║
║   <  ≋ ≋ ≋  Bothrops alternatus  ·  South American Pit Viper  ≋ ≋ ≋  >        ║
║    \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/         ║
║                  ≋≋≋                                                             ║
║             ≋≋≋≋≋≋≋≋≋≋                                                          ║
║          ≋≋≋≋( ◉  ◉ )≋≋≋                  __|====|__                           ║
║           ≋≋≋≋≋≋≋≋≋≋≋≋         F1    ____/  |    |  \____                      ║
║            ≋≋≋≋≋≋≋≋≋≋         ___   /  O  __|    |__  O  \                     ║
║             ≋≋≋≋~≋≋≋          |__|─/ \___/  \____/  \___/ \                    ║
║              ≋≋~⌇~≋≋               |  ─────────────────── |                   ║
║               ~~⌇~~                 \______________________/                   ║
║                                       ~~|~~|~~|~~|~~|~~|~~                     ║
║                                                                                  ║
║   ┌──── IBM 🐝 ─────────────────────────────────────────────────────────┐       ║
║   │  ____  ____  __  __       ╔══════════════════════════════════════╗  │       ║
║   │ |  _ \|  _ \|  \/  |     ║  ░░░░░░░░░  IBM Bob  ░░░░░░░░░░░░░  ║  │       ║
║   │ | |_) | |_) | |\/| |     ║      Your AI Coding Partner          ║  │       ║
║   │ |  _ <|  _ <| |  | |     ║  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  ║  │       ║
║   │ |_| \_\_| \_\_|  |_|     ╚══════════════════════════════════════╝  │       ║
║   │    (>o<)  🐝    Powering this entry — design · code · analysis      │       ║
║   └─────────────────────────────────────────────────────────────────────┘       ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║   Circuit   ▸  Corkscrew (Laguna Seca style — TORCS)                            ║
║   Driver    ▸  snakeoil3_v2.py  (39 experiments, rule-based)                    ║
║   Best Lap  ▸  121.652 s  ·  max 187.5 km/h  ·  damage 19  (Exp 32)            ║
║   Baseline  ▸  149.49 s   ·  stock snakeoil   ·  damage 0                      ║
║   Gain      ▸  −27.8 s  vs baseline  (+18.6 % faster)                          ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 🏁 Competition

**AI Racing League — Go full speed with IBM Bob**  
Academic challenge hosted by IBM, where participants tune a rule-based TORCS racing agent
to achieve the fastest possible lap on a designated circuit, guided end-to-end by
[IBM Bob](https://www.ibm.com/products/ibm-bob), IBM's AI coding assistant.

| | |
|---|---|
| **Circuit** | Corkscrew |
| **Simulator** | TORCS (The Open Racing Car Simulator) |
| **Driver type** | Rule-based Python agent |
| **Development tool** | IBM Bob (AI coding partner) |
| **Team** | Yarará (solo entry) |

---

## 🎬 Lap Video

▶ **[Watch the registered lap on YouTube](https://www.youtube.com/watch?v=g7Ml5rowLyY)**

> _Replace the link above with your actual YouTube URL before publishing._

---

## 📁 Repository Structure

```
repository/
│
├── README.md                         ← You are here
├── SUBMISSION.md                     ← Official competition entry document
├── FIRSTLAP.md                       ← Record of the first successful lap + baseline snapshot
├── CHANGELOG.md                      ← Full change log of all 39 experiments
├── LICENSE
│
├── driver/                           ← Racing agent code
│   ├── snakeoil3_v2.py               ← Final submitted driver (Yarará entry)
│   ├── snakeoil3_v1.py               ← Code base received from the competition
│   ├── EXECUTIVE-SUMMARY.md          ← Non-technical overview of the driver
│   └── TECHNICAL-SUMMARY.md          ← Parameter-level documentation
│
├── reports/                          ← Experiment data and analysis logs
│   ├── experiment-list.md            ← Full list of 39 experiments with rationale
│   ├── results_notes.md              ← Per-experiment results, observations, next steps
│   ├── lap_data.csv.rar              ← Step-level telemetry (compressed)
│   ├── lap_summary.csv.rar           ← Per-lap summary metrics (compressed)
│   ├── EXECUTIVE-SUMMARY.md          ← Non-technical overview of results
│   └── TECHNICAL-SUMMARY.md          ← Technical summary of all 39 experiments
│
└── analysis/                         ← Track analysis tooling
    ├── find_corners.py               ← Corner-mapping tool (sensor sweep analysis)
    ├── tuning-card.md                ← Quick-reference for all tunable parameters
    ├── corner-map-report-corkscrew-sectores.txt   ← Corner sector analysis output
    ├── corner-map-report-corkscrew-sensores.txt   ← Sensor-level corner map output
    ├── EXECUTIVE-SUMMARY.md          ← Non-technical overview of the analysis
    └── TECHNICAL-SUMMARY.md          ← Technical methodology and findings
```

---

## 🐍 The Project — Yarará Racing

Yarará is the South American pit viper (*Bothrops alternatus*) — a snake that reads the
terrain ahead, calculates the angle, and strikes with precision. That's the philosophy
behind this entry: **read the sensors, understand the geometry, act with intent.**

Starting from the stock `snakeoil3` Python client, 39 iterative experiments were conducted
over the Corkscrew circuit, each guided by telemetry analysis and IBM Bob's reasoning support.
The agent evolved from a 149-second baseline to a **121.6-second flying lap** — a 28-second
improvement achieved entirely through rule-based logic tuning, with zero external ML libraries.

### Key milestones

| Milestone | Experiment | Lap Time | Max Speed | Damage |
|---|---|---|---|---|
| Baseline (stock driver) | Exp 0 | 149.49 s | ~121 km/h | 0 |
| First sub-baseline lap | Exp 6 | 133.99 s | 171.4 km/h | 0 |
| First sub-130 s lap | Exp 11 | 127.02 s | 171.5 km/h | 39 |
| First zero-damage fast lap | Exp 13 | 124.09 s | 171.3 km/h | 0 |
| First damage-free steady state (4 laps) | Exp 36 | 148.3 s | 174.8 km/h | 0 |
| Racing line introduced | Exp 38 | 143.7 s | 176.2 km/h | 0 |
| **All-time best** | **Exp 32** | **121.652 s** | **187.5 km/h** | **19** |

---

## 🔧 How It Works — Driver Architecture

The driver (`snakeoil3_v2.py`) is a hand-tuned rule-based controller operating on TORCS's
19-beam sensor array. No machine learning is involved — every decision is a deterministic
function of the car's state.

```
Sensor input (19 beams + speed + position)
         │
         ├── Zone speed map     →  target_speed per track segment
         │                          (calibrated to corner radius)
         │
         ├── Multi-beam brake   →  quadratic proportional braking
         │                          (force ∝ (speed/ref)² · proximity²)
         │
         ├── Trail brake        →  force reduction when steering
         │                          (keeps front grip through corner entry)
         │
         ├── Throttle suppress  →  narrow 3-beam forward vision
         │                          (lifts off before brake zone)
         │
         ├── Racing line        →  dynamic target_trackPos per zone
         │                          (outside-apex-outside geometry)
         │
         ├── Steering           →  angle gain + centre gain + turn_bias
         │                          (reactive correction + anticipation)
         │
         └── Traction control   →  rear/front wheel spin gate
                                    (fires only during acceleration)
```

---

## 🚀 How to Run

**Requirements:** Python 3.x · TORCS with SCR patch · vtorcs-RL-color

```bash
# Start TORCS server in practice mode first, then:
python driver/snakeoil3_v2.py

# Optional flags (see top of file for full list):
python driver/snakeoil3_v2.py -p 3001 -e exp_id -s corkscrew
```

The driver writes per-step telemetry to `telemetry/<EXPERIMENT_ID>_lap_data.csv` and
lap summaries to `lap_summary.csv` automatically.

---

## 📊 Results at a Glance

```
Lap Time (seconds) — selected experiments
                                                      ← best: 121.6 s
  149 ┤▇  Exp 0  (baseline)
  145 ┤
  140 ┤
  137 ┤  ▇  Exp 6  (proportional brake)
  135 ┤
  133 ┤  ▇  Exp 9  (new best at the time)
  130 ┤
  127 ┤  ▇  Exp 11 (damage spike)
  125 ┤  ▇  Exp 13 (zero damage)
  123 ┤  ▇  Exp 17 (quadratic brake)
  122 ┤                                      ▇  Exp 32 (all-time best)
  121 ┤                                      ▇  121.652 s
      └────────────────────────────────────────────────────────────────
       Exp0   Exp6   Exp9  Exp11 Exp13 Exp17  ...  Exp32
```

---

## 🏎️ TORCS — The Simulator

```
  ████████╗ ██████╗ ██████╗  ██████╗███████╗
     ██╔══╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
     ██║   ██║   ██║██████╔╝██║     ███████╗
     ██║   ██║   ██║██╔══██╗██║     ╚════██║
     ██║   ╚██████╔╝██║  ██║╚██████╗███████║
     ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
  The Open Racing Car Simulator
```

TORCS is an open-source realistic car racing simulator widely used as a benchmark
environment for AI and reinforcement learning research.

> "The detailed explanation of original TORCS for AI research is given by
> Daniele Loiacono et al." — [arxiv.org/pdf/1304.1672.pdf](https://arxiv.org/pdf/1304.1672.pdf)

**Key TORCS references used in this project:**

| Component | Source |
|---|---|
| TORCS simulator core | [torcs.sourceforge.net](http://torcs.sourceforge.net/) |
| vtorcs-RL-color | [github.com/giuse/vtorcs](https://github.com/giuse/vtorcs) |
| SCR server patch | [scr.geccocompetitions.com](http://scr.geccocompetitions.com/) |
| Sensor/API reference | [xed.ch/help/torcs.html](http://xed.ch/help/torcs.html) |
| gym-torcs wrapper | [github.com/ugo-nama-kun/gym_torcs](https://github.com/ugo-nama-kun/gym_torcs) |

---

## 👏 Attributions & Credits

### snakeoil Python client

The Python client interface used as the base for this driver was written by
**Chris X Edwards** and is the canonical starting point for TORCS Python bots.

```
# snakeoil.py
# Chris X Edwards <snakeoil@xed.ch>
# Snake Oil is a Python library for interfacing with a TORCS
# race car simulator which has been patched with the server
# extensions used in the Simulated Car Racing competitions.
# http://scr.geccocompetitions.com/
```

### gym-torcs

The OpenAI-Gym-style TORCS wrapper (`gym_torcs.py`) was developed by
**Naoto Yoshida** during a spring 2016 internship at Preferred Networks.

> *"gym-torcs was developed during the spring internship 2016 at Preferred Networks."*

A notable application of gym-torcs was the DDPG experiment with Keras by
**Ben Lau**: [yanpanlau.github.io/2016/10/11/Torcs-Keras.html](https://yanpanlau.github.io/2016/10/11/Torcs-Keras.html)

### Python 3 adaptation

The Python 3 fork that makes the client compatible with modern Python was included
in the competition materials from IBM (`snakeoil3_jm2.py`, `jmcncarai.py`).

### IBM Bob

All experiment design, code modifications, telemetry analysis, and documentation
in this repository were produced in collaboration with
[IBM Bob](https://www.ibm.com/products/ibm-bob) — IBM's AI coding assistant.

---

## 👤 About the Competitor

| | |
|---|---|
| **Name** | Esteban David Galdames |
| **LinkedIn** | [linkedin.com/in/esteban-david-galdames](https://www.linkedin.com/in/esteban-david-galdames) |
| **GitHub** | [github.com/EstebanDavidGaldames](https://github.com/EstebanDavidGaldames) |

---

## 📄 License

Original gym-torcs code is provided under the MIT License.
See [`LICENSE`](https://github.com/EstebanDavidGaldames/AI-Racing-League-YARARA/blob/main/LICENSE) for details.

---

<sub>Yarará Racing · AI Racing League — Go full speed with IBM Bob · Solo Entry · Circuit: Corkscrew</sub>
