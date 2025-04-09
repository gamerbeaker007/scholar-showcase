import streamlit as st

from src.api import db_actions


def get_page():
    st.title("MANAGERS")
    df = db_actions.get_all_managers()
    st.dataframe(df)
