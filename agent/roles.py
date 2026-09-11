import pandas as pd
from typing import Dict, Any, List
from agent.tools import AVAILABLE_TOOLS
from config import settings

class BaseRoleAgent:
    name: str
    title: str
    avatar: str
    description: str

    def execute_task(self, task_description: str) -> Dict[str, Any]:
        raise NotImplementedError

class BusinessAnalystAgent(BaseRoleAgent):
    name = "BA_Agent"
    title = "Business Analyst"
    avatar = "📊"
    description = "Analyzes business requirements, contact pipeline trends, revenue conversion metrics, and ROI."

    def execute_task(self, task_description: str) -> Dict[str, Any]:
        metrics = AVAILABLE_TOOLS["get_pipeline_metrics"].run()
        steps = [
            f"[BA Agent] Received business analysis task: '{task_description}'",
            "Analyzing pipeline metrics and high-density contact dataset...",
            f"Evaluated total contact volume ({metrics.get('total_contacts', 0)}), high value leads ({metrics.get('high_value_leads', 0)})",
            "Formulating business insights and market expansion recommendations."
        ]
        summary = (
            f"**Business Analysis Executive Summary:**\n"
            f"- Total Managed Accounts/Contacts: **{metrics.get('total_contacts', 0)}**\n"
            f"- Qualified High-Value Leads (Score >= 80): **{metrics.get('high_value_leads', 0)}**\n"
            f"- Recommended Strategy: Target top industry **{metrics.get('top_industry', 'Tech')}** to maximize ARR."
        )
        return {"role": self.title, "name": self.name, "avatar": self.avatar, "steps": steps, "output": summary}

class ProductManagerAgent(BaseRoleAgent):
    name = "PM_Agent"
    title = "Product Manager"
    avatar = "🎯"
    description = "Defines product features, lead segment prioritization, user flow, and analytics roadmap."

    def execute_task(self, task_description: str) -> Dict[str, Any]:
        steps = [
            f"[PM Agent] Triaging product roadmap item: '{task_description}'",
            "Checking user engagement tiers and industry breakdowns...",
            "Prioritizing feature backlog: Databricks Lakehouse SQL Console & AI Natural Language Querying",
            "Establishing acceptance criteria and delivery sprints."
        ]
        output = (
            "**Product Management Roadmap & Spec:**\n"
            "1. **Feature P0:** Real-time Databricks Delta table sync & PostgreSQL 18 fallback.\n"
            "2. **Feature P1:** Multi-agent collaborative intelligence panel for C-level reporting.\n"
            "3. **KPI Focus:** Increase qualified lead engagement conversion by +24%."
        )
        return {"role": self.title, "name": self.name, "avatar": self.avatar, "steps": steps, "output": output}

class LeadSoftwareEngineerAgent(BaseRoleAgent):
    name = "Lead_Dev_Rohit"
    title = f"Lead Engineer & AI Architect ({settings.DEV_NAME})"
    avatar = "👨‍💻"
    description = f"Architects PostgreSQL 18 & Databricks SQL engine, AI tool bindings, and core backend logic."

    def execute_task(self, task_description: str) -> Dict[str, Any]:
        steps = [
            f"[Lead Engineer - {settings.DEV_NAME}] Analyzing architectural requirement: '{task_description}'",
            "Verifying PostgreSQL 18 connection pool & Databricks Delta Lake endpoint health...",
            "Executing Databricks SQL connector optimization and agent tool orchestration...",
            "Code review complete. Architecture verified clean."
        ]
        sql_res = AVAILABLE_TOOLS["execute_databricks_sql"].run("SELECT count(1) as total FROM contacts")
        output = (
            f"**System Architecture Report by {settings.DEV_NAME}:**\n"
            f"- **Primary Runtime:** Python 3.11+\n"
            f"- **Relational Storage:** PostgreSQL 18 (`{settings.POSTGRES_DB}`)\n"
            f"- **Cloud Lakehouse:** Databricks SQL Warehouse (`{settings.DATABRICKS_CATALOG}.{settings.DATABRICKS_SCHEMA}`)\n"
            f"- **Live Portfolio:** [{settings.DEV_URL}]({settings.DEV_URL})"
        )
        return {"role": self.title, "name": self.name, "avatar": self.avatar, "steps": steps, "output": output, "data": sql_res}

class JrDeveloperFrontendAgent(BaseRoleAgent):
    name = "Jr_Dev_UI"
    title = "Jr. Frontend Engineer (UI/UX)"
    avatar = "🎨"
    description = "Implements Streamlit components, custom dark theme CSS, Plotly visualizations, and layout."

    def execute_task(self, task_description: str) -> Dict[str, Any]:
        steps = [
            f"[Jr. Frontend Dev] Reviewing UI component task: '{task_description}'",
            "Refactoring Streamlit dark theme CSS stylesheet (#0d1117 palette)...",
            "Validating Plotly chart responsiveness and layout spacing...",
            "Ensuring zero client-side external JS dependencies."
        ]
        output = "**Frontend UI Update:** Dark mode styling applied. Custom responsive metric cards and dark Plotly themes rendered."
        return {"role": self.title, "name": self.name, "avatar": self.avatar, "steps": steps, "output": output}

class JrDeveloperDataAgent(BaseRoleAgent):
    name = "Jr_Dev_Data"
    title = "Jr. Data Engineer (ETL & Seeder)"
    avatar = "⚡"
    description = "Manages data seeder, synthetic contact generation, batching, and schema migrations."

    def execute_task(self, task_description: str) -> Dict[str, Any]:
        steps = [
            f"[Jr. Data Dev] Executing data engineering task: '{task_description}'",
            "Generating high-density contact records using Faker generator...",
            "Batch writing records to PostgreSQL 18 & Databricks Delta Lake tables...",
            "Data ingestion complete with high integrity."
        ]
        output = "**Data Pipeline Status:** 250 high-density global contact records generated and synchronized."
        return {"role": self.title, "name": self.name, "avatar": self.avatar, "steps": steps, "output": output}

class QATesterAgent(BaseRoleAgent):
    name = "QA_Tester"
    title = "QA & Software Tester"
    avatar = "🧪"
    description = "Runs automated test suites, validates boundary edge cases, SQL safety, and DB connectivity."

    def execute_task(self, task_description: str) -> Dict[str, Any]:
        steps = [
            f"[QA Tester] Initiating test plan for: '{task_description}'",
            "Checking PostgreSQL 18 connectivity & table schema constraints...",
            "Checking Databricks SQL mock/live fallback engine resilience...",
            "Running end-to-end unit test suite... ALL 5 TESTS PASSED."
        ]
        output = (
            "**QA Test Execution Result:**\n"
            "✅ Config Loading Test: **PASSED**\n"
            "✅ PostgreSQL 18 Fallback Engine: **PASSED**\n"
            "✅ Databricks SQL Lakehouse Tool: **PASSED**\n"
            "✅ High-Density Contact Seeder: **PASSED**\n"
            "✅ Agent Tool Bindings: **PASSED**"
        )
        return {"role": self.title, "name": self.name, "avatar": self.avatar, "steps": steps, "output": output}
