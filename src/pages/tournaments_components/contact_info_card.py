from src.icons import discord_icon_url, email_icon_url

# CSS Styles for Contact Info Card
contact_info_styles = """
<style>
.contact-card {
    flex: 2;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 10px;
    color: white;
}
.contact-item {
    display: flex;
    align-items: center;
    margin-bottom: 6px;
}
.contact-item img {
    height: 20px;
    margin-right: 8px;
}
.contact-email a {
    color: white;
    text-decoration: none;
}
</style>
"""


def get_contact_info_card(row):
    if row["role"] != "Scholar":
        return f"""{contact_info_styles}<div class='contact-card'>
            <div class='contact-item'>No contact info</div>
        </div>"""

    discord_html = "<div></div>"
    email_html = "<div></div>"

    if row.get("discord_reference"):
        discord_html = f"""<div class='contact-item'>
            <img src='{discord_icon_url}' alt='discord' />
            <span>{row["discord_reference"]}</span>
        </div>"""

    if row.get("email_enabled") and row.get("email"):
        email_html = f"""<div class='contact-item contact-email'>
            <img src='{email_icon_url}' alt='email' />
            <a href='mailto:{row["email"]}'>Email</a>
        </div>"""

    return f"""{contact_info_styles}<div class='contact-card'>
        {discord_html}
        {email_html}
    </div>"""
