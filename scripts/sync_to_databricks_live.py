import os
import sys
import time
import pandas as pd
from typing import List

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.postgres_client import postgres_client
from database.databricks_client import databricks_client
from config import settings

def sync_postgres_to_databricks_live(batch_size: int = 1000, max_records: int = 120000):
    print("=" * 70)
    print("🚀 AUTOMATED POSTGRES 18 -> DATABRICKS LAKEHOUSE LIVE DATA SYNC")
    print(f"Target Catalog: {settings.DATABRICKS_CATALOG}")
    print(f"Target Schema:  {settings.DATABRICKS_SCHEMA}")
    print(f"Target Table:   {settings.DATABRICKS_CATALOG}.{settings.DATABRICKS_SCHEMA}.contacts")
    print("=" * 70)

    if not databricks_client.is_connected():
        print("\n⚠️ Databricks connection is currently in STANDBY mode.")
        print("To enable direct live streaming over network:")
        print("1. Open Databricks SQL Warehouse Connection Details.")
        print("2. Set DATABRICKS_HTTP_PATH in your .env file.")
        print(f"3. All 1,20,000 PostgreSQL records are pre-compiled into 'data/databricks_seed_batch.sql' for instant SQL Editor upload.")
        return

    print(f"\nFetching {max_records} records from local PostgreSQL 18...")
    df = postgres_client.get_contacts(limit=max_records)
    if df.empty:
        print("No contacts found in PostgreSQL. Please seed PostgreSQL database first.")
        return

    total_rows = len(df)
    print(f"Loaded {total_rows} records. Starting batch sync into Databricks Delta table...")
    start_t = time.time()
    
    target_table = f"{settings.DATABRICKS_CATALOG}.{settings.DATABRICKS_SCHEMA}.contacts"

    for i in range(0, total_rows, batch_size):
        batch_df = df.iloc[i:i+batch_size]
        value_tuples = []
        for _, row in batch_df.iterrows():
            uuid_str = str(row['uuid']).replace("'", "''")
            fn = str(row['first_name']).replace("'", "''")
            ln = str(row['last_name']).replace("'", "''")
            email = str(row['email']).replace("'", "''")
            phone = str(row['phone']).replace("'", "''")
            company = str(row['company']).replace("'", "''")
            title = str(row['title']).replace("'", "''")
            industry = str(row['industry']).replace("'", "''")
            country = str(row['country']).replace("'", "''")
            region = str(row['region']).replace("'", "''")
            rev = str(row['revenue_tier']).replace("$", "").replace("'", "''")
            score = float(row['engagement_score']) if pd.notnull(row['engagement_score']) else 0.0
            status = str(row['lead_status']).replace("'", "''")
            
            created_t = row['created_at'].strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(row['created_at']) else '2026-01-01 00:00:00'
            updated_t = row['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(row['updated_at']) else '2026-01-01 00:00:00'

            tuple_str = f"('{uuid_str}', '{fn}', '{ln}', '{email}', '{phone}', '{company}', '{title}', '{industry}', '{country}', '{region}', '{rev}', {score}, '{status}', TIMESTAMP'{created_t}', TIMESTAMP'{updated_t}')"
            value_tuples.append(tuple_str)

        insert_sql = f"INSERT INTO {target_table} VALUES\n" + ",\n".join(value_tuples)
        databricks_client.execute_query(insert_sql)
        print(f"Synced batch {i//batch_size + 1}/{(total_rows + batch_size - 1)//batch_size} ({len(batch_df)} records)...")

    elapsed = round(time.time() - start_t, 2)
    print(f"\n✅ SUCCESS: Synced {total_rows} contacts into Databricks Lakehouse in {elapsed} seconds!")

if __name__ == "__main__":
    sync_postgres_to_databricks_live()
