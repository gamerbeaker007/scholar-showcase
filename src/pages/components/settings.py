import re

import streamlit as st

from src.api import db_actions
from src.models.models import User, RoleEnum
from src.utils import notifications, local_storage_manager


def is_valid_email(email: str) -> bool:
    if email:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    return True


def is_valid_discord(discord: str) -> bool:
    if not discord:
        return True

    if len(discord) > 50:
        return False

    # Legacy format: Username#1234
    legacy_pattern = r"^[\w]{2,32}#\d{4}$"

    # New Discord username format
    # Must be 2–32 chars, only a-z, 0-9, _ and ., no __ or .. or ._ or _.,
    # cannot start/end with . or _
    new_format_pattern = r"^(?!.*[_.]{2})[a-z0-9](?:[a-z0-9._]{0,30}[a-z0-9])?$"

    # Also allow user ID (Discord Snowflake ID)
    user_id_pattern = r"^\d{17,20}$"

    return bool(
        re.match(legacy_pattern, discord.lower()) or
        re.match(new_format_pattern, discord.lower()) or
        re.match(user_id_pattern, discord.lower())
    )


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
    discord = st.text_input("Discord*", value=user.discord_reference)

    valid_email = is_valid_email(email)
    if email and not valid_email:
        st.error("Please enter a valid email address.")

    valid_discord = is_valid_discord(discord)
    if discord and not valid_discord:
        st.error("Please enter a valid discord name.")

    st.write("\\* By entering these fields you consent that a others can see you email or"
             " discord username to be used to contact you")

    save_disabled = (not valid_email or not valid_discord)
    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 Save", key="save_settings_btn", disabled=save_disabled):
            if is_valid_discord(discord) and is_valid_email(email):
                user.role = role
                if email:
                    user.email = email
                if discord:
                    user.discord_reference = discord.lower()
                notifications.set_start_up_message("Settings saved.")
                update_use = db_actions.update_user(user)
                local_storage_manager.save_user(update_use)
                st.rerun()
            else:
                st.error("Invalid email or discord name unable to perform save")

    with col_cancel:
        if st.button("❌ Cancel", key="cancel_settings_btn"):
            st.rerun()
