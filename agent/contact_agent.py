import json
import logging
import pandas as pd
from typing import Dict, Any, List
from agent.tools import AVAILABLE_TOOLS

logger = logging.getLogger(__name__)

class ContactAgent:
    """Agent orchestrator for Contact Intelligence System."""

    def __init__(self):
        self.tools = AVAILABLE_TOOLS

    def run(self, user_prompt: str) -> Dict[str, Any]:
        """
        Parses intent from user prompt, selects appropriate tool,
        executes tool call, and constructs step-by-step reasoning output.
        """
        user_prompt_lower = user_prompt.lower()
        reasoning_steps = [
            f"Received user query: '{user_prompt}'",
            "Analyzing prompt intent and selecting execution tool..."
        ]
        
        result_data = None
        tool_used = "N/A"

        if "databricks" in user_prompt_lower or "sql" in user_prompt_lower or "delta" in user_prompt_lower:
            tool_used = "execute_databricks_sql"
            reasoning_steps.append(f"Intent classified: Databricks SQL analytics. Calling '{tool_used}' tool.")
            sql = "SELECT industry, count(1) as total_contacts, avg(engagement_score) as avg_score FROM contacts GROUP BY industry ORDER BY total_contacts DESC"
            reasoning_steps.append(f"Executing generated SQL: {sql}")
            result_data = self.tools[tool_used].run(sql_query=sql)

        elif "high value" in user_prompt_lower or "score" in user_prompt_lower or "lead" in user_prompt_lower:
            tool_used = "score_leads"
            reasoning_steps.append(f"Intent classified: High-Value Lead Scoring. Calling '{tool_used}' tool with min_score=80.0.")
            result_data = self.tools[tool_used].run(min_score=80.0)

        elif "metric" in user_prompt_lower or "pipeline" in user_prompt_lower or "summary" in user_prompt_lower or "overview" in user_prompt_lower:
            tool_used = "get_pipeline_metrics"
            reasoning_steps.append(f"Intent classified: Aggregated Metrics requested. Calling '{tool_used}' tool.")
            metrics = self.tools[tool_used].run()
            reasoning_steps.append(f"Metrics retrieved: Total Contacts={metrics['total_contacts']}, High Value={metrics['high_value_leads']}")
            result_data = pd.DataFrame([metrics])

        else:
            tool_used = "search_contacts"
            reasoning_steps.append(f"Intent classified: General Contact Search. Calling '{tool_used}' tool.")
            result_data = self.tools[tool_used].run(query=user_prompt)

        reasoning_steps.append("Tool execution completed successfully. Formatting output response.")

        return {
            "prompt": user_prompt,
            "tool_used": tool_used,
            "reasoning_steps": reasoning_steps,
            "data": result_data
        }

contact_agent = ContactAgent()
