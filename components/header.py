import streamlit as st

def workspace_header(title, subtitle):

    st.markdown(
        f"""
<div class="glass-card">
    <div class="glass-title">{title}</div>
    <div class="glass-content">{subtitle}</div>
</div>
""",
        unsafe_allow_html=True
    )