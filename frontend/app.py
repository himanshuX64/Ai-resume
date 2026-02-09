"""
Streamlit frontend for Resume Skill Gap Analyzer
"""
import streamlit as st
import requests
import json
import pandas as pd
from typing import List, Dict
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page configuration
st.set_page_config(
    page_title="Resume Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .skill-badge {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        margin: 0.2rem;
        border-radius: 0.3rem;
        font-size: 0.9rem;
    }
    .skill-match {
        background-color: #d4edda;
        color: #155724;
    }
    .skill-missing {
        background-color: #f8d7da;
        color: #721c24;
    }
    .skill-additional {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)


def display_header():
    """Display app header"""
    st.markdown('<div class="main-header">🎯 Resume Skill Gap Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Recruiter-Level Skill Matching</div>', unsafe_allow_html=True)


def get_sample_job_roles() -> Dict[str, Dict]:
    """Get sample job role requirements"""
    return {
        "Data Scientist": {
            "required_skills": [
                "Python", "Machine Learning", "Statistics", "Pandas", "NumPy",
                "Scikit-learn", "SQL", "Data Visualization", "Deep Learning"
            ],
            "preferred_skills": [
                "TensorFlow", "PyTorch", "AWS", "Docker", "Spark", "NLP", "Computer Vision"
            ],
            "min_experience": 2.0
        },
        "Full Stack Developer": {
            "required_skills": [
                "JavaScript", "React", "Node.js", "HTML", "CSS", "REST API",
                "Git", "SQL", "MongoDB"
            ],
            "preferred_skills": [
                "TypeScript", "Next.js", "Docker", "AWS", "GraphQL", "Redis", "CI/CD"
            ],
            "min_experience": 2.0
        },
        "Machine Learning Engineer": {
            "required_skills": [
                "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
                "Model Deployment", "Docker", "Git", "Linux"
            ],
            "preferred_skills": [
                "Kubernetes", "MLOps", "AWS", "FastAPI", "Spark", "Airflow", "CI/CD"
            ],
            "min_experience": 3.0
        },
        "Backend Developer": {
            "required_skills": [
                "Python", "FastAPI", "Django", "REST API", "SQL", "PostgreSQL",
                "Git", "Docker", "Testing"
            ],
            "preferred_skills": [
                "Redis", "Celery", "Kubernetes", "AWS", "Microservices", "GraphQL"
            ],
            "min_experience": 2.0
        },
        "DevOps Engineer": {
            "required_skills": [
                "Docker", "Kubernetes", "CI/CD", "Linux", "Git", "AWS",
                "Terraform", "Monitoring", "Scripting"
            ],
            "preferred_skills": [
                "Ansible", "Jenkins", "Prometheus", "Grafana", "Python", "Helm"
            ],
            "min_experience": 3.0
        }
    }


def parse_skills_input(skills_text: str) -> List[str]:
    """Parse skills from text input"""
    # Split by common delimiters
    import re
    skills = re.split(r'[,;\n|]', skills_text)
    # Clean and filter
    skills = [s.strip() for s in skills if s.strip()]
    return skills


def display_skill_badges(skills: List[str], badge_class: str):
    """Display skills as badges"""
    if not skills:
        st.write("None")
        return
    
    html = ""
    for skill in skills:
        html += f'<span class="skill-badge {badge_class}">{skill}</span>'
    st.markdown(html, unsafe_allow_html=True)


