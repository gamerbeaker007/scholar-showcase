import streamlit as st

from src.api import spl
from src.utils.icons import WEB_URL
from src.utils.static_enums import league_ratings


def get_page():
    query_params = st.query_params.to_dict()
    player = query_params.get("player", [])

    if not player:
        player = st.text_input("account name")

    if player:

        wild_df = spl.get_leaderboard_with_player(player, "wild")
        modern_df = spl.get_leaderboard_with_player(player, "modern")
        survival_df = spl.get_leaderboard_with_player(player, "survival")

        col1, col2, col3 = st.columns(3)
        with col1:
            if not wild_df.empty:
                rating = wild_df.rating.iloc[0]
                icon = get_league_icon(rating, 'modern')
                st.write("Modern")
                st.image(icon)
                st.write(rating)
            else:
                st.write("N/A")
        with col2:
            if not modern_df.empty:
                rating = modern_df.rating.iloc[0]
                icon = get_league_icon(rating, 'wild')
                st.write("Wild")
                st.image(icon)
                st.write(rating)
            else:
                st.write("N/A")
        with col3:
            if not survival_df.empty:
                rating = survival_df.rating.iloc[0]
                icon = get_league_icon(rating, 'wild')
                st.write("Survival")
                st.image(icon)
                st.write(rating)
            else:
                st.write("N/A")

        st.title(f"🔍 Inspect Page - Player: {player if player else 'Unknown'}")
        st.write("Details about the player will go here.")
        st.dataframe(wild_df)
        st.dataframe(modern_df)
        st.dataframe(survival_df)


def get_league_icon(rating, format_type):
    for i in range(1, len(league_ratings)):
        if rating < league_ratings[i]:
            league_index = i - 1
            break
    else:
        league_index = 0
    return f"{WEB_URL}website/icons/leagues/{format_type}_150/league_{league_index}.png"
