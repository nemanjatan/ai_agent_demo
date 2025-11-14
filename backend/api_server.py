"""
FastAPI backend server for AI Agent Demo
Provides API endpoint to analyze websites and generate behavior patterns
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import sys

# Add parent directory to path to import demo_ai_agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from demo_ai_agent import run_demo

load_dotenv()

app = FastAPI(title="AI Agent Browser Automation API")

# CORS middleware - Allow all origins for Railway deployment
# In production, you should restrict this to your frontend domain
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.getenv("FRONTEND_URL", "*")  # Railway frontend URL
]

if os.getenv("RAILWAY_ENVIRONMENT"):
    # In Railway, allow all origins (you can restrict later)
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    url: str


class AnalyzeResponse(BaseModel):
    success: bool
    analysis: dict = None
    patterns: list = None
    full_response: str = None
    error: str = None


@app.get("/")
def root():
    return {"message": "AI Agent Browser Automation API", "version": "1.0.0"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_website(request: AnalyzeRequest):
    """
    Analyze a website and generate user behavior patterns.
    """
    try:
        if not request.url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        # Validate URL
        if not request.url.startswith(('http://', 'https://')):
            request.url = 'https://' + request.url
        
        print(f"Analyzing website: {request.url}")
        
        # Run the agent analysis
        result = run_demo(request.url)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to analyze website")
        
        # Parse the result
        # The result is a string, we need to extract structured data
        # For now, return the full response
        return AnalyzeResponse(
            success=True,
            full_response=result,
            analysis={
                "url": request.url,
                "status": "analyzed"
            },
            patterns=[]  # Can be parsed from result if needed
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return AnalyzeResponse(
            success=False,
            error=str(e)
        )


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    # Railway provides PORT environment variable
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
