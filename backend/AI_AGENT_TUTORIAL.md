# AI Agent for Browser Automation - Tutorial & Demo

## 🎯 What We're Building

An AI agent that can:
1. Browse a website autonomously
2. Analyze its structure
3. Generate realistic user behavior patterns
4. Use those patterns to scrape like a real user

---

## 📚 Concepts Explained

### What is an AI Agent?

An **AI agent** is a program that:
- Makes decisions on its own (using LLM like GPT)
- Uses "tools" (like clicking buttons, scrolling)
- Has a goal ("analyze this website")
- Takes actions until the goal is achieved

### How It Works

```
User: "Browse example.com and analyze structure"
   ↓
AI Agent: "I need to load the page first"
   ↓
[Uses Tool: load_page("example.com")]
   ↓
AI Agent: "I see a menu with links. Let me click one."
   ↓
[Uses Tool: click_element("#menu-item-1")]
   ↓
AI Agent: "I found the content. Let me analyze structure."
   ↓
[Uses Tool: analyze_page()]
   ↓
AI Agent: "Done! Here are the patterns I learned."
```

### Key Components

1. **LLM (GPT-4o-mini)**: The "brain" that decides what to do
2. **Playwright**: The "hands" that actually does the clicking/scrolling
3. **LangChain**: The "orchestrator" that connects LLM + tools
4. **Tools**: Functions the agent can call (click, scroll, analyze)

---

## 🛠️ Setup

### Install Dependencies

```bash
pip install langchain langchain-openai playwright python-dotenv
playwright install chromium
```

### Environment Setup

Create `.env`:
```env
OPENAI_API_KEY=your_key_here
```

---

## 📝 Code Walkthrough

### Step 1: Basic Browser Tool

```python
from playwright.sync_api import sync_playwright

def load_page(url):
    """Load a webpage and return its HTML."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
        return html

# Test it
html = load_page("https://example.com")
print(len(html))  # Should print HTML length
```

### Step 2: Click Tool

```python
def click_element(selector, url):
    """Click an element on a page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.click(selector)
        html = page.content()
        browser.close()
        return html

# Test it
html = click_element("a", "https://example.com")
```

### Step 3: Scroll Tool

```python
def scroll_page(url, pixels=500):
    """Scroll the page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.evaluate(f"window.scrollBy(0, {pixels})")
        html = page.content()
        browser.close()
        return html
```

### Step 4: Analysis Tool

```python
from bs4 import BeautifulSoup

def analyze_page(url):
    """Analyze page structure and extract key elements."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
    
    soup = BeautifulSoup(html, 'lxml')
    
    # Find all clickable elements
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    buttons = [btn.text for btn in soup.find_all(['button', 'a'])]
    
    # Get page structure
    structure = {
        'title': soup.find('title').text if soup.find('title') else None,
        'links_count': len(links),
        'buttons': buttons[:10],  # First 10
        'has_menu': bool(soup.find('nav') or soup.find(class_='menu')),
        'main_content': soup.find('main') is not None or soup.find('article') is not None
    }
    
    return structure
```

### Step 5: Create AI Agent

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
import os
from dotenv import load_dotenv

load_dotenv()

# Create tools
tools = [
    Tool(
        name="load_page",
        func=lambda url: load_page(url),
        description="Load a webpage and return its HTML. Input: URL string"
    ),
    Tool(
        name="click_element",
        func=lambda x: click_element(x.split(",")[0], x.split(",")[1]),
        description="Click an element on a page. Input: 'selector,url'"
    ),
    Tool(
        name="scroll_page",
        func=lambda x: scroll_page(x.split(",")[0], int(x.split(",")[1])),
        description="Scroll a page. Input: 'url,pixels'"
    ),
    Tool(
        name="analyze_page",
        func=analyze_page,
        description="Analyze page structure. Input: URL string. Returns: dict with structure info"
    ),
]

# Create agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  # Shows agent's thinking process
)

# Use it!
result = agent.run("Browse https://example.com and analyze its structure")
print(result)
```

---

## 🎬 Full Demo Script

```python
# demo_ai_agent.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Browser tools
def load_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle', timeout=30000)
        html = page.content()
        title = page.title()
        browser.close()
        return f"Page loaded: {title}. HTML length: {len(html)} characters."

