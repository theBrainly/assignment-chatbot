from typing import List, Dict, Any
from app.models.models import Employee
from app.rag.retrieval import VectorDatabase
from app.rag.augmentation import Augmenter
from app.rag.generation import ResponseGenerator

class RAGPipeline:
    def __init__(self, employees: List[Employee], use_openai: bool = True):
        """Initialize the RAG pipeline with employees data"""
        self.vector_db = VectorDatabase()
        self.vector_db.add_employees(employees)
        
        self.augmenter = Augmenter()
        self.generator = ResponseGenerator(use_openai=use_openai)
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query through the RAG pipeline"""
        # Retrieval: Find relevant employees
        retrieved_employees = self.vector_db.search(query)
        
        # Augmentation: Add context and prioritize results
        augmented_data = self.augmenter.augment_results(query, retrieved_employees)
        
        # Generation: Create a natural language response
        response = self.generator.generate_response(augmented_data)
        
        return response
