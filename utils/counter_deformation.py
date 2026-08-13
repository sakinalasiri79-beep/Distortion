# ============================================================
# COUNTER-DEFORMATION ENGINE
# Reverse camber, extra length, preset and fit-up compensation
# computed per region, ready to mark on cutting/fit-up drawings.
# ============================================================

def nozzle_counter_deformation(bulge_mm, tilt_deg, has_rf_pad):
    return {
        "reverse_dish_mm": round(-bulge_mm * (0.9 if has_rf_pad else 1.0), 3),
        "preset_angle_deg": round(-tilt_deg, 3),
        "fit_up_note": (
            "Pre-dish the cutout edge inward by the reverse_dish value before welding, "
            "so post-weld bulge returns it to flush."
            if not has_rf_pad else
            "RF pad already reduces bulge — apply reduced reverse-dish; verify with pad fillet last."
        ),
    }


def seam_counter_deformation(delta_L, delta_t, alpha_deg):
    return {
        "extra_length_allowance_mm": round(delta_L + delta_t + 1.0, 2),
        "fit_up_gap_addition_mm": round(delta_t, 2),
        "reverse_preset_deg": round(-alpha_deg, 3),
        "camber_note": (
            f"Cut plate {round(delta_L + delta_t + 1.0, 2)}mm longer than nominal length. "
            f"Set root gap {round(delta_t, 2)}mm wider than drawing nominal. "
            f"Pre-angle the joint by {round(-alpha_deg, 3)}° (opposite to predicted peaking direction) before tacking."
        ),
    }


def build_compensation_table(ranked_regions):
    table = []
    for r in ranked_regions:
        cd = nozzle_counter_deformation(r["bulge_mm"], r["tilt_deg"], "W5" in r.get("joint", ""))
        table.append({
            "region": r["name"],
            "reverse_dish_mm": cd["reverse_dish_mm"],
            "preset_angle_deg": cd["preset_angle_deg"],
            "note": cd["fit_up_note"],
        })
    return table