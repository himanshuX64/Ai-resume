"""
Test script for resume upload functionality
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.resume_parser import ResumeParser


def test_resume_parser():
    """Test the resume parser with sample text"""
    parser = ResumeParser()
    
    # Sample resume text
    sample_text = """
    John Doe
    Software Engineer
    
    SKILLS:
    Python, JavaScript, React, Node.js, SQL, MongoDB, Docker, AWS, Git
    Machine Learning, TensorFlow, Pandas, NumPy
    REST API, FastAPI, Django
    
    EXPERIENCE:
    5 years of experience in software development
    
    Senior Software Engineer at Tech Corp (2020-2024)
    - Developed web applications using React and Node.js
    - Implemented machine learning models with TensorFlow
    - Deployed applications on AWS using Docker and Kubernetes
    
    Software Engineer at StartUp Inc (2019-2020)
    - Built REST APIs with FastAPI
    - Worked with PostgreSQL and MongoDB databases
    - Implemented CI/CD pipelines
    
    EDUCATION:
    Bachelor of Science in Computer Science
    """
    
    print("Testing Resume Parser...")
    print("=" * 50)
    
    # Test skill extraction
    skills = parser.extract_skills_from_text(sample_text)
    print(f"\n[OK] Extracted {len(skills)} skills:")
    for skill in skills:
        print(f"  - {skill}")
    
    # Test experience extraction
    experience = parser.extract_experience_years(sample_text)
    print(f"\n[OK] Extracted experience: {experience} years")
    
    print("\n" + "=" * 50)
    print("[OK] Resume parser test completed successfully!")
    
    return True


def test_skill_normalization():
    """Test skill name normalization"""
    parser = ResumeParser()
    
    print("\nTesting Skill Normalization...")
    print("=" * 50)
    
    test_skills = [
        "python", "javascript", "node.js", "react", "sql",
        "aws", "docker", "machine learning", "tensorflow"
    ]
    
    print("\nNormalized skills:")
    for skill in test_skills:
        normalized = parser._normalize_skill_name(skill)
        print(f"  {skill:20} -> {normalized}")
    
    print("\n" + "=" * 50)
    print("[OK] Skill normalization test completed!")
    
    return True


if __name__ == "__main__":
    try:
        test_resume_parser()
        test_skill_normalization()
        print("\n[SUCCESS] All tests passed!")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {str(e)}")
        sys.exit(1)
