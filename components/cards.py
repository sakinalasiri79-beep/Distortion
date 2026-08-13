import streamlit as st


def glass_card(title, content):

    st.markdown(
        f'<div class="glass-card">'
        f'<div class="glass-title">{title}</div>'
        f'<div class="glass-content">{content}</div>'
        f'</div>',
        unsafe_allow_html=True
    )