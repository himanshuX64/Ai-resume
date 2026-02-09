"""
FastAPI backend for Resume Skill Gap Analyzer
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import (
    MatchRequest,
    MatchResponse,
    SkillGapAnalysis,
    ResumeSkills,
    JobRequirement
)
from utils.skill_matcher import SkillMatcher
from utils.resume_parser import ResumeParser

# Initialize FastAPI app
app = FastAPI(
    title="Resume Skill Gap Analyzer API",
    description="AI-powered resume skill matching and gap analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize skill matcher and resume parser
skill_matcher = SkillMatcher()
resume_parser = ResumeParser()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Resume Skill Gap Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "match_resume": "/match_resume",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Resume Skill Gap Analyzer"}


@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse resume file (PDF or DOCX)
    
    Args:
        file: Resume file to upload
        
    Returns:
        Parsed resume data including extracted skills
    """
    try:
        # Validate file type
        allowed_extensions = ['pdf', 'docx', 'doc']
        file_extension = file.filename.lower().split('.')[-1]
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        file_content = await file.read()
        
        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded"
            )
        
        # Parse resume
        parsed_data = resume_parser.parse_resume_full(file_content, file.filename)
        
        return {
            "status": "success",
            "filename": parsed_data['filename'],
            "name": parsed_data['name'],
            "email": parsed_data['email'],
            "phone": parsed_data['phone'],
            "skills": parsed_data['skills'],
            "education": parsed_data['education'],
            "work_experience": parsed_data['work_experience'],
            "experience_years": parsed_data['experience_years'],
            "text_preview": parsed_data['text'][:500] + "..." if len(parsed_data['text']) > 500 else parsed_data['text'],
            "total_skills_found": len(parsed_data['skills'])
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )


@app.post("/match_resume", response_model=MatchResponse)
async def match_resume(request: MatchRequest):
    """
    Match resume skills with job requirements and perform gap analysis
    
    Args:
        request: MatchRequest containing resume skills and job requirements
        
    Returns:
        MatchResponse with detailed skill gap analysis
    """
    try:
        # Extract data from request
        resume_skills = request.resume_skills.skills
        job_requirement = request.job_requirement
        
        # Validate inputs
        if not resume_skills:
            raise HTTPException(
                status_code=400, 
                detail="Resume skills cannot be empty"
            )
        
        if not job_requirement.required_skills:
            raise HTTPException(
                status_code=400,
                detail="Job required skills cannot be empty"
            )
        
        # Perform skill gap analysis
        analysis_result = skill_matcher.analyze_skill_gap(
            resume_skills=resume_skills,
            required_skills=job_requirement.required_skills,
            preferred_skills=job_requirement.preferred_skills or []
        )
        
        # Generate recommendations
        recommendations = skill_matcher.generate_recommendations(
            missing_required=analysis_result['missing_required'],
            missing_preferred=analysis_result['missing_preferred'],
            job_fit_score=analysis_result['job_fit_score']
        )
        
        # Combine matching skills
        all_matching = (
            analysis_result['matching_required'] + 
            analysis_result['matching_preferred']
        )
        
        # Create response
        skill_gap_analysis = SkillGapAnalysis(
            job_fit_score=analysis_result['job_fit_score'],
            matching_skills=all_matching,
            missing_skills=analysis_result['missing_required'],
            additional_skills=analysis_result['additional_skills'],
            similarity_score=analysis_result['similarity_score'],
            recommendations=recommendations
        )
        
        response = MatchResponse(
            analysis=skill_gap_analysis,
            job_title=job_requirement.job_title,
            status="success"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/batch_match")
async def batch_match_resume(
    resume_skills: ResumeSkills,
    job_requirements: List[JobRequirement]
):
    """
    Match resume against multiple job requirements
    
    Args:
        resume_skills: Resume skills
        job_requirements: List of job requirements
        
    Returns:
        List of match results sorted by fit score
    """
    try:
        if not resume_skills.skills:
            raise HTTPException(
                status_code=400,
                detail="Resume skills cannot be empty"
            )
        
        if not job_requirements:
            raise HTTPException(
                status_code=400,
                detail="Job requirements list cannot be empty"
            )
        
        results = []
        
        for job_req in job_requirements:
            analysis_result = skill_matcher.analyze_skill_gap(
                resume_skills=resume_skills.skills,
                required_skills=job_req.required_skills,
                preferred_skills=job_req.preferred_skills or []
            )
            
            results.append({
                "job_title": job_req.job_title,
                "fit_score": analysis_result['job_fit_score'],
                "similarity_score": analysis_result['similarity_score'],
                "required_match_percentage": analysis_result['required_match_percentage'],
                "skills_matched": analysis_result['total_skills_matched'],
                "missing_required_count": len(analysis_result['missing_required'])
            })
        
        # Sort by fit score descending
        results.sort(key=lambda x: x['fit_score'], reverse=True)
        
        return {
            "status": "success",
            "total_jobs_analyzed": len(results),
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
