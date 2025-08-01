from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from app.models.models import Employee

class VectorDatabase:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.employee_vectors = {}
        self.employees = []
    
    def add_employees(self, employees: List[Employee]):
        """Add employees to the vector database"""
        self.employees = employees
        
        for employee in employees:
            # Create a text representation of the employee
            employee_text = f"{employee.name} {' '.join(employee.skills)} {' '.join(employee.projects)}"
            # Generate embedding
            embedding = self.model.encode(employee_text)
            self.employee_vectors[employee.id] = embedding
    
    def search(self, query: str, top_k: int = 5) -> List[Employee]:
        """Search for relevant employees based on the query"""
        query_vector = self.model.encode(query)
        
        # Calculate similarity scores
        scores = {}
        for employee_id, vector in self.employee_vectors.items():
            similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            scores[employee_id] = similarity
        
        # Sort by similarity score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_employee_ids = [employee_id for employee_id, _ in sorted_scores[:top_k]]
        
        # Return top employees
        return [employee for employee in self.employees if employee.id in top_employee_ids]
