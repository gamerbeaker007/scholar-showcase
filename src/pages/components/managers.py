import streamlit as st

from src.api import db_actions
from src.pages.tournaments_components.contact_info_card import get_contact_info_card
from src.pages.tournaments_components.player_info_card import get_player_info_card
from src.utils.themes import get_back_colors

container_style = """<style>
    .flex-container {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
    }

    </style>"""


def get_page():
    st.title("Registered Managers")
    row_colors = get_back_colors()

    df = db_actions.get_all_managers()

    if df.empty:
        st.markdown(
            """
            <div style="display: flex; center; margin-top: 1em;">
                <div style="background-color: #d0e7ff; padding: 1.5em;
                 border-radius: 8px; max-width: 600px; color: #003366;">
                    <strong>ℹ️ Info:</strong><br><br>
                    There are currently no managers available who have chosen to share their details.
                    If a manager is interested, they will reach out to the scholar directly.
                    <br><br>
                    Once managers become available for contact, they will be listed on this page.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    for idx, (_, row) in enumerate(df.iterrows()):
        bg_color = row_colors[idx % 2]

        player_info_card = get_player_info_card(row)
        contact_info_info = get_contact_info_card(row)

        st.markdown(f"""
        <div style='background-color:{bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
            <div class='flex-container'>
                {player_info_card}
                {contact_info_info}
            </div>
        </div>
        """, unsafe_allow_html=True)
