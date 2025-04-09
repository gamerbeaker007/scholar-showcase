import streamlit as st

st.set_page_config(page_title="My App", layout="wide")


from src.pages import login, settings, tournaments, managers, scholars  # noqa: E402
from src.utils import notifications  # noqa: E402

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
                print("SS")
                settings.show_settings_dialog(user)
    with col_logout:
        if user:
            if st.button("🚪 Logout", key="logout_btn", help="Logout"):
                print("LL")
                login.logout()
        else:
            if st.button("Login", key="login_btn", help="Login with Hive Keychain"):
                login.show_login_dialog()

    tournaments.get_page()

    managers.get_page()

    scholars.get_page()
