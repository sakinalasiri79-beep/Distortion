# ==========================================================
# PV WeldWise Offline Engineering AI
# ==========================================================

def explain_welding(
    material,
    thickness,
    joint,
    recommended_process,
    selected_process,
    current,
    voltage,
    electrode,
    groove,
    root_gap,
    passes
):

    explanation = []

    # ==========================================================
    # PROCESS VALIDATION
    # ==========================================================

    if selected_process == recommended_process:

        explanation.append("## ✅ Welding Process Validation")

        explanation.append(
            f"The selected welding process **{selected_process}** is recommended for this application."
        )

    else:

        explanation.append("## ❌ Welding Process Validation")

        explanation.append(
            f"You selected **{selected_process}**, but the recommended process is **{recommended_process}**."
        )

        explanation.append(
            "Using the selected process may reduce productivity, increase distortion, "
            "or produce inadequate penetration for the selected material and thickness."
        )

    # ==========================================================
    # MATERIAL
    # ==========================================================

    explanation.append("\n## 🧱 Material Analysis")

    if "SA516" in material:

        explanation.append(
            "SA516 Grade 70 is one of the most widely used pressure vessel steels because of "
            "its excellent weldability, toughness and mechanical strength."
        )

    elif "Carbon" in material:

        explanation.append(
            "Carbon steel offers good weldability and is commonly used for fabrication."
        )

    elif "SS304" in material:

        explanation.append(
            "SS304 provides excellent corrosion resistance and good weldability."
        )

    elif "SS316" in material:

        explanation.append(
            "SS316 contains molybdenum which improves corrosion resistance in aggressive environments."
        )

    # ==========================================================
    # THICKNESS
    # ==========================================================

    explanation.append("\n## 📏 Thickness Analysis")

    if thickness <= 10:

        explanation.append(
            "Thin plates require lower heat input to avoid burn-through and distortion."
        )

    elif thickness <= 20:

        explanation.append(
            "Medium thickness plates normally require multiple welding passes for complete penetration."
        )

    else:

        explanation.append(
            "Thicker sections require higher heat input and multiple passes to ensure full penetration."
        )

    # ==========================================================
    # JOINT
    # ==========================================================

    explanation.append("\n## 🔩 Joint Analysis")

    explanation.append(
        f"The selected joint is **{joint}**."
    )

    if "Butt" in joint:

        explanation.append(
            "Butt joints are preferred for pressure-retaining welds because they provide full penetration."
        )

    elif "Fillet" in joint:

        explanation.append(
            "Fillet joints are mainly used for structural attachments and supports."
        )

    # ==========================================================
    # ELECTRODE
    # ==========================================================

    explanation.append("\n## ⚙ Electrode Recommendation")

    explanation.append(f"Recommended Electrode : **{electrode}**")

    if electrode == "E7018":

        explanation.append(
            "E7018 is a low-hydrogen electrode that minimizes hydrogen cracking and provides excellent strength."
        )

    elif "ER308" in electrode:

        explanation.append(
            "ER308L filler maintains corrosion resistance while welding SS304."
        )

    elif "ER316" in electrode:

        explanation.append(
            "ER316L filler is suitable for SS316 and maintains corrosion resistance."
        )

    # ==========================================================
    # PARAMETERS
    # ==========================================================

    explanation.append("\n## 🔥 Welding Parameters")

    explanation.append(f"• Current : {current}")
    explanation.append(f"• Voltage : {voltage}")
    explanation.append(f"• Groove Angle : {groove}")
    explanation.append(f"• Root Gap : {root_gap}")
    explanation.append(f"• Welding Passes : {passes}")

    # ==========================================================
    # DISTORTION
    # ==========================================================

    explanation.append("\n## 📊 Distortion Assessment")

    if thickness <= 10:

        explanation.append(
            "Thin sections are more susceptible to angular distortion. Use intermittent welding and proper clamping."
        )

    elif thickness <= 20:

        explanation.append(
            "Moderate distortion is expected. Balanced welding sequence is recommended."
        )

    else:

        explanation.append(
            "Thick sections develop significant residual stresses. Controlled heat input and inter-pass temperature are recommended."
        )

    # ==========================================================
    # ENGINEERING RECOMMENDATIONS
    # ==========================================================

    explanation.append("\n## 👨‍🏭 Engineering Recommendations")

    explanation.append(
        "• Use balanced welding sequence.\n"
        "• Maintain inter-pass temperature.\n"
        "• Use proper edge preparation.\n"
        "• Clamp the workpiece before welding.\n"
        "• Inspect each weld pass visually.\n"
        "• Perform suitable NDT before hydrostatic testing."
    )

    # ==========================================================
    # ASME NOTE
    # ==========================================================

    explanation.append("\n## 📘 ASME Perspective")

    explanation.append(
        "These recommendations follow common engineering practices consistent with "
        "ASME Section IX for pressure vessel fabrication. Final production welding "
        "must always be qualified using an approved Welding Procedure Specification (WPS) "
        "and Procedure Qualification Record (PQR)."
    )

    return "\n\n".join(explanation)


