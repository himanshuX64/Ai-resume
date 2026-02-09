# Resume Upload Feature Guide

## Overview
The Resume Upload feature allows users to upload their resume files (PDF or DOCX) and automatically extract skills for job matching analysis.

## Features

### 1. **Supported File Formats**
- PDF (.pdf)
- Microsoft Word (.docx, .doc)

### 2. **Automatic Skill Extraction**
The system automatically extracts skills from your resume using:
- Pattern matching for common technical skills
- Skills section detection
- Intelligent skill normalization

### 3. **Experience Detection**
Automatically detects years of experience from resume text patterns like:
- "5 years of experience"
- "5+ years"
- "Experience: 5 years"

## How to Use

### Frontend (Streamlit)

1. **Navigate to the application**
   ```bash
   streamlit run frontend/app.py
   ```

2. **Select Upload Method**
   - Choose "Upload Resume" from the input method radio buttons
   - Click "Browse files" to select your resume
   - Supported formats: PDF, DOCX

3. **View Extracted Data**
   - Skills are automatically extracted and displayed
   - View the list of detected skills
   - See a preview of the resume text
   - Check detected years of experience (if found)

4. **Proceed with Analysis**
   - Select a target job role
   - Click "Analyze Skill Gap"
   - View your match results

### Backend API

#### Upload Resume Endpoint

**Endpoint:** `POST /upload_resume`

**Request:**
```bash
curl -X POST "http://localhost:8000/upload_resume" \
  -F "file=@/path/to/resume.pdf"
```

**Response:**
```json
{
  "status": "success",
  "filename": "resume.pdf",
  "skills": [
    "Python",
    "JavaScript",
    "React",
    "Node.js",
    "SQL",
    "Docker",
    "AWS"
  ],
  "experience_years": 5.0,
  "text_preview": "John Doe\nSoftware Engineer...",
  "total_skills_found": 15
}
```

**Error Response:**
```json
{
  "detail": "Invalid file type. Allowed types: pdf, docx, doc"
}
```

## Technical Implementation

### 1. Resume Parser Module (`utils/resume_parser.py`)

**Key Components:**

- **`ResumeParser` Class**: Main parser class
  - `parse_pdf()`: Extract text from PDF files
  - `parse_docx()`: Extract text from DOCX files
  - `extract_skills_from_text()`: Extract skills using pattern matching
  - `extract_experience_years()`: Detect years of experience
  - `parse_resume_full()`: Complete parsing with all features

**Skill Detection:**
- Uses regex patterns for common technical skills
- Detects skills sections in resumes
- Normalizes skill names (e.g., "python" → "Python", "nodejs" → "Node.js")

**Supported Skill Categories:**
- Programming Languages (Python, Java, JavaScript, etc.)
- Frameworks (React, Django, FastAPI, etc.)
- Databases (SQL, MongoDB, PostgreSQL, etc.)
- Cloud & DevOps (AWS, Docker, Kubernetes, etc.)
- Machine Learning (TensorFlow, PyTorch, Scikit-learn, etc.)
- Tools & Technologies (Git, CI/CD, Linux, etc.)

### 2. Backend Integration

**File Upload Handling:**
```python
@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    # Validate file type
    # Read file content
    # Parse resume
    # Return extracted data
```

**Features:**
- File type validation
- Error handling for corrupted files
- Async file processing
- Comprehensive error messages

### 3. Frontend Integration

**Streamlit File Uploader:**
```python
uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=['pdf', 'docx', 'doc']
)
```

**Features:**
- Real-time file upload
- Progress indicators
- Skill preview
- Resume text preview
- Error handling with user-friendly messages

## Skill Extraction Examples

### Example 1: Skills Section
```
SKILLS:
Python, JavaScript, React, Node.js, SQL, MongoDB
Docker, AWS, Git, Machine Learning, TensorFlow
```

**Extracted Skills:**
- Python
- JavaScript
- React
- Node.js
- SQL
- MongoDB
- Docker
- AWS
- Git
- Machine Learning
- TensorFlow

### Example 2: Experience Section
```
Senior Software Engineer at Tech Corp (2020-2024)
- Developed web applications using React and Node.js
- Implemented machine learning models with TensorFlow
- Deployed applications on AWS using Docker
```

**Extracted Skills:**
- React
- Node.js
- Machine Learning
- TensorFlow
- AWS
- Docker

## Testing

### Run Unit Tests
```bash
python test_resume_upload.py
```

### Test with Sample Resume
1. Create a sample resume with your skills
2. Save as PDF or DOCX
3. Upload through the web interface
4. Verify extracted skills

### API Testing with cURL
```bash
# Upload PDF resume
curl -X POST "http://localhost:8000/upload_resume" \
  -F "file=@sample_resume.pdf"

# Upload DOCX resume
curl -X POST "http://localhost:8000/upload_resume" \
  -F "file=@sample_resume.docx"
```

## Error Handling

### Common Errors and Solutions

1. **"Invalid file type"**
   - Solution: Use only PDF or DOCX files

2. **"Empty file uploaded"**
   - Solution: Ensure the file is not corrupted or empty

3. **"Error parsing PDF/DOCX"**
   - Solution: Check if the file is password-protected or corrupted

4. **"Cannot connect to API"**
   - Solution: Ensure the backend server is running on port 8000

## Dependencies

Required Python packages:
```
PyPDF2==3.0.1          # PDF parsing
python-docx==1.1.0     # DOCX parsing
fastapi==0.109.0       # Backend API
python-multipart==0.0.6 # File upload support
streamlit==1.30.0      # Frontend
```

## Best Practices

### For Users:
1. Use clear, well-formatted resumes
2. Include a dedicated "Skills" section
3. List skills explicitly (not just in job descriptions)
4. Use standard skill names (e.g., "Python" not "python programming")

### For Developers:
1. Validate file types before processing
2. Handle large files appropriately
3. Implement proper error handling
4. Add logging for debugging
5. Consider adding file size limits

## Future Enhancements

Potential improvements:
- [ ] Support for more file formats (TXT, RTF)
- [ ] Advanced NLP for better skill extraction
- [ ] Education and certification extraction
- [ ] Contact information extraction
- [ ] Job title and company extraction
- [ ] Multi-language support
- [ ] Resume quality scoring
- [ ] Skill proficiency level detection

## Troubleshooting

### Issue: Skills not detected
**Solution:**
- Ensure skills are clearly listed in the resume
- Add a dedicated "Skills" section
- Use common skill names

### Issue: Wrong experience years detected
**Solution:**
- Use clear format: "X years of experience"
- Place experience information prominently

### Issue: File upload fails
**Solution:**
- Check file size (should be < 10MB)
- Ensure file is not corrupted
- Verify file format (PDF or DOCX only)
- Check backend server is running

## API Reference

### Endpoints

#### 1. Upload Resume
- **URL:** `/upload_resume`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file`: Resume file (PDF or DOCX)
- **Success Response:** 200 OK
- **Error Responses:** 400 Bad Request, 500 Internal Server Error

#### 2. Health Check
- **URL:** `/health`
- **Method:** `GET`
- **Response:** `{"status": "healthy"}`

## Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Test with a simple resume file
4. Check backend logs for detailed errors

## License

This feature is part of the Resume Skill Gap Analyzer project.
