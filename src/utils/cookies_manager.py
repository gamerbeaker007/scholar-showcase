import streamlit as st
import json
from streamlit_cookies_manager import EncryptedCookieManager
from src.models.models import User

cookie_password = st.secrets["cookies"]["password"]

# Global reference to the cookie manager
cookies = None


def init_cookies_manager():
    global cookies
    cookies = EncryptedCookieManager(
        prefix="scholar-showcase/",
        password=cookie_password
    )
    return cookies


def save_cookie_user(user: User):
    if cookies is None:
        init_cookies_manager()

    if cookies.ready():
        user_json = json.dumps(user.to_dict())
        cookies['user'] = user_json
        cookies.save()


def get_cookie_user() -> User | None:
    if cookies is None:
        init_cookies_manager()

    if not cookies.ready():
        return None

    user_json = cookies.get('user')
    if not user_json:
        return None

    try:
        return User(**json.loads(user_json))
    except Exception as e:
        st.error(f"Failed to parse user from cookie: {e}")
        return None


def del_cookie_user():
    if cookies is None:
        init_cookies_manager()

    if cookies.ready():
        cookies['user'] = ""
        cookies.save()
