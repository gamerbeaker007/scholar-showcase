import streamlit as st
import os
import toml

from src.utils.local_storage_manager import get_stored_theme, store_theme


def load_themes():
    themes_file = os.path.join('.streamlit', 'themes.toml')
    if os.path.exists(themes_file):
        with open(themes_file, 'r') as f:
            themes = toml.load(f)
            return {k.replace('theme.', ''): v for k, v in themes.items()}
    return {}


def update_theme(theme_dict):
    for key, value in theme_dict.items():
        st.config.set_option(f"theme.{key}", value)  # type: ignore # noqa: SLF001


def get_section():
    # Theme selector
    themes = load_themes()
    theme_names = list(themes.keys())

    stored_theme = get_stored_theme()
    if not stored_theme:
        selected_theme = theme_names[0]
    else:
        selected_theme = stored_theme

    with (st.sidebar):
        st.markdown("### Select Theme")

        col1, col2, col3, _ = st.columns([1, 1, 1, 5], gap='small')
        with col1:
            if st.button("L"):
                selected_theme = 'light'
        with col2:
            if st.button("D"):
                selected_theme = 'dark'
        with col3:
            if st.button("S"):
                selected_theme = 'scholar'

        # Apply theme if changed
        if 'current_theme' not in st.session_state or selected_theme != st.session_state.current_theme:
            if selected_theme in themes:
                store_theme(selected_theme)
                update_theme(themes[selected_theme])
                st.session_state.current_theme = selected_theme
                st.rerun()


def get_back_colors():
    theme = st.session_state.get("current_theme", "scholar")
    if theme == "dark":
        return ["#111", "#222"]
    elif theme == "light":
        return ["#edede9", "#d5bdaf"]
    elif theme == "scholar":
        return ["#dda15e", "#bc6c25"]
    else:
        return ["#ffffff", "#eeeeee"]  # default fallback