def click_element(selector_and_url):
    selector, url = selector_and_url.split("|")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        try:
            page.click(selector, timeout=5000)
            page.wait_for_load_state('networkidle')
            html = page.content()
            browser.close()
            return f"Clicked {selector}. Page updated. HTML length: {len(html)}"
        except:
            browser.close()
            return f"Could not click {selector}"

def analyze_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        html = page.content()
        browser.close()
    
    soup = BeautifulSoup(html, 'lxml')
    
    # Extract structure
    links = [a.get('href', '') for a in soup.find_all('a', href=True)[:20]]
    buttons = [btn.text.strip() for btn in soup.find_all(['button', 'a']) if btn.text.strip()][:10]
    
    structure = {
        'title': soup.find('title').text if soup.find('title') else 'No title',
        'links_count': len([a for a in soup.find_all('a', href=True)]),
        'sample_links': links[:5],
        'sample_buttons': buttons[:5],
        'has_navigation': bool(soup.find('nav') or soup.find(class_='menu') or soup.find('header')),
        'has_article': bool(soup.find('article') or soup.find('main'))
    }
    
    return json.dumps(structure, indent=2)

# Create tools
tools = [
    Tool(
        name="load_page",
        func=load_page,
        description="Load a webpage. Input: URL as string. Returns: confirmation message with page title."
    ),
    Tool(
        name="click_element",
        func=click_element,
        description="Click an element on a page. Input: 'selector|url' (e.g., 'a.article-link|https://example.com'). Returns: confirmation."
    ),
    Tool(
        name="analyze_page",
        func=analyze_page,
        description="Analyze page structure and extract key information. Input: URL string. Returns: JSON with structure data."
    ),
]

# Create agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=5  # Limit to prevent infinite loops
)

# Demo task
print("=" * 60)
print("AI AGENT DEMO: Browser Automation")
print("=" * 60)
print()

task = """
Browse the website https://example.com and analyze its structure.
Tell me:
1. What is the page title?
2. How many links are there?
3. What are some key elements you found?
4. Based on your analysis, suggest 3 realistic user behavior patterns (e.g., "Click on a link, scroll down, wait 2 seconds")
"""

result = agent.run(task)
print()
print("=" * 60)
print("RESULT:")
print("=" * 60)
print(result)
```

---

## 🚀 How to Run the Demo

1. **Install dependencies:**
```bash
pip install langchain langchain-openai playwright beautifulsoup4 python-dotenv
playwright install chromium
```

2. **Set up environment:**
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

3. **Run the demo:**
```bash
python demo_ai_agent.py
```

---

## 📊 What the Demo Shows

The agent will:
1. ✅ Load the page
2. ✅ Analyze its structure
3. ✅ Extract key information
4. ✅ Generate behavior patterns based on what it found

**Example Output:**
```
Page title: Example Domain
Links found: 2
Key elements: Navigation menu, main content area
Suggested patterns:
1. Click on a link → Wait 2s → Scroll down
2. Scroll down → Click article link → Wait 3s
3. Click menu → Wait 1s → Click submenu → Scroll
```

---

## 🎓 Key Learnings

1. **Agent = LLM + Tools**: The AI decides what to do, tools execute
2. **Tools are functions**: Simple Python functions the agent can call
3. **Agent is goal-oriented**: It breaks down tasks into steps
4. **Verbose mode**: Shows agent's thinking process

---

## 🔧 Next Steps

1. **Test on real websites** (your mention monitoring sites)
2. **Generate pattern database** (store patterns from multiple sites)
3. **Integrate with your pipeline** (use patterns during scraping)
4. **Add more tools** (hover, type text, handle popups)

---

## 💡 Tips for Vladimir Demo

1. **Start simple**: Test on example.com first
2. **Show verbose output**: Let him see the agent thinking
3. **Generate patterns**: Show actual behavior patterns created
4. **Compare costs**: Show token usage vs. manual pattern creation
5. **Highlight speed**: One agent can analyze 10 sites in ~30 minutes

---

## ⚠️ Common Issues

**Issue**: Agent gets stuck in loops
**Fix**: Set `max_iterations=5` to limit steps

**Issue**: Costs too high
**Fix**: Use GPT-4o-mini (cheaper), clean HTML before analysis

**Issue**: Agent makes wrong decisions
**Fix**: Give clearer instructions, add more specific tools

---

Ready to test? Run the demo and let me know how it goes!

