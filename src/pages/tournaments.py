import pandas as pd
import streamlit as st

from src.api import spl

tournament_name = 'Scarred Hand Bronze Cup'


def get_page():
    st.title("Tournament Overview")
    df = spl.get_complete_tournaments()
    # st.dataframe(df)
    bronze_rows = df[df['name'].str.startswith(tournament_name)]
    # st.write(bronze_rows.index.size)
    # st.dataframe(bronze_rows)

    all_players = pd.DataFrame()
    for index, row in bronze_rows.iterrows():
        players = spl.get_tournament(row['id'])
        all_players = pd.concat([all_players, players])

    # st.dataframe(all_players)
    grouped = all_players.groupby('player').agg({
        'wins': 'sum',
        'losses': 'sum',
        'finish': lambda x: list(x),  # Collect all end_place values into a list
    }).reset_index()

    # Add a new column to count how many tournaments each player played (length of the end_place list)
    grouped['tournaments_played'] = grouped['finish'].apply(len)

    # Optional: move columns around if you want 'tournaments_played' earlier
    grouped = grouped[['player', 'tournaments_played', 'wins', 'losses', 'finish']]

    st.write(f"Scanned tournaments with title {tournament_name}")
    st.write(f"Found tournaments: {bronze_rows.index.size}")
    st.write("This are the are the players and how many wins and losses and their finishes")
    cols = st.columns([2, 1])
    with cols[0]:
        st.dataframe(grouped, use_container_width=100)
