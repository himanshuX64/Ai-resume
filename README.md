# 🎯 Smart Resume Skill Gap Analyzer

A recruiter-level AI-powered system that analyzes resume skills against job requirements, predicts job fit scores, and provides actionable recommendations for career development.

## 🔥 Key Features

- **Intelligent Skill Matching**: Uses TF-IDF and Cosine Similarity for accurate skill comparison
- **Job Fit Score**: Predicts compatibility (0-100%) between resume and job requirements
- **Gap Analysis**: Identifies missing skills, matching skills, and additional skills
- **Smart Recommendations**: Provides personalized career development suggestions
- **Batch Comparison**: Compare your resume against multiple job roles simultaneously
- **Interactive UI**: Beautiful Streamlit interface for easy interaction
- **RESTful API**: FastAPI backend for integration with other systems

## 🚀 What Makes It Unique

Unlike simple keyword matching tools, this analyzer:
- Performs **semantic similarity analysis** using TF-IDF vectorization
- Provides **weighted scoring** (60% required skills, 20% preferred skills, 20% similarity)
- Generates **actionable recommendations** based on skill gaps
- Supports **skill normalization** and synonym matching
- Offers **recruiter-level insights** with detailed breakdowns

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance REST API framework
- **Pydantic**: Data validation and schema management
- **scikit-learn**: TF-IDF vectorization and cosine similarity
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Frontend
- **Streamlit**: Interactive web interface
- **Requests**: API communication

### ML/AI Components
- **TF-IDF (Term Frequency-Inverse Document Frequency)**: Skill importance weighting
- **Cosine Similarity**: Semantic similarity measurement
- **Custom Skill Processor**: Normalization and synonym handling

## 📁 Project Structure

```
Ai-resume/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── models.py            # Pydantic data models
├── frontend/
│   └── app.py               # Streamlit UI
├── utils/
│   ├── __init__.py
│   ├── skill_processor.py   # Skill normalization utilities
│   └── skill_matcher.py     # TF-IDF & similarity engine
├── data/
│   └── sample_jobs.json     # Sample job requirements
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or navigate to the project directory**
```bash
cd Ai-resume
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

### Step 1: Start the Backend API

Open a terminal and run:

```bash
python backend/main.py
```

The API will start at `http://localhost:8000`

You can verify it's running by visiting:
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Step 2: Start the Frontend UI

Open a **new terminal** (keep the backend running) and run:

```bash
streamlit run frontend/app.py
```

The Streamlit app will open automatically in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Single Job Analysis

1. **Enter Your Skills**
   - Type your skills in the text area (comma or newline separated)
   - Example: `Python, Machine Learning, SQL, Docker, AWS`

2. **Select Target Job**
   - Choose from pre-defined roles (Data Scientist, Full Stack Developer, etc.)
   - Or create a custom job with your own requirements

3. **Analyze**
   - Click "Analyze Skill Gap"
   - View your job fit score, matching skills, and missing skills
   - Read personalized recommendations

### Multiple Jobs Comparison

1. Navigate to the "Multiple Jobs Comparison" tab
2. Enter your skills
3. Click "Compare All Jobs"
4. View a ranked table of all job matches
5. Identify your best-fit roles

## 🔌 API Endpoints

### POST `/match_resume`

Match resume skills with a single job requirement.

**Request Body:**
```json
{
  "resume_skills": {
    "skills": ["Python", "Machine Learning", "SQL"]
  },
  "job_requirement": {
    "job_title": "Data Scientist",
    "required_skills": ["Python", "Machine Learning", "Statistics"],
    "preferred_skills": ["TensorFlow", "AWS"]
  }
}
```

**Response:**
```json
{
  "analysis": {
    "job_fit_score": 75.5,
    "matching_skills": ["Python", "Machine Learning"],
    "missing_skills": ["Statistics"],
    "additional_skills": ["SQL"],
    "similarity_score": 0.85,
    "recommendations": [...]
  },
  "job_title": "Data Scientist",
  "status": "success"
}
```

### POST `/batch_match`

Compare resume against multiple job requirements.

**Request Body:**
```json
{
  "resume_skills": {
    "skills": ["Python", "Machine Learning", "SQL"]
  },
  "job_requirements": [
    {
      "job_title": "Data Scientist",
      "required_skills": ["Python", "Machine Learning"],
      "preferred_skills": ["TensorFlow"]
    },
    {
      "job_title": "Backend Developer",
      "required_skills": ["Python", "SQL", "FastAPI"],
      "preferred_skills": ["Docker"]
    }
  ]
}
```

### GET `/health`

Health check endpoint.

## 🧮 Scoring Algorithm

The job fit score (0-100) is calculated using:

```
Job Fit Score = (Required Skills Match × 60%) + 
                (Preferred Skills Match × 20%) + 
                (TF-IDF Similarity × 20%)
```

### Score Interpretation:
- **80-100%**: Excellent match - You meet most requirements
- **60-79%**: Good match - Minor skill gaps to address
- **40-59%**: Moderate match - Significant development needed
- **0-39%**: Low match - Major skill gaps present

## 🎨 Features in Detail

### Skill Normalization
- Converts skills to lowercase
- Handles synonyms (e.g., "JS" → "JavaScript", "ML" → "Machine Learning")
- Removes duplicates and special characters
- Supports multi-word skills (e.g., "Machine Learning", "Deep Learning")

### TF-IDF Analysis
- Weighs skill importance based on frequency
- Supports unigrams and bigrams
- Handles skill variations and combinations

### Cosine Similarity
- Measures semantic similarity between skill sets
- Range: 0 (no similarity) to 1 (identical)
- Complements exact matching with fuzzy comparison

## 📊 Sample Job Roles Included

1. **Data Scientist** - ML, Python, Statistics, Pandas
2. **Full Stack Developer** - React, Node.js, JavaScript
3. **Machine Learning Engineer** - PyTorch, TensorFlow, MLOps
4. **Backend Developer** - FastAPI, Django, PostgreSQL
5. **DevOps Engineer** - Docker, Kubernetes, AWS
6. **Frontend Developer** - React, TypeScript, CSS
7. **Data Engineer** - Spark, Airflow, ETL
8. **Cloud Architect** - AWS, Terraform, Microservices
9. **AI Research Scientist** - Deep Learning, Research, NLP
10. **Mobile Developer** - React Native, iOS, Android

## 🔮 Future Enhancements

- [ ] PDF/DOCX resume upload and parsing
- [ ] Resume text extraction using NLP
- [ ] Job description scraping from job boards
- [ ] Skill trend analysis and market insights
- [ ] Learning resource recommendations
- [ ] Career path visualization
- [ ] Export reports as PDF
- [ ] User authentication and history tracking

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available for educational and commercial use.

## 👨‍💻 Author

Built with ❤️ for helping job seekers find their perfect role

## 🙏 Acknowledgments

- scikit-learn for ML algorithms
- FastAPI for the amazing web framework
- Streamlit for the beautiful UI components
- The open-source community

---

**Happy Job Hunting! 🎯**

For questions or support, please open an issue on the repository.
