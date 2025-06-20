import logging

import pandas as pd
import streamlit as st

from src.api import spl, db_actions
from src.pages.tournaments_components import filter_section
from src.pages.tournaments_components.battle_info_card import get_battle_info_card
from src.pages.tournaments_components.contact_info_card import get_contact_info_card
from src.pages.tournaments_components.player_info_card import get_player_info_card
from src.utils.themes import get_back_colors
from src.utils.tournaments_utils import get_qualified_tournaments, calculate_win_rate

log = logging.getLogger("Tournaments")


def get_aggregated_players(tournament_ids: list[str]):
    all_players = pd.DataFrame()

    for tournament_id in tournament_ids:
        log.info(f"Processing tournament ID: {tournament_id}")
        players = spl.get_tournament(tournament_id)
        all_players = pd.concat([all_players, players], ignore_index=True)

    if all_players.empty:
        return all_players

    grouped = all_players.groupby('player').agg({
        'wins': 'sum',
        'losses': 'sum',
        'finish': lambda x: list(x),
    }).reset_index()
    grouped['tournaments'] = grouped['finish'].apply(len)
    grouped['battles'] = grouped["wins"] + grouped["losses"]
    grouped['win rate'] = grouped.apply(calculate_win_rate, axis=1)

    return grouped[['player', 'tournaments', 'wins', 'losses', 'finish', 'battles', 'win rate']]


def add_player_overview(df, tournament_name):
    row_colors = get_back_colors()

    st.markdown(f"## Participants of tournament {tournament_name}")

    for idx, (_, row) in enumerate(df.iterrows()):
        bg_color = row_colors[idx % 2]

        player_info_card = get_player_info_card(row)
        battle_info_card = get_battle_info_card(row)
        contact_info_card = get_contact_info_card(row)

        st.markdown(f"""
        <div style='background-color:{bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
            <div class='flex-container'>
                {player_info_card}
                {battle_info_card}
                {contact_info_card}
            </div>
        </div>
        """, unsafe_allow_html=True)


def merge_data_with_scholars(grouped):
    scholars = db_actions.get_all_scholars()

    merged_df = pd.merge(
        grouped,
        scholars,
        how='left',
        left_on='player',
        right_on='account',
        suffixes=('', '_scholar')
    )

    merged_df = merged_df.sort_values(by='wins', ascending=False)
    return merged_df


def get_page():
    st.title("Tournament Overview")

    use_all = st.checkbox("All Qualified Tournaments", value=True)

    qualified_names = get_qualified_tournaments()
    tournament_name = None
    if not use_all:
        tournament_name = st.selectbox("Select tournament:", options=qualified_names)

    with st.spinner("Loading data..."):
        df = spl.get_complete_tournaments()

        if use_all:
            matching_tournaments = df[df['name'].isin(qualified_names)]
        elif tournament_name:
            matching_tournaments = df[df['name'].str.startswith(tournament_name)]
        else:
            matching_tournaments = pd.DataFrame()

        if matching_tournaments.empty:
            st.warning('❌ No tournaments found.')
            return

        tournament_ids = matching_tournaments['id'].tolist()
        grouped = get_aggregated_players(tournament_ids)
        merged_df = merge_data_with_scholars(grouped)

        df['start_date'] = pd.to_datetime(df['start_date'])
        start = df['start_date'].min().strftime('%Y-%m-%d')
        end = df['start_date'].max().strftime('%Y-%m-%d')
        st.markdown(
            f"""
            ##### 🏆 Found <span style="color:#2E86AB; font-weight:bold;">{df.index.size} tournaments</span>
            between <b>{start}</b> and <b>{end}</b>
            🎓 <span style="color:#27AE60; font-weight:bold;">{matching_tournaments.index.size} qualified</span>
            for the <b>scholarship model</b>.
            """,
            unsafe_allow_html=True
        )

        merged_df = filter_section.get_page(merged_df)
        add_player_overview(merged_df, "All Tournaments" if use_all else tournament_name)
