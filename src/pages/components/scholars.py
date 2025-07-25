import streamlit as st

from src.api.db_actions import get_scholar
from src.pages.tournaments_components.additional_contact_info_card import get_additional_contact_info_card
from src.pages.tournaments_components.contact_info_card import get_contact_info_card
from src.pages.tournaments_components.player_info_card import get_player_info_card
from src.utils.themes import get_back_colors


def add_scholar_card(player):
    st.subheader("📝 Scholar Contact Info")
    bg_color = get_back_colors()
    scholar = get_scholar(player)
    if not scholar.empty:
        row = scholar.iloc[0]
        player_info_card = get_player_info_card(row, False)
        contact_info_info = get_contact_info_card(row)

        st.markdown(f"""
                <div style='background-color:{bg_color[1]}; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                    <div class='flex-container'>
                        {player_info_card}
                        {contact_info_info}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        additional_contact_info = get_additional_contact_info_card(row)
        st.markdown(f"""
                <div>
                <strong>Addition Information</strong>
                    <div class='flex-container'>
                        {additional_contact_info}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Not registered as scholar")
