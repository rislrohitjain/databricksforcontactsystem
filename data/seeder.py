import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from faker import Faker
from database.postgres_client import postgres_client
from database.databricks_client import databricks_client

fake = Faker()

INDUSTRIES = [
    "Artificial Intelligence & Tech",
    "Financial Services & Banking",
    "Healthcare & Biotechnology",
    "Cloud Computing & SaaS",
    "Manufacturing & Logistics",
    "Retail & E-Commerce",
    "Energy & Renewable Tech"
]

TITLES = [
    "Chief Technology Officer",
    "VP of Engineering",
    "Director of Data Science",
    "Head of AI Innovations",
    "Lead Enterprise Architect",
    "VP of Infrastructure",
    "Senior Cloud Architect",
    "Director of Product Management"
]

REVENUE_TIERS = [
    "$1M - $10M",
    "$10M - $50M",
    "$50M - $250M",
    "$250M - $1B",
    "$1B+"
]

REGIONS_COUNTRIES = {
    "North America": ["United States", "Canada"],
    "Europe": ["United Kingdom", "Germany", "France", "Netherlands", "Switzerland"],
    "APAC": ["Japan", "Singapore", "Australia", "India"],
    "LATAM": ["Brazil", "Mexico"],
    "EMEA": ["United Arab Emirates", "Saudi Arabia"]
}

LEAD_STATUSES = ["New Lead", "In Progress", "Qualified", "Nurturing", "Closed Won"]

def generate_contacts(count: int = 250) -> List[Dict[str, Any]]:
    contacts = []
    base_time = datetime.utcnow()

    for _ in range(count):
        region = random.choice(list(REGIONS_COUNTRIES.keys()))
        country = random.choice(REGIONS_COUNTRIES[region])
        first_name = fake.first_name()
        last_name = fake.last_name()
        company = fake.company()
        domain = company.lower().replace(" ", "").replace(",", "").replace("-", "") + ".com"
        email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
        
        created_days_ago = random.randint(1, 180)
        created_at = base_time - timedelta(days=created_days_ago)

        contact = {
            "uuid": str(uuid.uuid4()),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": fake.phone_number(),
            "company": company,
            "title": random.choice(TITLES),
            "industry": random.choice(INDUSTRIES),
            "country": country,
            "region": region,
            "revenue_tier": random.choice(REVENUE_TIERS),
            "engagement_score": round(random.uniform(30.0, 99.5), 1),
            "lead_status": random.choice(LEAD_STATUSES),
            "created_at": created_at,
            "updated_at": created_at + timedelta(days=random.randint(0, 10))
        }
        contacts.append(contact)
    return contacts

def seed_database(count: int = 250) -> Dict[str, Any]:
    contacts = generate_contacts(count)
    pg_success = postgres_client.insert_contacts(contacts)
    databricks_client.sync_contacts(contacts)
    return {
        "status": "success",
        "count": len(contacts),
        "postgres_seeded": pg_success,
        "databricks_synced": True
    }

if __name__ == "__main__":
    res = seed_database(100)
    print(f"Seeding completed: {res}")
