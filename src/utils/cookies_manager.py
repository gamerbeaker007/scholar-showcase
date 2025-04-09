import streamlit as st
import json
from streamlit_cookies_manager import EncryptedCookieManager
from src.models.models import User

def get_cookies():
    if "cookies" not in st.session_state:
        cookie_password = st.secrets["cookies"]["password"]
        st.session_state.cookies = EncryptedCookieManager(
            prefix="scholar-showcase/",
            password=cookie_password
        )
    return st.session_state.cookies

def save_cookie_user(user: User):
    cookies = get_cookies()
    if cookies.ready():
        cookies['user'] = json.dumps(user.to_dict())
        cookies.save()

def get_cookie_user() -> User | None:
    cookies = get_cookies()
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
    cookies = get_cookies()
    if cookies.ready():
        cookies['user'] = ""
        cookies.save()
