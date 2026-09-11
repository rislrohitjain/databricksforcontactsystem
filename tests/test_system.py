import unittest
import pandas as pd
from config import settings
from database.postgres_client import postgres_client
from database.databricks_client import databricks_client
from data.seeder import seed_database
from agent.tools import AVAILABLE_TOOLS
from agent.agent_team import agent_team

class TestDatabricksContactSystem(unittest.TestCase):

    def test_01_config_loading(self):
        self.assertEqual(settings.APP_NAME, "DatabricksContactSystem")
        self.assertEqual(settings.POSTGRES_DB, "databricksforcontactsystem")
        self.assertEqual(settings.DEV_NAME, "Rohit Jain")
        self.assertTrue("https://rohitjain-resume.vercel.app/" in settings.DEV_URL)

    def test_02_data_seeding(self):
        res = seed_database(50)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["count"], 50)
        
        df = postgres_client.get_contacts(limit=100)
        self.assertFalse(df.empty)
        self.assertIn("email", df.columns)
        self.assertIn("engagement_score", df.columns)

    def test_03_databricks_client(self):
        stats = databricks_client.get_lakehouse_stats()
        self.assertIn("catalog", stats)
        
        query_df = databricks_client.execute_query("SELECT 1")
        self.assertIsInstance(query_df, pd.DataFrame)

    def test_04_agent_tools(self):
        search_tool = AVAILABLE_TOOLS["search_contacts"]
        res_df = search_tool.run(limit=10)
        self.assertIsInstance(res_df, pd.DataFrame)

        lead_tool = AVAILABLE_TOOLS["score_leads"]
        high_val_df = lead_tool.run(min_score=50.0)
        self.assertIsInstance(high_val_df, pd.DataFrame)

    def test_05_agent_team_sprint(self):
        team_members = agent_team.get_team_members()
        self.assertEqual(len(team_members), 6)
        
        ba_res = agent_team.execute_role_task("ba", "Analyze enterprise contacts")
        self.assertIn("output", ba_res)
        
        sprint_res = agent_team.execute_team_sprint("Build enterprise contacts analytics pipeline")
        self.assertEqual(len(sprint_res), 6)

if __name__ == "__main__":
    unittest.main()
