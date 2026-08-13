import streamlit as st
from itertools import combinations
from components.theme import load_css
from utils.nozzle_engine import heat_input, nozzle_weld_type, check_nozzle_spacing, nozzle_local_bulge, flange_angular_tilt
from utils.distortion_engine import (
    weld_cross_section_area, transverse_shrinkage, longitudinal_shrinkage,
    angular_distortion, rank_critical_regions
)
from utils.distortion_vector import (
    nozzle_distortion_vector, seam_distortion_vector, resultant_vessel_vector, classify_severity
)
from utils.sequence_optimizer import optimize_sequence, optimize_seam_sequence
from utils.counter_deformation import build_compensation_table, seam_counter_deformation

st.set_page_config(page_title="Sequence Optimization & Compensation", layout="wide")
load_css()
st.title("🧮 Distortion Vector, Sequence Optimization & Counter-Deformation")
st.page_link("pages/2_Geometry.py", label="⬅️ Edit Geometry", icon="📐")


def card(title, body_html, color="#4CAF50"):
    st.markdown(f"""<div class="glass-card"><h4 style="margin-bottom:6px;color:{color};">{title}</h4>
    <div class="glass-content">{body_html}</div></div>""", unsafe_allow_html=True)


if "vessel_geo" not in st.session_state or "nozzle_table" not in st.session_state:
    st.warning("⚠️ Set geometry on the Vessel Geometry page first.")
    st.stop()

case = st.radio("Select Case", ["Case 1 - SS Multi-Nozzle Shell", "Case 2 - CS Longitudinal Seam"])

if case.startswith("Case 1"):
    geo = st.session_state.vessel_geo.get("Case 1")
    nozzles = st.session_state.nozzle_table.get("Case 1")
    if not geo or not nozzles:
        st.warning("⚠️ Case 1 geometry not set.")
        st.stop()

    radius, shell_thk = geo["radius_mm"], geo["shell_thk_mm"]
    Q = heat_input(22, 110, 150)

    results = []
    for n in nozzles:
        bulge = nozzle_local_bulge(Q, n["od_mm"], shell_thk, n["has_pad"])
        tilt = flange_angular_tilt(Q, n["length_mm"], n["thk_mm"])
        wtype = nozzle_weld_type(shell_thk, n["has_pad"])
        results.append({"name": n["name"], "bulge_mm": bulge, "tilt_deg": tilt,
                         "interacting": False, "joint": wtype["joint"],
                         "orientation_deg": n["orientation_deg"]})

    pair_checks = []
    for a, b in combinations(nozzles, 2):
        pc = check_nozzle_spacing(a, b, radius, shell_thk)
        if pc["interacting"]:
            pair_checks.append(pc)
            for r in results:
                if r["name"] in (a["name"], b["name"]):
                    r["interacting"] = True

    ranked = rank_critical_regions(results)

    # ---------------- DISTORTION VECTORS ----------------
    st.header("1️⃣ Distortion Vector Model")
    vectors = []
    for r in ranked:
        v = nozzle_distortion_vector(r["bulge_mm"], r["tilt_deg"], r["orientation_deg"])
        vectors.append(v)
        sev, color = classify_severity(v["magnitude_mm"])
        card(r["name"], f"""
            Axial: <b>{v['axial_mm']} mm</b> | Circumferential: <b>{v['circumferential_mm']} mm</b> | Angular: <b>{v['angular_deg']}°</b><br>
            Resultant magnitude: <b>{v['magnitude_mm']} mm</b> — Severity: <b>{sev}</b>
        """, color=color)

    resultant = resultant_vessel_vector(vectors)
    st.subheader("Net Vessel Resultant Vector")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Net Axial", f"{resultant['net_axial_mm']} mm")
    c2.metric("Net Circumferential", f"{resultant['net_circumferential_mm']} mm")
    c3.metric("Net Angular", f"{resultant['net_angular_deg']}°")
    c4.metric("Net Magnitude", f"{resultant['net_magnitude_mm']} mm")

    # ---------------- SEQUENCE OPTIMIZATION ----------------
    st.header("2️⃣ Sequence Optimization")
    seq_plan = optimize_sequence(ranked, pair_checks, "Case 1")
    for s in seq_plan:
        card(f"Build Order #{s['build_order']} — {s['region']}", f"""
            <b>Weld Direction:</b> {s['weld_direction']}<br>
            <b>Balance Building:</b> {s['balance_building']}<br>
            <b>Heat Distribution:</b> {s['heat_distribution']}<br>
            <b>Restraint Strategy:</b> {s['restraint_strategy']}
        """, color="#2196F3")

    # ---------------- COUNTER DEFORMATION ----------------
    st.header("3️⃣ Counter-Deformation Plan")
    comp_table = build_compensation_table(ranked)
    st.dataframe(comp_table, use_container_width=True, hide_index=True)

else:
    geo = st.session_state.vessel_geo.get("Case 2")
    if not geo:
        st.warning("⚠️ Case 2 geometry not set.")
        st.stop()

    thickness = geo["shell_thk_mm"]
    root_gap = geo.get("root_gap_mm", 2.0)
    groove_angle = geo.get("groove_angle_deg", 60.0)
    num_passes = geo.get("num_passes", 4)
    seam_length = geo["overall_length_mm"]

    Q = heat_input(24, 160, 200)
    Aw = weld_cross_section_area(root_gap, groove_angle, thickness)
    plate_area = thickness * seam_length

    delta_t = transverse_shrinkage(Aw, thickness)
    delta_L = longitudinal_shrinkage(Aw, plate_area, seam_length)
    alpha = angular_distortion(Q, thickness, num_passes)

    st.header("1️⃣ Distortion Vector Model")
    v = seam_distortion_vector(delta_L, delta_t, alpha)
    sev, color = classify_severity(v["magnitude_mm"])
    card("Longitudinal Seam", f"""
        Axial (shrinkage): <b>{v['axial_mm']} mm</b> | Circumferential (closes gap): <b>{v['circumferential_mm']} mm</b> | Angular (peaking): <b>{v['angular_deg']}°</b><br>
        Resultant magnitude: <b>{v['magnitude_mm']} mm</b> — Severity: <b>{sev}</b>
    """, color=color)

    st.header("2️⃣ Sequence Optimization")
    seq = optimize_seam_sequence(seam_length, num_passes)
    card("Longitudinal Seam Sequence", f"""
        <b>Build Order:</b> {seq['build_order']}<br>
        <b>Weld Direction:</b> {seq['weld_direction']}<br>
        <b>Balance Building:</b> {seq['balance_building']}<br>
        <b>Heat Distribution:</b> {seq['heat_distribution']}<br>
        <b>Restraint Strategy:</b> {seq['restraint_strategy']}
    """, color="#2196F3")

    st.header("3️⃣ Counter-Deformation Plan")
    cd = seam_counter_deformation(delta_L, delta_t, alpha)
    card("Compensation Values", f"""
        Extra length allowance: <b>{cd['extra_length_allowance_mm']} mm</b><br>
        Fit-up gap addition: <b>{cd['fit_up_gap_addition_mm']} mm</b><br>
        Reverse preset angle: <b>{cd['reverse_preset_deg']}°</b><br><br>
        {cd['camber_note']}
    """, color="#9C27B0")
    