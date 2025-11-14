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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables first
load_dotenv()

# Add current directory to path to import demo_ai_agent
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import demo_ai_agent - wrap in try/except to catch import errors
try:
    from demo_ai_agent import run_demo
    logger.info("Successfully imported demo_ai_agent")
except Exception as e:
    logger.error(f"Failed to import demo_ai_agent: {e}")
    run_demo = None

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
        if not run_demo:
            raise HTTPException(status_code=500, detail="AI agent module not available")
        
        if not request.url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        # Validate URL
        if not request.url.startswith(('http://', 'https://')):
            request.url = 'https://' + request.url
        
        logger.info(f"Analyzing website: {request.url}")
        
        # Run the agent analysis in a thread pool to avoid blocking
        # (Playwright sync API needs to run outside asyncio context)
        import asyncio
        import re
        import json
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_demo, request.url)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to analyze website")
        
        # Try to extract structured data from the result
        analysis_data = {
            "url": request.url,
            "status": "analyzed"
        }
        
        # Try to extract title from result
        title_match = re.search(r'"title":\s*"([^"]+)"', result)
        if title_match:
            analysis_data["title"] = title_match.group(1)
        
        # Try to extract links count
        links_match = re.search(r'"links_count":\s*(\d+)', result)
        if links_match:
            analysis_data["links_count"] = int(links_match.group(1))
        
        # Try to extract has_navigation
        nav_match = re.search(r'"has_navigation":\s*(true|false)', result)
        if nav_match:
            analysis_data["has_navigation"] = nav_match.group(1) == "true"
        
        # Try to extract has_main_content
        main_match = re.search(r'"has_main_content":\s*(true|false)', result)
        if main_match:
            analysis_data["has_main_content"] = main_match.group(1) == "true"
        
        # Try to extract page_type
        page_type_match = re.search(r'"page_type":\s*"([^"]+)"', result)
        if page_type_match:
            analysis_data["page_type"] = page_type_match.group(1)
        
        # Extract patterns from the response
        patterns = []
        pattern_blocks = re.findall(r'\*\*Pattern \d+:([^*]+)\*\*', result, re.DOTALL)
        for i, block in enumerate(pattern_blocks, 1):
            if block.strip():
                patterns.append({
                    "number": i,
                    "title": block.split('\n')[0].strip() if block.split('\n') else f"Pattern {i}",
                    "description": block.strip()[:500]  # First 500 chars
                })
        
        # If no patterns found in that format, try numbered list format
        if not patterns:
            numbered_patterns = re.findall(r'(\d+)\.\s+\*\*?([^*]+)\*\*?', result)
            for num, title in numbered_patterns[:7]:
                patterns.append({
                    "number": int(num),
                    "title": title.strip(),
                    "description": ""
                })
        
        return AnalyzeResponse(
            success=True,
            full_response=result,
            analysis=analysis_data,
            patterns=patterns
        )
        
    except Exception as e:
        logger.error(f"Error analyzing website: {str(e)}")
        return AnalyzeResponse(
            success=False,
            error=str(e)
        )


@app.get("/api/health")
def health():
    return {"status": "ok"}


# App is now ready to be served by uvicorn
# When Railway runs: uvicorn api_server:app --host 0.0.0.0 --port $PORT
# The 'app' object will be used

if __name__ == "__main__":
    import uvicorn
    # Railway provides PORT environment variable
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
