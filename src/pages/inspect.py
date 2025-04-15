import pandas as pd
import streamlit as st

from src.api import spl
from src.pages.inspect_components.leauge_component import league_info, league_info_style


def get_page():
    query_params = st.query_params.to_dict()
    player = query_params.get("player", None)

    st.title("Inspect specific player")

    player = st.text_input("account name", value=player)

    st.title(f"🔍 Inspect Page - Player: {player if player else 'Unknown'}")
    with st.spinner("Loading data..."):
        if player:
            # wild_df = spl.get_leaderboard_with_player(player, "wild")
            # modern_df = spl.get_leaderboard_with_player(player, "modern")
            # survival_df = spl.get_leaderboard_with_player(player, "survival")
            #
            # # Get all non-empty league dataframes
            # league_data = []
            # guild_name = None
            # if not modern_df.empty:
            #     league_data.append(("modern", modern_df))
            #     guild_name = modern_df.guild_name.iloc[0]
            # if not wild_df.empty:
            #     league_data.append(("wild", wild_df))
            #     guild_name = wild_df.guild_name.iloc[0]
            # if not survival_df.empty:
            #     league_data.append(("survival", survival_df))
            #     guild_name = survival_df.guild_name.iloc[0]
            #
            # # Show cards in left-to-right order using columns
            # st.markdown(league_info_style, unsafe_allow_html=True)
            # columns = st.columns(3)
            #
            # for i, (format_type, df) in enumerate(league_data):
            #     with columns[i]:
            #         league_info(df, format_type)
            #
            # if guild_name:
            #     st.subheader(f"Member of guild: {guild_name}")
            # else:
            #     st.subheader("No member of a guild")

            st.subheader("More specific stats.....")

            result = spl.get_player_profile(player)
            if result:
                modern_df = pd.DataFrame(result['season_details']['modern'], index=[0])
                wild_df = pd.DataFrame(result['season_details']['wild'], index=[0])
                survival_df = pd.DataFrame(result['season_details']['survival'], index=[0])

                league_data = []
                if not modern_df.empty:
                    league_data.append(("modern", modern_df))
                if not wild_df.empty:
                    league_data.append(("wild", wild_df))
                if not survival_df.empty:
                    league_data.append(("survival", survival_df))

                # Show cards in left-to-right order using columns
                st.markdown(league_info_style, unsafe_allow_html=True)
                columns = st.columns(3)

                for i, (format_type, df) in enumerate(league_data):
                    with columns[i]:
                        league_info(df, format_type)

            # if guild_name:
            #     st.subheader(f"Member of guild: {guild_name}")
            # else:
            #     st.subheader("No member of a guild")
