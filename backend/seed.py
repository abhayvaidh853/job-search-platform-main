import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().with_name(".env"))

if not os.getenv("MONGODB_URL") or not os.getenv("DATABASE_NAME"):
    raise RuntimeError(
        "Set MONGODB_URL and DATABASE_NAME in backend\\.env before seeding."
    )

from app.database.mongodb import client, get_database


SAMPLE_COMPANIES = [
    {
        "_seed_key": "sample-company-techcorp",
        "name": "TechCorp Solutions",
        "industry": "Information Technology",
        "location": "Bangalore",
        "description": "Enterprise software and cloud technology solutions.",
        "website": "https://example.com/techcorp",
        "logo": None,
        "company_size": "201-500",
    },
    {
        "_seed_key": "sample-company-datamind",
        "name": "DataMind AI",
        "industry": "Artificial Intelligence",
        "location": "Remote",
        "description": "Building AI and machine learning products for modern businesses.",
        "website": "https://example.com/datamind",
        "logo": None,
        "company_size": "51-200",
    },
    {
        "_seed_key": "sample-company-creative-studio",
        "name": "Creative Studio",
        "industry": "Design & Digital Media",
        "location": "Mumbai",
        "description": "A design agency focused on UI/UX, branding, and web design.",
        "website": "https://example.com/creative-studio",
        "logo": None,
        "company_size": "11-50",
    },
    {
        "_seed_key": "sample-company-appnation",
        "name": "AppNation",
        "industry": "Mobile Development",
        "location": "Delhi",
        "description": "A startup building high-performance mobile experiences.",
        "website": "https://example.com/appnation",
        "logo": None,
        "company_size": "11-50",
    },
]

SAMPLE_JOBS = [
    {
        "_seed_key": "sample-job-frontend-developer",
        "title": "Frontend Developer",
        "company": "TechCorp Solutions",
        "location": "Bangalore",
        "job_type": "Full Time",
        "work_mode": "Hybrid",
        "experience": "1-3 Years",
        "salary": "₹8,00,000 - ₹12,00,000",
        "description": "Build responsive user interfaces using React.",
        "skills": ["React", "JavaScript", "CSS", "TypeScript"],
    },
    {
        "_seed_key": "sample-job-python-backend-engineer",
        "title": "Python Backend Engineer",
        "company": "DataMind AI",
        "location": "Remote",
        "job_type": "Full Time",
        "work_mode": "Remote",
        "experience": "2-4 Years",
        "salary": "₹10,00,000 - ₹15,00,000",
        "description": "Develop REST APIs and scalable services with Python.",
        "skills": ["Python", "FastAPI", "MongoDB", "REST API"],
    },
    {
        "_seed_key": "sample-job-ui-ux-designer",
        "title": "UI/UX Designer",
        "company": "Creative Studio",
        "location": "Mumbai",
        "job_type": "Full Time",
        "work_mode": "On-site",
        "experience": "Fresher",
        "salary": "₹6,00,000 - ₹9,00,000",
        "description": "Design intuitive user experiences, prototypes, and mockups.",
        "skills": ["Figma", "UI/UX", "Wireframing"],
    },
    {
        "_seed_key": "sample-job-react-native-developer",
        "title": "React Native Developer",
        "company": "AppNation",
        "location": "Delhi",
        "job_type": "Internship",
        "work_mode": "Remote",
        "experience": "Fresher",
        "salary": "₹25,000 / month",
        "description": "Help build cross-platform mobile applications.",
        "skills": ["React Native", "JavaScript", "Redux"],
    },
]


def upsert_samples(collection, samples):
    inserted = 0
    updated = 0

    for sample in samples:
        document = sample.copy()
        seed_key = document.pop("_seed_key")
        result = collection.update_one(
            {"_seed_key": seed_key},
            {
                "$set": document,
                "$setOnInsert": {
                    "_seed_key": seed_key,
                    "created_at": datetime.now(timezone.utc),
                },
            },
            upsert=True,
        )
        inserted += result.upserted_id is not None
        updated += result.upserted_id is None and result.modified_count > 0

    return inserted, updated


def seed_database():
    try:
        db = get_database()
        companies_inserted, companies_updated = upsert_samples(
            db.companies, SAMPLE_COMPANIES
        )
        jobs_inserted, jobs_updated = upsert_samples(db.jobs, SAMPLE_JOBS)

        print(
            "Seed complete. "
            f"Companies: {companies_inserted} inserted, {companies_updated} updated. "
            f"Jobs: {jobs_inserted} inserted, {jobs_updated} updated."
        )
    finally:
        client.close()


if __name__ == "__main__":
    seed_database()
