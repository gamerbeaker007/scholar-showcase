import streamlit as st

from src.pages.components import managers, scholars


def get_page():
    st.title("✅ Registered Page")
    managers.get_page()
    scholars.get_page()
