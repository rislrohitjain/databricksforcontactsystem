import streamlit as st

def inject_dark_theme():
    st.markdown("""
    <style>
    /* Dark Theme Core Overlay */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Metric Cards Styling */
    .metric-card {
        background: linear-gradient(135deg, #1f242d 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.8rem;
        color: #58a6ff;
        font-weight: 700;
    }
    .metric-subtitle {
        font-size: 0.8rem;
        color: #3fb950;
        margin-top: 4px;
    }

    /* Developer Attribution Banner */
    .dev-badge {
        background-color: #21262d;
        border: 1px solid #388bfd;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .dev-badge a {
        color: #58a6ff;
        font-weight: 600;
        text-decoration: none;
    }
    .dev-badge a:hover {
        text-decoration: underline;
    }

    /* Table & Container Fixes */
    .stDataFrame {
        border: 1px solid #30363d;
        border-radius: 6px;
    }

    /* Footer Styling */
    .app-footer {
        border-top: 1px solid #30363d;
        padding-top: 16px;
        margin-top: 40px;
        text-align: center;
        color: #8b949e;
        font-size: 0.85rem;
    }
    .app-footer a {
        color: #58a6ff;
        text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)
