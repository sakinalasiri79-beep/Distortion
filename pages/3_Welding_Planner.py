import streamlit as st
from components.theme import load_css
from utils.welding_process import get_weld_plan, compute_pass_heat_input
from utils.fabrication_sequence import build_fabrication_sequence
from utils.nozzle_engine import (
    heat_input, nozzle_weld_type, check_nozzle_spacing,
    nozzle_local_bulge, flange_angular_tilt, nearest_neighbor
)
from utils.distortion_engine import rank_critical_regions
from itertools import combinations

st.set_page_config(page_title="Welding Process Plan", layout="wide")
load_css()
st.title("🔧 Welding Process & Priority Plan")
st.page_link("pages/2_Geometry.py", label="⬅️ Edit Geometry", icon="📐")


def card(title, body_html, color="#4CAF50"):
    st.markdown(f"""<div class="glass-card"><h4 style="margin-bottom:6px;color:{color};">{title}</h4>
    <div class="glass-content">{body_html}</div></div>""", unsafe_allow_html=True)


def render_plan(joint_code):
    plan = get_weld_plan(joint_code)
    st.markdown(f"**Material:** {plan['material']} &nbsp;|&nbsp; **Max interpass temp:** {plan['interpass_temp_max_C']}°C")
    for p in plan["passes"]:
        arc = f"{p['arc_length_mm']} mm" if p["arc_length_mm"] else "N/A (submerged arc - flux covered)"
        purge = f"<br>Purge: <b>{p['purge']}</b>" if "purge" in p else ""
        Q, S = compute_pass_heat_input(p)
        card(f"{p['pass']} Pass — {p['process']}", f"""
            Filler/Electrode: <b>{p['filler']}</b>, dia <b>{p['dia_mm']} mm</b><br>
            Arc length: <b>{arc}</b><br>
            Current: <b>{p['current_A'][0]}-{p['current_A'][1]} A</b> &nbsp; Voltage: <b>{p['voltage_V'][0]}-{p['voltage_V'][1]} V</b><br>
            Travel speed: <b>{S:.0f} mm/min</b> &nbsp; Heat input: <b>{Q} kJ/mm</b><br>
            Travel angle: <b>{p['travel_angle_deg']}°</b> &nbsp; Work angle: <b>{p['work_angle_deg']}°</b><br>
            Technique: {p['technique']}{purge}
        """, color="#2196F3")
    card("Total Passes", f"<b>{len(plan['passes'])}</b> passes for this joint", color="#9C27B0")
    card("Sequence Note", plan["sequence_note"], color="#FF9800")


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
                         "interacting": False, "joint": wtype["joint"]})

    pair_checks = []
    for a, b in combinations(nozzles, 2):
        pc = check_nozzle_spacing(a, b, radius, shell_thk)
        if pc["interacting"]:
            pair_checks.append(pc)
            for r in results:
                if r["name"] in (a["name"], b["name"]):
                    r["interacting"] = True

    ranked = rank_critical_regions(results)
    seq = build_fabrication_sequence(ranked, pair_checks)

    st.subheader("📋 Full Priority Order — Process & Electrode per Step")
    joint_lookup = {r["name"]: r["joint"] for r in results}

    for s in seq:
        st.markdown(f"### Step {s['step']} — {s['stage']}")
        card(s['item'], s['reason'], color="#4CAF50")

        if "N-" in s['item'] or "MH" in s['item']:
            for nm in joint_lookup:
                if nm in s['item']:
                    render_plan(joint_lookup[nm])
                    this_nozzle = next((n for n in nozzles if n["name"] == nm), None)
                    if this_nozzle:
                        nn = nearest_neighbor(this_nozzle, nozzles, radius, shell_thk)
                        if nn:
                            status = "⚠️ TOO CLOSE" if nn["interacting"] else "✅ Safe spacing"
                            card("Distance to Nearest Nozzle", f"""
                                Nearest: <b>{nn['pair']}</b><br>
                                Edge distance: <b>{nn['edge_distance_mm']} mm</b><br>
                                Minimum required: <b>{nn['min_required_mm']} mm</b><br>
                                Status: <b>{status}</b>
                            """, color="#F44336" if nn["interacting"] else "#4CAF50")
                    break
        elif "L.S" in s['item'] or "C.S" in s['item'] or "Seam" in s['item']:
            render_plan("W2")
        elif "W1" in s['item'] or "Shell" in s['item']:
            render_plan("W1")
        st.divider()

else:
    st.subheader("Longitudinal Seam — Full Process")
    render_plan("LONG_SEAM")
    st.subheader("Circumferential Seam / Head Attachment — Full Process")
    render_plan("CIRC_SEAM")
    st.page_link("pages/4_Distortion_Analysis.py", label="➡️ Distortion Analysis", icon="🧮")