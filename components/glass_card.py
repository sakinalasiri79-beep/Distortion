import streamlit as st

def glass_card(title, content):
    st.markdown(f"""<div style="background:#FFFFFF;padding:20px;border-radius:15px;border:1px solid #DCEEFE;box-shadow:0 4px 14px rgba(0,0,0,0.05);margin-bottom:15px;">
<h4>{title}</h4>
<p>{content}</p>
</div>""", unsafe_allow_html=True)