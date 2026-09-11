# Databricks Contact Intelligence System (`databricksforcontactsystem`)

An enterprise-grade Python application integrating local **PostgreSQL 18** with **Databricks SQL Lakehouse**, featuring high-density contact records, a pure Python dark-themed analytics dashboard, and an extensible agentic AI layer.

---

## Developer Attribution
- **Lead Engineer & AI Automation Architect:** Rohit Jain
- **Live Portfolio:** [https://rohitjain-resume.vercel.app/](https://rohitjain-resume.vercel.app/)

---

## Key Features
- **Dual Database Architecture**: Local relational database (**PostgreSQL 18**) and cloud analytics warehouse (**Databricks SQL Lakehouse**) with automatic offline/mock fallbacks.
- **High-Density Contact Engine**: Synthetic generation & streaming of high-density global B2B contact datasets.
- **Pure Python Dark Theme Analytics Dashboard**: Interactive Streamlit dashboard with zero client-side external JS dependencies.
- **Extensible Agentic AI Layer**: Decoupled agent engine with query parsing, lead scoring, metrics aggregation tools, and execution tracing.
- **Enterprise Configuration**: Structured configuration using `pydantic-settings` and `.env` environment variables.

---

## Quickstart

```bash
# 1. Clone & install dependencies
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env

# 3. Launch Streamlit Application
streamlit run app.py
```
