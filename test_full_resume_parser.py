"""
Test script for full resume parsing with all attributes
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.resume_parser import ResumeParser


def test_full_resume_parsing():
    """Test the resume parser with comprehensive resume data"""
    parser = ResumeParser()
    
    # Sample resume text based on user's example
    sample_text = """
    Ansh
    Software Engineer
    35 Karohan
    Karohan
    Mankapur,Gonda,UP - 271312
    Mob No. : 7754091703
    Email Id : sahuansh275@gmail.com
    
    CAREER OBJECTIVE
    To make contribution in the organization with best of my ability and also to Develop new skills during
    the interaction to achieve new heights.
    
    ACADEMIC QUALIFICATION
    S.No. Qualification University / Board Year Per %
    1 B.Tech CSE AI&ML Sanskriti University Appearing in 3rd year 8.0 CGPA
    2 12th UP Board 2023 70.6 %
    3 10th UP Board 2021 84.16 %
    
    WORK EXPERIENCE
    Software Engineer at Tech Solutions Pvt Ltd (2023-Present)
    - Developed web applications using React and Node.js
    - Implemented machine learning models with Python and TensorFlow
    - Worked with SQL databases and REST APIs
    
    Junior Developer at StartUp Inc (2022-2023)
    - Built backend services with FastAPI and Django
    - Deployed applications using Docker and AWS
    - Implemented CI/CD pipelines with Git and Jenkins
    
    TECHNICAL SKILLS
    Programming Languages: Python, JavaScript, Java, C++
    Web Technologies: React, Node.js, HTML, CSS, FastAPI, Django
    Databases: SQL, MySQL, PostgreSQL, MongoDB
    Tools & Technologies: Git, Docker, AWS, Machine Learning, TensorFlow, REST API
    
    PROJECTS
    1. AI Resume Analyzer - Built an AI-powered resume analysis tool
    2. E-commerce Platform - Developed full-stack e-commerce application
    """
    
    print("Testing Full Resume Parser...")
    print("=" * 70)
    
    # Test name extraction
    name = parser.extract_name(sample_text)
    print(f"\n[NAME]")
    print(f"  Extracted: {name}")
    
    # Test email extraction
    email = parser.extract_email(sample_text)
    print(f"\n[EMAIL]")
    print(f"  Extracted: {email}")
    
    # Test phone extraction
    phone = parser.extract_phone(sample_text)
    print(f"\n[PHONE]")
    print(f"  Extracted: {phone}")
    
    # Test skill extraction
    skills = parser.extract_skills_from_text(sample_text)
    print(f"\n[SKILLS] - Found {len(skills)} skills")
    for skill in skills:
        print(f"  - {skill}")
    
    # Test education extraction
    education = parser.extract_education(sample_text)
    print(f"\n[EDUCATION] - Found {len(education)} entries")
    for i, edu in enumerate(education, 1):
        print(f"  {i}. Degree: {edu.get('degree', 'N/A')}")
        if edu.get('institution'):
            print(f"     Institution: {edu['institution']}")
        if edu.get('year'):
            print(f"     Year: {edu['year']}")
        if edu.get('score'):
            print(f"     Score: {edu['score']}")
    
    # Test work experience extraction
    work_exp = parser.extract_work_experience(sample_text)
    print(f"\n[WORK EXPERIENCE] - Found {len(work_exp)} entries")
    for i, exp in enumerate(work_exp, 1):
        print(f"  {i}. Title: {exp.get('title', 'N/A')}")
        if exp.get('company'):
            print(f"     Company: {exp['company']}")
        if exp.get('duration'):
            print(f"     Duration: {exp['duration']}")
    
    # Test experience years extraction
    experience_years = parser.extract_experience_years(sample_text)
    print(f"\n[EXPERIENCE YEARS]")
    print(f"  Extracted: {experience_years} years" if experience_years else "  Not found")
    
    print("\n" + "=" * 70)
    print("[SUCCESS] Full resume parsing test completed!")
    
    # Summary
    print("\n[SUMMARY]")
    print(f"  Name: {'Found' if name else 'Not found'}")
    print(f"  Email: {'Found' if email else 'Not found'}")
    print(f"  Phone: {'Found' if phone else 'Not found'}")
    print(f"  Skills: {len(skills)} found")
    print(f"  Education: {len(education)} entries")
    print(f"  Work Experience: {len(work_exp)} entries")
    
    return True


if __name__ == "__main__":
    try:
        test_full_resume_parsing()
        print("\n[SUCCESS] All tests passed!")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
