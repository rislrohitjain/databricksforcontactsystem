import pandas as pd
from typing import Dict, Any, List, Optional
from database.postgres_client import postgres_client
from database.databricks_client import databricks_client

class BaseAgentTool:
    name: str
    description: str

    def run(self, **kwargs) -> Any:
        raise NotImplementedError

class SearchContactsTool(BaseAgentTool):
    name = "search_contacts"
    description = "Search contact records in PostgreSQL/Databricks by query, industry, region, or lead status."

    def run(self, query: str = "", industry: str = "", region: str = "", status: str = "", limit: int = 50) -> pd.DataFrame:
        filters = {
            "search": query,
            "industry": industry,
            "region": region,
            "lead_status": status
        }
        return postgres_client.get_contacts(limit=limit, filters=filters)

class DatabricksQueryTool(BaseAgentTool):
    name = "execute_databricks_sql"
    description = "Execute analytical SQL queries directly on Databricks Delta Lakehouse."

    def run(self, sql_query: str) -> pd.DataFrame:
        return databricks_client.execute_query(sql_query)

class LeadScoringTool(BaseAgentTool):
    name = "score_leads"
    description = "Evaluate and rank enterprise contacts based on engagement score and revenue tier."

    def run(self, min_score: float = 75.0, min_tier: Optional[str] = None) -> pd.DataFrame:
        df = postgres_client.get_contacts(limit=1000)
        if df.empty:
            return pd.DataFrame()
        
        filtered = df[df["engagement_score"] >= min_score]
        if min_tier and "revenue_tier" in filtered.columns:
            filtered = filtered[filtered["revenue_tier"] == min_tier]
            
        return filtered.sort_values(by="engagement_score", ascending=False)

class PipelineMetricsTool(BaseAgentTool):
    name = "get_pipeline_metrics"
    description = "Aggregate enterprise contact pipeline stats across regions and lead qualification stages."

    def run(self) -> Dict[str, Any]:
        return postgres_client.get_metrics()

AVAILABLE_TOOLS = {
    "search_contacts": SearchContactsTool(),
    "execute_databricks_sql": DatabricksQueryTool(),
    "score_leads": LeadScoringTool(),
    "get_pipeline_metrics": PipelineMetricsTool()
}
