# ==========================================================
# WPS CALCULATOR
# Engineering Rule-Based Welding Recommendation
# ==========================================================

from utils.recommendation_engine import get_material, get_electrode


# ==========================================================
# SMART FALLBACK FOR MATERIALS NOT IN THE DATABASE
# Guesses a reasonable process family from the material name
# instead of defaulting everything to SMAW/E7018 (which would
# be wrong — e.g. carbon-steel electrodes on titanium/aluminum).
# This is a conservative starting point only, always flagged
# as unverified.
# ==========================================================

def guess_material_family(name):

    n = (name or "").lower()

    if "titanium" in n or n.strip().startswith("ti-") or " ti " in n:
        return {
            "Process": "GTAW",
            "Electrode": "ERTi filler (inert gas purge required)",
            "CTE": 8.6e-6,
            "Note": "Reactive metal — requires argon shielding front & back of weld"
        }

    if "aluminum" in n or "aluminium" in n:
        return {
            "Process": "GMAW",
            "Electrode": "ER4043 / ER5356 (verify grade match)",
            "CTE": 23.8e-6,
            "Note": "Aluminum alloys weld with AC/pulsed GMAW or GTAW, not SMAW"
        }

    if "duplex" in n:
        return {
            "Process": "GTAW",
            "Electrode": "ER2209 (verify grade match)",
            "CTE": 13.0e-6,
            "Note": "Duplex stainless — control heat input to preserve phase balance"
        }

    if "stainless" in n or " ss" in n or n.startswith("ss"):
        return {
            "Process": "GTAW",
            "Electrode": "ER308L / ER316L (verify grade match)",
            "CTE": 16.5e-6,
            "Note": "Austenitic stainless — low-carbon filler to avoid carbide precipitation"
        }

    # default: carbon/low-alloy steel family
    return {
        "Process": "SMAW",
        "Electrode": "E7018 (verify grade match)",
        "CTE": 12.0e-6,
        "Note": "Assumed carbon/low-alloy steel — confirm before use"
    }


def calculate_wps(material, thickness):

    # -----------------------------
    # PROCESS + ELECTRODE
    # (looked up from materials.csv / electrodes.csv,
    #  falling back to a family-aware guess — not a
    #  blanket carbon-steel default — if not found)
    # -----------------------------

    material_row = get_material(material)
    electrode_row = get_electrode(material)

    fallback = guess_material_family(material)

    process = (
        material_row["Typical_Process"]
        if material_row else fallback["Process"]
    )

    electrode = (
        electrode_row["Electrode"]
        if electrode_row else fallback["Electrode"]
    )

    # -----------------------------
    # CURRENT (A)
    # -----------------------------

    if thickness <= 6:

        current = 110

    elif thickness <= 10:

        current = 125

    elif thickness <= 20:

        current = 145

    elif thickness <= 40:

        current = 170

    else:

        current = 190

    # -----------------------------
    # VOLTAGE (V)
    # -----------------------------

    if thickness <= 10:

        voltage = 24

    elif thickness <= 20:

        voltage = 25

    elif thickness <= 40:

        voltage = 27

    else:

        voltage = 29

    # -----------------------------
    # TRAVEL SPEED
    # -----------------------------

    if thickness <= 10:

        speed = 220

    elif thickness <= 20:

        speed = 180

    elif thickness <= 40:

        speed = 150

    else:

        speed = 130

    # -----------------------------
    # GROOVE
    # -----------------------------

    if thickness <= 10:

        groove = "45°"

        root_gap = "2 mm"

        passes = 2

    elif thickness <= 20:

        groove = "60°"

        root_gap = "3 mm"

        passes = 3

    elif thickness <= 40:

        groove = "60°"

        root_gap = "4 mm"

        passes = 5

    else:

        groove = "70°"

        root_gap = "5 mm"

        passes = 7

    return {

        "Process": process,

        "Electrode": electrode,

        "Current": current,

        "Voltage": voltage,

        "Travel_Speed": speed,

        "Groove_Angle": groove,

        "Root_Gap": root_gap,

        "Passes": passes

    }