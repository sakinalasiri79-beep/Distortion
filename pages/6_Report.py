import streamlit as st
from datetime import datetime
from components.theme import load_css
from utils.distortion_engine import recommend_compensation, shell_ovality_estimate
from utils.counter_deformation import build_compensation_table
from utils.fabrication_sequence import build_fabrication_sequence

st.set_page_config(page_title="Engineering Report", layout="wide")
load_css()

st.title("📄 Engineering Report")
st.caption("Consolidated summary for fabrication planning and future ANSYS validation.")

st.page_link("pages/2_Geometry.py", label="⬅️ Edit Geometry", icon="📐")
st.page_link("pages/5_Sequence_And_Compensation.py", label="⬅️ Sequence & Compensation", icon="🧮")


def card(title, body_html, color="#4CAF50"):
    st.markdown(f"""<div class="glass-card"><h4 style="margin-bottom:6px;color:{color};">{title}</h4>
    <div class="glass-content">{body_html}</div></div>""", unsafe_allow_html=True)


def build_report_text(project, case_label, case_key, geo, nozzles, analysis):

    lines = []

    lines.append("PV WELDWISE - ENGINEERING REPORT")
    lines.append("=" * 40)
    lines.append(f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}")
    lines.append(f"Case: {case_label}")
    lines.append("")

    lines.append("1. PROJECT INFORMATION")
    lines.append("-" * 40)
    lines.append(f"Project Name : {project.get('project_name') or '-'}")
    lines.append(f"Project ID   : {project.get('project_id') or '-'}")
    lines.append(f"Engineer     : {project.get('engineer') or '-'}")
    lines.append(f"Company      : {project.get('company') or '-'}")
    lines.append("")

    lines.append("2. VESSEL GEOMETRY")
    lines.append("-" * 40)

    if not geo:
        lines.append(f"{case_key} geometry not set yet.")
    else:
        lines.append(f"Shell ID          : {geo['shell_id_mm']} mm")
        lines.append(f"Shell Thickness   : {geo['shell_thk_mm']} mm")
        lines.append(f"Overall Length    : {geo['overall_length_mm']} mm")
        lines.append(f"Head Type         : {geo['head_type']}")

        if case_key == "Case 2":
            lines.append(f"Root Gap          : {geo.get('root_gap_mm', '-')} mm")
            lines.append(f"Groove Angle      : {geo.get('groove_angle_deg', '-')} deg")
            lines.append(f"Number of Passes  : {geo.get('num_passes', '-')}")

    lines.append("")

    case_analysis = analysis.get(case_key)

    if case_key == "Case 1" and nozzles:
        lines.append("NOZZLE INPUT TABLE")
        lines.append("-" * 40)
        for n in nozzles:
            lines.append(
                f"- {n.get('name')}: OD {n.get('od_mm')} mm, "
                f"length {n.get('length_mm')} mm, thk {n.get('thk_mm')} mm, "
                f"orientation {n.get('orientation_deg')} deg, "
                f"pad {'Yes' if n.get('has_pad') else 'No'}"
            )
        lines.append("")

    lines.append("3. DISTORTION PREDICTION")
    lines.append("-" * 40)

    if not case_analysis:
        lines.append("Not computed yet - visit the Distortion Analysis page for this case.")

    elif case_key == "Case 1":
        ranked = case_analysis["ranked"]
        ovality = shell_ovality_estimate([r["bulge_mm"] for r in ranked])

        lines.append(f"Heat Input             : {case_analysis['heat_input']} kJ/mm")
        lines.append(f"Shell Radius            : {case_analysis['radius']} mm")
        lines.append(f"Estimated Shell Ovality : {ovality} mm")
        lines.append("")
        lines.append("Critical Region Ranking:")
        for r in ranked:
            flag = "INTERACTING" if r["interacting"] else "ok"
            lines.append(f"  - {r['name']}: bulge {r['bulge_mm']} mm, tilt {r['tilt_deg']} deg [{flag}]")

        lines.append("")
        lines.append("4. FABRICATION COMPENSATION")
        lines.append("-" * 40)
        comp_table = build_compensation_table(ranked)
        for row in comp_table:
            lines.append(f"  - {row}")

        lines.append("")
        lines.append("5. RECOMMENDED WELDING SEQUENCE")
        lines.append("-" * 40)
        for s in build_fabrication_sequence(ranked, case_analysis["pair_checks"]):
            lines.append(f"  Step {s['step']} - {s['stage']}: {s['item']} ({s['reason']})")

    else:
        lines.append(f"Transverse Shrinkage   : {case_analysis['delta_t']} mm")
        lines.append(f"Longitudinal Shrinkage : {case_analysis['delta_L']} mm")
        lines.append(f"Angular Distortion     : {case_analysis['alpha']} deg")
        lines.append(f"Heat Input             : {case_analysis['heat_input']} kJ/mm")

        comp = recommend_compensation(
            case_analysis["delta_L"], case_analysis["delta_t"], case_analysis["alpha"]
        )

        lines.append("")
        lines.append("4. FABRICATION COMPENSATION")
        lines.append("-" * 40)
        lines.append(f"Extra Length Allowance : {comp['extra_length_allowance_mm']} mm")
        lines.append(f"Fit-up Gap Addition    : {comp['fit_up_gap_addition_mm']} mm")
        lines.append(f"Reverse Preset Angle   : {comp['reverse_preset_deg']} deg")

        lines.append("")
        lines.append("5. RECOMMENDED WELDING SEQUENCE")
        lines.append("-" * 40)
        lines.append("  Step 1 - Longitudinal Seam First: weld while plate is flat/rolled, before circumferential or nozzle welds.")
        lines.append("  Step 2 - Circumferential Seams / Head Attachment: backstep/skip sequencing, symmetric from center outward.")
        lines.append("  Step 3 - Nozzles (see Case 1): only after shell geometry is confirmed within tolerance.")

    lines.append("")
    lines.append("=" * 40)
    lines.append("PV WeldWise v1.0 - Developed for BrainBolt Engineers Sprint 2026")

    return "\n".join(lines)


