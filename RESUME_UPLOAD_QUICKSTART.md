# Resume Upload Feature - Quick Start

## What's New?

The Resume Skill Gap Analyzer now supports **automatic resume upload and skill extraction**! Upload your PDF or DOCX resume and let AI extract your skills automatically.

## Quick Usage

### 1. Start the Application

```bash
# Terminal 1: Start Backend
python backend/main.py

# Terminal 2: Start Frontend
streamlit run frontend/app.py
```

### 2. Upload Your Resume

1. Open the app in your browser (usually http://localhost:8501)
2. Select **"Upload Resume"** as the input method
3. Click **"Browse files"** and select your resume (PDF or DOCX)
4. Wait for automatic skill extraction
5. Review the extracted skills
6. Select a target job role
7. Click **"Analyze Skill Gap"**

## Features

✅ **Automatic Skill Extraction** - AI-powered skill detection from resume text  
✅ **PDF & DOCX Support** - Upload resumes in common formats  
✅ **Experience Detection** - Automatically finds years of experience  
✅ **Smart Filtering** - Filters out non-skill text  
✅ **Skill Normalization** - Standardizes skill names (e.g., "python" → "Python")  

## Supported Skills

The system can detect 100+ technical skills including:

- **Languages**: Python, JavaScript, Java, C++, TypeScript, etc.
- **Frameworks**: React, Django, FastAPI, Node.js, Angular, etc.
- **Databases**: SQL, MongoDB, PostgreSQL, Redis, etc.
- **Cloud & DevOps**: AWS, Docker, Kubernetes, CI/CD, etc.
- **ML/AI**: TensorFlow, PyTorch, Machine Learning, NLP, etc.
- **Tools**: Git, Linux, REST API, GraphQL, etc.

## API Usage

### Upload Resume via API

```bash
curl -X POST "http://localhost:8000/upload_resume" \
  -F "file=@/path/to/your/resume.pdf"
```

### Response Example

```json
{
  "status": "success",
  "filename": "john_doe_resume.pdf",
  "skills": [
    "Python", "JavaScript", "React", "Node.js", "SQL",
    "Docker", "AWS", "Machine Learning", "TensorFlow"
  ],
  "experience_years": 5.0,
  "text_preview": "John Doe\nSoftware Engineer...",
  "total_skills_found": 19
}
```

## Tips for Best Results

1. **Use a clear resume format** with a dedicated "Skills" section
2. **List skills explicitly** (not just in job descriptions)
3. **Use standard skill names** (e.g., "Python" not "python programming")
4. **Keep file size reasonable** (< 10MB)
5. **Ensure file is not password-protected**

## Files Added

- [`utils/resume_parser.py`](utils/resume_parser.py) - Resume parsing logic
- [`backend/main.py`](backend/main.py) - Added `/upload_resume` endpoint
- [`frontend/app.py`](frontend/app.py) - Added file upload UI
- [`test_resume_upload.py`](test_resume_upload.py) - Test script
- [`RESUME_UPLOAD_GUIDE.md`](RESUME_UPLOAD_GUIDE.md) - Detailed documentation

## Testing

Run the test script to verify functionality:

```bash
python test_resume_upload.py
```

Expected output:
```
Testing Resume Parser...
==================================================

[OK] Extracted 19 skills:
  - AWS
  - Docker
  - Python
  - React
  ...

[OK] Extracted experience: 5.0 years

[SUCCESS] All tests passed!
```

## Troubleshooting

**Problem**: Skills not detected  
**Solution**: Ensure skills are clearly listed in a "Skills" section

**Problem**: File upload fails  
**Solution**: Check file format (PDF/DOCX only) and ensure backend is running

**Problem**: Wrong skills extracted  
**Solution**: Use standard skill names and avoid ambiguous terms

## Next Steps

After uploading your resume:
1. Review the extracted skills
2. Add any missing skills manually if needed
3. Select a target job role
4. Run the skill gap analysis
5. Review recommendations

## Need Help?

- See [`RESUME_UPLOAD_GUIDE.md`](RESUME_UPLOAD_GUIDE.md) for detailed documentation
- Check [`README.md`](README.md) for general project information
- Run tests with `python test_resume_upload.py`

---

**Enjoy the new resume upload feature! 🚀**
