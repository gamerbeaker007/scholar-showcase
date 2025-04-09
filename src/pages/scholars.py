import streamlit as st

from src.api import db_actions


def get_page():
    st.title("SCHOLARS")
    df = db_actions.get_all_scholars()
    st.dataframe(df)
