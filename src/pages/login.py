import streamlit as st

from src.api import db_actions
from src.models.models import User
from src.utils import cookies_manager
from streamlit_hive_login import st_hive_login


def login(account):
    user = db_actions.get_user(account)
    if user:
        return user
    else:
        user = db_actions.create_user(account)
        return user


@st.dialog("Login to your account")
def show_login_dialog():
    st.title("Login with hive key chain")
    result = st_hive_login()

    if result:
        if result.get("success"):
            user = login(result['username'])
            cookies_manager.save_cookie_user(user)
            st.rerun()
        else:
            st.error(result.get("error", "Hive Keychain failed or was denied."))


def get_user() -> User | None:
    return cookies_manager.get_cookie_user()


def logout():
    cookies_manager.del_cookie_user()
    st.rerun()
