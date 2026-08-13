"""
==========================================================
PV WeldWise
Engineering Compensation Engine
==========================================================

Provides engineering recommendations BEFORE welding to
minimize distortion.

These recommendations are based on fabrication practices
used in pressure vessel manufacturing.
==========================================================
"""


# ---------------------------------------------------------
# REVERSE CAMBER
# ---------------------------------------------------------

def reverse_camber(shell_ovality):

    if shell_ovality < 1:
        return "Not Required"

    elif shell_ovality < 2:
        return "0.5°"

    elif shell_ovality < 4:
        return "1.0°"

    else:
        return "1.5°"


# ---------------------------------------------------------
# EXTRA CUTTING LENGTH
# ---------------------------------------------------------

def extra_shell_length(shrinkage):

    return round(shrinkage, 1)


# ---------------------------------------------------------
# CLAMP SPACING
# ---------------------------------------------------------

def clamp_spacing(thickness):

    if thickness <= 10:
        return "300 mm"

    elif thickness <= 20:
        return "450 mm"

    else:
        return "600 mm"


# ---------------------------------------------------------
# WELDING SEQUENCE
# ---------------------------------------------------------

def welding_sequence(heat_input):

    if heat_input <= 1.20:

        return (
            "Back-Step Welding + Skip Welding"
        )

    elif heat_input <= 1.80:

        return (
            "Balanced Welding Sequence"
        )

    else:

        return (
            "Back-Step + Skip + Symmetrical Welding"
        )


# ---------------------------------------------------------
# STRONGBACK REQUIREMENT
# ---------------------------------------------------------

def strongback_required(shell_ovality):

    if shell_ovality >= 2:

        return "Recommended"

    return "Not Necessary"


# ---------------------------------------------------------
# MAXIMUM HEAT INPUT
# ---------------------------------------------------------

def allowable_heat_input(thickness):

    if thickness <= 10:

        return "≤ 1.0 kJ/mm"

    elif thickness <= 20:

        return "≤ 1.2 kJ/mm"

    else:

        return "≤ 1.5 kJ/mm"


# ---------------------------------------------------------
# MASTER FUNCTION
# ---------------------------------------------------------

def get_compensation(
    shell_ovality,
    shrinkage,
    thickness,
    heat_input
):

    return {

        "Reverse Camber":
            reverse_camber(shell_ovality),

        "Extra Shell Length":
            f"{extra_shell_length(shrinkage)} mm",

        "Clamp Spacing":
            clamp_spacing(thickness),

        "Recommended Welding Sequence":
            welding_sequence(heat_input),

        "Strongbacks":
            strongback_required(shell_ovality),

        "Maximum Heat Input":
            allowable_heat_input(thickness)

    }