import math

def cylindrical_edge_distance(radius_mm, angle_a_deg, axial_a_mm, od_a_mm,
                               angle_b_deg, axial_b_mm, od_b_mm):
    """
    Real nozzle-to-nozzle spacing on a cylindrical shell using actual
    shell radius + orientation angle (clock position, 0-360°) + axial
    distance from a fixed datum (e.g. tangent line) - not flat x/y guesses.
    """
    delta_theta = math.radians(abs(angle_a_deg - angle_b_deg))
    if delta_theta > math.pi:
        delta_theta = 2 * math.pi - delta_theta
    arc_distance = radius_mm * delta_theta           # distance around the shell
    axial_distance = abs(axial_a_mm - axial_b_mm)     # distance along the shell length
    center_distance = math.hypot(arc_distance, axial_distance)
    edge_distance = center_distance - (od_a_mm / 2 + od_b_mm / 2)
    return round(edge_distance, 1), round(center_distance, 1)


def default_vessel_geometry(case):
    if case == "Case 1":
        return {
            "shell_id_mm": 1400.0,
            "shell_thk_mm": 5.0,
            "overall_length_mm": 2199.0,
            "head_type": "Ellipsoidal 2:1",
        }
    else:
        return {
            "shell_id_mm": 1400.0,
            "shell_thk_mm": 8.0,
            "overall_length_mm": 2199.0,
            "head_type": "Ellipsoidal 2:1",
        }


def default_nozzle_table():
    """
    Sizes/schedule pulled from your actual BOM/nozzle table (accurate).
    orientation_deg and axial_mm are PLACEHOLDERS marked for you to
    correct by reading the clock position + distance-from-tangent-line
    off your GA drawing - takes ~1 min, and this is the number that
    actually drives spacing accuracy.
    """
    return [
        {"name": "N-01",  "od_mm": 114.3, "thk_mm": 8.56, "has_pad": True,  "length_mm": 480,  "orientation_deg": 0,   "axial_mm": 905},
        {"name": "N-02",  "od_mm": 60.3,  "thk_mm": 5.54, "has_pad": False, "length_mm": 1486, "orientation_deg": 90,  "axial_mm": 1050},
        {"name": "N-02A", "od_mm": 88.9,  "thk_mm": 7.62, "has_pad": True,  "length_mm": 179,  "orientation_deg": 96,  "axial_mm": 905},
        {"name": "N-03",  "od_mm": 60.3,  "thk_mm": 5.54, "has_pad": False, "length_mm": 449,  "orientation_deg": 180, "axial_mm": 930},
        {"name": "N-04",  "od_mm": 88.9,  "thk_mm": 7.62, "has_pad": False, "length_mm": 1480, "orientation_deg": 270, "axial_mm": 1050},
        {"name": "N-04A", "od_mm": 273.0, "thk_mm": 9.27, "has_pad": True,  "length_mm": 189,  "orientation_deg": 276, "axial_mm": 905},
        {"name": "N-05",  "od_mm": 88.9,  "thk_mm": 7.62, "has_pad": True,  "length_mm": 257,  "orientation_deg": 315, "axial_mm": 550},
        {"name": "N-06",  "od_mm": 60.3,  "thk_mm": 5.54, "has_pad": False, "length_mm": 449,  "orientation_deg": 45,  "axial_mm": 320},
        {"name": "MH-01", "od_mm": 610.0, "thk_mm": 8.0,  "has_pad": False, "length_mm": 172,  "orientation_deg": 132, "axial_mm": 855},
    ]