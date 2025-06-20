import logging
import re

import streamlit as st

from src.api import db_actions, spl
from src.models.models import User, RoleEnum, RewardSplitEnum, PreferredModesEnum, PreferredLeagueEnum
from src.utils import notifications, local_storage_manager

log = logging.getLogger("Settings")


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


def render_basic_user_info(user: User) -> RoleEnum:
    st.text_input("Username", value=user.account, disabled=True)
    role_options = list(RoleEnum)
    current_index = role_options.index(user.role)
    return st.selectbox("Role", options=RoleEnum, index=current_index)


def render_account_input(field: str, label: str, help_text: str):
    if field not in st.session_state:
        st.session_state[field] = []

    st.markdown(f"#### {label}", help=help_text)
    cols = st.columns([6, 1, 1])
    display_warning = False
    with cols[0]:
        input_value = st.text_input(f"{field}_input",
                                    key=f"{field}_input",
                                    label_visibility="collapsed",
                                    placeholder=f"Enter {label.lower()}")
    with cols[1]:
        if st.button("➕", key=f"add_{field}"):
            input_val = input_value.strip()
            if input_val and spl.get_player_profile(player=input_val):
                if input_val not in st.session_state[field]:
                    st.session_state[field].append(input_val)
            else:
                display_warning = True
    with cols[2]:
        if st.button("➖", key=f"remove_{field}"):
            input_val = input_value.strip()
            if input_val in st.session_state[field]:
                st.session_state[field].remove(input_val)

    items = st.session_state.get(field, [])
    if display_warning:
        st.warning("Not a valid SPL account entered")
    if items:
        st.markdown(
            f"<strong>Current {label}:</strong><ul style='margin-bottom: 0; padding-left: 1.2em;'>"
            + "".join(f"<li style='margin-bottom: 0;'>{account}</li>" for account in items)
            + "</ul>",
            unsafe_allow_html=True
        )


def render_scholar_fields(user: User):
    available_for_hire = user.available_for_hire if user.available_for_hire is not None else True

    with st.container(border=True):
        preferred_mode = st.selectbox(
            "Preferred Mode",
            options=PreferredModesEnum,
            index=list(PreferredModesEnum).index(user.preferred_mode) if user.preferred_mode else 0
        )
        preferred_league = st.selectbox(
            "Preferred League",
            options=PreferredLeagueEnum,
            index=list(PreferredLeagueEnum).index(user.preferred_league) if user.preferred_league else 0
        )
        reward_split = st.selectbox(
            "Reward Split (Manager/Scholar)",
            options=RewardSplitEnum,
            index=list(RewardSplitEnum).index(user.reward_split) if user.reward_split else 0
        )

        render_account_input("scholar_accounts",
                             "Scholar Accounts",
                             "Add the accounts here you already play as scholar.")
        render_account_input("alt_accounts",
                             "Alt Accounts",
                             "Add the alt accounts here you also play with.")

        available_for_hire = st.checkbox("Available for Hire", value=available_for_hire)

    return preferred_mode, preferred_league, reward_split, available_for_hire


def handle_save_and_cancel(user: User,
                           role,
                           preferred_mode,
                           preferred_league,
                           reward_split,
                           available_for_hire,
                           discord):
    valid_discord = is_valid_discord(discord)
    if discord and not valid_discord:
        st.error("Please enter a valid discord name.")

    st.write("By entering these fields you consent that others can see your Discord username to contact you.")

    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 Save", key="save_settings_btn", disabled=not valid_discord):
            user.role = role
            user.discord_reference = discord.lower() if discord else None

            if role == RoleEnum.Scholar:
                if not preferred_mode or not reward_split:
                    st.error("Preferred Mode and Reward Split are required for Scholars.")
                    return
                user.preferred_mode = preferred_mode
                user.preferred_league = preferred_league
                user.reward_split = reward_split
                user.alt_accounts = st.session_state.get("alt_accounts", [])
                user.scholar_accounts = st.session_state.get("scholar_accounts", [])
                user.available_for_hire = available_for_hire
            else:
                user.preferred_mode = None
                user.preferred_league = None
                user.reward_split = None
                user.alt_accounts = []
                user.scholar_accounts = []
                user.available_for_hire = False

            log.info(f"Settings saved for user {user.account}")
            notifications.set_start_up_message("Settings saved.")
            updated_user = db_actions.update_user(user)
            local_storage_manager.save_user(updated_user)
            st.session_state.alt_accounts = []
            st.session_state.scholar_accounts = []
            st.rerun()

    with col_cancel:
        if st.button("❌ Cancel", key="cancel_settings_btn"):
            st.session_state.alt_accounts = []
            st.session_state.scholar_accounts = []
            st.rerun()


@st.dialog("User Settings")
def show_settings_dialog(user: User):
    if not user:
        st.warning("You must be logged in to access settings.")
        return

    role = render_basic_user_info(user)
    preferred_mode = preferred_league = reward_split = available_for_hire = None

    if role == RoleEnum.Scholar:
        preferred_mode, preferred_league, reward_split, available_for_hire = render_scholar_fields(user)

    discord = st.text_input("Discord", value=user.discord_reference or "")
    handle_save_and_cancel(user, role, preferred_mode, preferred_league, reward_split, available_for_hire, discord)
