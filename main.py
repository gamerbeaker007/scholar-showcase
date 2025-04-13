import importlib
import logging
import sys

import streamlit as st
from st_pages import get_nav_from_toml

from src.pages import tournaments, inspect, registered
from src.pages.components.login_section import login_section
from src.utils import dev_mode


def reload_all():
    """Reload all imported modules. workaround for streamlit to load also changed modules"""
    for module_name in list(sys.modules.keys()):
        # Reload only modules that are not built-in and not part of the standard library
        if module_name.startswith("src"):
            importlib.reload(sys.modules[module_name])


reload_all()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True
)

log = logging.getLogger("Main")

st.set_page_config(page_title="SPL Scholar Showcase", layout="wide")
nav = get_nav_from_toml('.streamlit/pages.toml')
pg = st.navigation(nav)

dev_mode.show_dev_warning()

# Add login to sidebar
login_section()

placeholder = st.empty()
# Dynamically call the page-specific function based on the selected page
if pg.title == "Tournaments":
    with placeholder.container():
        tournaments.get_page()
if pg.title == "Inspect":
    with placeholder.container():
        inspect.get_page()
if pg.title == "Registered":
    with placeholder.container():
        registered.get_page()
