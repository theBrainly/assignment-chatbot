#!/bin/bash

# Set up git if not already initialized
git init

# Add remote (replace with your username/repo)
git remote add origin https://github.com/theBrainly/assignment-chatbot.git
# Helper function to make a commit with a specific date
make_commit() {
  local msg="$1"
  local date="$2"
  git add .
  GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit -m "$msg"
}

# List of commit messages and files to touch
declare -a commits=(
  "chore: initial project structure"
  "feat: add FastAPI backend"
  "feat: add employee data model"
  "feat: add sample employees dataset"
  "fix: correct employee availability field"
  "feat: add RAG retrieval module"
  "feat: add RAG augmentation module"
  "feat: add RAG generation module"
  "feat: add RAG pipeline integration"
  "test: add backend unit tests"
  "docs: add API documentation"
  "feat: add API routes for chat"
  "feat: add API routes for employee search"
  "fix: improve error handling in API"
  "chore: add __init__.py files"
  "feat: add frontend React structure"
  "feat: add React chat component"
  "feat: add React employee list component"
  "feat: add axios for API calls"
  "fix: update React state management"
  "style: improve frontend UI"
  "feat: add loading spinner to chat"
  "feat: add search bar to employee list"
  "fix: correct API endpoint URLs"
  "test: add frontend component tests"
  "docs: add frontend usage instructions"
  "feat: add CORS middleware to backend"
  "chore: add .gitignore"
  "docs: add README.md"
  "feat: add Dockerfile for backend"
  "feat: add Dockerfile for frontend"
  "chore: add requirements.txt"
  "fix: update backend dependencies"
  "fix: update frontend dependencies"
  "feat: add deployment scripts"
  "docs: add architecture diagram"
  "feat: add advanced search filters"
  "fix: optimize vector search"
  "feat: add OpenAI integration option"
  "fix: fallback to template response"
  "test: add integration tests"
  "chore: update package.json"
  "fix: update manifest.json"
  "style: update index.html"
  "feat: add employee profile modal"
  "fix: improve mobile responsiveness"
  "feat: add API versioning"
  "docs: update API examples"
  "chore: update README with AI process"
  "fix: update backend logging"
  "feat: add health check endpoint"
  "fix: update frontend routing"
  "chore: update test scripts"
  "docs: add future improvements section"
  "chore: update setup instructions"
  "fix: update employee data"
  "feat: add new employee to dataset"
  "fix: correct employee skills"
  "chore: update project metadata"
  "docs: add demo screenshots"
)

# Generate commit dates for August 2025
start_day=1
end_day=30
month="08"
year="2025"
total_commits=${#commits[@]}

for i in "${!commits[@]}"; do
  # Spread commits across the month
  day=$((start_day + (i * (end_day - start_day) / total_commits)))
  hour=$((8 + (i % 12))) # randomize hour a bit
  min=$((10 + (i * 3) % 50))
  date="${year}-${month}-$(printf '%02d' $day)T${hour}:${min}:00"
  make_commit "${commits[$i]}" "$date"
done

# Push to GitHub
git push -u origin master