import streamlit as st


# ==========================================
# PAGE HEADER
# ==========================================

def page_header(title, subtitle=""):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg,#0F4C81,#1E6BA8);
            padding:18px;
            border-radius:12px;
            color:white;
            margin-bottom:15px;
        ">
            <h2 style="margin:0;">⚙️ PV WeldWise</h2>
            <p style="margin:0;font-size:16px;">
                {title}
            </p>
            <small>{subtitle}</small>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# PROGRESS BAR
# ==========================================

def progress(step):

    steps = [
        "Project",
        "Geometry",
        "Welding",
        "Distortion",
        "Report"
    ]

    cols = st.columns(len(steps))

    for i, col in enumerate(cols):

        if i < step:
            col.success(f"✅ {steps[i]}")

        elif i == step:
            col.info(f"🔵 {steps[i]}")

        else:
            col.write(f"⚪ {steps[i]}")

    st.divider()


# ==========================================
# FOOTER
# ==========================================

def footer():

    st.markdown(
        """
        <hr>

        <div style='text-align:center;color:gray;'>

        <b>PV WeldWise Version 1.0</b>

        <br>

        Developed by Team RoboForge

        <br>

        BrainBolt South Region 2026

        </div>
        """,
        unsafe_allow_html=True
    )