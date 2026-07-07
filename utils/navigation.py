import streamlit as st

def home_button():
    st.divider()

    if st.button("🏠 Home"):
        st.switch_page("app.py")