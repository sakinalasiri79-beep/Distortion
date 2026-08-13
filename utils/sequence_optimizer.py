# ============================================================
# SEQUENCE OPTIMIZATION ENGINE
# Produces build order, weld direction, balance-building pattern,
# heat distribution strategy and restraint strategy.
# ============================================================

def optimize_sequence(ranked_regions, pair_checks, vessel_type="Case 1"):
    plan = []

    for r in ranked_regions:
        name = r["name"]
        is_pair = any(name in pc["pair"] for pc in pair_checks if pc["interacting"])

        if is_pair:
            direction = "Interleaved — alternate direction each pass (A→B→A→B)"
            balance = "Weld symmetric points on both nozzles before moving to next pass — do not complete either fully first"
            heat_dist = "Split total heat input across both nozzles per cycle; allow interpass cooling between each alternation"
            restraint = "Bridge strongback clamped across both nozzles before first arc strike"
        elif r.get("tilt_deg", 0) > 0.15:
            direction = "Radial, start at 12 o'clock, alternate 12→6→3→9 (cross pattern)"
            balance = "Cross-pattern balances pull on both axes simultaneously, preventing one-sided tilt"
            heat_dist = "4 segments minimum, skip-step (not continuous 360°), full interpass cool between segments"
            restraint = "Local clamp ring or tack-and-strongback around nozzle before welding"
        else:
            direction = "Continuous, single direction, start from datum mark"
            balance = "Low-risk joint — standard sequence sufficient"
            heat_dist = "Single pass sequence acceptable within interpass limit"
            restraint = "Standard tack welds at 4 points (90° apart) before final weld"

        plan.append({
            "region": name,
            "build_order": r.get("priority", "-"),
            "weld_direction": direction,
            "balance_building": balance,
            "heat_distribution": heat_dist,
            "restraint_strategy": restraint,
        })

    return plan


def optimize_seam_sequence(seam_length_mm, num_passes):
    segment_mm = 300
    num_segments = max(1, round(seam_length_mm / segment_mm))
    return {
        "build_order": "Root pass first (full length, backstep), then fill/cap layer by layer",
        "weld_direction": f"Backstep sequence: {num_segments} segments of ~{segment_mm}mm, welding each segment backward into the previous one's start point",
        "balance_building": "Start at seam midpoint, work outward in both directions alternately to cancel net longitudinal pull",
        "heat_distribution": f"{num_passes} passes total — thinner/more passes spread heat input over time, reducing peaking vs one heavy pass",
        "restraint_strategy": "Strongbacks at both ends + mid-length before root pass; remove only after fill+cap complete and cooled to interpass limit",
    }