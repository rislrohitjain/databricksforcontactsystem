import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.postgres_client import postgres_client
from database.databricks_client import databricks_client
from data.seeder import seed_database
from agent.contact_agent import contact_agent
from agent.agent_team import agent_team
from config import settings

def render_overview_tab():
    st.subheader("📊 Executive Contact Analytics & Infrastructure Overview")

    # Prominent Connection Details Banner on Root Page
    pg_conn = postgres_client.is_connected()
    db_conn = databricks_client.is_connected()
    db_stats = databricks_client.get_lakehouse_stats()

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #161b22 0%, #1f242d 100%); border: 1px solid #30363d; border-radius: 8px; padding: 18px; margin-bottom: 20px;">
        <div style="font-weight: 700; color: #58a6ff; font-size: 1.1rem; margin-bottom: 10px;">
            🔌 Connected Databases & Live Infrastructure Status
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px;">
            <div style="background: #0d1117; padding: 12px; border-radius: 6px; border-left: 4px solid #3fb950;">
                <div style="color: #8b949e; font-size: 0.75rem; text-transform: uppercase;">Local Relational Engine</div>
                <div style="color: #c9d1d9; font-weight: 700; font-size: 0.95rem;">🐘 PostgreSQL 18</div>
                <div style="color: #8b949e; font-size: 0.8rem;">Host: <code>{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}</code></div>
                <div style="color: #8b949e; font-size: 0.8rem;">Database: <code>{settings.POSTGRES_DB}</code> (User: <code>{settings.POSTGRES_USER}</code>)</div>
                <div style="color: #3fb950; font-size: 0.8rem; font-weight: 600; margin-top: 4px;">
                    ● Status: {'CONNECTED & LIVE' if pg_conn else 'ONLINE (In-Memory Fallback Active)'}
                </div>
            </div>
            <div style="background: #0d1117; padding: 12px; border-radius: 6px; border-left: 4px solid #58a6ff;">
                <div style="color: #8b949e; font-size: 0.75rem; text-transform: uppercase;">Cloud Warehouse Engine</div>
                <div style="color: #c9d1d9; font-weight: 700; font-size: 0.95rem;">🌩️ Databricks SQL Lakehouse</div>
                <div style="color: #8b949e; font-size: 0.8rem;">Host: <code>{settings.DATABRICKS_SERVER_HOSTNAME}</code></div>
                <div style="color: #8b949e; font-size: 0.8rem;">Catalog/Schema: <code>{settings.DATABRICKS_CATALOG}.{settings.DATABRICKS_SCHEMA}</code></div>
                <div style="color: #58a6ff; font-size: 0.8rem; font-weight: 600; margin-top: 4px;">
                    ● Status: {db_stats['status']}
                </div>
            </div>
            <div style="background: #0d1117; padding: 12px; border-radius: 6px; border-left: 4px solid #a371f7;">
                <div style="color: #8b949e; font-size: 0.75rem; text-transform: uppercase;">Lead Engineer Attribution</div>
                <div style="color: #c9d1d9; font-weight: 700; font-size: 0.95rem;">👨‍💻 {settings.DEV_NAME}</div>
                <div style="color: #8b949e; font-size: 0.8rem;">Role: {settings.DEV_ROLE}</div>
                <div style="margin-top: 6px;">
                    <a href="{settings.DEV_URL}" target="_blank" style="color: #3fb950; font-weight: 600; font-size: 0.8rem; text-decoration: none;">
                        🌐 Live Portfolio: rohitjain-resume.vercel.app ↗
                    </a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    metrics = postgres_client.get_metrics()
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Contacts</div>
            <div class="metric-value">{metrics.get('total_contacts', 0):,}</div>
            <div class="metric-subtitle">PostgreSQL 18 + Databricks Sync</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">High-Value Leads</div>
            <div class="metric-value">{metrics.get('high_value_leads', 0):,}</div>
            <div class="metric-subtitle">Engagement Score ≥ 80.0</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Engagement</div>
            <div class="metric-value">{metrics.get('avg_engagement', 0.0):.1f} / 100</div>
            <div class="metric-subtitle">High Interaction Index</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Top Domain Sector</div>
            <div class="metric-value" style="font-size: 1.2rem;">{metrics.get('top_industry', 'Tech')}</div>
            <div class="metric-subtitle">Highest Account Density</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    df = postgres_client.get_contacts(limit=1000)

    if not df.empty:
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("#### 🏢 Contact Distribution by Industry")
            ind_counts = df["industry"].value_counts().reset_index()
            ind_counts.columns = ["Industry", "Contacts"]
            fig_ind = px.bar(
                ind_counts, x="Contacts", y="Industry", orientation="h",
                color="Contacts", color_continuous_scale="Blues",
                template="plotly_dark"
            )
            fig_ind.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_ind, use_container_width=True)

        with col_right:
            st.markdown("#### 🌍 Global Region Breakdown")
            reg_counts = df["region"].value_counts().reset_index()
            reg_counts.columns = ["Region", "Count"]
            fig_reg = px.pie(
                reg_counts, values="Count", names="Region",
                color_discrete_sequence=px.colors.sequential.Darkmint,
                hole=0.4, template="plotly_dark"
            )
            fig_reg.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_reg, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🎯 Lead Status Qualification Funnel")
            status_df = df["lead_status"].value_counts().reset_index()
            status_df.columns = ["Status", "Count"]
            fig_status = px.bar(
                status_df, x="Status", y="Count", color="Status",
                template="plotly_dark"
            )
            fig_status.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_status, use_container_width=True)

        with col_b:
            st.markdown("#### 💰 Enterprise Revenue Tier Distribution")
            rev_df = df["revenue_tier"].value_counts().reset_index()
            rev_df.columns = ["Revenue Tier", "Count"]
            fig_rev = px.funnel(
                rev_df, x="Count", y="Revenue Tier",
                template="plotly_dark"
            )
            fig_rev.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_rev, use_container_width=True)
    else:
        st.info("No contact data available yet. Use the 'Data Seeder' tab to generate high-density contact records.")