# --------------------------------------------------
# GUARDS
# --------------------------------------------------

if "project" not in st.session_state:
    st.warning("⚠️ No project found. Start from the **New Project** page.")
    st.stop()

if "vessel_geo" not in st.session_state:
    st.warning("⚠️ No geometry found. Go to the **Vessel Geometry** page first.")
    st.stop()

project = st.session_state.project
analysis = st.session_state.get("analysis", {})

st.write("")

# --------------------------------------------------
# CASE SELECTOR
# --------------------------------------------------

case = st.radio(
    "Select Case",
    ["Case 1 - SS Multi-Nozzle Shell", "Case 2 - CS Longitudinal Seam"],
    horizontal=True
)
case_key = "Case 1" if case.startswith("Case 1") else "Case 2"
geo = st.session_state.vessel_geo.get(case_key)
nozzles = st.session_state.get("nozzle_table", {}).get("Case 1") if case_key == "Case 1" else None

st.write("")

# --------------------------------------------------
# 1. PROJECT INFORMATION
# --------------------------------------------------

st.subheader("1️⃣ Project Information")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Project", project.get("project_name") or "—")
c2.metric("Project ID", project.get("project_id") or "—")
c3.metric("Engineer", project.get("engineer") or "—")
c4.metric("Company", project.get("company") or "—")

st.caption(f"Report generated {datetime.now().strftime('%d %b %Y, %H:%M')} • {case}")

st.divider()

# --------------------------------------------------
# 2. GEOMETRY
# --------------------------------------------------

st.subheader("2️⃣ Vessel Geometry")

if not geo:
    st.warning(
        f"⚠️ {case_key} geometry not set yet — go to the **Vessel Geometry** page, "
        f"select **{case_key}** there, and fill in the fields. It hasn't been saved "
        f"because that case has never actually been selected on that page."
    )
else:
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Shell ID", f"{geo['shell_id_mm']} mm")
    g2.metric("Shell Thickness", f"{geo['shell_thk_mm']} mm")
    g3.metric("Overall Length", f"{geo['overall_length_mm']} mm")
    g4.metric("Head Type", geo['head_type'])

    if case_key == "Case 2":
        s1, s2, s3 = st.columns(3)
        s1.metric("Root Gap", f"{geo.get('root_gap_mm', '—')} mm")
        s2.metric("Groove Angle", f"{geo.get('groove_angle_deg', '—')}°")
        s3.metric("Number of Passes", geo.get('num_passes', '—'))

    if case_key == "Case 1" and nozzles:
        with st.expander("📋 Nozzle Input Table"):
            st.dataframe(nozzles, use_container_width=True, hide_index=True)

