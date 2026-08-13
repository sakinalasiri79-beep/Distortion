# ============================================================
# DISTORTION VECTOR ENGINE
# Combines longitudinal, transverse and angular distortion into
# a single resultant vector per joint/nozzle, and an aggregate
# vessel-level resultant.
# ============================================================
import math


def nozzle_distortion_vector(bulge_mm, tilt_deg, orientation_deg):
    """
    Nozzle bulge acts radially outward (tangential-plane component),
    tilt acts as an angular rotation about the nozzle axis.
    Resolve bulge into local axial/circumferential components using
    the nozzle's clock position, so vectors from different nozzles
    can be summed meaningfully around the shell.
    """
    theta = math.radians(orientation_deg)
    axial_component = bulge_mm * math.sin(theta)
    circumferential_component = bulge_mm * math.cos(theta)
    magnitude = math.hypot(axial_component, circumferential_component)
    return {
        "axial_mm": round(axial_component, 4),
        "circumferential_mm": round(circumferential_component, 4),
        "angular_deg": tilt_deg,
        "magnitude_mm": round(magnitude, 4),
    }


def seam_distortion_vector(delta_L, delta_t, alpha_deg):
    """
    Longitudinal seam: delta_L acts along shell axis, delta_t acts
    circumferentially (closing the seam), alpha is peaking rotation.
    """
    magnitude = math.hypot(delta_L, delta_t)
    return {
        "axial_mm": round(delta_L, 4),
        "circumferential_mm": round(delta_t, 4),
        "angular_deg": round(alpha_deg, 4),
        "magnitude_mm": round(magnitude, 4),
    }


def resultant_vessel_vector(vectors):
    """
    Sums all individual distortion vectors (nozzles + seams) to get
    the net predicted shape error of the whole vessel. Angular terms
    are summed separately since they're rotational, not linear.
    """
    axial_sum = sum(v["axial_mm"] for v in vectors)
    circ_sum = sum(v["circumferential_mm"] for v in vectors)
    angular_sum = sum(v["angular_deg"] for v in vectors)
    magnitude = math.hypot(axial_sum, circ_sum)
    return {
        "net_axial_mm": round(axial_sum, 3),
        "net_circumferential_mm": round(circ_sum, 3),
        "net_angular_deg": round(angular_sum, 3),
        "net_magnitude_mm": round(magnitude, 3),
    }


def classify_severity(magnitude_mm, tolerance_mm=3.0):
    if magnitude_mm <= tolerance_mm * 0.5:
        return "Low", "#4CAF50"
    elif magnitude_mm <= tolerance_mm:
        return "Moderate", "#FF9800"
    else:
        return "High — exceeds tolerance", "#F44336"