def render_directory_tab():
    st.subheader("📇 High-Density Global Contact Directory")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        search_txt = st.text_input("🔍 Search Name/Email/Company", "")
    with c2:
        ind_filter = st.selectbox("Industry Filter", ["All"] + list(postgres_client.get_contacts(limit=1000)["industry"].unique() if not postgres_client.get_contacts(limit=1000).empty else []))
    with c3:
        reg_filter = st.selectbox("Region Filter", ["All"] + list(postgres_client.get_contacts(limit=1000)["region"].unique() if not postgres_client.get_contacts(limit=1000).empty else []))
    with c4:
        status_filter = st.selectbox("Status Filter", ["All"] + list(postgres_client.get_contacts(limit=1000)["lead_status"].unique() if not postgres_client.get_contacts(limit=1000).empty else []))

    filters = {
        "search": search_txt,
        "industry": "" if ind_filter == "All" else ind_filter,
        "region": "" if reg_filter == "All" else reg_filter,
        "lead_status": "" if status_filter == "All" else status_filter
    }

    df = postgres_client.get_contacts(limit=500, filters=filters)
    st.markdown(f"**Displaying {len(df)} matching records:**")

    if not df.empty:
        display_cols = ["first_name", "last_name", "email", "company", "title", "industry", "country", "region", "revenue_tier", "engagement_score", "lead_status"]
        valid_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[valid_cols], use_container_width=True, height=450)
    else:
        st.warning("No contact records matched the selected criteria.")

def render_databricks_tab():
    st.subheader("🌩️ Databricks SQL Lakehouse Console")

    stats = databricks_client.get_lakehouse_stats()
    st.markdown(f"""
    <div style="background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 14px; margin-bottom: 16px;">
        <span style="color: #8b949e;">Lakehouse Target:</span> <strong>{stats['catalog']}.{stats['schema']}</strong> &nbsp;|&nbsp; 
        <span style="color: #8b949e;">Status:</span> <span style="color: #3fb950; font-weight: 600;">{stats['status']}</span> &nbsp;|&nbsp; 
        <span style="color: #8b949e;">Format:</span> <strong>{stats['delta_table_format']}</strong>
    </div>
    """, unsafe_allow_html=True)

    default_sql = "SELECT industry, COUNT(1) AS contact_count, ROUND(AVG(engagement_score), 2) AS avg_engagement FROM contacts GROUP BY industry ORDER BY contact_count DESC"
    sql_input = st.text_area("✍️ Databricks Delta SQL Query", default_sql, height=120)

    if st.button("🚀 Run Databricks Query", type="primary"):
        with st.spinner("Executing SQL query on Databricks Delta Lake engine..."):
            res_df = databricks_client.execute_query(sql_input)
            st.success("Query executed successfully.")
            st.dataframe(res_df, use_container_width=True)

