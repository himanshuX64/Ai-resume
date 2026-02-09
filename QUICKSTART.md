# Quick Start Guide

## Installation

1. **Install dependencies (REQUIRED FIRST STEP)**
```bash
pip install -r requirements.txt
```

Wait for all packages to install. This includes FastAPI, Streamlit, scikit-learn, and other dependencies.

## Running the Application

### Option 1: Using Run Scripts (Recommended)

**Terminal 1 - Start Backend:**
```bash
python run_backend.py
```
Wait for: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Start Frontend:**
```bash
streamlit run frontend/app.py
```
The browser will open automatically at `http://localhost:8501`

### Option 2: Direct Execution

**Terminal 1 - Start Backend:**
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run frontend/app.py
```

### Option 2: Test First

Run the test suite to verify everything works:
```bash
python test_app.py
```

## Using the Application

1. **Enter Your Skills**
   - Type skills separated by commas
   - Example: `Python, Machine Learning, SQL, Docker, AWS`

2. **Select a Job Role**
   - Choose from 10 pre-defined roles
   - Or create a custom role

3. **Analyze**
   - Click "Analyze Skill Gap"
   - View your job fit score (0-100%)
   - See matching and missing skills
   - Read personalized recommendations

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Match Resume
```bash
curl -X POST http://localhost:8000/match_resume \
  -H "Content-Type: application/json" \
  -d '{
    "resume_skills": {
      "skills": ["Python", "Machine Learning", "SQL"]
    },
    "job_requirement": {
      "job_title": "Data Scientist",
      "required_skills": ["Python", "Machine Learning", "Statistics"],
      "preferred_skills": ["TensorFlow", "AWS"]
    }
  }'
```

## Troubleshooting

**API Connection Error:**
- Make sure backend is running on port 8000
- Check firewall settings

**Module Import Error:**
- Ensure you're in the project root directory
- Verify all dependencies are installed

**Port Already in Use:**
- Backend: Change port in `backend/main.py`
- Frontend: Use `streamlit run frontend/app.py --server.port 8502`

## Features

- **TF-IDF Analysis**: Semantic skill matching
- **Cosine Similarity**: 0-1 similarity score
- **Weighted Scoring**: 60% required + 20% preferred + 20% similarity
- **Gap Analysis**: Identifies missing skills
- **Smart Recommendations**: Personalized career advice
- **Batch Comparison**: Compare against multiple jobs

## Sample Job Roles

1. Data Scientist
2. Full Stack Developer
3. Machine Learning Engineer
4. Backend Developer
5. DevOps Engineer
6. Frontend Developer
7. Data Engineer
8. Cloud Architect
9. AI Research Scientist
10. Mobile Developer

## Next Steps

- Customize job requirements in `data/sample_jobs.json`
- Integrate with your own resume parser
- Add more skill synonyms in `utils/skill_processor.py`
- Deploy to cloud (AWS, GCP, Azure)

For detailed documentation, see [README.md](README.md)
