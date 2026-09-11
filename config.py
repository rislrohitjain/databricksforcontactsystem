import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

from urllib.parse import quote_plus

class Settings(BaseSettings):
    APP_NAME: str = "DatabricksContactSystem"
    HOST: str = "0.0.0.0"
    PORT: int = 8501

    # PostgreSQL 18
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "Admin@123"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "databricksforcontactsystem"

    # Databricks Lakehouse
    DATABRICKS_SERVER_HOSTNAME: str = "dbc-e68b8705-9d03.cloud.databricks.com"
    DATABRICKS_HTTP_PATH: str = "/sql/1.0/endpoints/YOUR_WAREHOUSE_HTTP_PATH"
    DATABRICKS_ACCESS_TOKEN: str = "YOUR_DATABRICKS_ACCESS_TOKEN"
    DATABRICKS_CATALOG: str = "workspace"
    DATABRICKS_SCHEMA: str = "default"

    # Developer Profile
    DEV_NAME: str = "Rohit Jain"
    DEV_ROLE: str = "Sr. Software Engineer & AI Automation Architect"
    DEV_URL: str = "https://rohitjain-resume.vercel.app/"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def postgres_dsn(self) -> str:
        pwd_quoted = quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql://{self.POSTGRES_USER}:{pwd_quoted}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
