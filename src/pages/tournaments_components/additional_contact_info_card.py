import pandas as pd

# CSS Styles for Contact Info Card
additional_contact_info_styles = """
<style>
.additional-contact-card {
    flex: 2;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 1rem;
    padding-left: 1rem;
}
.additional-contact-item {
    display: flex;
    align-items: center;
    margin-bottom: 0.1rem;
}
.additional-contact-label {
    width: 160px;
    display: flex;
    align-items: center;
    font-weight: bold;
}
.additional-contact-label img {
    height: 20px;
    margin-right: 8px;
}
.additional-contact-value {
    flex: 1;
}
</style>
"""


def get_additional_contact_info_card(row: pd.Series):
    if pd.isna(row["role"]) or row["role"] == 'Undefined':
        return """<div class='additional-contact-card'>
            <div class='additional-contact-item'>No contact info</div>
        </div>"""

    alt_accounts_html = "<div />"
    scholar_accounts_html = "<div />"

    if isinstance(row.get("alt_accounts"), list) and row["alt_accounts"]:
        alt_items = "".join(f"<li>{acc}</li>" for acc in row["alt_accounts"])
        alt_accounts_html = f"""<div class='additional-contact-item'>
            <div class='additional-contact-label'>👥 Alt Accounts</div>
            <div class='additional-contact-value'><ul style="padding-left: 20px; margin: 0;">{alt_items}</ul></div>
        </div>"""

    if isinstance(row.get("scholar_accounts"), list) and row["scholar_accounts"]:
        scholar_items = "".join(f"<li>{acc}</li>" for acc in row["scholar_accounts"])
        scholar_accounts_html = f"""<div class='additional-contact-item'>
            <div class='additional-contact-label'>🎮 Scholar Accounts</div>
            <div class='additional-contact-value'><ul style="padding-left: 20px; margin: 0;">{scholar_items}</ul></div>
        </div>"""

    return f"""<div class='additional-contact-card'>
        {alt_accounts_html}
        {scholar_accounts_html}
    </div>"""
