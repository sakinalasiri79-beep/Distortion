import streamlit as st
import pandas as pd
from components.theme import load_css
from utils.geometry import default_vessel_geometry, default_nozzle_table

st.set_page_config(page_title="Vessel Geometry", layout="wide")
load_css()

st.title("📐 Vessel Geometry Input")
st.caption("Enter the real dimensions from your GA drawing. This feeds the Distortion Analysis page directly.")

case = st.radio("Case", ["Case 1", "Case 2"], horizontal=True)

if "vessel_geo" not in st.session_state:
    st.session_state.vessel_geo = {}
if "nozzle_table" not in st.session_state:
    st.session_state.nozzle_table = {}

geo_defaults = default_vessel_geometry(case)
st.subheader("Shell / Head Geometry")
c1, c2, c3, c4 = st.columns(4)
shell_id = c1.number_input("Shell ID (mm)", value=geo_defaults["shell_id_mm"])
shell_thk = c2.number_input("Shell Thickness (mm)", value=geo_defaults["shell_thk_mm"])
overall_len = c3.number_input("Overall Length (mm)", value=geo_defaults["overall_length_mm"])
head_type = c4.text_input("Head Type", value=geo_defaults["head_type"])

st.session_state.vessel_geo[case] = {
    "shell_id_mm": shell_id, "shell_thk_mm": shell_thk,
    "overall_length_mm": overall_len, "head_type": head_type,
    "radius_mm": shell_id / 2 + shell_thk / 2,
}

if case == "Case 1":
    st.subheader("Nozzle Table")
    st.caption("⚠️ Correct `orientation_deg` (clock position 0-360°) and `axial_mm` "
               "(distance from tangent line/datum) to match your actual drawing — "
               "sizes/thickness are already pulled from your BOM.")

    df = pd.DataFrame(default_nozzle_table())
    edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="nozzle_editor")
    st.session_state.nozzle_table["Case 1"] = edited.to_dict("records")

else:
    st.subheader("Longitudinal Seam Geometry")
    c1, c2, c3 = st.columns(3)
    root_gap = c1.number_input("Root Gap (mm)", value=2.0)
    groove_angle = c2.number_input("Groove Angle (deg)", value=60.0)
    num_passes = c3.number_input("Number of Passes", value=4, step=1)
    st.session_state.vessel_geo["Case 2"].update({
        "root_gap_mm": root_gap, "groove_angle_deg": groove_angle, "num_passes": num_passes
    })


st.success("Geometry saved — go to Welding Planner to see the priority sequence.")
st.page_link("pages/3_Welding_Planner.py", label="➡️ Go to Welding Planner", icon="🔧")