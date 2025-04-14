import streamlit as st
import os
import toml


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

    if 'current_theme' not in st.session_state:
        st.session_state.current_theme = 'dark' if 'dark' in theme_names else theme_names[0]

    with st.sidebar:
        st.markdown("### Select Theme")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Light"):
                selected_theme = 'light'
        with col2:
            if st.button("Dark"):
                selected_theme = 'dark'
        with col3:
            if st.button("Scholar"):
                selected_theme = 'custom'

        # Apply theme if changed
        if 'selected_theme' in locals() and selected_theme != st.session_state.current_theme:
            if selected_theme in themes:
                update_theme(themes[selected_theme])
                st.session_state.current_theme = selected_theme
                st.rerun()
