import pandas as pd
import streamlit as st

from src.models.models import RoleEnum

filter_players = "filter_players"
filter_role = "filter_role"
sorting = "sorting"


def apply_filters(df: pd.DataFrame):
    if st.session_state.get(filter_players):
        df = df[df.player.isin(st.session_state[filter_players])]
    if st.session_state.get(filter_role):
        df = df[df.role == RoleEnum.Scholar.value]

    return df


def apply_sorting(df: pd.DataFrame):
    if st.session_state.get(sorting):
        sort_by = st.session_state.get(sorting).lower()
        if sort_by in df.columns.to_list():
            if sort_by == 'player':
                ascending = True
            else:
                ascending = False
            df = df.sort_values(by=sort_by, ascending=ascending)
    return df


def get_page(df: pd.DataFrame):
    filtered_df = df.copy()

    players_options = df['player'].dropna().sort_values().unique().tolist()
    sorting_options = ['Win', 'Win Rate', 'Losses', 'Player', 'Battles', 'Tournaments']

    st.markdown("### 🎛️ Filters")
    st.multiselect(
        "Players",
        options=players_options,
        key=filter_players,
        default=st.session_state.get(filter_players, []))

    st.checkbox(
        "Registered Scholars",
        key=filter_role,
        value=False,
    )
    st.selectbox(
        "Sorting",
        options=sorting_options,
        key=sorting,
    )

    df = apply_filters(filtered_df)
    return apply_sorting(df)
