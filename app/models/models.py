from pydantic import BaseModel
from typing import List, Optional, Literal

class Employee(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: Literal["available", "busy"]

class Employees(BaseModel):
    employees: List[Employee]

class ChatQuery(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    recommended_employees: List[Employee]
