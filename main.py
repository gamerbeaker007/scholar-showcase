import importlib
import logging
import sys

import streamlit as st

from src.pages import login, settings, managers, scholars, tournaments
from src.utils import notifications


def reload_all():
    """Reload all imported modules. workaround for streamlit to load also changed modules"""
    for module_name in list(sys.modules.keys()):
        # Reload only modules that are not built-in and not part of the standard library
        if module_name.startswith("src"):
            importlib.reload(sys.modules[module_name])


reload_all()

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
)

st.set_page_config(page_title="My App", layout="wide")

st.title("Scholar Showcase demo")

# Always show main content
with st.container(border=True):
    st.title("Main")

    st.write("Welcome to the main page!")
    notifications.show_start_up_message()

    _, col_user, col_settings, col_logout = st.columns([10, 2, 1, 2])
    user = login.get_user()
    with col_user:
        if user:
            st.write(f"👋 {user.account}")
    with col_settings:
        if user:
            if st.button("⚙️", key="settings_btn", help="Settings"):
                settings.show_settings_dialog(user)
    with col_logout:
        if user:
            if st.button("🚪 Logout", key="logout_btn", help="Logout"):
                login.logout()
        else:
            if st.button("Login", key="login_btn", help="Login with Hive Keychain"):
                login.show_login_dialog()

    tournaments.get_page()

    managers.get_page()

    scholars.get_page()