st.divider()

# --------------------------------------------------
# 3-5. DISTORTION / COMPENSATION / SEQUENCE — CASE 1
# --------------------------------------------------

case_analysis = analysis.get(case_key)

if case_key == "Case 1":

    st.subheader("3️⃣ Distortion Prediction")

    if not case_analysis:
        st.info("ℹ️ Not computed yet — visit the **Distortion Analysis** page with Case 1 selected to populate this section.")
    else:
        ranked = case_analysis["ranked"]
        pair_checks = case_analysis["pair_checks"]
        ovality = shell_ovality_estimate([r["bulge_mm"] for r in ranked])

        m1, m2, m3 = st.columns(3)
        m1.metric("Heat Input", f"{case_analysis['heat_input']} kJ/mm")
        m2.metric("Shell Radius", f"{case_analysis['radius']} mm")
        m3.metric("Estimated Shell Ovality", f"{ovality} mm")

        st.dataframe(ranked, use_container_width=True, hide_index=True)

        if pair_checks:
            st.warning(f"⚠️ {len(pair_checks)} interacting nozzle pair(s) — see Distortion Analysis for mitigation actions.")
        else:
            st.success("No interacting nozzle pairs at current geometry.")

        st.subheader("4️⃣ Fabrication Compensation")
        comp_table = build_compensation_table(ranked)
        st.dataframe(comp_table, use_container_width=True, hide_index=True)

        st.subheader("5️⃣ Recommended Welding Sequence")
        for s in build_fabrication_sequence(ranked, pair_checks):
            card(
                f"Step {s['step']} — {s['stage']}",
                f"<b style='color:#4CAF50;'>{s['item']}</b><br><small>{s['reason']}</small>"
            )

# --------------------------------------------------
# 3-5. DISTORTION / COMPENSATION / SEQUENCE — CASE 2
# --------------------------------------------------

else:

    st.subheader("3️⃣ Distortion Prediction")

    if not case_analysis:
        st.info("ℹ️ Not computed yet — visit the **Distortion Analysis** page with Case 2 selected to populate this section.")
    else:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Transverse Shrinkage", f"{case_analysis['delta_t']} mm")
        m2.metric("Longitudinal Shrinkage", f"{case_analysis['delta_L']} mm")
        m3.metric("Angular Distortion", f"{case_analysis['alpha']}°")
        m4.metric("Heat Input", f"{case_analysis['heat_input']} kJ/mm")

        st.subheader("4️⃣ Fabrication Compensation")
        comp = recommend_compensation(case_analysis["delta_L"], case_analysis["delta_t"], case_analysis["alpha"])
        card("Compensation Values", f"""
            Extra length allowance: <b>{comp['extra_length_allowance_mm']} mm</b><br>
            Fit-up gap addition: <b>{comp['fit_up_gap_addition_mm']} mm</b><br>
            Reverse preset angle: <b>{comp['reverse_preset_deg']}°</b>
        """)

        st.subheader("5️⃣ Recommended Welding Sequence")
        card("Step 1 — Longitudinal Seam First", "Weld while the plate is flat/rolled, before circumferential or nozzle welds.")
        card("Step 2 — Circumferential Seams / Head Attachment", "Backstep/skip sequencing, symmetric from center outward.")
        card("Step 3 — Nozzles (see Case 1 tab)", "Only after shell geometry is confirmed within tolerance.")

st.divider()

# --------------------------------------------------
# EXPORT
# --------------------------------------------------

st.subheader("⬇️ Export")
st.caption("💡 Tip: your browser's Print dialog (Ctrl/Cmd + P → Save as PDF) also works for a formatted printout of this page.")

report_text = build_report_text(project, case, case_key, geo, nozzles, analysis)

st.download_button(
    "📥 Download Report (.txt)",
    data=report_text,
    file_name=f"{(project.get('project_id') or 'PV').replace(' ', '_')}_Engineering_Report_{case_key.replace(' ', '')}.txt",
    mime="text/plain",
    use_container_width=True
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""<div class="footer">
<b>PV WeldWise Version 1.0</b><br>
Developed for <b>BrainBolt Engineers Sprint 2026</b>
</div>""", unsafe_allow_html=True)