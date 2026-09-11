import os
import sys
import pandas as pd
from datetime import datetime

# Add root project path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.postgres_client import postgres_client
from config import settings

def export_to_databricks_sql(output_file: str = "data/databricks_seed_batch.sql", limit: int = 120000, batch_size: int = 1000):
    print(f"Reading up to {limit} contacts from PostgreSQL 18 database...")
    df = postgres_client.get_contacts(limit=limit)
    if df.empty:
        print("No contacts found in PostgreSQL database. Please seed local DB first.")
        return

    print(f"Loaded {len(df)} records from PostgreSQL. Generating optimized Databricks Delta SQL insert statements...")
    
    catalog = settings.DATABRICKS_CATALOG
    schema = settings.DATABRICKS_SCHEMA
    target_table = f"{catalog}.{schema}.contacts" if catalog and schema else "contacts"

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"-- Databricks Delta Lakehouse Bulk Seeder Script\n")
        f.write(f"-- Target: {target_table}\n")
        f.write(f"-- Total Records: {len(df)}\n")
        f.write(f"-- Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"USE CATALOG {catalog};\n")
        f.write(f"CREATE SCHEMA IF NOT EXISTS {schema};\n")
        f.write(f"USE SCHEMA {schema};\n\n")

        total_rows = len(df)
        for i in range(0, total_rows, batch_size):
            batch_df = df.iloc[i:i+batch_size]
            f.write(f"INSERT INTO {target_table} VALUES\n")
            value_tuples = []
            for _, row in batch_df.iterrows():
                # Escape single quotes in string values
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
                # Remove $ from revenue tier to prevent Databricks widget parameter error
                rev = str(row['revenue_tier']).replace("$", "").replace("'", "''")
                score = float(row['engagement_score']) if pd.notnull(row['engagement_score']) else 0.0
                status = str(row['lead_status']).replace("'", "''")
                
                created_t = row['created_at'].strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(row['created_at']) else '2026-01-01 00:00:00'
                updated_t = row['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(row['updated_at']) else '2026-01-01 00:00:00'

                tuple_str = f"('{uuid_str}', '{fn}', '{ln}', '{email}', '{phone}', '{company}', '{title}', '{industry}', '{country}', '{region}', '{rev}', {score}, '{status}', TIMESTAMP'{created_t}', TIMESTAMP'{updated_t}')"
                value_tuples.append(tuple_str)
            
            f.write(",\n".join(value_tuples))
            f.write(";\n\n")
            print(f"Batch {i//batch_size + 1}/{(total_rows + batch_size - 1)//batch_size} ({len(batch_df)} rows) appended.")

    print(f"\nSUCCESS: Databricks SQL script written to {output_file}")
    print(f"File size: {os.path.getsize(output_file) / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    export_to_databricks_sql()
