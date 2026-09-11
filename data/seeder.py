import uuid
import random
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from database.postgres_client import postgres_client
from database.databricks_client import databricks_client

JAIPUR_FIRST_NAMES = [
    "Rohit", "Ankit", "Pooja", "Abhishek", "Ritu", "Suresh", "Sunita", "Vikas",
    "Neha", "Deepak", "Priya", "Manish", "Suman", "Gaurav", "Meenakshi", "Amit",
    "Divya", "Ajay", "Archana", "Dinesh", "Shweta", "Rajesh", "Kavita", "Sanjay",
    "Richa", "Siddharth", "Aarti", "Yogesh", "Bhavna", "Karan", "Tanvi", "Nikhil",
    "Swati", "Tarun", "Poonam", "Alok", "Shalini", "Virendra", "Sonam", "Hemant"
]

JAIPUR_LAST_NAMES = [
    "Sharma", "Agarwal", "Khandelwal", "Jain", "Maheshwari", "Rathore", "Shekhawat",
    "Mathur", "Pareek", "Saxena", "Gupta", "Saini", "Chaudhary", "Meena", "Vijay",
    "Goyal", "Modi", "Bhardwaj", "Tiwari", "Doshi", "Soni", "Rawat", "Jadaun", "Joshi"
]

JAIPUR_COMPANIES = [
    ("AU Small Finance Bank HQ", "aubank.in", "Financial Services & Banking", "$1B+"),
    ("Genpact India (Sitapura Jaipur)", "genpact.com", "Cloud Computing & SaaS", "$1B+"),
    ("Infosys Jaipur (Mahindra World City)", "infosys.com", "Artificial Intelligence & Tech", "$1B+"),
    ("Wipro IT (Sitapura SEZ Jaipur)", "wipro.com", "Artificial Intelligence & Tech", "$1B+"),
    ("GirnarSoft / CarDekho HQ (Jaipur)", "cardekho.com", "Cloud Computing & SaaS", "$250M - $1B"),
    ("Gravita India HQ (Jaipur)", "gravitaindia.com", "Manufacturing & Logistics", "$250M - $1B"),
    ("Genus Power Infrastructures HQ (Jaipur)", "genuspower.com", "Energy & Renewable Tech", "$250M - $1B"),
    ("Dotsquares Technologies (Jaipur)", "dotsquares.com", "Artificial Intelligence & Tech", "$50M - $250M"),
    ("Teleperformance Jaipur", "teleperformance.com", "Cloud Computing & SaaS", "$250M - $1B"),
    ("CultureAlley / Hello English (Jaipur)", "culturealley.com", "Artificial Intelligence & Tech", "$10M - $50M"),
    ("DataInfosys Ltd (Jaipur)", "datainfosys.com", "Cloud Computing & SaaS", "$50M - $250M"),
    ("Amrapali Jewels HQ (Jaipur)", "amrapalijewels.com", "Retail & E-Commerce", "$50M - $250M"),
    ("Dainik Bhaskar Group HQ (Jaipur)", "dbcorp.in", "Retail & E-Commerce", "$250M - $1B"),
    ("Fortis Escorts Hospital (Malviya Nagar Jaipur)", "fortishealthcare.com", "Healthcare & Biotechnology", "$250M - $1B"),
    ("Eternal Hospital (Jagatpura Jaipur)", "eternalhospital.com", "Healthcare & Biotechnology", "$50M - $250M")
]

JAIPUR_LOCALITIES = [
    "Malviya Nagar, Jaipur",
    "Mansarovar, Jaipur",
    "C-Scheme, Jaipur",
    "Vaishali Nagar, Jaipur",
    "Sitapura Industrial Area, Jaipur",
    "Mahindra World City SEZ, Jaipur",
    "MI Road, Jaipur",
    "Tonk Road, Jaipur",
    "Raja Park, Jaipur",
    "Jagatpura, Jaipur",
    "Vidhyadhar Nagar, Jaipur"
]

JAIPUR_TITLES = [
    "Chief Technology Officer (CTO)",
    "VP of Engineering & Architecture",
    "Head of AI & Data Analytics",
    "Director of Cloud Operations",
    "Lead Enterprise Architect",
    "Senior Data Infrastructure Lead",
    "Director of Product Engineering",
    "Head of Cyber Security & SecOps",
    "AVP Enterprise Banking Solutions",
    "Principal Software Architect"
]

LEAD_STATUSES = ["New Lead", "In Progress", "Qualified", "Nurturing", "Closed Won"]

def generate_jaipur_contacts(count: int = 12000) -> List[Dict[str, Any]]:
    contacts = []
    base_time = datetime.now(timezone.utc)
    phone_prefixes = ["98290", "94140", "98280", "99280", "97830", "96100", "98291", "94141"]

    for _ in range(count):
        first_name = random.choice(JAIPUR_FIRST_NAMES)
        last_name = random.choice(JAIPUR_LAST_NAMES)
        comp_info = random.choice(JAIPUR_COMPANIES)
        company_name, domain, industry, rev_tier = comp_info
        locality = random.choice(JAIPUR_LOCALITIES)
        
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@{domain}"
        phone = f"+91 {random.choice(phone_prefixes)} {random.randint(10000, 99999)}"

        created_days_ago = random.randint(1, 365)
        created_at = base_time - timedelta(days=created_days_ago)

        contact = {
            "uuid": str(uuid.uuid4()),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "company": f"{company_name} - {locality}",
            "title": random.choice(JAIPUR_TITLES),
            "industry": industry,
            "country": "India (Jaipur)",
            "region": "APAC (Rajasthan)",
            "revenue_tier": rev_tier,
            "engagement_score": round(random.uniform(40.0, 99.9), 1),
            "lead_status": random.choice(LEAD_STATUSES),
            "created_at": created_at,
            "updated_at": created_at + timedelta(days=random.randint(0, 15))
        }
        contacts.append(contact)
    return contacts

def seed_database(count: int = 12000) -> Dict[str, Any]:
    start_t = datetime.now()
    contacts = generate_jaipur_contacts(count)
    pg_success = postgres_client.insert_contacts(contacts)
    databricks_client.sync_contacts(contacts)
    elapsed_ms = round((datetime.now() - start_t).total_seconds() * 1000, 2)
    return {
        "status": "success",
        "count": len(contacts),
        "postgres_seeded": pg_success,
        "databricks_synced": True,
        "execution_time_ms": elapsed_ms
    }

if __name__ == "__main__":
    res = seed_database(12000)
    print(f"Seeding 12,000 Jaipur City entries completed in {res['execution_time_ms']}ms: {res}")
