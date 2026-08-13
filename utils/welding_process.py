# ============================================================
# WELDING PROCESS ENGINE
# Maps each joint type (W1-W7 from your sketch) + material to
# actual process, electrode, arc length, heat input and technique.
# ============================================================

WELD_PROCESS_MAP = {
    # ---------------- CASE 1: SS 316L ----------------
    "W1": {
        "material": "SA-240 316L",
        "passes": [
            {"pass": "Root", "process": "GTAW", "filler": "ER316L", "dia_mm": 1.6,
             "arc_length_mm": 2.0, "current_A": (90, 110), "voltage_V": (11, 13),
             "travel_speed_mm_min": (80, 120),
             "technique": "Stringer, no weave", "travel_angle_deg": 10, "work_angle_deg": 90,
             "purge": "Mandatory Ar backing purge (O2 < 50 ppm) to prevent root oxidation/sensitization"},
            {"pass": "Fill", "process": "SMAW", "filler": "E316L-16", "dia_mm": 3.15,
             "arc_length_mm": 3.15, "current_A": (100, 130), "voltage_V": (21, 24),
             "travel_speed_mm_min": (100, 150),
             "technique": "Slight weave, max width = 2.5x electrode dia", "travel_angle_deg": 15, "work_angle_deg": 90},
            {"pass": "Cap", "process": "SMAW", "filler": "E316L-16", "dia_mm": 4.0,
             "arc_length_mm": 4.0, "current_A": (130, 160), "voltage_V": (23, 26),
             "travel_speed_mm_min": (100, 150),
             "technique": "Weave, max width = 3x electrode dia", "travel_angle_deg": 15, "work_angle_deg": 90},
        ],
        "interpass_temp_max_C": 150,
        "sequence_note": "Backstep sequence in 250-300mm segments to balance shrinkage along the seam."
    },
    "W2": {
        "material": "SA-240 316L",
        "passes": [
            {"pass": "Root", "process": "GTAW", "filler": "ER316L", "dia_mm": 1.6,
             "arc_length_mm": 2.0, "current_A": (90, 110), "voltage_V": (11, 13),
             "travel_speed_mm_min": (80, 120),
             "technique": "Stringer, no weave", "travel_angle_deg": 10, "work_angle_deg": 90,
             "purge": "Mandatory Ar backing purge"},
            {"pass": "Fill+Cap", "process": "SMAW", "filler": "E316L-16", "dia_mm": 3.15,
             "arc_length_mm": 3.15, "current_A": (100, 130), "voltage_V": (21, 24),
             "travel_speed_mm_min": (100, 150),
             "technique": "Slight weave", "travel_angle_deg": 15, "work_angle_deg": 90},
        ],
        "interpass_temp_max_C": 150,
        "sequence_note": "Balanced/symmetric sequence from mid-length outward toward both ends."
    },
    "W3": {
        "material": "SA-182 F316L",
        "passes": [
            {"pass": "Root", "process": "GTAW", "filler": "ER316L", "dia_mm": 1.6,
             "arc_length_mm": 2.0, "current_A": (80, 100), "voltage_V": (10, 12),
             "travel_speed_mm_min": (80, 120),
             "technique": "Stringer, no weave", "travel_angle_deg": 10, "work_angle_deg": 90,
             "purge": "Mandatory Ar backing purge"},
            {"pass": "Fill", "process": "SMAW", "filler": "E316L-16", "dia_mm": 3.15,
             "arc_length_mm": 3.15, "current_A": (95, 120), "voltage_V": (20, 23),
             "travel_speed_mm_min": (100, 150),
             "technique": "Slight weave", "travel_angle_deg": 15, "work_angle_deg": 90},
        ],
        "interpass_temp_max_C": 150,
        "sequence_note": "Weld in 3 or 4 symmetric arc segments (not one continuous 360° pass) to prevent flange-face angular tilt."
    },
    "W4": {
        "material": "SA-312 TP316L",
        "passes": [
            {"pass": "Root", "process": "GTAW", "filler": "ER316L", "dia_mm": 1.6,
             "arc_length_mm": 1.8, "current_A": (75, 95), "voltage_V": (10, 12),
             "travel_speed_mm_min": (80, 120),
             "technique": "Stringer, no weave", "travel_angle_deg": 10, "work_angle_deg": 90,
             "purge": "Mandatory Ar backing purge"},
            {"pass": "Fill", "process": "SMAW", "filler": "E316L-16", "dia_mm": 2.5,
             "arc_length_mm": 2.5, "current_A": (70, 90), "voltage_V": (19, 22),
             "travel_speed_mm_min": (100, 150),
             "technique": "Stringer preferred over weave - lower heat input on unreinforced hole", "travel_angle_deg": 15, "work_angle_deg": 90},
        ],
        "interpass_temp_max_C": 120,
        "sequence_note": "Weld in 4 symmetric quadrant segments (0°→90°→180°→270°), skip-step, not continuous - this joint has no pad to resist bulging."
    },
    "W5": {
        "material": "SA-312 TP316L",
        "passes": [
            {"pass": "Root", "process": "GTAW", "filler": "ER316L", "dia_mm": 1.6,
             "arc_length_mm": 2.0, "current_A": (80, 100), "voltage_V": (10, 12),
             "travel_speed_mm_min": (80, 120),
             "technique": "Stringer, no weave", "travel_angle_deg": 10, "work_angle_deg": 90,
             "purge": "Mandatory Ar backing purge"},
            {"pass": "Fill", "process": "SMAW", "filler": "E316L-16", "dia_mm": 3.15,
             "arc_length_mm": 3.15, "current_A": (95, 120), "voltage_V": (20, 23),
             "travel_speed_mm_min": (100, 150),
             "technique": "Slight weave", "travel_angle_deg": 15, "work_angle_deg": 90},
            {"pass": "Pad fillet", "process": "SMAW", "filler": "E316L-16", "dia_mm": 3.15,
             "arc_length_mm": 3.15, "current_A": (90, 115), "voltage_V": (20, 22),
             "travel_speed_mm_min": (90, 130),
             "technique": "Stringer, single pass fillet around pad OD", "travel_angle_deg": 45, "work_angle_deg": 45},
        ],
        "interpass_temp_max_C": 150,
        "sequence_note": "Weld nozzle-to-shell groove first, let cool, then pad fillet - pad acts as the final distortion-locking pass."
    },
    "W7": {
        "material": "SA-312 TP316L",
        "passes": [
            {"pass": "Root", "process": "GTAW", "filler": "ER316L", "dia_mm": 1.6,
             "arc_length_mm": 1.8, "current_A": (75, 95), "voltage_V": (10, 12),
             "travel_speed_mm_min": (80, 120),
             "technique": "Stringer, no weave", "travel_angle_deg": 10, "work_angle_deg": 90,
             "purge": "Mandatory Ar backing purge"},
            {"pass": "Fill", "process": "SMAW", "filler": "E316L-16", "dia_mm": 3.15,
             "arc_length_mm": 3.15, "current_A": (95, 120), "voltage_V": (20, 23),
             "travel_speed_mm_min": (100, 150),
             "technique": "Slight weave", "travel_angle_deg": 15, "work_angle_deg": 90},
        ],
        "interpass_temp_max_C": 150,
        "sequence_note": "Weld in symmetric segments around the flange."
    },

    # ---------------- CASE 2: CS SA-516 Gr.70 ----------------
    "LONG_SEAM": {
        "material": "SA-516 Gr.70",
        "passes": [
            {"pass": "Root", "process": "GTAW", "filler": "ER70S-2", "dia_mm": 2.0,
             "arc_length_mm": 2.5, "current_A": (100, 130), "voltage_V": (12, 15),
             "travel_speed_mm_min": (80, 120),
             "technique": "Stringer, no weave", "travel_angle_deg": 10, "work_angle_deg": 90},
            {"pass": "Fill+Cap", "process": "SAW", "filler": "EM12K / F7A2-EM12K flux", "dia_mm": 4.0,
             "arc_length_mm": None, "current_A": (350, 450), "voltage_V": (28, 32),
             "travel_speed_mm_min": (400, 500),
             "technique": "Automatic, single stringer pass per layer, constant travel speed",
             "travel_angle_deg": 0, "work_angle_deg": 90},
        ],
        "interpass_temp_max_C": 250,
        "sequence_note": "Backstep in 300mm segments for root; SAW fill/cap run continuously once root is qualified and restrained."
    },
    "CIRC_SEAM": {
        "material": "SA-516 Gr.70",
        "passes": [
            {"pass": "Root", "process": "SMAW", "filler": "E7018", "dia_mm": 3.15,
             "arc_length_mm": 3.15, "current_A": (110, 140), "voltage_V": (22, 25),
             "travel_speed_mm_min": (100, 150),
             "technique": "Stringer, no weave", "travel_angle_deg": 10, "work_angle_deg": 90},
            {"pass": "Fill+Cap", "process": "SMAW", "filler": "E7018", "dia_mm": 4.0,
             "arc_length_mm": 4.0, "current_A": (150, 180), "voltage_V": (24, 27),
             "travel_speed_mm_min": (100, 150),
             "technique": "Weave, max width 3x electrode dia", "travel_angle_deg": 15, "work_angle_deg": 90},
        ],
        "interpass_temp_max_C": 250,
        "sequence_note": "Symmetric backstep from a fixed start point, working both directions equally."
    },
}


def get_weld_plan(joint_code):
    """Returns the full pass-by-pass welding plan for a joint code."""
    return WELD_PROCESS_MAP.get(joint_code, WELD_PROCESS_MAP["W4"])


def compute_pass_heat_input(pass_data):
    """Q = 60*V*I / (1000*S), using midpoint V/I/S. Returns (Q kJ/mm, S mm/min)."""
    eff = 0.95 if pass_data["process"] == "SAW" else 0.85
    V = sum(pass_data["voltage_V"]) / 2
    I = sum(pass_data["current_A"]) / 2
    S = sum(pass_data["travel_speed_mm_min"]) / 2
    Q = (60 * V * I * eff) / (1000 * S)
    return round(Q, 3), S