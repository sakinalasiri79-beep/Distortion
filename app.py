import streamlit as st
import base64
from components.theme import load_css

# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------

st.set_page_config(
    page_title="PV WeldWise",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_css()



# ----------------------------------------------------
# HIDE STREAMLIT DEFAULTS
# ----------------------------------------------------

st.markdown("""
<style>

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# HERO IMAGE
# ----------------------------------------------------

def get_base64(path):

    with open(path, "rb") as image:

        return base64.b64encode(image.read()).decode()

hero = get_base64("assets/hero.png")

# ----------------------------------------------------
# NAVBAR
# ----------------------------------------------------

st.markdown("""
<div class="navbar">
<div class="logo">
⚙️ PV WeldWise
</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero-container">
<img src="data:image/png;base64,{hero}">
<div class="overlay"></div>
<div class="hero-text">
<h1>Predict & Control Welding Distortion</h1>
<h3>Engineering Support for Pressure Vessel Fabrication</h3>
<p>
PV WeldWise helps you predict shrinkage, angular distortion and
total deformation before fabrication begins — and generates
reverse camber, extra length and welding sequence
recommendations to compensate for it, based on ASME Section IX
practices.
</p>
</div>
</div>
""", unsafe_allow_html=True)
# ----------------------------------------------------
# START PROJECT BUTTON
# ----------------------------------------------------

st.write("")

c1, c2, c3 = st.columns([2, 1.2, 2])

with c2:

    if st.button(
        "🚀 Start New Project",
        use_container_width=True
    ):

        st.switch_page("pages/1_Project.py")

st.write("")
st.write("")

# ----------------------------------------------------
# ENGINEERING MODULES
# ----------------------------------------------------

st.markdown(
    """<h2 class="center-title">Engineering Modules</h2>""",
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

cards = [

    (
        "⚙️",
        "Smart WPS Generator",
        "Generates optimized Welding Procedure Specifications based on material, joint type and thickness."
    ),

    (
        "📈",
        "Distortion Prediction",
        "Predicts heat input, shrinkage, angular distortion and total deformation before fabrication."
    ),

    (
        "🛠",
        "Fabrication Intelligence",
        "Recommends reverse camber, welding sequence, clamping and strongbacks to minimize welding distortion."
    ),

    (
        "📄",
        "Engineering Report",
        "Creates a complete engineering report for fabrication planning and future ANSYS validation."
    )

]

for col, card in zip(
    [col1, col2, col3, col4],
    cards
):

    with col:

        st.markdown(
            f"""<div class="card">
<h3>{card[0]} {card[1]}</h3>
<p>{card[2]}</p>
</div>""",
            unsafe_allow_html=True
        )

st.write("")
st.write("")

# ----------------------------------------------------
# ENGINEERING WORKFLOW
# ----------------------------------------------------

st.markdown(
    """<h2 class="center-title">Engineering Workflow</h2>""",
    unsafe_allow_html=True
)

st.markdown(
    """<div class="glass-card">
<div class="glass-content" style="text-align:center;font-size:20px;">
📐 Geometry
<br>⬇️<br>
⚙️ Smart WPS Generator
<br>⬇️<br>
📈 Distortion Prediction
<br>⬇️<br>
🛠 Distortion Compensation
<br>⬇️<br>
📄 Engineering Report
</div>
</div>""",
    unsafe_allow_html=True
)

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.markdown(
    """<div class="footer">
<b>PV WeldWise Version 1.0</b><br>
Developed for <b>BrainBolt Engineers Sprint 2026</b>
</div>""",
    unsafe_allow_html=True
)