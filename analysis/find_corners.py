#!/usr/bin/env python3
"""
find_corners.py — Corner Map Report for TORCS Corkscrew telemetry
==================================================================
Reads lap_data.csv and lap_summary.csv produced by snakeoil3_v2.py
and reports candidate corner and straight zones for one recorded lap.

Usage
-----
  python find_corners.py --run RUN_ID --episode EPISODE_ID --lap LAP_ID

If any argument is omitted the tool lists the available IDs at that
tier and exits without processing any data.

Thresholds
----------
  Corner candidate  : forward_track < 40 m   (heuristic — adjust as needed)
  Straight candidate: forward_track > 150 m  (heuristic — adjust as needed)

These are discovery starting points, NOT exact track geometry boundaries.
forward_track is the dead-ahead (0°) radar beam; it is NOT sidewall clearance.

Requires: Python 3 standard library only.
Does not import or modify snakeoil3_v2.py in any way.
"""

import argparse
import collections
import csv
import math
import os
import sys

# ---------------------------------------------------------------------------
# Schema — must match snakeoil3_v2.py exactly
# ---------------------------------------------------------------------------

LAP_DATA_COLS = [
    "run_id", "episode_id", "lap_id", "step",
    "utc_timestamp", "elapsed_time_s",
    "experiment_id", "code_sha256", "track_id", "lap_status",
    "distFromStart", "distRaced", "curLapTime", "lastLapTime",
    "speedX", "trackPos", "angle",
    "steer", "accel", "brake", "gear",
    "forward_track", "min_valid_track", "damage",
]

LAP_SUMMARY_COLS = [
    "run_id", "episode_id", "lap_id",
    "experiment_id", "code_sha256",
    "status", "sim_lap_time_s",
    "damage_initial", "damage_final",
    "max_speed_kmh", "completion_reason",
]

# ---------------------------------------------------------------------------
# Sensor validity ranges
# ---------------------------------------------------------------------------

SENSOR_RANGES = {
    # field          : (min_exclusive_or_none, max_inclusive_or_none, allow_zero)
    "forward_track"  : (0.0,  200.0, False),   # (0, 200]
    "min_valid_track": (0.0,  200.0, False),   # (0, 200]
    "speedX"         : (-30.0, 300.0, True),   # [-30, 300]
    "trackPos"       : (-2.0,   2.0, True),    # [-2, 2]
    "angle"          : (-math.pi, math.pi, True),
    "damage"         : (0.0, 10000.0, True),
}

# ---------------------------------------------------------------------------
# Zone classification thresholds (adjustable via CLI)
# ---------------------------------------------------------------------------

DEFAULT_CORNER_THRESHOLD   = 40.0   # metres
DEFAULT_STRAIGHT_THRESHOLD = 150.0  # metres
GAP_TOLERANCE_STEPS        = 5      # missing steps before a gap is flagged

# ---------------------------------------------------------------------------
# Classification constants
# ---------------------------------------------------------------------------

CORNER     = "CORNER"
STRAIGHT   = "STRAIGHT"
TRANSITION = "TRANSITION"
UNKNOWN    = "UNKNOWN"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_float(value):
    """Return float or None; treats empty string as None."""
    if value is None or str(value).strip() == "":
        return None
    try:
        f = float(value)
        return f if math.isfinite(f) else None
    except (ValueError, TypeError):
        return None


def _validate_sensor(value_f, field):
    """
    Return True if value_f (already a float or None) is within the
    documented valid range for *field*.  None is always invalid.
    """
    if value_f is None:
        return False
    lo, hi, allow_zero = SENSOR_RANGES[field]
    if not allow_zero and value_f <= lo:
        return False
    if allow_zero and value_f < lo:
        return False
    if value_f > hi:
        return False
    return True


def _deg(radians):
    """Convert radians to degrees, rounded to one decimal place."""
    if radians is None:
        return "n/a"
    return "%.1f°" % math.degrees(radians)


def _script_dir():
    return os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# CSV loading helpers
# ---------------------------------------------------------------------------

