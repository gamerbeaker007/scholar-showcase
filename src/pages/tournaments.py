import logging

import pandas as pd
import streamlit as st

from src.api import spl

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


def get_page():
    st.title("Tournament Overview")
    df = spl.get_complete_tournaments()

    bronze_rows = df[df['name'].str.startswith(tournament_name)]

    if bronze_rows.empty:
        st.warning(f'No tournaments found with name {tournament_name}')
        return

    tournament_ids = bronze_rows['id'].tolist()
    grouped = get_aggregated_players(tournament_ids)

    st.write(f"Scanned tournaments with title {tournament_name}")
    st.write(f"Found tournaments: {bronze_rows.index.size}")
    st.write("This are the are the players and how many wins and losses and their finishes")
    cols = st.columns([2, 1])
    with cols[0]:
        st.dataframe(grouped, use_container_width=100)
