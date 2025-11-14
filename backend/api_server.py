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
        
        # Try to find and parse the JSON structure from analyze_page output
        # The JSON is embedded in the response, we need to extract it carefully
        # Find JSON block that contains "title" and "links_count"
        
        logger.info("Attempting to extract JSON analysis data from agent response")
        logger.info(f"Result length: {len(result)}, First 1000 chars: {result[:1000]}")
        
        # Strategy 1: Look for JSON block starting with { and containing "title"
        # This handles both single-line and multi-line formatted JSON
        json_extracted = False
        
        # Try multiple patterns to find JSON block
        # Pattern 1: { followed by "title" on same line
        json_start_match = re.search(r'\{\s*"title"', result, re.MULTILINE)
        
        # Pattern 2: { followed by "title" on next line (formatted JSON with indentation)
        if not json_start_match:
            json_start_match = re.search(r'\{\s*\n\s*"title"', result, re.MULTILINE)
        
        # Pattern 3: Look for JSON after "Observation:" or in code blocks
        if not json_start_match:
            # Find any { that might be followed by title (with potential whitespace/newlines)
            json_start_match = re.search(r'\{\s*[\s\n]*"title"', result, re.MULTILINE | re.DOTALL)
        
        # Pattern 4: Look for JSON structure anywhere - be more flexible
        if not json_start_match:
            # Just look for any { that contains title somewhere nearby
            json_start_match = re.search(r'\{[^}]*"title"', result, re.MULTILINE | re.DOTALL)
        
        if json_start_match:
            start_pos = json_start_match.start()
            # Count braces to find the complete JSON block
            brace_count = 0
            in_string = False
            escape_next = False
            end_pos = start_pos
            
            for i in range(start_pos, len(result)):
                char = result[i]
                
                if escape_next:
                    escape_next = False
                    continue
                
                if char == '\\':
                    escape_next = True
                    continue
                
                if char == '"' and not escape_next:
                    in_string = not in_string
                    continue
                
                if not in_string:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_pos = i + 1
                            break
            
            if end_pos > start_pos:
                json_str = result[start_pos:end_pos]
                try:
                    page_info = json.loads(json_str)
                    if "title" in page_info and "links_count" in page_info:
                        analysis_data.update({
                            "title": page_info.get("title", ""),
                            "links_count": page_info.get("links_count", 0),
                            "has_navigation": page_info.get("has_navigation", False),
                            "has_main_content": page_info.get("has_main_content", False),
                            "page_type": page_info.get("page_type", "")
                        })
                        json_extracted = True
                        logger.info(f"✓ Successfully extracted JSON block: {analysis_data}")
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON decode error: {e}, trying regex fallback")
        
        # Strategy 2: ALWAYS try regex extraction to fill in any missing fields
        # This handles cases where JSON is embedded in text or formatted differently
        # Run regex extraction even if JSON block extraction succeeded, to ensure all fields are captured
        logger.info("Running regex extraction to ensure all fields are captured")
        
        # Extract title - handle escaped quotes, may span multiple lines in formatted JSON
        # Match: "title": "value" or "title" : "value" (with spaces)
        if "title" not in analysis_data or not analysis_data.get("title") or analysis_data.get("title") == "Not extracted":
            title_pattern = r'"title"\s*:\s*"((?:[^"\\]|\\.)*)"'
            title_match = re.search(title_pattern, result, re.DOTALL)
            if title_match:
                title = title_match.group(1).replace('\\"', '"').replace('\\n', ' ').replace('\\', '').strip()
                if title and title != 'No title found':
                    analysis_data["title"] = title
                    logger.info(f"✓ Extracted title via regex: {title[:50]}...")
        
        # Extract links_count - be more flexible with whitespace
        if "links_count" not in analysis_data or not analysis_data.get("links_count"):
            links_pattern = r'"links_count"\s*:\s*(\d+)'
            links_match = re.search(links_pattern, result)
            if links_match:
                analysis_data["links_count"] = int(links_match.group(1))
                logger.info(f"✓ Extracted links_count via regex: {analysis_data['links_count']}")
        
        # Extract has_navigation - handle whitespace variations
        if "has_navigation" not in analysis_data:
            nav_pattern = r'"has_navigation"\s*:\s*(true|false)'
            nav_match = re.search(nav_pattern, result, re.IGNORECASE)
            if nav_match:
                analysis_data["has_navigation"] = nav_match.group(1).lower() == "true"
                logger.info(f"✓ Extracted has_navigation via regex: {analysis_data['has_navigation']}")
        
        # Extract has_main_content - handle whitespace variations
        if "has_main_content" not in analysis_data:
            main_pattern = r'"has_main_content"\s*:\s*(true|false)'
            main_match = re.search(main_pattern, result, re.IGNORECASE)
            if main_match:
                analysis_data["has_main_content"] = main_match.group(1).lower() == "true"
                logger.info(f"✓ Extracted has_main_content via regex: {analysis_data['has_main_content']}")
        
        # Extract page_type
        if "page_type" not in analysis_data or not analysis_data.get("page_type"):
            page_type_pattern = r'"page_type"\s*:\s*"((?:[^"\\]|\\.)*)"'
            page_type_match = re.search(page_type_pattern, result)
            if page_type_match:
                page_type = page_type_match.group(1).replace('\\"', '"').replace('\\n', ' ').replace('\\', '').strip()
                if page_type:
                    analysis_data["page_type"] = page_type
                    logger.info(f"✓ Extracted page_type via regex: {analysis_data['page_type']}")
        
        # Log final analysis data
        logger.info(f"Final analysis data: {analysis_data}")
        
        # Extract patterns from the response - look for **Pattern X: Title** format
        patterns = []
        logger.info("Attempting to extract patterns from response")
        
        # Match pattern blocks: **Pattern X: Title** followed by steps
        pattern_regex = r'\*\*Pattern (\d+):\s*([^*]+)\*\*(.*?)(?=\*\*Pattern \d+:|$)'
        pattern_matches = re.findall(pattern_regex, result, re.DOTALL)
        logger.info(f"Found {len(pattern_matches)} patterns with **Pattern format")
        
        for num_str, title, content in pattern_matches:
            # Extract steps from content (lines starting with -)
            steps = [line.strip() for line in content.split('\n') if line.strip().startswith('-')]
            
            patterns.append({
                "number": int(num_str),
                "title": title.strip(),
                "steps": steps,
                "description": content.strip()[:1000]  # First 1000 chars for full details
            })
            logger.info(f"✓ Extracted Pattern {num_str}: {title.strip()} ({len(steps)} steps)")
        
        # If no patterns found in that format, try numbered list format
        if not patterns:
            logger.info("Trying numbered list format for patterns")
            numbered_patterns = re.findall(r'(\d+)\.\s+\*\*?([^*]+)\*\*?(.*?)(?=\d+\.\s+\*\*|$)', result, re.DOTALL)
            logger.info(f"Found {len(numbered_patterns)} patterns with numbered list format")
            for num, title, content in numbered_patterns[:7]:
                steps = [line.strip() for line in content.split('\n') if line.strip().startswith('-')]
                patterns.append({
                    "number": int(num),
                    "title": title.strip(),
                    "steps": steps,
                    "description": content.strip()[:1000]
                })
                logger.info(f"✓ Extracted Pattern {num}: {title.strip()} ({len(steps)} steps)")
        
        logger.info(f"Total patterns extracted: {len(patterns)}")
        
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