def _load_csv(path, expected_cols):
    """
    Load *path* into a list of dicts.  Validate header against expected_cols.
    Returns (rows, error_message).  On success error_message is None.
    """
    if not os.path.exists(path):
        return None, "File not found: %s" % path
    with open(path, "r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        actual = list(reader.fieldnames or [])
        if actual != expected_cols:
            missing  = [c for c in expected_cols if c not in actual]
            extra    = [c for c in actual if c not in expected_cols]
            msg = (
                "Schema mismatch in %s\n"
                "  Expected : %s\n"
                "  Found    : %s\n"
                "  Missing  : %s\n"
                "  Extra    : %s\n"
                "Rename or regenerate the file to match snakeoil3_v2.py."
                % (path, expected_cols, actual, missing, extra)
            )
            return None, msg
        rows = list(reader)
    return rows, None


# ---------------------------------------------------------------------------
# ID discovery
# ---------------------------------------------------------------------------

def _collect_ids(summary_rows, data_rows):
    """
    Return an OrderedDict  run_id -> { episode_id -> set(lap_ids) }
    built from *both* files so the listing is complete even if one file
    is ahead of the other by a partial lap.
    """
    tree = collections.OrderedDict()

    def _add(run, ep, lap):
        if run not in tree:
            tree[run] = collections.OrderedDict()
        if ep not in tree[run]:
            tree[run][ep] = set()
        tree[run][ep].add(lap)

    for r in summary_rows:
        _add(r.get("run_id", ""), r.get("episode_id", ""), r.get("lap_id", ""))
    for r in data_rows:
        _add(r.get("run_id", ""), r.get("episode_id", ""), r.get("lap_id", ""))

    return tree


def _print_available_ids(tree, chosen_run=None, chosen_ep=None):
    """Print available IDs at the appropriate tier and exit."""
    if not tree:
        print("No data found in lap_data.csv or lap_summary.csv.")
        sys.exit(0)

    if chosen_run is None:
        # Top level: list all runs
        print("\nAvailable run IDs:")
        for rid in tree:
            ep_count  = len(tree[rid])
            lap_count = sum(len(v) for v in tree[rid].values())
            print("  %s  (%d episode(s), %d lap(s))" % (rid, ep_count, lap_count))
        print(
            "\nSelect a run with:\n"
            "  python find_corners.py --run RUN_ID\n"
        )
        sys.exit(0)

    if chosen_run not in tree:
        print("\nRun ID not found: %s" % chosen_run)
        print("Available run IDs:")
        for rid in tree:
            print("  %s" % rid)
        sys.exit(1)

    if chosen_ep is None:
        # Second level: list episodes within the chosen run
        print("\nRun: %s" % chosen_run)
        print("Available episode IDs:")
        for eid, laps in tree[chosen_run].items():
            print("  %s  (%d lap(s): %s)"
                  % (eid, len(laps), ", ".join(sorted(laps, key=lambda x: _lap_sort_key(x)))))
        print(
            "\nSelect an episode with:\n"
            "  python find_corners.py --run %s --episode EPISODE_ID\n"
            % chosen_run
        )
        sys.exit(0)

    if chosen_ep not in tree[chosen_run]:
        print("\nEpisode ID not found: %s  (in run %s)" % (chosen_ep, chosen_run))
        print("Available episode IDs for this run:")
        for eid in tree[chosen_run]:
            print("  %s" % eid)
        sys.exit(1)

    # Third level: list laps within chosen run+episode
    laps = tree[chosen_run][chosen_ep]
    print("\nRun    : %s" % chosen_run)
    print("Episode: %s" % chosen_ep)
    print("Available lap IDs: %s"
          % ", ".join(sorted(laps, key=lambda x: _lap_sort_key(x))))
    print(
        "\nSelect a lap with:\n"
        "  python find_corners.py --run %s --episode %s --lap LAP_ID\n"
        % (chosen_run, chosen_ep)
    )
    sys.exit(0)


def _lap_sort_key(lap_id_str):
    """Sort lap IDs numerically when possible, lexically otherwise."""
    try:
        return (0, int(lap_id_str))
    except (ValueError, TypeError):
        return (1, str(lap_id_str))


# ---------------------------------------------------------------------------
# Summary lookup
# ---------------------------------------------------------------------------

def _find_summary_row(summary_rows, run_id, episode_id, lap_id):
    """Return the matching summary row dict or None."""
    for r in summary_rows:
        if (r.get("run_id")    == run_id
                and r.get("episode_id") == episode_id
                and r.get("lap_id")     == lap_id):
            return r
    return None


# ---------------------------------------------------------------------------
# Data filtering and validation
# ---------------------------------------------------------------------------

def _filter_lap_rows(data_rows, run_id, episode_id, lap_id):
    """Return rows for the selected lap, sorted by step."""
    matched = [
        r for r in data_rows
        if (r.get("run_id")    == run_id
            and r.get("episode_id") == episode_id
            and r.get("lap_id")     == lap_id)
    ]
    # Sort by step counter (ascending)
    matched.sort(key=lambda r: _lap_sort_key(r.get("step", "")))
    return matched


def _validate_rows(rows):
    """
    For each row compute cleaned floats and validity flags.
    Returns (cleaned_rows, invalid_count).

    Each cleaned row is the original dict plus:
      _step        : int or None
      _dist        : float or None   (distFromStart)
      _speed       : float or None   (speedX)
      _track_pos   : float or None
      _angle_rad   : float or None
      _fwd         : float or None   (forward_track)
      _min_vt      : float or None   (min_valid_track)
      _damage      : float or None
      _fwd_valid   : bool
      _row_valid   : bool  (all required fields in range)
    """
    cleaned = []
    invalid_count = 0

    for r in rows:
        step_f    = _safe_float(r.get("step"))
        dist_f    = _safe_float(r.get("distFromStart"))
        speed_f   = _safe_float(r.get("speedX"))
        tpos_f    = _safe_float(r.get("trackPos"))
        angle_f   = _safe_float(r.get("angle"))
        fwd_f     = _safe_float(r.get("forward_track"))
        minvt_f   = _safe_float(r.get("min_valid_track"))
        damage_f  = _safe_float(r.get("damage"))

        # forward_track validity is the primary classification gate
        fwd_valid = (fwd_f is not None
                     and _validate_sensor(fwd_f, "forward_track"))

        # A row is "valid" for statistical purposes if the core driving
        # sensors are in range — forward_track invalidity alone doesn't
        # invalidate everything else.
        sensor_ok = (
            (speed_f  is None or _validate_sensor(speed_f,  "speedX"))
            and (tpos_f  is None or _validate_sensor(tpos_f,  "trackPos"))
            and (angle_f is None or _validate_sensor(angle_f, "angle"))
            and (damage_f is None or _validate_sensor(damage_f, "damage"))
            and (minvt_f is None or _validate_sensor(minvt_f, "min_valid_track"))
        )

        row_valid = sensor_ok  # out-of-range sensor values invalidate the row

        if not row_valid:
            invalid_count += 1

        rc = dict(r)
        rc.update({
            "_step"      : int(step_f) if step_f is not None else None,
            "_dist"      : dist_f,
            "_speed"     : speed_f,
            "_track_pos" : tpos_f,
            "_angle_rad" : angle_f,
            "_fwd"       : fwd_f,
            "_min_vt"    : minvt_f,
            "_damage"    : damage_f,
            "_fwd_valid" : fwd_valid,
            "_row_valid" : row_valid,
        })
        cleaned.append(rc)

    return cleaned, invalid_count


# ---------------------------------------------------------------------------
# Zone classification
# ---------------------------------------------------------------------------

def _classify_row(row, corner_thresh, straight_thresh):
    """Return CORNER, STRAIGHT, TRANSITION, or UNKNOWN for one cleaned row."""
    if not row["_fwd_valid"]:
        return UNKNOWN
    fwd = row["_fwd"]
    if fwd < corner_thresh:
        return CORNER
    if fwd > straight_thresh:
        return STRAIGHT
    return TRANSITION


# ---------------------------------------------------------------------------
# Zone grouping
# ---------------------------------------------------------------------------

def _group_zones(cleaned_rows, corner_thresh, straight_thresh):
    """
    Walk cleaned_rows in step order.  Merge consecutive rows with the same
    classification into Zone namedtuples.  Flag gaps where consecutive step
    numbers differ by more than GAP_TOLERANCE_STEPS.

    Returns list of Zone objects for CORNER and STRAIGHT classifications only
    (TRANSITION and UNKNOWN zones are skipped in the output but tracked for
    gap detection purposes).

    Also returns all_zones (including TRANSITION / UNKNOWN) for wraparound
    analysis.
    """
    if not cleaned_rows:
        return [], []

    Zone = collections.namedtuple("Zone", [
        "classification",
        "rows",         # list of cleaned row dicts
        "gaps",         # list of (step_before_gap, step_after_gap) tuples
    ])

    zones       = []
    current_cls = None
    current_rows = []
    current_gaps = []

    prev_step = None

    def _flush():
        if current_rows:
            zones.append(Zone(current_cls, list(current_rows), list(current_gaps)))

    for row in cleaned_rows:
        cls  = _classify_row(row, corner_thresh, straight_thresh)
        step = row["_step"]

        # Detect step gap (regardless of classification change)
        gap_here = False
        if prev_step is not None and step is not None:
            diff = step - prev_step
            if diff > GAP_TOLERANCE_STEPS:
                gap_here = True

        if cls != current_cls:
            _flush()
            current_cls  = cls
            current_rows = [row]
            current_gaps = [(prev_step, step)] if gap_here else []
        else:
            if gap_here:
                current_gaps.append((prev_step, step))
            current_rows.append(row)

        prev_step = step

    _flush()

    # Return all zones and the filtered (CORNER / STRAIGHT only) subset
    highlighted = [z for z in zones if z.classification in (CORNER, STRAIGHT)]
    return highlighted, zones


# ---------------------------------------------------------------------------
# Wraparound detection and merge
# ---------------------------------------------------------------------------

def _detect_and_merge_wraparound(highlighted_zones, cleaned_rows):
    """
    If the first and last zones in *highlighted_zones* share the same
    classification and the distFromStart of the last zone's rows is
    significantly higher than the first zone's rows (indicating the car
    crossed the start/finish line mid-zone), merge them and tag with [WRAP].

    Returns the (possibly merged) zone list.
    """
    if len(highlighted_zones) < 2:
        return highlighted_zones

    first = highlighted_zones[0]
    last  = highlighted_zones[-1]

    if first.classification != last.classification:
        return highlighted_zones

    # Check for wraparound: last zone ends at high distFromStart,
    # first zone starts at low distFromStart.
    last_dist  = _zone_dist_end(last)
    first_dist = _zone_dist_start(first)

    if last_dist is None or first_dist is None:
        return highlighted_zones

    # Use half the apparent lap length as the wraparound threshold.
    all_dists = [r["_dist"] for r in cleaned_rows if r["_dist"] is not None]
    if not all_dists:
        return highlighted_zones
    apparent_lap = max(all_dists) - min(all_dists)
    if apparent_lap <= 0:
        return highlighted_zones

    if last_dist > apparent_lap * 0.5 and first_dist < apparent_lap * 0.5:
        # Merge: last zone rows come first chronologically (end of lap),
        # first zone rows come after (start of next lap sample / wrap)
        merged_rows = last.rows + first.rows
        merged_gaps = last.gaps + first.gaps

        Zone = collections.namedtuple("Zone", ["classification", "rows", "gaps"])
        merged = Zone(
            classification="CORNER_WRAP" if first.classification == CORNER else "STRAIGHT_WRAP",
            rows=merged_rows,
            gaps=merged_gaps,
        )
        # Replace first and last with the merged zone
        result = [merged] + highlighted_zones[1:-1]
        return result

    return highlighted_zones


def _zone_dist_start(zone):
    dists = [r["_dist"] for r in zone.rows if r["_dist"] is not None]
    return min(dists) if dists else None


def _zone_dist_end(zone):
    dists = [r["_dist"] for r in zone.rows if r["_dist"] is not None]
    return max(dists) if dists else None


# ---------------------------------------------------------------------------
# Zone statistics
# ---------------------------------------------------------------------------

def _zone_stats(zone):
    """
    Compute all reportable statistics for one zone.
    Returns a dict.
    """
    rows = zone.rows

    dists   = [r["_dist"]      for r in rows if r["_dist"]      is not None]
    speeds  = [r["_speed"]     for r in rows if r["_speed"]      is not None]
    tpos    = [r["_track_pos"] for r in rows if r["_track_pos"]  is not None]
    angles  = [r["_angle_rad"] for r in rows if r["_angle_rad"]  is not None]
    fwds    = [r["_fwd"]       for r in rows if r["_fwd_valid"]]
    minvts  = [r["_min_vt"]    for r in rows if r["_min_vt"]     is not None]
    damages = [r["_damage"]    for r in rows if r["_damage"]     is not None]

    dist_start  = min(dists)  if dists  else None
    dist_end    = max(dists)  if dists  else None
    zone_length = (dist_end - dist_start) if (dist_start is not None and dist_end is not None) else None

    min_speed   = min(speeds) if speeds else None
    max_speed   = max(speeds) if speeds else None
    min_fwd     = min(fwds)   if fwds   else None
    min_minvt   = min(minvts) if minvts else None
    angle_min   = min(angles) if angles else None
    angle_max   = max(angles) if angles else None
    tpos_min    = min(tpos)   if tpos   else None
    tpos_max    = max(tpos)   if tpos   else None

    damage_inc  = None
    if len(damages) >= 2:
        damage_inc = damages[-1] - damages[0]
        if damage_inc < 0:
            damage_inc = 0.0  # damage never decreases; negative = sensor noise

    sample_count = len(rows)

    return {
        "dist_start"  : dist_start,
        "dist_end"    : dist_end,
        "zone_length" : zone_length,
        "min_speed"   : min_speed,
        "max_speed"   : max_speed,
        "min_fwd"     : min_fwd,
        "min_minvt"   : min_minvt,
        "angle_min"   : angle_min,
        "angle_max"   : angle_max,
        "tpos_min"    : tpos_min,
        "tpos_max"    : tpos_max,
        "damage_inc"  : damage_inc,
        "sample_count": sample_count,
        "gap_count"   : len(zone.gaps),
        "gaps"        : zone.gaps,
    }


# ---------------------------------------------------------------------------
# Track-position interpretation
# ---------------------------------------------------------------------------

def _tpos_label(tpos_min, tpos_max):
    """Plain-language lateral position label."""
    if tpos_min is None or tpos_max is None:
        return "unknown"
    mid = (tpos_min + tpos_max) / 2.0
    crossed = (tpos_min < 0 and tpos_max > 0)
    if crossed:
        return "crossed centre"
    if mid > 0.4:
        return "right side"
    if mid < -0.4:
        return "left side"
    return "near centre"


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

SEP_HEAVY = "=" * 62
SEP_LIGHT = "-" * 62

def _fmt_optional(value, fmt="%.1f"):
    return (fmt % value) if value is not None else "n/a"


def _print_zone_block(label, zone, stats, idx):
    """Print one zone block (corner or straight)."""
    wrap_tag = " [WRAP]" if "WRAP" in zone.classification else ""
    print()
    print("  Zone %s%s" % (label, wrap_tag))
    print("    Distance from start : %s m → %s m  (%s m long)"
          % (_fmt_optional(stats["dist_start"]),
             _fmt_optional(stats["dist_end"]),
             _fmt_optional(stats["zone_length"])))
    gap_note = "no gaps"
    if stats["gap_count"] > 0:
        gap_note = "%d gap(s) > %d steps detected" % (stats["gap_count"], GAP_TOLERANCE_STEPS)
    print("    Samples             : %d  [%s]" % (stats["sample_count"], gap_note))
    print("    Speed               : %s – %s km/h"
          % (_fmt_optional(stats["min_speed"]), _fmt_optional(stats["max_speed"])))

    if stats["min_fwd"] is not None:
        print("    Min forward_track   : %.1f m" % stats["min_fwd"])
    else:
        print("    Min forward_track   : n/a")

    if stats["min_minvt"] is not None:
        print("    Min valid track     : %.1f m" % stats["min_minvt"])
    else:
        print("    Min valid track     : n/a")

    # Heading
    if stats["angle_min"] is not None and stats["angle_max"] is not None:
        print("    Heading (angle)     : %.3f rad (%s) → %.3f rad (%s)"
              % (stats["angle_min"], _deg(stats["angle_min"]),
                 stats["angle_max"], _deg(stats["angle_max"])))
    else:
        print("    Heading (angle)     : n/a")

    # Track position
    tpos_lbl = _tpos_label(stats["tpos_min"], stats["tpos_max"])
    if stats["tpos_min"] is not None and stats["tpos_max"] is not None:
        print("    Track position      : %.2f → %.2f  (%s)"
              % (stats["tpos_min"], stats["tpos_max"], tpos_lbl))
    else:
        print("    Track position      : n/a")

    # Damage
    if stats["damage_inc"] is None:
        print("    Damage increase     : n/a  (insufficient damage readings)")
    elif stats["damage_inc"] > 0:
        print("    Damage increase     : %.0f  ⚠  contact or kerb strike" % stats["damage_inc"])
    else:
        print("    Damage increase     : 0")


def _print_report(
    summary_row,
    run_id, episode_id, lap_id,
    cleaned_rows, invalid_count,
    corner_zones, straight_zones,
    corner_thresh, straight_thresh,
    track_id,
):
    """Render the full report to stdout."""

    # ---- header -----------------------------------------------------------
    print()
    print(SEP_HEAVY)
    print(" CORNER MAP REPORT — %s" % (track_id if track_id else "unknown track"))
    print(SEP_HEAVY)
    print(" Run     : %s" % run_id)
    print(" Episode : %s" % episode_id)

    # Summary metadata
    lap_status       = summary_row.get("status",           "n/a") if summary_row else "n/a (no summary row)"
    sim_lap_time     = summary_row.get("sim_lap_time_s",   "")    if summary_row else ""
    dmg_initial      = summary_row.get("damage_initial",   "")    if summary_row else ""
    dmg_final        = summary_row.get("damage_final",     "")    if summary_row else ""
    max_speed_sum    = summary_row.get("max_speed_kmh",    "")    if summary_row else ""
    completion_rsn   = summary_row.get("completion_reason","")    if summary_row else ""

    print(" Lap     : %s  (status: %s)" % (lap_id, lap_status))

    if lap_status in ("partial", "warmup"):
        print()
        print(" ⚠  WARNING: This lap was not completed. The zone map")
        print("    may be missing sections not driven before the session ended.")

    if lap_status == "warmup_completed":
        print()
        print(" ℹ  NOTE: This is the warm-up lap (lap 0). Sensor readings")
        print("    may not represent a representative flying lap.")

    lap_time_str = sim_lap_time if sim_lap_time else "n/a (lap not completed)"
    print(" Sim lap time  : %s s" % lap_time_str)

    dmg_i_str = dmg_initial if dmg_initial else "n/a"
    dmg_f_str = dmg_final   if dmg_final   else "n/a"
    dmg_note  = ""
    di_f = _safe_float(dmg_initial)
    df_f = _safe_float(dmg_final)
    if di_f is not None and df_f is not None:
        if df_f - di_f > 0:
            dmg_note = "  ⚠  %.0f damage units this lap" % (df_f - di_f)
        else:
            dmg_note = "  (no damage this lap)"
    print(" Damage        : %s → %s%s" % (dmg_i_str, dmg_f_str, dmg_note))

    max_spd_str = ("%.1f km/h" % float(max_speed_sum)) if _safe_float(max_speed_sum) else "n/a"
    print(" Max speed     : %s" % max_spd_str)

    if completion_rsn:
        print(" Ended because : %s" % completion_rsn)

    total_rows = len(cleaned_rows)
    print()
    print(" Source        : lap_data.csv  (%d step rows, %d invalid row(s) excluded)"
          % (total_rows, invalid_count))

    # ---- thresholds note --------------------------------------------------
    print()
    print(" Thresholds used:")
    print("   Corner candidate   : forward_track < %.0f m" % corner_thresh)
    print("   Straight candidate : forward_track > %.0f m" % straight_thresh)
    print("   [These are heuristic discovery values, not exact track geometry.")
    print("    Adjust with --corner-threshold and --straight-threshold.]")

    # ---- corner zones -----------------------------------------------------
    print()
    print(SEP_LIGHT)
    print(" CORNER ZONES  (forward_track < %.0f m)" % corner_thresh)
    print(SEP_LIGHT)

    if not corner_zones:
        print()
        print("  No corner zones found with this threshold.")
        print("  Try lowering --corner-threshold.")
    else:
        for idx, zone in enumerate(corner_zones, start=1):
            stats = _zone_stats(zone)
            _print_zone_block("C%d" % idx, zone, stats, idx)

    # ---- straight zones ---------------------------------------------------
    print()
    print(SEP_LIGHT)
    print(" STRAIGHT ZONES  (forward_track > %.0f m)" % straight_thresh)
    print(SEP_LIGHT)

    if not straight_zones:
        print()
        print("  No straight zones found with this threshold.")
        print("  Try raising --straight-threshold.")
    else:
        for idx, zone in enumerate(straight_zones, start=1):
            stats = _zone_stats(zone)
            _print_zone_block("S%d" % idx, zone, stats, idx)

    # ---- sensor notes -----------------------------------------------------
    print()
    print(SEP_LIGHT)
    print(" SENSOR NOTES")
    print(SEP_LIGHT)
    print()
    print("  • forward_track is the dead-ahead (0°) radar beam.")
    print("    It measures the distance to the track boundary ahead of the")
    print("    car's current nose direction. It is NOT lateral clearance.")
    print()
    print("  • A reading of 200 m means 'no boundary detected within range',")
    print("    not that a wall is exactly 200 m away.")
    print()
    print("  • A single short sample may be sensor noise. Zones with fewer")
    print("    than 5 samples should be treated with caution.")
    print()
    print("  • min_valid_track is the minimum reading across all 19 angled")
    print("    beams. It can indicate proximity to track edges or barriers")
    print("    that the forward beam alone would not detect.")
    print()
    print("  • The 40 m / 150 m thresholds are starting points.")
    print("    Use --corner-threshold and --straight-threshold to refine them")
    print("    once you have verified the circuit geometry.")
    print()
    print("  • Distance from start and zone lengths are derived from the")
    print("    distFromStart sensor and reflect where the car was, not the")
    print("    true geometric length of the corner.")
    print()
    print(SEP_HEAVY)
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="find_corners.py",
        description=(
            "Corner Map Report for TORCS telemetry.\n"
            "Reads lap_data.csv and lap_summary.csv produced by snakeoil3_v2.py.\n\n"
            "Specify --run, --episode, and --lap together to analyse one lap.\n"
            "Omit any argument to list the available IDs at that tier."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--run",     metavar="RUN_ID",     default=None,
                        help="Run UUID to analyse.")
    parser.add_argument("--episode", metavar="EPISODE_ID", default=None,
                        help="Episode UUID within the chosen run.")
    parser.add_argument("--lap",     metavar="LAP_ID",     default=None,
                        help="Lap number within the chosen episode.")
    parser.add_argument("--data",    metavar="PATH",
                        default=os.path.join(_script_dir(), "lap_data.csv"),
                        help="Path to lap_data.csv  [default: same directory as this script]")
    parser.add_argument("--summary", metavar="PATH",
                        default=os.path.join(_script_dir(), "lap_summary.csv"),
                        help="Path to lap_summary.csv  [default: same directory as this script]")
    parser.add_argument("--corner-threshold",   metavar="METRES", type=float,
                        default=DEFAULT_CORNER_THRESHOLD,
                        help="forward_track below this = corner candidate  [default: 40]")
    parser.add_argument("--straight-threshold", metavar="METRES", type=float,
                        default=DEFAULT_STRAIGHT_THRESHOLD,
                        help="forward_track above this = straight candidate [default: 150]")

    args = parser.parse_args()

    corner_thresh   = args.corner_threshold
    straight_thresh = args.straight_threshold

    if corner_thresh >= straight_thresh:
        parser.error(
            "--corner-threshold (%.1f) must be less than --straight-threshold (%.1f)."
            % (corner_thresh, straight_thresh)
        )

    # ---- load both CSV files ----------------------------------------------
    summary_rows, err = _load_csv(args.summary, LAP_SUMMARY_COLS)
    if err:
        print("ERROR: %s" % err)
        sys.exit(1)

    data_rows, err = _load_csv(args.data, LAP_DATA_COLS)
    if err:
        print("ERROR: %s" % err)
        sys.exit(1)

    # ---- build ID tree ----------------------------------------------------
    id_tree = _collect_ids(summary_rows, data_rows)

    # ---- handle missing arguments: list IDs and exit ----------------------
    if args.run is None:
        _print_available_ids(id_tree)                           # exits

    if args.episode is None:
        _print_available_ids(id_tree, chosen_run=args.run)      # exits

    if args.lap is None:
        _print_available_ids(id_tree,
                             chosen_run=args.run,
                             chosen_ep=args.episode)            # exits

    # ---- validate selected IDs exist in the tree --------------------------
    # (the helper also validates and prints a useful message before exiting)
    if args.run not in id_tree:
        _print_available_ids(id_tree)                           # exits with error

    if args.episode not in id_tree.get(args.run, {}):
        _print_available_ids(id_tree, chosen_run=args.run)      # exits with error

    lap_id_str = args.lap
    if lap_id_str not in id_tree.get(args.run, {}).get(args.episode, set()):
        _print_available_ids(id_tree,
                             chosen_run=args.run,
                             chosen_ep=args.episode)            # exits with error

    # ---- look up summary row ----------------------------------------------
    summary_row = _find_summary_row(summary_rows, args.run, args.episode, lap_id_str)
    if summary_row is None:
        print(
            "\n⚠  No summary row found for this lap in lap_summary.csv.\n"
            "   The lap may have ended abnormally (e.g. SIGKILL) before the\n"
            "   final summary row could be written. Data rows will still be\n"
            "   analysed but lap status and time are unavailable.\n"
        )

    # ---- filter and validate data rows ------------------------------------
    lap_rows = _filter_lap_rows(data_rows, args.run, args.episode, lap_id_str)

    if not lap_rows:
        print(
            "\nERROR: No data rows found for run=%s episode=%s lap=%s.\n"
            "Check that the IDs are correct and that lap_data.csv is not empty."
            % (args.run, args.episode, lap_id_str)
        )
        sys.exit(1)

    cleaned_rows, invalid_count = _validate_rows(lap_rows)

    # ---- infer track name -------------------------------------------------
    track_ids = [r.get("track_id", "") for r in cleaned_rows if r.get("track_id", "")]
    track_id  = track_ids[0] if track_ids else ""

    # ---- classify and group zones -----------------------------------------
    highlighted_zones, all_zones = _group_zones(cleaned_rows, corner_thresh, straight_thresh)

    # Separate corner and straight zones
    corner_zones   = [z for z in highlighted_zones
                      if z.classification in (CORNER, "CORNER_WRAP")]
    straight_zones = [z for z in highlighted_zones
                      if z.classification in (STRAIGHT, "STRAIGHT_WRAP")]

    # Apply wraparound merge
    corner_zones   = _detect_and_merge_wraparound(corner_zones,   cleaned_rows)
    straight_zones = _detect_and_merge_wraparound(straight_zones, cleaned_rows)

    # ---- render report ----------------------------------------------------
    _print_report(
        summary_row      = summary_row,
        run_id           = args.run,
        episode_id       = args.episode,
        lap_id           = lap_id_str,
        cleaned_rows     = cleaned_rows,
        invalid_count    = invalid_count,
        corner_zones     = corner_zones,
        straight_zones   = straight_zones,
        corner_thresh    = corner_thresh,
        straight_thresh  = straight_thresh,
        track_id         = track_id,
    )


if __name__ == "__main__":
    main()
