import pandas as pd
import streamlit as st

from src.api import spl


def get_page():
    query_params = st.query_params.to_dict()
    player = query_params.get("player", [""])

    df = pd.DataFrame()
    if player:
        df = spl.get_leaderboard_with_player(player)
    else:
        player_input = st.text_input("account name")
        if player_input:
            df = spl.get_leaderboard_with_player(player)

    st.title(f"🔍 Inspect Page - Player: {player if player else 'Unknown'}")
    st.write("Details about the player will go here.")
    st.dataframe(df)
