def build_fabrication_sequence(ranked_nozzles, pair_checks):
    sequence = []
    step = 1

    def add(stage, item, reason):
        nonlocal step
        sequence.append({"step": step, "stage": stage, "item": item, "reason": reason})
        step += 1

    add("Stage 1 — Longitudinal Seams", "L.S.-1 / L.S.-2 (shell long seams)",
        "Weld while the plate is still flat/rolled, before any circumferential or nozzle weld.")

    add("Stage 2 — Circumferential Seams", "C.S.-1 / C.S.-2, W1 (D'end to Shell)",
        "Join courses/heads while the shell is still unpierced.")

    add("Stage 3 — Dimensional Check", "Verify ovality & straightness before piercing",
        "Correct any seam-induced distortion now.")

    manhole = next((n for n in ranked_nozzles if "MH" in n["name"]), None)
    if manhole:
        add("Stage 4 — Largest Cutout", manhole["name"],
            "Weld while the shell has maximum flexibility; use symmetric multi-pass sequence.")

    pairs_added = set()
    for pc in pair_checks:
        if pc["interacting"]:
            names = pc["pair"].split(" - ")
            pairs_added.update(names)
            add("Stage 5 — Coupled Nozzle Pairs", pc["pair"],
                f"Spacing ({pc['edge_distance_mm']}mm) under required {pc['min_required_mm']}mm — weld INTERLEAVED.")

    solo = [n for n in ranked_nozzles if n["name"] not in pairs_added and (not manhole or n["name"] != manhole["name"])]
    solo_sorted = sorted(solo, key=lambda n: n.get("priority", 99))
    for n in solo_sorted:
        add("Stage 6 — Remaining Nozzles (high → low risk)", n["name"],
            f"Predicted bulge {n['bulge_mm']}mm, tilt {n['tilt_deg']}°. Alternate opposite azimuths.")

    add("Stage 7 — Structural Attachments", "Saddles, lifting lugs, earthing lugs, stiffeners, nameplate",
        "Weld last so they don't add restraint during pressure-boundary welding.")

    add("Stage 8 — Final Inspection", "NDE (RT/UT/PT), dimensional check, hydrotest",
        "Confirm distortion is within tolerance before hydrotest.")

    return sequence