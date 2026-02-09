"""
Pydantic models for Resume Skill Gap Analyzer
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class ResumeSkills(BaseModel):

    """Model for resume skills input"""
    skills: List[str] = Field(..., description="List of skills from resume")
    experience_years: Optional[float] = Field(None, description="Years of experience")
    education: Optional[str] = Field(None, description="Education level")
    job_titles: Optional[List[str]] = Field(None, description="Previous job titles")


class JobRequirement(BaseModel):

    """Model for job role requirements"""
    job_title: str = Field(..., description="Job title/role")
    required_skills: List[str] = Field(..., description="Required skills for the job")
    preferred_skills: Optional[List[str]] = Field(None, description="Preferred/nice-to-have skills")
    min_experience: Optional[float] = Field(None, description="Minimum years of experience")
    education_required: Optional[str] = Field(None, description="Required education level")


class SkillGapAnalysis(BaseModel):

    """Model for skill gap analysis results"""
    job_fit_score: float = Field(..., description="Overall job fit score (0-100)")
    matching_skills: List[str] = Field(..., description="Skills that match job requirements")
    missing_skills: List[str] = Field(..., description="Required skills not in resume")
    additional_skills: List[str] = Field(..., description="Resume skills not required for job")
    similarity_score: float = Field(..., description="Cosine similarity score (0-1)")
    recommendations: List[str] = Field(..., description="Recommendations to improve fit")


class MatchRequest(BaseModel):

    """Model for match resume request"""
    resume_skills: ResumeSkills
    job_requirement: JobRequirement


class MatchResponse(BaseModel):
    
    """Model for match resume response"""
    analysis: SkillGapAnalysis
    job_title: str
    status: str = "success"
