
# Run script for FastAPI backend

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import and run the backend
from backend.main import app
import uvicorn

if __name__ == "__main__":
    print("Starting Resume Skill Gap Analyzer API...")
    print("API will be available at: http://localhost:8000")
    print("API docs available at: http://localhost:8000/docs")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
