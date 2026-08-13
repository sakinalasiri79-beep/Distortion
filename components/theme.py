import streamlit as st
from pathlib import Path


def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "style.css"

    with open(css_path, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )