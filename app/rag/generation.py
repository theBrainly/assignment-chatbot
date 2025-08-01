from typing import List, Dict, Any
import os
from app.models.models import Employee

class ResponseGenerator:
    def __init__(self, use_openai=True):
        self.use_openai = use_openai
        if use_openai:
            try:
                import openai
                self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except ImportError:
                print("OpenAI package not installed. Using template responses instead.")
                self.use_openai = False
    
    def generate_response(self, augmented_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a natural language response based on the augmented data"""
        if self.use_openai:
            return self._generate_with_openai(augmented_data)
        else:
            return self._generate_with_template(augmented_data)
    
    def _generate_with_openai(self, augmented_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response using OpenAI"""
        query = augmented_data["query"]
        employees = augmented_data["employees"]
        
        if not employees:
            return {"response": "I couldn't find any employees matching your criteria.", "recommended_employees": []}
        
        # Create a prompt for the OpenAI API
        employee_descriptions = []
        for e in employees[:3]:  # Limit to top 3
            skills_str = ", ".join(e.skills)
            projects_str = ", ".join(e.projects)
            exp = f"{e.experience_years} years"
            status = "currently available" if e.availability == "available" else "currently busy on other projects"
            
            employee_descriptions.append(
                f"- {e.name}: {exp} experience, skills in {skills_str}. "
                f"Worked on: {projects_str}. Status: {status}"
            )
        
        employees_prompt = "\n".join(employee_descriptions)
        
        prompt = f"""
        Based on the query: "{query}", I found these potential matches:
        
        {employees_prompt}
        
        Please generate a helpful response that recommends these employees for the query, highlighting why they're a good match, 
        mentioning their relevant skills, experience, and projects. Keep the tone professional and informative.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an HR assistant helping match employees to project requirements."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        return {"response": response.choices[0].message.content, "recommended_employees": employees}
    
    def _generate_with_template(self, augmented_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response using templates (fallback option)"""
        query = augmented_data["query"]
        employees = augmented_data["employees"]
        intent = augmented_data["intent"]
        
        if not employees:
            return {"response": "I couldn't find any employees matching your criteria.", "recommended_employees": []}
        
        # Create a response using templates
        response_parts = [f"Based on your request for '{query}', I found {len(employees)} potential candidates:"]
        
        for i, employee in enumerate(employees[:3], 1):  # Limit to top 3
            skills = ", ".join(employee.skills[:3])
            projects = ", ".join(employee.projects[:2])
            status = "currently available" if employee.availability == "available" else "currently busy on other projects"
            
            response_parts.append(
                f"{i}. {employee.name} has {employee.experience_years} years of experience with skills in {skills}. "
                f"They've worked on projects such as {projects} and are {status}."
            )
        
        # Add relevant filter information
        if intent["min_experience"] > 0:
            response_parts.append(f"All recommended employees have at least {intent['min_experience']} years of experience.")
        
        if intent["skills"]:
            skills_str = ", ".join(intent["skills"])
            response_parts.append(f"I prioritized candidates with expertise in {skills_str}.")
        
        if intent["project_domain"]:
            response_parts.append(f"I focused on candidates with experience in {intent['project_domain']} projects.")
        
        response = "\n\n".join(response_parts)
        return {"response": response, "recommended_employees": employees}
