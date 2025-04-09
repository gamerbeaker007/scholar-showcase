import re

import streamlit as st

from src.api import db_actions
from src.models.models import User, RoleEnum
from src.utils import notifications, cookies_manager


def is_valid_email(email: str) -> bool:
    if email:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    return True


@st.dialog("User Settings")
def show_settings_dialog(user: User):

    if not user:
        st.warning("You must be logged in to access settings.")
        return

    st.text_input("Username", value=user.account, disabled=True)

    role_options = list(RoleEnum)
    current_index = role_options.index(user.role)
    role = st.selectbox("Role", options=RoleEnum, index=current_index)

    email = st.text_input("Email*", value=user.email)
    email_valid = is_valid_email(email)
    if email and not email_valid:
        st.error("Please enter a valid email address.")

    discord = st.text_input("Discord*", value=user.discord_reference)

    st.write("\\* By entering these fields you consent that a others can see you email or"
             " discord username to used to contant you")

    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 Save", key="save_settings_btn", disabled=not email_valid):
            user.role = role
            if email:
                user.email = email
                user.email_enabled = True
            else:
                user.email_enabled = False
            if discord:
                user.discord_reference = discord
                user.discord_enabled = True
            else:
                user.discord_enabled = False
            notifications.set_start_up_message("Settings saved.")
            update_use = db_actions.update_user(user)
            cookies_manager.save_cookie_user(update_use)
            st.rerun()

    with col_cancel:
        if st.button("❌ Cancel", key="cancel_settings_btn"):
            st.rerun()
