import re
from typing import List, Dict, Any
from app.models.models import Employee

class Augmenter:
    def __init__(self):
        pass
    
    def extract_query_intent(self, query: str) -> Dict[str, Any]:
        """Extract intent and parameters from the query"""
        intent = {
            "looking_for": "developers",  # Default
            "min_experience": 0,
            "skills": [],
            "project_domain": None
        }
        
        # Extract years of experience
        experience_match = re.search(r'(\d+)\+?\s*years?\s+experience', query, re.IGNORECASE)
        if experience_match:
            intent["min_experience"] = int(experience_match.group(1))
        
        # Extract skills (this is a simplified approach)
        common_skills = ["python", "react", "javascript", "java", "aws", "docker", 
                         "kubernetes", "machine learning", "tensorflow", "pytorch", 
                         "node.js", "react native"]
        
        for skill in common_skills:
            if skill.lower() in query.lower():
                intent["skills"].append(skill)
        
        # Extract project domain
        domains = ["healthcare", "finance", "education", "e-commerce", "social media", "banking"]
        for domain in domains:
            if domain.lower() in query.lower():
                intent["project_domain"] = domain
                break
        
        return intent
    
    def augment_results(self, query: str, employees: List[Employee]) -> Dict[str, Any]:
        """Augment the retrieved employees with additional context"""
        intent = self.extract_query_intent(query)
        
        # Filter by minimum experience if specified
        if intent["min_experience"] > 0:
            employees = [e for e in employees if e.experience_years >= intent["min_experience"]]
        
        # Prioritize by skills match
        if intent["skills"]:
            for employee in employees:
                employee_skills = [s.lower() for s in employee.skills]
                employee.skill_match_score = sum(1 for s in intent["skills"] if s.lower() in employee_skills)
            
            employees.sort(key=lambda e: e.skill_match_score, reverse=True)
        
        # Prioritize by project domain match
        if intent["project_domain"]:
            for employee in employees:
                employee.domain_match = any(intent["project_domain"].lower() in p.lower() for p in employee.projects)
            
            employees.sort(key=lambda e: getattr(e, "domain_match", False), reverse=True)
        
        # Prioritize by availability
        employees.sort(key=lambda e: 0 if e.availability == "available" else 1)
        
        return {
            "query": query,
            "intent": intent,
            "employees": employees
        }
