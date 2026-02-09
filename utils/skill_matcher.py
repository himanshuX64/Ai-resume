"""
TF-IDF and Cosine Similarity based skill matching engine
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from utils.skill_processor import SkillProcessor


class SkillMatcher:
    """Match resume skills with job requirements using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.processor = SkillProcessor()
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),  # Unigrams and bigrams
            max_features=1000,
            min_df=1
        )
    
    def calculate_similarity(
        self, 
        resume_skills: List[str], 
        job_skills: List[str]
    ) -> float:
        """
        Calculate cosine similarity between resume and job skills
        
        Args:
            resume_skills: List of skills from resume
            job_skills: List of required job skills
            
        Returns:
            Cosine similarity score (0-1)
        """
        # Convert skills to text
        resume_text = self.processor.skills_to_text(resume_skills)
        job_text = self.processor.skills_to_text(job_skills)
        
        # Handle empty cases
        if not resume_text or not job_text:
            return 0.0
        
        # Create TF-IDF vectors
        try:
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0
    
    def analyze_skill_gap(
        self,
        resume_skills: List[str],
        required_skills: List[str],
        preferred_skills: List[str] = None
    ) -> Dict:
        """
        Perform comprehensive skill gap analysis
        
        Args:
            resume_skills: Skills from resume
            required_skills: Required skills for job
            preferred_skills: Preferred/nice-to-have skills
            
        Returns:
            Dictionary with detailed analysis
        """
        if preferred_skills is None:
            preferred_skills = []
        
        # Normalize all skills
        resume_skills_norm = self.processor.normalize_skills(resume_skills)
        required_skills_norm = self.processor.normalize_skills(required_skills)
        preferred_skills_norm = self.processor.normalize_skills(preferred_skills)
        
        # Calculate overlaps
        resume_set = set(resume_skills_norm)
        required_set = set(required_skills_norm)
        preferred_set = set(preferred_skills_norm)
        
        # Matching skills
        matching_required = list(resume_set.intersection(required_set))
        matching_preferred = list(resume_set.intersection(preferred_set))
        
        # Missing skills
        missing_required = list(required_set - resume_set)
        missing_preferred = list(preferred_set - resume_set)
        
        # Additional skills (in resume but not required)
        additional_skills = list(resume_set - required_set - preferred_set)
        
        # Calculate similarity score
        similarity_score = self.calculate_similarity(resume_skills, required_skills)
        
        # Calculate job fit score (0-100)
        job_fit_score = self._calculate_job_fit_score(
            matching_required,
            required_skills_norm,
            matching_preferred,
            preferred_skills_norm,
            similarity_score
        )
        
        return {
            'matching_required': matching_required,
            'matching_preferred': matching_preferred,
            'missing_required': missing_required,
            'missing_preferred': missing_preferred,
            'additional_skills': additional_skills,
            'similarity_score': similarity_score,
            'job_fit_score': job_fit_score,
            'required_match_percentage': (
                len(matching_required) / len(required_skills_norm) * 100 
                if required_skills_norm else 0
            ),
            'total_skills_matched': len(matching_required) + len(matching_preferred)
        }
    
    def _calculate_job_fit_score(
        self,
        matching_required: List[str],
        required_skills: List[str],
        matching_preferred: List[str],
        preferred_skills: List[str],
        similarity_score: float
    ) -> float:
        """
        Calculate overall job fit score (0-100)
        
        Scoring breakdown:
        - 60% weight on required skills match
        - 20% weight on preferred skills match
        - 20% weight on TF-IDF similarity
        """
        # Required skills score (0-60)
        required_score = 0
        if required_skills:
            required_match_ratio = len(matching_required) / len(required_skills)
            required_score = required_match_ratio * 60
        
        # Preferred skills score (0-20)
        preferred_score = 0
        if preferred_skills:
            preferred_match_ratio = len(matching_preferred) / len(preferred_skills)
            preferred_score = preferred_match_ratio * 20
        
        # Similarity score (0-20)
        similarity_component = similarity_score * 20
        
        # Total score
        total_score = required_score + preferred_score + similarity_component
        
        return round(total_score, 2)
    
    def generate_recommendations(
        self,
        missing_required: List[str],
        missing_preferred: List[str],
        job_fit_score: float
    ) -> List[str]:
        """
        Generate recommendations to improve job fit
        
        Args:
            missing_required: Missing required skills
            missing_preferred: Missing preferred skills
            job_fit_score: Current job fit score
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if job_fit_score >= 80:
            recommendations.append("[EXCELLENT] You meet most requirements.")
        elif job_fit_score >= 60:
            recommendations.append("[GOOD] Consider strengthening a few areas.")
        elif job_fit_score >= 40:
            recommendations.append("[MODERATE] Significant skill gaps to address.")
        else:
            recommendations.append("[LOW] Major skill development needed.")
        
        # Priority missing skills
        if missing_required:
            top_missing = missing_required[:5]  # Top 5 critical skills
            recommendations.append(
                f"[PRIORITY] Learn these required skills - {', '.join(top_missing)}"
            )
        
        # Preferred skills
        if missing_preferred and job_fit_score < 90:
            top_preferred = missing_preferred[:3]
            recommendations.append(
                f"[BONUS] Consider learning - {', '.join(top_preferred)}"
            )
        
        # General advice based on score
        if job_fit_score < 50:
            recommendations.append(
                "[ADVICE] Take online courses or certifications in missing skills"
            )
            recommendations.append(
                "[ADVICE] Consider entry-level or junior positions to build experience"
            )
        elif job_fit_score < 70:
            recommendations.append(
                "[ADVICE] Build projects showcasing the missing skills"
            )
            recommendations.append(
                "[ADVICE] Network with professionals in this field"
            )
        else:
            recommendations.append(
                "[ADVICE] Highlight your matching skills prominently in your resume"
            )
            recommendations.append(
                "[ADVICE] Prepare to discuss your relevant experience in interviews"
            )
        
        return recommendations
    
    def create_skill_matrix(
        self,
        resume_skills: List[str],
        job_requirements: List[Dict]
    ) -> pd.DataFrame:
        """
        Create a skill comparison matrix for multiple jobs
        
        Args:
            resume_skills: Skills from resume
            job_requirements: List of job requirement dictionaries
            
        Returns:
            Pandas DataFrame with comparison matrix
        """
        results = []
        
        for job in job_requirements:
            analysis = self.analyze_skill_gap(
                resume_skills,
                job.get('required_skills', []),
                job.get('preferred_skills', [])
            )
            
            results.append({
                'Job Title': job.get('job_title', 'Unknown'),
                'Fit Score': analysis['job_fit_score'],
                'Similarity': round(analysis['similarity_score'] * 100, 2),
                'Required Match %': round(analysis['required_match_percentage'], 2),
                'Skills Matched': analysis['total_skills_matched'],
                'Missing Required': len(analysis['missing_required'])
            })
        
        df = pd.DataFrame(results)
        df = df.sort_values('Fit Score', ascending=False)
        
        return df