# ==========================================================
# DISTORTION RESULT EXPLANATION
# (same offline, rule-based approach as explain_welding above)
# ==========================================================

def explain_distortion(
    material,
    thickness,
    diameter,
    joint,
    head,
    heat_input,
    total_deformation,
    risk,
    shell_ovality,
    peaking_longitudinal_seam,
    bulging_nozzle_welds,
    flange_face_angular,
    nozzles
):

    exp = []

    # ----------------------------------------------------------
    # OVERALL RISK
    # ----------------------------------------------------------

    exp.append("## ⚠ Overall Distortion Risk")

    if risk.startswith("LOW"):
        exp.append(
            f"With a heat input of **{heat_input:.2f} kJ/mm** on **{thickness} mm** "
            f"**{material}**, the predicted total deformation of **{total_deformation:.2f} mm** "
            "is low. Standard fit-up and clamping practice should be sufficient."
        )
    elif risk.startswith("MEDIUM"):
        exp.append(
            f"With a heat input of **{heat_input:.2f} kJ/mm** on **{thickness} mm** "
            f"**{material}**, the predicted total deformation of **{total_deformation:.2f} mm** "
            "is moderate — balanced/symmetric welding sequence and interpass temperature "
            "control are recommended to keep it there."
        )
    else:
        exp.append(
            f"With a heat input of **{heat_input:.2f} kJ/mm** on **{thickness} mm** "
            f"**{material}**, the predicted total deformation of **{total_deformation:.2f} mm** "
            "is high. Strongbacks, reverse camber, controlled heat input and a strict "
            "welding sequence are strongly recommended before fabrication begins."
        )

    # ----------------------------------------------------------
    # SHELL OVALITY
    # ----------------------------------------------------------

    exp.append("\n## 🔵 Shell Ovality")

    if shell_ovality < 1:
        exp.append(
            f"Estimated at **{shell_ovality:.2f} mm** out-of-round — minor. The "
            f"{diameter} mm diameter shell at {thickness} mm thickness has enough "
            "stiffness to resist significant girth-weld shrinkage."
        )
    else:
        exp.append(
            f"Estimated at **{shell_ovality:.2f} mm** out-of-round. Larger diameter "
            "shells are more prone to out-of-roundness from circumferential weld "
            "shrinkage — internal strongbacks/spider bracing during girth welding "
            "will help hold roundness."
        )

    # ----------------------------------------------------------
    # PEAKING
    # ----------------------------------------------------------

    exp.append("\n## 📐 Peaking at Longitudinal Seam")

    exp.append(
        f"Estimated at **{peaking_longitudinal_seam:.2f} mm** over a 200 mm gauge "
        f"length, driven by the angular distortion at the {joint.lower()}. Proper "
        "edge preparation and balanced multi-pass welding reduce peaking."
    )

    # ----------------------------------------------------------
    # NOZZLE BULGING
    # ----------------------------------------------------------

    exp.append("\n## 🟠 Bulging Near Nozzle Welds")

    if not nozzles:
        exp.append("No nozzles specified for this geometry — not applicable.")
    else:
        exp.append(
            f"With **{nozzles}** nozzle attachment weld(s), local heat concentration "
            f"around the reinforcement pads is estimated to cause **{bulging_nozzle_welds:.2f} mm** "
            "of local bulging. Chill bars/heat sinks around the nozzle openings "
            "during welding help limit this."
        )

    # ----------------------------------------------------------
    # FLANGE FACE ANGULAR
    # ----------------------------------------------------------

    exp.append("\n## 🟣 Flange Face Angular Distortion")

    exp.append(
        f"Estimated at **{flange_face_angular:.2f}°** at the {head.lower()} head/flange "
        "region. Flange faces should be checked for flatness after welding using a "
        "straightedge before gasket installation."
    )

    # ----------------------------------------------------------
    # CLOSING NOTE
    # ----------------------------------------------------------

    exp.append(
        "\n---\n*These are rule-based engineering estimates derived from the "
        "calculated heat input and geometry factors — useful for identifying which "
        "locations need the most attention, not a substitute for measurement or FEA "
        "validation.*"
    )

    return "\n\n".join(exp)