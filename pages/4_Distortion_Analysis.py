import streamlit as st
from itertools import combinations
from components.theme import load_css
from utils.nozzle_engine import (
    heat_input, nozzle_weld_type, check_nozzle_spacing,
    nozzle_local_bulge, flange_angular_tilt
)
from utils.distortion_engine import (
    weld_cross_section_area, transverse_shrinkage, longitudinal_shrinkage,
    angular_distortion, recommend_compensation, rank_critical_regions,
    classify_distortion, mitigation_for_close_nozzles, shell_ovality_estimate
)
from utils.fabrication_sequence import build_fabrication_sequence

st.set_page_config(page_title="Distortion Analysis", layout="wide")
load_css()
st.title("📈 Welding Distortion Prediction")
st.page_link("pages/2_Geometry.py", label="⬅️ Edit Geometry", icon="📐")
st.page_link("pages/3_Welding_Planner.py", label="⬅️ Welding Process Plan", icon="🔧")


def card(title, body_html, color="#4CAF50"):
    st.markdown(f"""<div class="glass-card"><h4 style="margin-bottom:6px;color:{color};">{title}</h4>
    <div class="glass-content">{body_html}</div></div>""", unsafe_allow_html=True)


if "vessel_geo" not in st.session_state or "nozzle_table" not in st.session_state:
    st.warning("⚠️ No geometry found. Go to the **Vessel Geometry** page first and enter/confirm your drawing data.")
    st.stop()

if "analysis" not in st.session_state:
    st.session_state.analysis = {}

case = st.radio("Select Case", ["Case 1 - SS Multi-Nozzle Shell", "Case 2 - CS Longitudinal Seam"])

# ================= CASE 1 =================
if case.startswith("Case 1"):
    geo = st.session_state.vessel_geo.get("Case 1")
    nozzles = st.session_state.nozzle_table.get("Case 1")
    if not geo or not nozzles:
        st.warning("⚠️ Case 1 geometry not set yet — go to Vessel Geometry page.")
        st.stop()

    radius = geo["radius_mm"]
    shell_thk = geo["shell_thk_mm"]

    # ---- REUSE cached result from Welding Planner if available, else compute ----
    cached = st.session_state.analysis.get("Case 1")
    if cached:
        ranked = cached["ranked"]
        pair_checks = cached["pair_checks"]
        Q = cached["heat_input"]
        st.caption("✅ Using the same analysis computed on the Welding Planner page — numbers are consistent across pages.")
    else:
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
        st.session_state.analysis["Case 1"] = {
            "ranked": ranked, "pair_checks": pair_checks,
            "radius": radius, "shell_thk": shell_thk, "heat_input": Q,
        }
        st.caption("ℹ️ Computed fresh here — visit Welding Planner first if you want the exact same run shared across pages.")

    st.metric("Predicted Heat Input", f"{Q} kJ/mm")
    st.metric("Shell Radius Used", f"{radius} mm")

    st.subheader("🎯 Critical Region Ranking")
    st.dataframe(ranked, use_container_width=True, hide_index=True)

    st.subheader("🧭 Distortion Type Classification (per problem statement)")
    for r in ranked:
        dtype = classify_distortion(r["joint"], r["interacting"])
        card(r["name"], f"<b>{dtype}</b><br>Predicted bulge: {r['bulge_mm']}mm | Tilt: {r['tilt_deg']}°",
             color="#F44336" if r["interacting"] else "#2196F3")

    ovality = shell_ovality_estimate([r["bulge_mm"] for r in ranked])
    st.metric("Estimated Shell Ovality (aggregate)", f"{ovality} mm")

    st.subheader("🔗 Nozzle Pair Interaction Checks (real cylindrical spacing)")
    if pair_checks:
        for pc in pair_checks:
            card(pc["pair"], f"""
                Center distance: <b>{pc['center_distance_mm']} mm</b><br>
                Edge distance: <b>{pc['edge_distance_mm']} mm</b><br>
                Minimum required: <b>{pc['min_required_mm']} mm</b><br>
                Status: <b>⚠️ INTERACTING — combine as coupled zone</b>
            """)

        st.subheader("🚨 Mitigation — Close Nozzle Pairs")
        for pc in pair_checks:
            m = mitigation_for_close_nozzles(pc)
            card(f"⚠️ {pc['pair']}", f"""
                {m['problem']}<br><br>
                <b>Actions:</b><ul>{''.join(f'<li>{a}</li>' for a in m['actions'])}</ul>
            """, color="#F44336")
    else:
        st.success("No interacting nozzle pairs at current geometry.")

    st.subheader("🔧 Recommended Welding Sequence (Priority Order)")
    for s in build_fabrication_sequence(ranked, pair_checks):
        card(f"Step {s['step']} — {s['stage']}", f"""<b style="color:#4CAF50;">{s['item']}</b><br><small>{s['reason']}</small>""")

    st.page_link("pages/5_Sequence_And_Compensation.py", label="➡️ Sequence Optimization & Counter-Deformation", icon="🧮")

# ================= CASE 2 =================
else:
    geo = st.session_state.vessel_geo.get("Case 2")
    if not geo:
        st.warning("⚠️ Case 2 geometry not set yet — go to Vessel Geometry page.")
        st.stop()

    thickness = geo["shell_thk_mm"]
    root_gap = geo.get("root_gap_mm", 2.0)
    groove_angle = geo.get("groove_angle_deg", 60.0)
    num_passes = geo.get("num_passes", 4)
    seam_length = geo["overall_length_mm"]

    V, I, S = 24, 160, 200
    Q = heat_input(V, I, S)
    Aw = weld_cross_section_area(root_gap, groove_angle, thickness)
    plate_area = thickness * seam_length

    delta_t = transverse_shrinkage(Aw, thickness)
    delta_L = longitudinal_shrinkage(Aw, plate_area, seam_length)
    alpha = angular_distortion(Q, thickness, num_passes)

    st.session_state.analysis["Case 2"] = {
        "delta_t": delta_t, "delta_L": delta_L, "alpha": alpha,
        "Aw": Aw, "heat_input": Q,
    }

    c1, c2, c3 = st.columns(3)
    c1.metric("Transverse Shrinkage", f"{delta_t} mm")
    c2.metric("Longitudinal Shrinkage", f"{delta_L} mm")
    c3.metric("Angular Distortion (Peaking)", f"{alpha}°")

    comp = recommend_compensation(delta_L, delta_t, alpha)
    st.subheader("🛠 Fabrication Compensation")
    card("Compensation Values", f"""
        Extra length allowance: <b>{comp['extra_length_allowance_mm']} mm</b><br>
        Fit-up gap addition: <b>{comp['fit_up_gap_addition_mm']} mm</b><br>
        Reverse preset angle: <b>{comp['reverse_preset_deg']}°</b>
    """)

    st.subheader("🧭 Distortion Type Classification")
    card("Longitudinal Seam", f"<b>{classify_distortion('LONG_SEAM')}</b>", color="#2196F3")

    st.subheader("🔧 Recommended Welding Sequence")
    card("Step 1 — Longitudinal Seam First", "Weld while the plate is flat/rolled, before circumferential or nozzle welds.")
    card("Step 2 — Circumferential Seams / Head Attachment", "Backstep/skip sequencing, symmetric from center outward.")
    card("Step 3 — Nozzles (see Case 1 tab)", "Only after shell geometry is confirmed within tolerance.")

    st.page_link("pages/5_Sequence_And_Compensation.py", label="➡️ Sequence Optimization & Counter-Deformation", icon="🧮")