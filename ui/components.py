import streamlit as st
from config import settings

def render_header():
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #161b22 0%, #0d1117 100%); padding: 20px; border-radius: 8px; border: 1px solid #30363d; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <h1 style="color: #58a6ff; margin: 0; font-size: 2.2rem; font-weight: 700;">
                    🌩️ Databricks Contact Intelligence System
                </h1>
                <p style="color: #8b949e; margin-top: 6px; font-size: 1.05rem;">
                    Enterprise Lakehouse Analytics • PostgreSQL 18 Relational Engine • Multi-Role Agentic AI
                </p>
            </div>
            <div style="text-align: right; background: #21262d; padding: 12px 18px; border-radius: 6px; border: 1px solid #388bfd;">
                <div style="color: #c9d1d9; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;">Lead Software Engineer</div>
                <div style="color: #58a6ff; font-weight: 700; font-size: 1.1rem;">{settings.DEV_NAME}</div>
                <div style="color: #8b949e; font-size: 0.8rem; margin-bottom: 4px;">{settings.DEV_ROLE}</div>
                <a href="{settings.DEV_URL}" target="_blank" style="color: #3fb950; font-size: 0.85rem; font-weight: 600; text-decoration: none;">
                    🌐 View Live Portfolio ↗
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px 0; border-bottom: 1px solid #30363d; margin-bottom: 16px;">
            <h3 style="color: #58a6ff; margin: 0;">⚡ Navigation & Control</h3>
            <p style="color: #8b949e; font-size: 0.8rem; margin-top: 4px;">PostgreSQL 18 + Databricks</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background-color: #21262d; border: 1px solid #30363d; border-radius: 6px; padding: 12px; margin-bottom: 20px;">
            <div style="color: #8b949e; font-size: 0.75rem; text-transform: uppercase;">Lead Engineer</div>
            <div style="color: #58a6ff; font-weight: 700; font-size: 0.95rem;">{settings.DEV_NAME}</div>
            <div style="color: #c9d1d9; font-size: 0.8rem; margin-bottom: 6px;">{settings.DEV_ROLE}</div>
            <a href="{settings.DEV_URL}" target="_blank" style="color: #3fb950; font-size: 0.8rem; font-weight: 600; text-decoration: none;">
                🔗 rohitjain-resume.vercel.app
            </a>
        </div>
        """, unsafe_allow_html=True)

def render_footer():
    st.markdown(f"""
    <div class="app-footer">
        <p>
            <strong>Databricks Contact Intelligence System</strong> | Designed & Developed by 
            <a href="{settings.DEV_URL}" target="_blank" style="color: #58a6ff; font-weight: 600;">{settings.DEV_NAME}</a> ({settings.DEV_ROLE})
            <br/>
            Portfolio: <a href="{settings.DEV_URL}" target="_blank">{settings.DEV_URL}</a> | Powered by Python 3.11+, Streamlit, PostgreSQL 18 & Databricks Delta Lake
        </p>
    </div>
    """, unsafe_allow_html=True)
