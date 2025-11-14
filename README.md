# AI Agent Browser Automation Demo

A complete demo showcasing an AI agent that browses websites, analyzes their structure, and generates realistic user behavior patterns.

## 🎯 What This Demo Shows

- ✅ AI agent that autonomously browses websites
- ✅ Analyzes page structure (links, navigation, content)
- ✅ Generates site-specific user behavior patterns
- ✅ Beautiful React frontend for testing
- ✅ FastAPI backend for API integration

## 📁 Project Structure

```
ai_agent_demo/
├── backend/
│   ├── demo_ai_agent.py      # Core AI agent logic
│   ├── api_server.py          # FastAPI backend server
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables (create this)
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Styles
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Run backend server
python api_server.py
```

Backend will run on `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on `http://localhost:3000`

### 3. Use the Demo

1. Open `http://localhost:3000` in your browser
2. Enter a website URL (e.g., `https://metro-manhattan.com`)
3. Click "Analyze Website"
4. Wait 30-60 seconds for analysis
5. View generated behavior patterns!

## 🎨 Features

### Frontend
- Clean, modern UI
- Real-time loading states
- Error handling
- Display of analysis results
- Pattern visualization

### Backend
- FastAPI REST API
- CORS enabled for frontend
- Error handling
- OpenAI GPT-4o-mini integration
- Playwright browser automation

## 📊 Example Output

After analyzing a website, you'll see:

**Page Analysis:**
- Page title
- Number of links
- Navigation structure
- Content areas

**Generated Patterns:**
1. Pattern 1: Click "Listings" → Wait 3s → Scroll → Click listing
2. Pattern 2: Click "Commercial Space" → Wait 2s → Click "Office Space"
3. ...and more site-specific patterns

## 🔧 Configuration

### Environment Variables

Create `backend/.env`:
```env
OPENAI_API_KEY=sk-proj-...
```

### Customization

- **Change demo URL**: Edit `frontend/src/App.jsx` default URL
- **Adjust agent behavior**: Edit `backend/demo_ai_agent.py`
- **Modify API endpoint**: Edit `backend/api_server.py`

## 💡 How It Works

1. **User enters URL** in React frontend
2. **Frontend sends POST** to `/api/analyze`
3. **Backend runs AI agent** with LangChain + Playwright
4. **Agent browses site**, analyzes structure
5. **Agent generates patterns** using GPT-4o-mini
6. **Results returned** to frontend
7. **Frontend displays** analysis and patterns

## 📝 API Endpoints

### POST `/api/analyze`
Analyze a website and generate patterns.

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "url": "https://example.com",
    "status": "analyzed"
  },
  "full_response": "Generated patterns...",
  "patterns": []
}
```

## 🐛 Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Verify OPENAI_API_KEY is set in .env
- Ensure all dependencies are installed

**Frontend won't start:**
- Run `npm install` again
- Check if port 3000 is available
- Clear node_modules and reinstall

**Agent fails:**
- Check OpenAI API key is valid
- Verify Playwright browser is installed
- Check website URL is accessible

## 🚢 Production Deployment

For production:
1. Build frontend: `npm run build`
2. Serve frontend static files via nginx
3. Deploy backend to cloud (Railway, Render, etc.)
4. Update CORS settings in `api_server.py`
5. Set environment variables on hosting platform

## 📚 Learn More

- [AI Agent Tutorial](./AI_AGENT_TUTORIAL.md)
- [Quick Start Guide](./QUICK_START.md)
- [LangChain Documentation](https://python.langchain.com/)
- [Playwright Documentation](https://playwright.dev/)

## 📞 Support

For questions or issues, check the tutorial documentation or reach out to the developer.

---

**Built with:** React + Vite + FastAPI + LangChain + Playwright + OpenAI GPT-4o-mini
