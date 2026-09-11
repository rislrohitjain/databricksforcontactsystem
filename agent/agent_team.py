import logging
from typing import Dict, Any, List
from agent.roles import (
    BusinessAnalystAgent,
    ProductManagerAgent,
    LeadSoftwareEngineerAgent,
    JrDeveloperFrontendAgent,
    JrDeveloperDataAgent,
    QATesterAgent
)

logger = logging.getLogger(__name__)

class AgentTeamOrchestrator:
    """Orchestrates collaborative workflows across specialized team agent roles."""

    def __init__(self):
        self.team = {
            "ba": BusinessAnalystAgent(),
            "pm": ProductManagerAgent(),
            "lead_dev": LeadSoftwareEngineerAgent(),
            "jr_dev_ui": JrDeveloperFrontendAgent(),
            "jr_dev_data": JrDeveloperDataAgent(),
            "qa_tester": QATesterAgent()
        }

    def get_team_members(self) -> List[Dict[str, str]]:
        return [
            {"key": k, "name": agent.name, "title": agent.title, "avatar": agent.avatar, "description": agent.description}
            for k, agent in self.team.items()
        ]

    def execute_role_task(self, role_key: str, task: str) -> Dict[str, Any]:
        if role_key in self.team:
            return self.team[role_key].execute_task(task)
        else:
            return {"error": f"Role '{role_key}' not found in agent team."}

    def execute_team_sprint(self, user_goal: str) -> List[Dict[str, Any]]:
        """Executes a full cross-functional agent team sprint on a user goal."""
        results = []
        results.append(self.team["ba"].execute_task(f"Extract business requirements for goal: {user_goal}"))
        results.append(self.team["pm"].execute_task(f"Define product specs for goal: {user_goal}"))
        results.append(self.team["lead_dev"].execute_task(f"Architect database and query strategy for: {user_goal}"))
        results.append(self.team["jr_dev_data"].execute_task(f"Generate & seed required contact dataset for: {user_goal}"))
        results.append(self.team["jr_dev_ui"].execute_task(f"Build analytics dashboard visualization for: {user_goal}"))
        results.append(self.team["qa_tester"].execute_task(f"Validate end-to-end functionality & quality for: {user_goal}"))
        return results

agent_team = AgentTeamOrchestrator()
