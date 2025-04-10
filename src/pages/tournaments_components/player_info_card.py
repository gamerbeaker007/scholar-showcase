from src.utils.icons import player_icon_url

# Define CSS styles
player_info_styles = """
<style>
.player-card {
    flex: 1;
    position: relative;
    min-height: 60px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    background-color: transparent;
    padding-left: 10px;
    transition: background 0.2s ease;
}
.player-card:hover {
    background-color: rgba(255, 255, 255, 0.05);
}
.player-card img {
    height: 40px;
    opacity: 0.8;
    margin-right: 12px;
}
.player-card span {
    color: white;
    font-weight: bold;
    font-size: 18px;
}
.player-card-link {
    display: flex;
    align-items: center;
    text-decoration: none;
}
</style>
"""


def get_player_info_card(row):
    return f"""{player_info_styles}<div class='player-card'>
            <a href='inspect?player={row["player"]}' target='_self' class='player-card-link '>
                <img src='{player_icon_url}' alt='player icon' />
                <span>{row["player"]}</span>
            </a>
        </div>"""
