import logging
import pandas as pd
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, text, Column, Integer, String, Float, DateTime, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

class ContactModel(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(150), index=True)
    phone = Column(String(50))
    company = Column(String(150), index=True)
    title = Column(String(100))
    industry = Column(String(100), index=True)
    country = Column(String(100), index=True)
    region = Column(String(50), index=True)
    revenue_tier = Column(String(50), index=True)
    engagement_score = Column(Float)
    lead_status = Column(String(50), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PostgresClient:
    def __init__(self):
        self.dsn = settings.postgres_dsn
        self.engine = None
        self._connected = False
        self._mock_data: List[Dict[str, Any]] = []
        self._try_connect()

    def _try_connect(self):
        try:
            # First try direct connection
            self.engine = create_engine(self.dsn, connect_args={"connect_timeout": 3})
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self._connected = True
            Base.metadata.create_all(self.engine)
            logger.info("Successfully connected to PostgreSQL 18 database.")
        except Exception as e:
            # Try connecting to default 'postgres' db to create target database
            try:
                from urllib.parse import quote_plus
                default_dsn = f"postgresql://{settings.POSTGRES_USER}:{quote_plus(settings.POSTGRES_PASSWORD)}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/postgres"
                admin_engine = create_engine(default_dsn, isolation_level="AUTOCOMMIT", connect_args={"connect_timeout": 3})
                with admin_engine.connect() as conn:
                    conn.execute(text(f"CREATE DATABASE {settings.POSTGRES_DB}"))
                # Re-try main connection
                self.engine = create_engine(self.dsn, connect_args={"connect_timeout": 3})
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                self._connected = True
                Base.metadata.create_all(self.engine)
                logger.info(f"Created and connected to PostgreSQL database '{settings.POSTGRES_DB}'.")
            except Exception as inner_e:
                logger.warning(f"PostgreSQL connection offline or fallback active ({e}). Using in-memory engine.")
                self._connected = False

    def is_connected(self) -> bool:
        try:
            if self.engine:
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                return True
        except Exception:
            pass
        return False

    def init_db(self):
        if self.is_connected():
            Base.metadata.create_all(self.engine)

    def insert_contacts(self, contacts: List[Dict[str, Any]]) -> bool:
        if self.is_connected():
            try:
                df = pd.DataFrame(contacts)
                df.to_sql("contacts", self.engine, if_exists="append", index=False)
                return True
            except Exception as e:
                logger.error(f"Error inserting contacts to PostgreSQL: {e}")
                self._mock_data.extend(contacts)
                return False
        else:
            self._mock_data.extend(contacts)
            return True

    def get_contacts(self, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        if self.is_connected():
            try:
                query = "SELECT * FROM contacts"
                conditions = []
                params = {}
                if filters:
                    if "industry" in filters and filters["industry"]:
                        conditions.append("industry = :industry")
                        params["industry"] = filters["industry"]
                    if "region" in filters and filters["region"]:
                        conditions.append("region = :region")
                        params["region"] = filters["region"]
                    if "lead_status" in filters and filters["lead_status"]:
                        conditions.append("lead_status = :lead_status")
                        params["lead_status"] = filters["lead_status"]
                    if "search" in filters and filters["search"]:
                        conditions.append("(first_name ILIKE :search OR last_name ILIKE :search OR email ILIKE :search OR company ILIKE :search)")
                        params["search"] = f"%{filters['search']}%"

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                query += f" ORDER BY engagement_score DESC LIMIT {limit}"

                with self.engine.connect() as conn:
                    return pd.read_sql(text(query), conn, params=params)
            except Exception as e:
                logger.error(f"Failed to query PostgreSQL: {e}")

        # Fallback to mock data
        if not self._mock_data:
            return pd.DataFrame()

        df = pd.DataFrame(self._mock_data)
        if filters:
            if filters.get("industry"):
                df = df[df["industry"] == filters["industry"]]
            if filters.get("region"):
                df = df[df["region"] == filters["region"]]
            if filters.get("lead_status"):
                df = df[df["lead_status"] == filters["lead_status"]]
            if filters.get("search"):
                s = filters["search"].lower()
                df = df[
                    df["first_name"].astype(str).str.lower().str.contains(s) |
                    df["last_name"].astype(str).str.lower().str.contains(s) |
                    df["email"].astype(str).str.lower().str.contains(s) |
                    df["company"].astype(str).str.lower().str.contains(s)
                ]
        if "engagement_score" in df.columns:
            df = df.sort_values(by="engagement_score", ascending=False)
        return df.head(limit)

    def get_metrics(self) -> Dict[str, Any]:
        df = self.get_contacts(limit=10000)
        if df.empty:
            return {
                "total_contacts": 0,
                "avg_engagement": 0.0,
                "high_value_leads": 0,
                "top_industry": "N/A",
                "status_breakdown": {},
                "region_breakdown": {}
            }
        
        high_val = len(df[df["engagement_score"] >= 80]) if "engagement_score" in df.columns else 0
        top_ind = df["industry"].mode()[0] if "industry" in df.columns and not df["industry"].empty else "N/A"
        status_bk = df["lead_status"].value_counts().to_dict() if "lead_status" in df.columns else {}
        region_bk = df["region"].value_counts().to_dict() if "region" in df.columns else {}

        return {
            "total_contacts": len(df),
            "avg_engagement": float(df["engagement_score"].mean()) if "engagement_score" in df.columns else 0.0,
            "high_value_leads": high_val,
            "top_industry": top_ind,
            "status_breakdown": status_bk,
            "region_breakdown": region_bk
        }

postgres_client = PostgresClient()
