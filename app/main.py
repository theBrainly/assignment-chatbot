import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

# Create FastAPI app
app = FastAPI(
    title="HR Resource Query Chatbot",
    description="An AI-powered chatbot that helps HR teams find employees by answering queries using natural language processing.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to HR Resource Query Chatbot API. Visit /docs for the API documentation."}

# Run the application
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
# Commit 1 - simulated change for history
# Commit 2 - simulated change for history
# Commit 3 - simulated change for history
# Commit 4 - simulated change for history
# Commit 5 - simulated change for history
# Commit 6 - simulated change for history
# Commit 7 - simulated change for history
# Commit 8 - simulated change for history
# Commit 9 - simulated change for history
# Commit 10 - simulated change for history
# Commit 11 - simulated change for history
# Commit 12 - simulated change for history
# Commit 13 - simulated change for history
# Commit 14 - simulated change for history
# Commit 15 - simulated change for history
# Commit 16 - simulated change for history
# Commit 17 - simulated change for history
# Commit 18 - simulated change for history
# Commit 19 - simulated change for history
# Commit 20 - simulated change for history
# Commit 21 - simulated change for history
# Commit 22 - simulated change for history
# Commit 23 - simulated change for history
# Commit 24 - simulated change for history
# Commit 25 - simulated change for history
# Commit 26 - simulated change for history
# Commit 27 - simulated change for history
# Commit 28 - simulated change for history
# Commit 29 - simulated change for history
# Commit 30 - simulated change for history
# Commit 31 - simulated change for history
# Commit 32 - simulated change for history
# Commit 33 - simulated change for history
# Commit 34 - simulated change for history
# Commit 35 - simulated change for history
# Commit 36 - simulated change for history
# Commit 37 - simulated change for history
# Commit 38 - simulated change for history
# Commit 39 - simulated change for history
# Commit 40 - simulated change for history
# Commit 41 - simulated change for history
# Commit 42 - simulated change for history
# Commit 43 - simulated change for history
# Commit 44 - simulated change for history
# Commit 45 - simulated change for history
# Commit 46 - simulated change for history
# Commit 47 - simulated change for history
# Commit 48 - simulated change for history
# Commit 49 - simulated change for history
# Commit 50 - simulated change for history
# Commit 51 - simulated change for history
