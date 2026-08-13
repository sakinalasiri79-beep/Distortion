import streamlit as st
from components.theme import load_css
st.set_page_config(
    page_title="New Project",
    layout="wide"
)
load_css()
# --------------------------------------------------
# HEADER CARD
# --------------------------------------------------

st.markdown("""
<div class="form-card">

<div class="form-title">
🚀 Create Engineering Project
</div>

<div class="form-subtitle">
Initialize a new pressure vessel fabrication project.
Enter the project details below to begin the engineering workflow.
</div>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PROGRESS
# --------------------------------------------------

st.progress(1/5)

st.caption("Step 1 of 5 • Project Information")

st.write("")

# --------------------------------------------------
# FORM
# --------------------------------------------------

left, right = st.columns(2)

with left:

    project_name = st.text_input(
        "📁 Project Name",
        placeholder="Pressure Vessel Design"
    )

    engineer = st.text_input(
        "👷 Engineer",
        placeholder="Your Name"
    )

with right:

    project_id = st.text_input(
        "🆔 Project ID",
        placeholder="PV-001"
    )

    company = st.text_input(
        "🏢 Company",
        placeholder="ABC Engineering Pvt Ltd"
    )

st.write("")
st.write("")

# --------------------------------------------------
# BUTTON
# --------------------------------------------------

if st.button(
    "🚀 Continue to Geometry",
    use_container_width=True
):

    st.session_state["project"] = {

        "project_name": project_name,
        "engineer": engineer,
        "company": company,
        "project_id": project_id

    }

    st.switch_page(
        "pages/2_Geometry.py"
    )