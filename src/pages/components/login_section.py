import logging

import streamlit as st

from src.pages.components import settings
from src.utils import notifications, local_storage_manager, login
from streamlit_hive_login import st_hive_login

log = logging.getLogger("Login")


@st.dialog("Login to your account")
def show_login_dialog():
    st.title("Login with hive key chain")
    result = st_hive_login()

    if result:
        if result.get("success"):
            user = result['username']
            log.info(f"Login success for user {user}")
            user = login.login(user)
            with st.spinner():
                local_storage_manager.save_user(user)
            st.rerun()
        else:
            st.error(result.get("error", "Hive Keychain failed or was denied."))


def login_section():
    with st.sidebar:
        user = login.get_user()

        if user:
            st.markdown(f"**Logged in as:** `{user.account}`")

            col1, col2 = st.columns([1, 1], gap="small")
            with col1:
                if st.button("⚙️ Settings", key="settings_btn", help="Settings"):
                    for key in ["scholar_accounts", "alt_accounts"]:
                        st.session_state.pop(key, None)
                    settings.show_settings_dialog(user)
            with col2:
                if st.button("🚪 Logout", key="logout_btn", help="Logout"):
                    login.logout()

        else:
            if st.button("🔐 Login", key="login_btn", help="Login with Hive Keychain"):
                show_login_dialog()

        st.markdown("---")
        notifications.show_start_up_message()
