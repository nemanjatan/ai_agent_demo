"""
AI Agent Demo - Browser Automation
This script demonstrates how an AI agent can browse websites and generate behavior patterns.
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain import hub
import os
from dotenv import load_dotenv
import json
import time

# Import AgentExecutor and create_react_agent with fallback for different LangChain versions
try:
    from langchain.agents import AgentExecutor, create_react_agent
except ImportError:
    try:
        # Try newer import paths for LangChain 0.3+
        from langchain.agents.agent import AgentExecutor
        from langchain.agents.react.agent import create_react_agent
    except ImportError:
        # Final fallback
        from langchain.agents.agent import AgentExecutor
        from langchain.agents import create_react_agent

load_dotenv()

# ========================================
# Browser Tools (What the agent can do)
# ========================================

def load_page(url):
    """Load a webpage and return basic info."""
    try:
        # Strip quotes if present
        url = url.strip().strip("'\"")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle', timeout=30000)
            html = page.content()
            title = page.title()
            browser.close()
            return f"Page loaded successfully. Title: '{title}'. HTML content length: {len(html)} characters."
    except Exception as e:
        return f"Error loading page: {str(e)}"


def click_element(selector_and_url):
    """
    Click an element on a page.
    Input format: "selector|url" (e.g., "a.article-link|https://example.com")
    """
    try:
        # Strip quotes if present
        selector_and_url = selector_and_url.strip().strip("'\"")
        selector, url = selector_and_url.split("|")
        selector = selector.strip()
        url = url.strip().strip("'\"")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            try:
                page.click(selector, timeout=5000)
                page.wait_for_load_state('networkidle', timeout=10000)
                new_title = page.title()
                html = page.content()
                browser.close()
                return f"Successfully clicked '{selector}'. New page title: '{new_title}'. HTML length: {len(html)} characters."
            except Exception as e:
                browser.close()
                return f"Could not click '{selector}': {str(e)}"
    except Exception as e:
        return f"Error in click_element: {str(e)}"


def scroll_page(url_and_pixels):
    """
    Scroll the page.
    Input format: "url|pixels" (e.g., "https://example.com|500")
    """
    try:
        # Strip quotes if present
        url_and_pixels = url_and_pixels.strip().strip("'\"")
        url, pixels = url_and_pixels.split("|")
        url = url.strip().strip("'\"")
        pixels = int(pixels.strip())
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            page.evaluate(f"window.scrollBy(0, {pixels})")
            time.sleep(0.5)  # Small delay to simulate human behavior
            html = page.content()
            browser.close()
            return f"Scrolled {pixels} pixels. Page content length: {len(html)} characters."
    except Exception as e:
        return f"Error scrolling: {str(e)}"


def analyze_page(url):
    """
    Analyze page structure and extract key information.
    Returns JSON string with structure data.
    """
    try:
        # Strip quotes if present
        url = url.strip().strip("'\"")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle', timeout=30000)
            html = page.content()
            browser.close()
        
        soup = BeautifulSoup(html, 'lxml')
        
        # Extract structure
        all_links = soup.find_all('a', href=True)
        links = [a.get('href', '') for a in all_links[:20]]
        
        buttons = []
        for btn in soup.find_all(['button', 'a']):
            text = btn.text.strip()
            if text and text not in buttons:
                buttons.append(text)
                if len(buttons) >= 10:
                    break
        
        # Find navigation
        has_nav = bool(soup.find('nav') or soup.find(class_='menu') or 
                      soup.find('header') or soup.find(id='menu'))
        
        # Find main content
        has_main = bool(soup.find('article') or soup.find('main') or 
                       soup.find(class_='content') or soup.find(id='content'))
        
        structure = {
            'title': soup.find('title').text.strip() if soup.find('title') else 'No title found',
            'links_count': len(all_links),
            'sample_links': links[:5],
            'sample_buttons': buttons[:5],
            'has_navigation': has_nav,
            'has_main_content': has_main,
            'page_type': 'article' if soup.find('article') else 'standard'
        }
        
        return json.dumps(structure, indent=2)
    except Exception as e:
        return f"Error analyzing page: {str(e)}"


# ========================================
# Create Tools for Agent
# ========================================
# Wrap Playwright sync functions to run in thread pool (needed for async FastAPI context)

from concurrent.futures import ThreadPoolExecutor
import functools

# Create a thread pool executor for Playwright operations
playwright_executor = ThreadPoolExecutor(max_workers=2)

def run_in_thread(func):
    """Decorator to run sync Playwright functions in a thread pool."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        future = playwright_executor.submit(func, *args, **kwargs)
        return future.result(timeout=60)  # 60 second timeout
    return wrapper