def render_agent_tab():
    st.subheader("🤖 Multi-Role Agentic AI Intelligence Console")

    st.markdown("""
    Select a single specialized team member or execute a **Full Agent Team Sprint** to analyze contacts, define product specs, architect queries, run QA tests, and generate executive reports.
    """)

    tabs = st.tabs(["⚡ Single Query Agent", "👥 Multi-Role Agent Team Sprint"])

    with tabs[0]:
        prompt = st.text_input("💬 Enter natural language task for Agent:", "Find top 5 healthcare contacts with engagement score > 80")
        if st.button("Execute Agent Task", type="primary"):
            with st.spinner("Agent evaluating intent and selecting tools..."):
                agent_res = contact_agent.run(prompt)
                st.markdown(f"**Tool Invoked:** `{agent_res['tool_used']}`")
                st.markdown("**Execution Reasoning Steps:**")
                for step in agent_res["reasoning_steps"]:
                    st.markdown(f"- `{step}`")

                if agent_res["data"] is not None and isinstance(agent_res["data"], pd.DataFrame):
                    st.markdown("**Output Dataset:**")
                    st.dataframe(agent_res["data"], use_container_width=True)

    with tabs[1]:
        st.markdown("### 🧑‍💼 Multi-Role Agent Team Members")
        team_members = agent_team.get_team_members()
        cols = st.columns(len(team_members))
        for idx, m in enumerate(team_members):
            with cols[idx]:
                st.markdown(f"### {m['avatar']}\n**{m['title']}**\n\n_{m['description']}_")

        st.markdown("---")
        sprint_goal = st.text_input("🎯 Define Sprint Goal for Agent Team:", "Analyze high-density contact pipeline and deliver enterprise growth roadmap")

        if st.button("🚀 Execute Collaborative Team Sprint", type="primary"):
            with st.spinner("Orchestrating multi-agent sprint execution across BA, PM, Lead Engineer, Jr Devs, and QA..."):
                sprint_output = agent_team.execute_team_sprint(sprint_goal)
                for res in sprint_output:
                    st.markdown(f"### {res['avatar']} {res['role']} (`{res['name']}`)")
                    for s in res["steps"]:
                        st.markdown(f"- `{s}`")
                    st.markdown(res["output"])
                    if "data" in res and res["data"] is not None:
                        st.dataframe(res["data"], use_container_width=True)
                    st.markdown("---")

def render_admin_tab():
    st.subheader("⚙️ Database Diagnostics & High-Density Seeder")

    st.markdown("#### Database Engine Health Checks")
    c1, c2 = st.columns(2)

    with c1:
        pg_status = postgres_client.is_connected()
        st.markdown(f"""
        <div style="background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 16px;">
            <h4>🐘 PostgreSQL 18 Local Database</h4>
            <p>Host: <code>{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}</code></p>
            <p>Database: <code>{settings.POSTGRES_DB}</code></p>
            <p>Status: <strong style="color: {'#3fb950' if pg_status else '#e3b341'};">{'ONLINE' if pg_status else 'STANDBY (Mock Active)'}</strong></p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        db_status = databricks_client.is_connected()
        st.markdown(f"""
        <div style="background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 16px;">
            <h4>🌩️ Cloud Databricks SQL Warehouse</h4>
            <p>Host: <code>{settings.DATABRICKS_SERVER_HOSTNAME}</code></p>
            <p>Catalog: <code>{settings.DATABRICKS_CATALOG}.{settings.DATABRICKS_SCHEMA}</code></p>
            <p>Status: <strong style="color: {'#3fb950' if db_status else '#e3b341'};">{'ONLINE' if db_status else 'STANDBY (Local Delta Mock)'}</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("#### ⚡ Seed High-Density India-Level Contact Dataset")
    seed_count = st.number_input("Number of realistic Indian enterprise contacts to generate:", min_value=100, max_value=20000, value=5000, step=500)

    if st.button("🌱 Generate & Seed 5,000+ Indian Contact Records", type="primary"):
        with st.spinner(f"Generating {seed_count} realistic Indian enterprise contact records..."):
            res = seed_database(seed_count)
            st.success(f"Successfully generated and seeded {res['count']} realistic Indian enterprise contacts to PostgreSQL 18 & Databricks!")

    df = postgres_client.get_contacts(limit=5000)
    if not df.empty:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Full Contact Dataset (CSV)",
            data=csv_data,
            file_name="databricks_contacts_dataset.csv",
            mime="text/csv"
        )
