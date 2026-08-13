import math
from utils.geometry import cylindrical_edge_distance

ELECTRODE_TABLE = {
    "root": {"dia_mm": 2.4, "arc_length_mm": 2.4, "current_A": (60, 90), "voltage_V": (18, 22)},
    "fill": {"dia_mm": 3.15, "arc_length_mm": 3.15, "current_A": (100, 140), "voltage_V": (20, 24)},
    "cap":  {"dia_mm": 4.0, "arc_length_mm": 4.0, "current_A": (140, 180), "voltage_V": (22, 26)},
}
GTAW_ROOT = {"dia_mm": 1.6, "arc_length_mm": 2.0, "current_A": (70, 110), "voltage_V": (10, 14)}


def get_electrode_params(pass_type="root", process="SMAW"):
    if process == "GTAW" and pass_type == "root":
        return GTAW_ROOT
    return ELECTRODE_TABLE.get(pass_type, ELECTRODE_TABLE["fill"])


def heat_input(voltage_V, current_A, travel_speed_mm_min, efficiency=0.85):
    Q = (60 * voltage_V * current_A * efficiency) / (1000 * travel_speed_mm_min)
    return round(Q, 3)


def nozzle_weld_type(shell_thk_mm, has_rf_pad):
    if has_rf_pad:
        return {"joint": "W5", "groove_angle_deg": 30, "tolerance_deg": 2.5,
                "note": "Shell/nozzle with RF pad - reinforced, lower local bulge risk"}
    return {"joint": "W4", "groove_angle_deg": 30, "tolerance_deg": 2.5,
            "note": "Shell/nozzle without pad - unreinforced, HIGHEST local bulge risk"}


def check_nozzle_spacing(nozzle_a, nozzle_b, radius_mm, shell_thk_mm):
    """Uses real cylindrical geometry: orientation angle + axial distance."""
    edge_distance, center_distance = cylindrical_edge_distance(
        radius_mm,
        nozzle_a["orientation_deg"], nozzle_a["axial_mm"], nozzle_a["od_mm"],
        nozzle_b["orientation_deg"], nozzle_b["axial_mm"], nozzle_b["od_mm"],
    )
    larger_od = max(nozzle_a["od_mm"], nozzle_b["od_mm"])
    min_required = max(2 * larger_od, 8 * shell_thk_mm)
    interacting = edge_distance < min_required
    return {
        "pair": f"{nozzle_a['name']} - {nozzle_b['name']}",
        "center_distance_mm": center_distance,
        "edge_distance_mm": edge_distance,
        "min_required_mm": round(min_required, 1),
        "interacting": interacting,
        "action": "COMBINE as coupled distortion zone" if interacting else "Independent - OK",
    }


def nearest_neighbor(nozzle, all_nozzles, radius_mm, shell_thk_mm):
    """Finds the closest other nozzle and the actual distance to it."""
    best = None
    for other in all_nozzles:
        if other["name"] == nozzle["name"]:
            continue
        pc = check_nozzle_spacing(nozzle, other, radius_mm, shell_thk_mm)
        if best is None or pc["edge_distance_mm"] < best["edge_distance_mm"]:
            best = pc
    return best


def nozzle_local_bulge(heat_input_kJmm, hole_dia_mm, shell_thk_mm, has_rf_pad):
    stiffness_factor = 2.2 if has_rf_pad else 1.0
    k = 0.015
    bulge_mm = k * (heat_input_kJmm * hole_dia_mm) / (shell_thk_mm**2 * stiffness_factor)
    return round(bulge_mm, 3)


def flange_angular_tilt(heat_input_kJmm, nozzle_length_mm, nozzle_thk_mm):
    k = 0.008
    tilt_deg = k * heat_input_kJmm * (nozzle_length_mm / nozzle_thk_mm) / 100
    return round(tilt_deg, 3)