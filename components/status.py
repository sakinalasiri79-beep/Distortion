import streamlit as st

def status_card(icon, title, value):
    st.success(f"{icon} {title}: {value}")