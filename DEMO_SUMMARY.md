# AI Agent Browser Automation - Demo Package

## 📦 What's Included

This package contains a complete, working demo of the AI agent browser automation system we discussed.

### 🎯 Demo Components

1. **React Frontend** (`frontend/`)
   - Beautiful, modern UI
   - Enter any website URL
   - View analysis and generated patterns
   - Real-time loading states

2. **FastAPI Backend** (`backend/`)
   - REST API endpoint
   - Integrates AI agent
   - Handles website analysis
   - Returns structured results

3. **AI Agent Core** (`backend/demo_ai_agent.py`)
   - LangChain + Playwright integration
   - GPT-4o-mini for pattern generation
   - Browser automation tools
   - Structure analysis

4. **Documentation**
   - Complete setup guide
   - API documentation
   - Tutorial explaining concepts

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)

```bash
cd ai_agent_demo
./setup.sh          # Install all dependencies
./start.sh          # Start backend + frontend
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
echo "OPENAI_API_KEY=your_key" > .env
python api_server.py
```

**Frontend (new terminal):**
```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser.

## 🎬 Demo Flow

1. User enters URL in React app
2. Frontend sends request to API
3. Backend runs AI agent
4. Agent browses website with Playwright
5. Agent analyzes structure
6. Agent generates patterns with GPT
7. Results displayed in UI

## 📊 Example Results

**Analyzed:** `https://metro-manhattan.com`

**Generated Patterns:**
1. Click "Listings" → Wait 3s → Scroll → Click listing → Wait 2s
2. Click "Commercial Space" → Wait 2s → Click "Office Space" → Wait 3s
3. Click "Contact Us" → Wait 2s → Fill form → Wait 1s
4. Click logo → Wait 1s → Scroll to featured listings
5. Click search bar → Wait 1s → Type query → Wait 2s

## 💰 Cost Analysis

- **Per website analysis:** ~$0.01 (GPT-4o-mini)
- **100 websites:** ~$1
- **1000 websites:** ~$10 (one-time)
- **After generation:** Patterns can be reused indefinitely (no cost)

## 🎯 Next Steps

1. **Test on multiple sites** - Try different websites
2. **Generate pattern database** - Store patterns for your top domains
3. **Integrate with scraping** - Use patterns in your mention monitoring pipeline
4. **Scale up** - Generate patterns for 100+ sites

## 📝 Files Structure

```
ai_agent_demo/
├── README.md                    # Main documentation
├── setup.sh                     # Setup script
├── start.sh                     # Start script
├── backend/
│   ├── demo_ai_agent.py        # Core AI agent
│   ├── api_server.py           # FastAPI server
│   ├── requirements.txt        # Python deps
│   └── .env                    # API keys (create this)
└── frontend/
    ├── src/
    │   ├── App.jsx             # Main React component
    │   └── index.css           # Styles
    ├── package.json            # Node deps
    └── vite.config.js          # Vite config
```

## 🔧 Technology Stack

- **Frontend:** React + Vite
- **Backend:** FastAPI (Python)
- **AI:** LangChain + OpenAI GPT-4o-mini
- **Browser:** Playwright
- **Parsing:** BeautifulSoup

## ✨ Features

✅ Autonomous website browsing
✅ Structure analysis (links, navigation, content)
✅ Site-specific pattern generation
✅ Realistic timing delays
✅ Scroll behavior patterns
✅ Modern web UI
✅ REST API integration
✅ Error handling
✅ Cost-effective (GPT-4o-mini)

## 🎓 For Developers

See:
- `AI_AGENT_TUTORIAL.md` - Complete tutorial
- `QUICK_START.md` - Quick reference
- `README.md` - Full documentation

---

**Ready to test?** Run `./setup.sh` then `./start.sh` and visit `http://localhost:3000`!
