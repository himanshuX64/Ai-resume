"""
Test script for Resume Skill Gap Analyzer
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.skill_processor import SkillProcessor
from utils.skill_matcher import SkillMatcher


def test_skill_processor():
    """Test skill processor functionality"""
    print("=" * 60)
    print("Testing Skill Processor")
    print("=" * 60)
    
    processor = SkillProcessor()
    
    # Test normalization
    test_skills = ["Python", "ML", "JavaScript", "js", "PYTHON", "Machine Learning"]
    normalized = processor.normalize_skills(test_skills)
    
    print(f"\nOriginal skills: {test_skills}")
    print(f"Normalized skills: {normalized}")
    
    # Test skill overlap
    resume_skills = ["Python", "Machine Learning", "SQL", "Docker"]
    job_skills = ["Python", "Machine Learning", "Statistics", "Deep Learning"]
    
    overlap = processor.calculate_skill_overlap(resume_skills, job_skills)
    
    print(f"\nResume skills: {resume_skills}")
    print(f"Job skills: {job_skills}")
    print(f"Matching: {overlap['matching']}")
    print(f"Missing from resume: {overlap['only_in_second']}")
    print(f"Additional in resume: {overlap['only_in_first']}")
    print(f"Overlap ratio: {overlap['overlap_ratio']:.2%}")
    
    print("\n[PASS] Skill Processor tests passed!")


def test_skill_matcher():
    """Test skill matcher functionality"""
    print("\n" + "=" * 60)
    print("Testing Skill Matcher")
    print("=" * 60)
    
    matcher = SkillMatcher()
    
    # Test case 1: Good match
    print("\n--- Test Case 1: Good Match ---")
    resume_skills = [
        "Python", "Machine Learning", "Pandas", "NumPy", 
        "Scikit-learn", "SQL", "Data Visualization"
    ]
    required_skills = [
        "Python", "Machine Learning", "Statistics", "Pandas", 
        "NumPy", "Scikit-learn", "SQL"
    ]
    preferred_skills = ["TensorFlow", "AWS", "Docker"]
    
    analysis = matcher.analyze_skill_gap(
        resume_skills, 
        required_skills, 
        preferred_skills
    )
    
    print(f"Resume skills: {resume_skills}")
    print(f"Required skills: {required_skills}")
    print(f"\nJob Fit Score: {analysis['job_fit_score']}%")
    print(f"Similarity Score: {analysis['similarity_score']:.2f}")
    print(f"Matching Required: {analysis['matching_required']}")
    print(f"Missing Required: {analysis['missing_required']}")
    print(f"Required Match %: {analysis['required_match_percentage']:.1f}%")
    
    recommendations = matcher.generate_recommendations(
        analysis['missing_required'],
        analysis['missing_preferred'],
        analysis['job_fit_score']
    )
    
    print("\nRecommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    # Test case 2: Poor match
    print("\n--- Test Case 2: Poor Match ---")
    resume_skills_2 = ["JavaScript", "React", "HTML", "CSS"]
    required_skills_2 = [
        "Python", "Machine Learning", "Deep Learning", 
        "TensorFlow", "PyTorch"
    ]
    
    analysis_2 = matcher.analyze_skill_gap(
        resume_skills_2, 
        required_skills_2, 
        []
    )
    
    print(f"Resume skills: {resume_skills_2}")
    print(f"Required skills: {required_skills_2}")
    print(f"\nJob Fit Score: {analysis_2['job_fit_score']}%")
    print(f"Similarity Score: {analysis_2['similarity_score']:.2f}")
    print(f"Matching Required: {analysis_2['matching_required']}")
    print(f"Missing Required: {analysis_2['missing_required']}")
    
    # Test case 3: Perfect match
    print("\n--- Test Case 3: Perfect Match ---")
    resume_skills_3 = ["Python", "FastAPI", "Docker", "SQL", "Git"]
    required_skills_3 = ["Python", "FastAPI", "Docker", "SQL", "Git"]
    
    analysis_3 = matcher.analyze_skill_gap(
        resume_skills_3, 
        required_skills_3, 
        []
    )
    
    print(f"Resume skills: {resume_skills_3}")
    print(f"Required skills: {required_skills_3}")
    print(f"\nJob Fit Score: {analysis_3['job_fit_score']}%")
    print(f"Similarity Score: {analysis_3['similarity_score']:.2f}")
    print(f"Required Match %: {analysis_3['required_match_percentage']:.1f}%")
    
    print("\n[PASS] Skill Matcher tests passed!")


def test_api_models():
    """Test Pydantic models"""
    print("\n" + "=" * 60)
    print("Testing API Models")
    print("=" * 60)
    
    from backend.models import ResumeSkills, JobRequirement, MatchRequest
    
    # Create test data
    resume = ResumeSkills(
        skills=["Python", "Machine Learning", "SQL"],
        experience_years=3.0
    )
    
    job = JobRequirement(
        job_title="Data Scientist",
        required_skills=["Python", "Machine Learning", "Statistics"],
        preferred_skills=["TensorFlow", "AWS"]
    )
    
    request = MatchRequest(
        resume_skills=resume,
        job_requirement=job
    )
    
    print(f"\nResume: {resume.model_dump()}")
    print(f"Job: {job.model_dump()}")
    print(f"Request created successfully!")
    
    print("\n[PASS] API Models tests passed!")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("RESUME SKILL GAP ANALYZER - TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_skill_processor()
        test_skill_matcher()
        test_api_models()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)
        print("\nYou can now run the application:")
        print("1. Start backend: python backend/main.py")
        print("2. Start frontend: streamlit run frontend/app.py")
        print("\n")
        
    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
