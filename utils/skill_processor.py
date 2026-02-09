"""
Skill extraction and preprocessing utilities
"""
import re
from typing import List, Set
import pandas as pd
import numpy as np


class SkillProcessor:
    """Process and normalize skills for comparison"""
    
    def __init__(self):
        # Common skill synonyms and variations
        self.skill_synonyms = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'ml': 'machine learning',
            'ai': 'artificial intelligence',
            'dl': 'deep learning',
            'nlp': 'natural language processing',
            'cv': 'computer vision',
            'db': 'database',
            'sql': 'structured query language',
            'nosql': 'non-relational database',
            'aws': 'amazon web services',
            'gcp': 'google cloud platform',
            'k8s': 'kubernetes',
            'ci/cd': 'continuous integration continuous deployment',
            'rest': 'restful api',
            'api': 'application programming interface',
        }
    
    def normalize_skill(self, skill: str) -> str:
        """
        Normalize a single skill string
        
        Args:
            skill: Raw skill string
            
        Returns:
            Normalized skill string
        """
        # Convert to lowercase
        skill = skill.lower().strip()
        
        # Remove special characters except +, #, and spaces
        skill = re.sub(r'[^\w\s+#/-]', '', skill)
        
        # Replace multiple spaces with single space
        skill = re.sub(r'\s+', ' ', skill)
        
        # Apply synonyms
        if skill in self.skill_synonyms:
            skill = self.skill_synonyms[skill]
        
        return skill
    
    def normalize_skills(self, skills: List[str]) -> List[str]:
        """
        Normalize a list of skills
        
        Args:
            skills: List of raw skill strings
            
        Returns:
            List of normalized skill strings
        """
        normalized = [self.normalize_skill(skill) for skill in skills]
        # Remove duplicates while preserving order
        seen = set()
        result = []
        for skill in normalized:
            if skill and skill not in seen:
                seen.add(skill)
                result.append(skill)
        return result
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """
        Extract potential skills from free text
        
        Args:
            text: Raw text (e.g., from resume)
            
        Returns:
            List of extracted skills
        """
        # Split by common delimiters
        delimiters = [',', ';', '|', '\n', '•', '·']
        pattern = '|'.join(map(re.escape, delimiters))
        
        potential_skills = re.split(pattern, text)
        
        # Clean and filter
        skills = []
        for skill in potential_skills:
            skill = skill.strip()
            # Filter out very short or very long strings
            if 2 <= len(skill) <= 50:
                skills.append(skill)
        
        return self.normalize_skills(skills)
    
    def create_skill_vector(self, skills: List[str], all_skills: Set[str]) -> np.ndarray:
        """
        Create a binary vector representation of skills
        
        Args:
            skills: List of skills to vectorize
            all_skills: Set of all possible skills
            
        Returns:
            Binary numpy array
        """
        skill_set = set(self.normalize_skills(skills))
        vector = np.array([1 if skill in skill_set else 0 for skill in sorted(all_skills)])
        return vector
    
    def skills_to_text(self, skills: List[str]) -> str:
        """
        Convert skills list to text for TF-IDF processing
        
        Args:
            skills: List of skills
            
        Returns:
            Space-separated skill string
        """
        normalized = self.normalize_skills(skills)
        return ' '.join(normalized)
    
    def calculate_skill_overlap(self, skills1: List[str], skills2: List[str]) -> dict:
        """
        Calculate overlap between two skill sets
        
        Args:
            skills1: First skill list
            skills2: Second skill list
            
        Returns:
            Dictionary with overlap statistics
        """
        set1 = set(self.normalize_skills(skills1))
        set2 = set(self.normalize_skills(skills2))
        
        matching = set1.intersection(set2)
        only_in_1 = set1 - set2
        only_in_2 = set2 - set1
        
        total_unique = len(set1.union(set2))
        overlap_ratio = len(matching) / total_unique if total_unique > 0 else 0
        
        return {
            'matching': list(matching),
            'only_in_first': list(only_in_1),
            'only_in_second': list(only_in_2),
            'overlap_ratio': overlap_ratio,
            'match_count': len(matching),
            'total_unique': total_unique
        }
