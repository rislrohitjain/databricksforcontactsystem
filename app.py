import streamlit as st
from config import settings
from ui.styles import inject_dark_theme
from ui.components import render_header, render_sidebar, render_footer
from ui.views import (
    render_overview_tab,
    render_directory_tab,
    render_databricks_tab,
    render_agent_tab,
    render_admin_tab
)
from database.postgres_client import postgres_client
from data.seeder import seed_database

st.set_page_config(
    page_title=f"{settings.APP_NAME} | Rohit Jain",
    page_icon="🌩️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Inject Dark Theme CSS
    inject_dark_theme()

    # Render Header & Sidebar
    render_header()
    render_sidebar()

    # Auto-seed sample dataset if database is empty on first startup
    existing_contacts = postgres_client.get_contacts(limit=1)
    if existing_contacts.empty:
        seed_database(250)

    # Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Overview",
        "📇 Contact Directory",
        "🌩️ Databricks Lakehouse SQL",
        "🤖 Multi-Role Agent AI",
        "⚙️ Diagnostics & Seeder"
    ])

    with tab1:
        render_overview_tab()

    with tab2:
        render_directory_tab()

    with tab3:
        render_databricks_tab()

    with tab4:
        render_agent_tab()

    with tab5:
        render_admin_tab()

    # Render Footer
    render_footer()

if __name__ == "__main__":
    main()