tools = [
    Tool(
        name="load_page",
        func=run_in_thread(load_page),
        description="Load a webpage and get basic information. Input: URL as string (e.g., 'https://example.com'). Returns: confirmation with page title and HTML length."
    ),
    Tool(
        name="click_element",
        func=run_in_thread(click_element),
        description="Click an element on a page. Input: 'selector|url' (e.g., 'a.article-link|https://example.com'). Use CSS selectors. Returns: confirmation message."
    ),
    Tool(
        name="scroll_page",
        func=run_in_thread(scroll_page),
        description="Scroll the page down. Input: 'url|pixels' (e.g., 'https://example.com|500'). Returns: confirmation."
    ),
    Tool(
        name="analyze_page",
        func=run_in_thread(analyze_page),
        description="Analyze page structure and extract key information like links, buttons, navigation, content areas. Input: URL as string. Returns: JSON with structure data including title, links count, sample links/buttons, navigation presence, main content presence."
    ),
]

# ========================================
# Create AI Agent
# ========================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Use newer LangChain API - create ReAct agent
try:
    # Try to pull the react prompt from hub
    prompt = hub.pull("hwchase17/react")
except Exception:
    # Fallback: use a simple prompt template
    from langchain.prompts import PromptTemplate
    prompt = PromptTemplate.from_template("""
You are a helpful assistant that can browse websites and analyze their structure.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Show agent's thinking process
    max_iterations=10,  # Limit to prevent infinite loops
    handle_parsing_errors=True
)


# ========================================
# Demo Task
# ========================================

def run_demo(url="https://example.com", verbose=False):
    """
    Run the AI agent demo.
    
    Args:
        url: Website URL to analyze
        verbose: If True, print detailed output (for CLI use)
    
    Returns:
        str: Generated behavior patterns
    """
    if verbose:
        print("=" * 70)
        print("AI AGENT DEMO: Browser Automation & Pattern Generation")
        print("=" * 70)
        print()
        print(f"Target URL: {url}")
        print()
        print("Agent will:")
        print("1. Load and analyze the webpage")
        print("2. Extract structure information")
        print("3. Generate realistic user behavior patterns")
        print()
        print("-" * 70)
        print("AGENT THINKING PROCESS:")
        print("-" * 70)
        print()
    
    task = f"""
    Browse the website {url} and analyze its structure.
    
    Please:
    1. Load the page and analyze its structure
    2. Extract key information (title, links count, navigation elements)
    3. Based on your analysis, generate 3-5 realistic user behavior patterns
    
    Each pattern should include:
    - Navigation sequence (e.g., "Click on a link → Wait 2 seconds → Scroll down")
    - Timing delays (realistic human delays)
    - Scroll behavior
    
    Format your response clearly with numbered patterns.
    """
    
    try:
        # Use agent_executor instead of deprecated agent
        result = agent_executor.invoke({"input": task})
        result_text = result.get("output", str(result))
        
        if verbose:
            print()
            print("=" * 70)
            print("FINAL RESULT:")
            print("=" * 70)
            print(result_text)
        
        return result_text
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        if verbose:
            print(error_msg)
        raise Exception(error_msg)


# ========================================
# Main
# ========================================

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with: OPENAI_API_KEY=your_key_here")
        exit(1)
    
    # Run demo
    # Using metro-manhattan.com as demo website
    demo_url = "https://metro-manhattan.com"
    
    print("\nStarting demo in 2 seconds...\n")
    time.sleep(2)
    
    result = run_demo(demo_url, verbose=True)
    
    print("\n" + "=" * 70)
    print("Demo completed!")
    print("=" * 70)
    print("\nNext steps:")
    print("- Try different websites")
    print("- Test on your mention monitoring sites")
    print("- Store patterns in database")
    print("- Integrate with scraping pipeline")
