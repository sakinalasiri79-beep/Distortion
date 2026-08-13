import streamlit as st


def workflow_progress(step):

    steps = [
        "Project",
        "Geometry",
        "Welding",
        "Distortion",
        "Report"
    ]

    cols = st.columns(len(steps))

    for i, col in enumerate(cols):

        with col:

            if i < step:
                st.success(f"✅ {steps[i]}")

            elif i == step:
                st.info(f"🔵 {steps[i]}")

            else:
                st.write(f"⚪ {steps[i]}")

    st.divider()