def display_analysis_results(response: Dict):
    """Display analysis results"""
    analysis = response['analysis']
    
    # Job Fit Score
    st.markdown("### 📊 Job Fit Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = analysis['job_fit_score']
        color = "green" if score >= 70 else "orange" if score >= 50 else "red"
        st.metric("Job Fit Score", f"{score}%", delta=None)
        st.progress(score / 100)
    
    with col2:
        similarity = analysis['similarity_score'] * 100
        st.metric("Similarity Score", f"{similarity:.1f}%")
        st.progress(similarity / 100)
    
    with col3:
        matched = len(analysis['matching_skills'])
        st.metric("Skills Matched", matched)
    
    # Detailed Breakdown
    st.markdown("---")
    st.markdown("### 🎯 Skill Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Matching Skills")
        display_skill_badges(analysis['matching_skills'], "skill-match")
        
        st.markdown("#### ❌ Missing Skills")
        display_skill_badges(analysis['missing_skills'], "skill-missing")
    
    with col2:
        st.markdown("#### 💡 Additional Skills")
        display_skill_badges(analysis['additional_skills'], "skill-additional")
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 💼 Recommendations")
    
    for i, rec in enumerate(analysis['recommendations'], 1):
        st.markdown(f"{i}. {rec}")


def main():
    """Main application"""
    display_header()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📋 Instructions")
        st.markdown("""
        1. Enter your resume skills
        2. Select or customize a job role
        3. Click 'Analyze Skill Gap'
        4. Review your match results
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 Settings")
        api_status = st.empty()
        
        # Check API health
        try:
            response = requests.get(f"{API_URL}/health", timeout=2)
            if response.status_code == 200:
                api_status.success("✅ API Connected")
            else:
                api_status.error("❌ API Error")
        except:
            api_status.warning("⚠️ API Offline - Start backend first")
    
    # Main content
    tab1, tab2 = st.tabs(["🎯 Single Job Analysis", "📊 Multiple Jobs Comparison"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📝 Your Resume Skills")
            
            skills_input_method = st.radio(
                "Input Method",
                ["Text Input", "Upload Resume"],
                horizontal=True
            )
            
            if skills_input_method == "Text Input":
                skills_text = st.text_area(
                    "Enter your skills (comma or newline separated)",
                    height=200,
                    placeholder="Python, Machine Learning, SQL, Docker, AWS...",
                    help="Enter each skill separated by comma, semicolon, or new line"
                )
                
                resume_skills = parse_skills_input(skills_text) if skills_text else []
                
                if resume_skills:
                    st.success(f"✅ {len(resume_skills)} skills detected")
                    with st.expander("View parsed skills"):
                        st.write(resume_skills)
            else:
                uploaded_file = st.file_uploader(
                    "Upload your resume (PDF or DOCX)",
                    type=['pdf', 'docx', 'doc'],
                    help="Upload your resume in PDF or DOCX format"
                )
                
                resume_skills = []
                
                if uploaded_file is not None:
                    with st.spinner("📄 Parsing resume..."):
                        try:
                            # Prepare file for upload
                            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                            
                            # Upload to backend
                            response = requests.post(
                                f"{API_URL}/upload_resume",
                                files=files,
                                timeout=30
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                resume_skills = result['skills']
                                
                                st.success(f"✅ Resume parsed successfully!")
                                
                                # Display extracted information
                                col_a, col_b = st.columns(2)
                                
                                with col_a:
                                    if result.get('name'):
                                        st.info(f"👤 **Name:** {result['name']}")
                                    if result.get('email'):
                                        st.info(f"📧 **Email:** {result['email']}")
                                    if result.get('phone'):
                                        st.info(f"📱 **Phone:** {result['phone']}")
                                
                                with col_b:
                                    st.info(f"📊 **Skills Found:** {result['total_skills_found']}")
                                    if result.get('experience_years'):
                                        st.info(f"💼 **Experience:** {result['experience_years']} years")
                                
                                # Education section
                                if result.get('education') and len(result['education']) > 0:
                                    with st.expander("🎓 Education", expanded=True):
                                        for edu in result['education']:
                                            st.markdown(f"**{edu.get('degree', 'N/A')}**")
                                            if edu.get('institution'):
                                                st.write(f"Institution: {edu['institution']}")
                                            if edu.get('year'):
                                                st.write(f"Year: {edu['year']}")
                                            if edu.get('score'):
                                                st.write(f"Score: {edu['score']}")
                                            st.markdown("---")
                                
                                # Work Experience section
                                if result.get('work_experience') and len(result['work_experience']) > 0:
                                    with st.expander("💼 Work Experience", expanded=True):
                                        for exp in result['work_experience']:
                                            st.markdown(f"**{exp.get('title', 'N/A')}**")
                                            if exp.get('company'):
                                                st.write(f"Company: {exp['company']}")
                                            if exp.get('duration'):
                                                st.write(f"Duration: {exp['duration']}")
                                            st.markdown("---")
                                
                                # Skills section
                                with st.expander("🔧 Extracted Skills", expanded=True):
                                    if resume_skills:
                                        # Display as badges
                                        skills_html = ""
                                        for skill in resume_skills:
                                            skills_html += f'<span class="skill-badge skill-additional">{skill}</span>'
                                        st.markdown(skills_html, unsafe_allow_html=True)
                                    else:
                                        st.write("No skills detected")
                                
                                # Resume preview
                                with st.expander("📄 Resume Text Preview"):
                                    st.text(result['text_preview'])
                            else:
                                st.error(f"❌ Error parsing resume: {response.text}")
                        
                        except requests.exceptions.ConnectionError:
                            st.error("❌ Cannot connect to API. Please start the backend server first.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
        with col2:
            st.markdown("### 💼 Target Job Role")
            
            sample_roles = get_sample_job_roles()
            
            job_selection = st.selectbox(
                "Select a job role",
                ["Custom"] + list(sample_roles.keys())
            )
            
            if job_selection == "Custom":
                job_title = st.text_input("Job Title", "Custom Role")
                required_skills_text = st.text_area(
                    "Required Skills",
                    height=100,
                    placeholder="Python, SQL, Machine Learning..."
                )
                preferred_skills_text = st.text_area(
                    "Preferred Skills (Optional)",
                    height=100,
                    placeholder="AWS, Docker, Kubernetes..."
                )
                
                required_skills = parse_skills_input(required_skills_text) if required_skills_text else []
                preferred_skills = parse_skills_input(preferred_skills_text) if preferred_skills_text else []
            else:
                job_title = job_selection
                job_data = sample_roles[job_selection]
                required_skills = job_data['required_skills']
                preferred_skills = job_data['preferred_skills']
                
                st.info(f"**Required Skills:** {', '.join(required_skills[:5])}...")
                st.info(f"**Preferred Skills:** {', '.join(preferred_skills[:3])}...")
        
        # Analyze button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            analyze_button = st.button("🚀 Analyze Skill Gap", use_container_width=True, type="primary")
        
        # Perform analysis
        if analyze_button:
            if not resume_skills:
                st.error("❌ Please enter your resume skills")
            elif not required_skills:
                st.error("❌ Please enter required job skills")
            else:
                with st.spinner("🔍 Analyzing skill gap..."):
                    try:
                        # Prepare request
                        payload = {
                            "resume_skills": {
                                "skills": resume_skills
                            },
                            "job_requirement": {
                                "job_title": job_title,
                                "required_skills": required_skills,
                                "preferred_skills": preferred_skills
                            }
                        }
                        
                        # Make API request
                        response = requests.post(
                            f"{API_URL}/match_resume",
                            json=payload,
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ Analysis Complete!")
                            st.markdown("---")
                            display_analysis_results(result)
                        else:
                            st.error(f"❌ API Error: {response.status_code}")
                            st.error(response.text)
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to API. Please start the backend server first.")
                        st.code("python backend/main.py")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with tab2:
        st.markdown("### 📊 Compare Against Multiple Jobs")
        st.info("🚧 Batch comparison feature - Enter your skills and we'll match against all sample roles")
        
        skills_text_batch = st.text_area(
            "Enter your skills",
            height=150,
            placeholder="Python, Machine Learning, SQL, Docker, AWS...",
            key="batch_skills"
        )
        
        if st.button("🔍 Compare All Jobs", type="primary"):
            if not skills_text_batch:
                st.error("❌ Please enter your skills")
            else:
                resume_skills_batch = parse_skills_input(skills_text_batch)
                
                with st.spinner("🔍 Analyzing against all job roles..."):
                    try:
                        sample_roles = get_sample_job_roles()
                        job_requirements = []
                        
                        for job_title, job_data in sample_roles.items():
                            job_requirements.append({
                                "job_title": job_title,
                                "required_skills": job_data['required_skills'],
                                "preferred_skills": job_data['preferred_skills']
                            })
                        
                        payload = {
                            "resume_skills": {
                                "skills": resume_skills_batch
                            },
                            "job_requirements": job_requirements
                        }
                        
                        response = requests.post(
                            f"{API_URL}/batch_match",
                            json=payload,
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"✅ Analyzed {result['total_jobs_analyzed']} job roles!")
                            
                            # Display results as table
                            df = pd.DataFrame(result['results'])
                            st.dataframe(
                                df.style.background_gradient(subset=['fit_score'], cmap='RdYlGn'),
                                use_container_width=True
                            )
                            
                            # Best match
                            best_match = result['results'][0]
                            st.success(f"🎯 Best Match: **{best_match['job_title']}** with {best_match['fit_score']}% fit score")
                        else:
                            st.error(f"❌ API Error: {response.status_code}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to API. Please start the backend server first.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
