import logging

import pandas as pd
import streamlit as st

from src.api import spl, db_actions
from src.pages.tournaments_components import filter_section
from src.pages.tournaments_components.battle_info_card import get_battle_info_card
from src.pages.tournaments_components.contact_info_card import get_contact_info_card
from src.pages.tournaments_components.player_info_card import get_player_info_card

tournament_name = 'Scarred Hand Bronze Cup'

log = logging.getLogger("Tournaments")


@st.cache_data(ttl="1h")
def get_aggregated_players(tournament_ids: list[str]):
    all_players = pd.DataFrame()

    for _id in tournament_ids:
        log.info(f"Processing tournament ID: {_id}")
        players = spl.get_tournament(_id)  # 🚨 not spl.get_tournament
        all_players = pd.concat([all_players, players], ignore_index=True)

    if all_players.empty:
        return all_players

    grouped = all_players.groupby('player').agg({
        'wins': 'sum',
        'losses': 'sum',
        'finish': lambda x: list(x),
    }).reset_index()
    grouped['tournaments_played'] = grouped['finish'].apply(len)
    return grouped[['player', 'tournaments_played', 'wins', 'losses', 'finish']]


def add_player_overview(df):
    st.markdown(f"## Participants of tournament {tournament_name}")
    row_colors = ["#111", "#222"]

    for idx, (_, row) in enumerate(df.iterrows()):
        bg_color = row_colors[idx % 2]

        player_info_card = get_player_info_card(row)
        battle_info_card = get_battle_info_card(row)
        contact_info_card = get_contact_info_card(row)

        st.markdown(f"""
<div style='background-color:{bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
    <div style='display: flex; justify-content: space-between;'>
        {player_info_card}
        {battle_info_card}
        {contact_info_card}
    </div>
</div>
""", unsafe_allow_html=True)


def merge_data_with_scholars(grouped):
    scholars = db_actions.get_all_scholars()
    scholars = scholars.rename(columns={"account": "player"})
    merged_df = pd.merge(
        grouped,
        scholars,
        how='left',
        on=['player']
    )
    merged_df = merged_df.sort_values(by='wins', ascending=False)
    return merged_df


def calculate_win_rate(row):
    battles = row["wins"] + row["losses"]
    return round(row["wins"] / battles * 100) if battles > 0 else 0


def get_page():
    st.title("Tournament Overview")
    df = spl.get_complete_tournaments()
    bronze_rows = df[df['name'].str.startswith(tournament_name)]

    if bronze_rows.empty:
        st.warning(f'No tournaments found with name {tournament_name}')
        return

    tournament_ids = bronze_rows['id'].tolist()
    grouped = get_aggregated_players(tournament_ids)
    grouped['tournaments'] = grouped['finish'].apply(len)
    grouped['battles'] = grouped["wins"] + grouped["losses"]
    grouped['win rate'] = grouped.apply(calculate_win_rate, axis=1)

    merged_df = merge_data_with_scholars(grouped)

    st.write(f"Scanned tournaments with title {tournament_name}")
    st.write(f"Found tournaments: {bronze_rows.index.size}")
    st.write("This are the are the players and how many wins and losses and their finishes")

    content_col, filters = st.columns([3, 1], gap='large')
    with filters:
        merged_df = filter_section.get_page(merged_df)
    with content_col:
        add_player_overview(merged_df)

    # cols = st.columns([2, 1])
    # with cols[0]:
    #     st.dataframe(merged_df, use_container_width=100)
