# Quick Start - AI Agent Demo

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r agent_requirements.txt
playwright install chromium
```

### Step 2: Set Up Environment

Create a `.env` file:
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

Or manually create `.env`:
```
OPENAI_API_KEY=sk-proj-...
```

### Step 3: Run the Demo

```bash
python demo_ai_agent.py
```

### Step 4: Watch the Magic! ✨

The agent will:
1. Load the page
2. Analyze structure
3. Generate behavior patterns

---

## 🎯 What You'll See

```
AI AGENT DEMO: Browser Automation & Pattern Generation
======================================================================

Target URL: https://example.com

Agent will:
1. Load and analyze the webpage
2. Extract structure information
3. Generate realistic user behavior patterns

AGENT THINKING PROCESS:
======================================================================

> Entering new AgentExecutor chain...
I need to analyze the website and generate behavior patterns.
First, I'll load the page to see what we're working with.
Action: load_page
Action Input: https://example.com
Observation: Page loaded successfully. Title: 'Example Domain'...

[Agent continues thinking and taking actions]

FINAL RESULT:
======================================================================
Based on my analysis of https://example.com:
...
3 realistic user behavior patterns:
1. Click on a link → Wait 2 seconds → Scroll down 300px
2. Load page → Wait 1 second → Scroll to bottom → Wait 3 seconds
3. Click navigation menu → Wait 1.5s → Click submenu → Wait 2s
```

---

## 🧪 Try Different Websites

Edit `demo_ai_agent.py` and change:
```python
demo_url = "https://example.com"  # Change this!
```

Or test with your mention monitoring sites:
```python
demo_url = "https://www.hostinger.com/reviews"
```

---

## 💡 Tips

1. **Start with simple sites** (example.com) to understand the flow
2. **Check verbose output** to see how the agent thinks
3. **Note the patterns** generated - these are what Vladimir wants!
4. **Watch costs** - GPT-4o-mini is cheap, but monitor usage

---

## ❓ Troubleshooting

**Error: OPENAI_API_KEY not found**
→ Create `.env` file with your API key

**Error: playwright not found**
→ Run `playwright install chromium`

**Agent gets stuck**
→ Edit `max_iterations=10` to a lower number (like 5)

**Too expensive**
→ Already using GPT-4o-mini (cheapest option)

---

## 📝 Next Steps After Demo Works

1. **Test on real sites** from your mention monitoring project
2. **Store patterns** in PostgreSQL database
3. **Integrate with scraping** pipeline
4. **Show Vladimir** the demo + generated patterns

---

Ready? Run `python demo_ai_agent.py` and see it work! 🎉

