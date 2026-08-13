import streamlit as st


def metric_card(icon, title, value):

    st.markdown(f"""<div class="metric-box">
<h2>{icon}</h2>
<h4>{title}</h4>
<h1>{value}</h1>
</div>""", unsafe_allow_html=True)