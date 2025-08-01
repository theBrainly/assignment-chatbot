import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.models import Employee, Employees, ChatQuery, ChatResponse
from app.rag.pipeline import RAGPipeline

router = APIRouter()

# Cache for the RAG pipeline
_rag_pipeline = None

def get_employees() -> List[Employee]:
    """Load employees from the JSON file"""
    try:
        with open("app/data/employees.json", "r") as f:
            data = json.load(f)
        
        employees_data = Employees(**data)
        return employees_data.employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load employee data: {str(e)}")

def get_rag_pipeline():
    """Get or create the RAG pipeline singleton"""
    global _rag_pipeline
    if _rag_pipeline is None:
        employees = get_employees()
        _rag_pipeline = RAGPipeline(employees, use_openai=False)  # Change to True to use OpenAI
    return _rag_pipeline

@router.post("/chat", response_model=ChatResponse)
async def chat(query: ChatQuery, rag: RAGPipeline = Depends(get_rag_pipeline)):
    """Process a chat query and return relevant employees with a natural language response"""
    try:
        result = rag.process_query(query.query)
        return ChatResponse(
            response=result["response"],
            recommended_employees=result["recommended_employees"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/employees/search", response_model=List[Employee])
async def search_employees(
    query: str = Query(..., description="The search query"),
    min_experience: int = Query(0, description="Minimum years of experience"),
    skills: List[str] = Query(None, description="Required skills"),
    rag: RAGPipeline = Depends(get_rag_pipeline)
):
    """Search for employees based on query parameters"""
    try:
        # Get initial results from RAG
        retrieved_employees = rag.vector_db.search(query)
        
        # Apply filters
        filtered_employees = retrieved_employees
        
        if min_experience > 0:
            filtered_employees = [e for e in filtered_employees if e.experience_years >= min_experience]
        
        if skills:
            filtered_employees = [
                e for e in filtered_employees 
                if all(skill.lower() in [s.lower() for s in e.skills] for skill in skills)
            ]
        
        return filtered_employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching employees: {str(e)}")
