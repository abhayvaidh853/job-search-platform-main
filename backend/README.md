# Backend

## Setup

Create a `.env` file in this directory with the MongoDB connection, database
name, JWT signing secret, and Gemini API key:

```env
MONGODB_URL=your-mongodb-connection-string
DATABASE_NAME=job_search_platform
JWT_SECRET_KEY=your-long-random-secret
GEMINI_API_KEY=your-gemini-api-key
```

Do not commit the `.env` file. Resume analysis sends extracted resume text to
Google Gemini to generate the report.

Install the backend dependencies and start the API from this directory:

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload
```