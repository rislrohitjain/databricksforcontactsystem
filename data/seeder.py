import uuid
import random
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from faker import Faker
from database.postgres_client import postgres_client
from database.databricks_client import databricks_client

fake_in = Faker('en_IN')
fake_gen = Faker()

INDIAN_FIRST_NAMES = [
    "Aarav", "Ananya", "Rajesh", "Priya", "Vikram", "Sunita", "Rohan", "Kavya", 
    "Aditya", "Neha", "Arjun", "Pooja", "Suresh", "Divya", "Rahul", "Meera", 
    "Amit", "Ritu", "Siddharth", "Sneha", "Manish", "Shreya", "Deepak", "Tanvi", 
    "Alok", "Swati", "Nikhil", "Anish", "Ishita", "Varun", "Trisha", "Gaurav",
    "Tarun", "Simran", "Abhishek", "Preeti", "Karan", "Bhavna", "Vishal", "Ridhi"
]

INDIAN_LAST_NAMES = [
    "Sharma", "Patel", "Kumar", "Iyer", "Singh", "Gupta", "Verma", "Rao", 
    "Joshi", "Mehta", "Nair", "Reddy", "Deshmukh", "Agarwal", "Banerjee", "Chawla", 
    "Mukherjee", "Kapoor", "Bhat", "Kulkarni", "Pillai", "Saxena", "Tripathi", "Chatterjee"
]

INDIAN_COMPANIES = [
    ("Tata Consultancy Services", "tcs.com", "Artificial Intelligence & Tech", "$1B+"),
    ("Infosys Technologies", "infosys.com", "Cloud Computing & SaaS", "$1B+"),
    ("Wipro Limited", "wipro.com", "Artificial Intelligence & Tech", "$1B+"),
    ("HCL Tech", "hcltech.com", "Cloud Computing & SaaS", "$1B+"),
    ("Tech Mahindra", "techmahindra.com", "Artificial Intelligence & Tech", "$250M - $1B"),
    ("Zoho Corporation", "zoho.com", "Cloud Computing & SaaS", "$250M - $1B"),
    ("Freshworks India", "freshworks.com", "Cloud Computing & SaaS", "$50M - $250M"),
    ("Reliance Industries & Jio", "jio.com", "Energy & Renewable Tech", "$1B+"),
    ("HDFC Bank", "hdfcbank.com", "Financial Services & Banking", "$1B+"),
    ("ICICI Bank", "icicibank.com", "Financial Services & Banking", "$1B+"),
    ("Axis Bank", "axisbank.com", "Financial Services & Banking", "$1B+"),
    ("Paytm / One97", "paytm.com", "Financial Services & Banking", "$250M - $1B"),
    ("PhonePe India", "phonepe.com", "Financial Services & Banking", "$250M - $1B"),
    ("Razorpay Software", "razorpay.com", "Financial Services & Banking", "$50M - $250M"),
    ("Flipkart India", "flipkart.com", "Retail & E-Commerce", "$1B+"),
    ("Swiggy Enterprise", "swiggy.in", "Retail & E-Commerce", "$250M - $1B"),
    ("Zomato Ltd", "zomato.com", "Retail & E-Commerce", "$250M - $1B"),
    ("Zepto Express", "zepto.in", "Retail & E-Commerce", "$50M - $250M"),
    ("Ola Electric", "olaelectric.com", "Manufacturing & Logistics", "$250M - $1B"),
    ("Ather Energy", "atherenergy.com", "Energy & Renewable Tech", "$50M - $250M"),
    ("Sun Pharma", "sunpharma.com", "Healthcare & Biotechnology", "$1B+"),
    ("Dr. Reddy's Labs", "drreddys.com", "Healthcare & Biotechnology", "$1B+"),
    ("Biocon India", "biocon.com", "Healthcare & Biotechnology", "$250M - $1B"),
    ("Larsen & Toubro", "larsentoubro.com", "Manufacturing & Logistics", "$1B+"),
    ("Postman API", "postman.com", "Cloud Computing & SaaS", "$50M - $250M"),
    ("BrowserStack", "browserstack.com", "Cloud Computing & SaaS", "$50M - $250M")
]

INDIAN_CITIES = [
    ("Bengaluru", "India", "APAC"),
    ("Mumbai", "India", "APAC"),
    ("Gurgaon / NCR", "India", "APAC"),
    ("Hyderabad", "India", "APAC"),
    ("Pune", "India", "APAC"),
    ("Chennai", "India", "APAC"),
    ("Noida / NCR", "India", "APAC"),
    ("Ahmedabad", "India", "APAC"),
    ("Kolkata", "India", "APAC"),
    ("Jaipur", "India", "APAC")
]

INDIAN_TITLES = [
    "Chief Technology Officer (CTO)",
    "VP of Engineering",
    "Head of AI & ML Labs",
    "Director of Data Engineering",
    "Lead Enterprise Architect",
    "Senior Cloud Infrastructure Lead",
    "Director of Product Engineering",
    "Head of Cyber Security & SecOps",
    "AVP Enterprise Solutions",
    "Principal Data Scientist"
]

LEAD_STATUSES = ["New Lead", "In Progress", "Qualified", "Nurturing", "Closed Won"]

def generate_indian_contacts(count: int = 5000) -> List[Dict[str, Any]]:
    contacts = []
    base_time = datetime.now(timezone.utc)
    phone_prefixes = ["98200", "99800", "97110", "98450", "98765", "99000", "98100", "96500", "99400", "97300"]

    for _ in range(count):
        first_name = random.choice(INDIAN_FIRST_NAMES)
        last_name = random.choice(INDIAN_LAST_NAMES)
        comp_info = random.choice(INDIAN_COMPANIES)
        company_name, domain, industry, rev_tier = comp_info
        
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 99)}@{domain}"
        city, country, region = random.choice(INDIAN_CITIES)
        phone = f"+91 {random.choice(phone_prefixes)} {random.randint(10000, 99999)}"

        created_days_ago = random.randint(1, 365)
        created_at = base_time - timedelta(days=created_days_ago)

        contact = {
            "uuid": str(uuid.uuid4()),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "company": f"{company_name} ({city})",
            "title": random.choice(INDIAN_TITLES),
            "industry": industry,
            "country": country,
            "region": region,
            "revenue_tier": rev_tier,
            "engagement_score": round(random.uniform(45.0, 99.8), 1),
            "lead_status": random.choice(LEAD_STATUSES),
            "created_at": created_at,
            "updated_at": created_at + timedelta(days=random.randint(0, 15))
        }
        contacts.append(contact)
    return contacts

def seed_database(count: int = 5000) -> Dict[str, Any]:
    contacts = generate_indian_contacts(count)
    pg_success = postgres_client.insert_contacts(contacts)
    databricks_client.sync_contacts(contacts)
    return {
        "status": "success",
        "count": len(contacts),
        "postgres_seeded": pg_success,
        "databricks_synced": True
    }

if __name__ == "__main__":
    res = seed_database(5000)
    print(f"Seeding 5,000 India-level entries completed: {res}")
