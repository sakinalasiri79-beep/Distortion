# ============================================================
# DISTORTION PREDICTION ENGINE
# Case 1: SS multi-nozzle shell | Case 2: CS longitudinal seam
# ============================================================
import math

def weld_cross_section_area(root_gap_mm, groove_angle_deg, thickness_mm):
    """Simplified V-groove weld metal area (mm^2) incl. root + reinforcement."""
    reinforcement_factor = 1.1
    area = (root_gap_mm * thickness_mm) + \
           (thickness_mm**2 * math.tan(math.radians(groove_angle_deg / 2)))
    return round(area * reinforcement_factor, 2)


def transverse_shrinkage(weld_area_mm2, thickness_mm):
    """δt ≈ 0.2 * (Aw / t)  [Blodgett/Masubuchi empirical]"""
    return round(0.2 * (weld_area_mm2 / thickness_mm), 3)


def longitudinal_shrinkage(weld_area_mm2, plate_area_mm2, weld_length_mm, k1=0.05):
    """δL = k1 * (Aw/A) * L"""
    return round(k1 * (weld_area_mm2 / plate_area_mm2) * weld_length_mm, 3)


def angular_distortion(heat_input_kJmm, thickness_mm, num_passes):
    """Decreases with more, thinner passes (multi-pass balances pull)."""
    k = 1.8
    alpha_deg = k * (heat_input_kJmm / (thickness_mm**2)) / num_passes
    return round(alpha_deg, 3)


def recommend_compensation(delta_L, delta_t, alpha_deg):
    return {
        "extra_length_allowance_mm": round(delta_L + delta_t + 1.0, 2),
        "fit_up_gap_addition_mm": round(delta_t, 2),
        "reverse_preset_deg": round(-alpha_deg, 3),
    }


def rank_critical_regions(regions):
    """regions: list of dicts with 'bulge_mm', 'tilt_deg', 'interacting'."""
    def score(r):
        s = r.get("bulge_mm", 0) * 10 + r.get("tilt_deg", 0) * 5
        if r.get("interacting"):
            s *= 1.5
        return s

    ranked = sorted(regions, key=score, reverse=True)
    for i, r in enumerate(ranked, 1):
        r["priority"] = i
    return ranked


DISTORTION_TYPE_MAP = {
    "W1": "Peaking at circumferential seam (D'end to Shell)",
    "W2": "Peaking at longitudinal/circumferential seam",
    "W3": "Flange face angular distortion",
    "W4": "Bulging near nozzle weld + shell ovality contribution (unreinforced — highest risk)",
    "W5": "Bulging near nozzle weld (reduced by RF pad) + shell ovality contribution",
    "W7": "Flange face angular distortion",
    "LONG_SEAM": "Peaking at longitudinal seam + shell ovality",
    "CIRC_SEAM": "Shell ovality / circumferential shrinkage",
}


def classify_distortion(joint_code, interacting=False):
    base = DISTORTION_TYPE_MAP.get(joint_code, "General shell distortion")
    if interacting:
        base += " — COMPOUNDED by adjacent nozzle HAZ overlap"
    return base


def mitigation_for_close_nozzles(pair_check):
    return {
        "problem": (
            f"{pair_check['pair']} are {pair_check['edge_distance_mm']}mm apart "
            f"(minimum safe spacing is {pair_check['min_required_mm']}mm). Their heat-affected "
            "zones overlap, so distortion from one nozzle adds directly onto the other instead "
            "of dissipating independently — this is exactly the 'bulging near nozzle welds' and "
            "'shell ovality' failure mode called out in the problem statement."
        ),
        "actions": [
            "Weld INTERLEAVED: alternate one pass on nozzle A, then the matching pass on nozzle B — never finish one completely before starting the other.",
            "Reduce heat input on both (GTAW root + stringer, no weave) to shrink each HAZ so they stop overlapping thermally.",
            "Clamp a temporary strongback bridging both nozzles before welding to restrain combined pull.",
            "Sequence opposite/symmetric points on each nozzle (e.g. 12 o'clock then 6 o'clock) rather than working around in one direction.",
            "Re-check ovality between the two nozzles before moving to the next stage — catch compounding early, before it propagates to the rest of the shell.",
        ]
    }


def shell_ovality_estimate(all_bulges_mm):
    """Simple aggregate proxy: sum of local bulge contributions around the shell."""
    return round(sum(all_bulges_mm), 3)