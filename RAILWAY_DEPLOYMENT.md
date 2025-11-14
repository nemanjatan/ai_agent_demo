# Railway Deployment Guide

## 🚂 Deploying AI Agent Demo to Railway

This guide covers deploying both the backend API and frontend to Railway.

## 📋 Prerequisites

1. Railway account (sign up at railway.app)
2. GitHub account (for connecting repository)
3. OpenAI API key

## 🎯 Deployment Options

### Option 1: Backend Only (Recommended for MVP)

Deploy just the API backend, then serve frontend separately or connect later.

### Option 2: Full Stack (Backend + Frontend)

Deploy both services as separate Railway services.

---

## 📦 Option 1: Deploy Backend Only

### Step 1: Prepare Repository

1. Push your code to GitHub:
```bash
cd ai_agent_demo
git init
git add .
git commit -m "Initial commit: AI Agent Demo"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will detect it's a Python project

### Step 3: Configure Build Settings

**Root Directory:** Set to `backend/`

**Build Command:**
```bash
pip install -r requirements.txt && playwright install chromium
```

**Start Command:**
```bash
python api_server.py
```

### Step 4: Set Environment Variables

In Railway dashboard, go to **Variables** tab:

```
OPENAI_API_KEY=sk-proj-...
PORT=8000  # Railway auto-sets this, but good to have
```

### Step 5: Deploy

1. Railway will auto-deploy on push
2. Wait for build to complete
3. Get your Railway URL (e.g., `https://your-app.railway.app`)

### Step 6: Update CORS

Once deployed, update `api_server.py` with your Railway frontend URL:

```python
allowed_origins = [
    "http://localhost:3000",
    "https://your-frontend.railway.app"  # Add your frontend URL
]
```

---

## 🎨 Option 2: Deploy Full Stack (Backend + Frontend)

### Step 2A: Deploy Backend

Follow **Option 1** steps above, but keep root directory as project root.

### Step 2B: Deploy Frontend (Separate Service)

1. In same Railway project, click **+ New**
2. Select **Empty Service**
3. Connect to same GitHub repo
4. Set **Root Directory:** `frontend/`

**Build Settings:**
- **Build Command:** `npm install && npm run build`
- **Start Command:** `npm run preview`

**Environment Variables:**
```
VITE_API_URL=https://your-backend.railway.app
```

### Step 2C: Update Frontend API URL

Create `frontend/.env.production`:
```
VITE_API_URL=https://your-backend.railway.app
```

Update `frontend/src/App.jsx`:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

---

## 🔧 Railway Configuration Files

### `railway.json` (Project Root)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python backend/api_server.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `backend/Procfile`
```
web: python api_server.py
```

### `backend/runtime.txt`
```
python-3.10.0
```

---

## 🌍 Environment Variables

Set these in Railway dashboard:

### Required:
```
OPENAI_API_KEY=sk-proj-...
```

### Optional:
```
PORT=8000                    # Auto-set by Railway
FRONTEND_URL=https://...     # Your frontend URL
RAILWAY_ENVIRONMENT=production
```

---

## 🔍 Troubleshooting

### Issue: Playwright browser not found

**Solution:** Add to build command:
```bash
playwright install chromium --with-deps
```

Or create `backend/.railway/install.sh`:
```bash
#!/bin/bash
pip install -r requirements.txt
playwright install chromium
```

### Issue: Frontend can't connect to backend

**Solution:** 
1. Check CORS settings in `api_server.py`
2. Verify `VITE_API_URL` is set correctly
3. Check Railway service URLs

### Issue: Build fails

**Solution:**
1. Check Railway logs
2. Verify `requirements.txt` has all dependencies
3. Ensure Python version is compatible (3.10+)

### Issue: Memory limits

**Solution:**
- Railway free tier has memory limits
- Playwright can be memory-intensive
- Consider upgrading plan or optimizing

---

## 📊 Railway Service Structure

```
Railway Project: ai-agent-demo
├── Service 1: backend-api
│   ├── Root: backend/
│   ├── Port: 8000
│   └── URL: https://backend-xxx.railway.app
│
└── Service 2: frontend-app (optional)
    ├── Root: frontend/
    ├── Port: 3000
    └── URL: https://frontend-xxx.railway.app
```

---

## 🚀 Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Repository connected
- [ ] Environment variables set (OPENAI_API_KEY)
- [ ] Build settings configured
- [ ] Root directory set correctly
- [ ] Deployed successfully
- [ ] Tested API endpoint
- [ ] CORS configured (if frontend separate)

---

## 🔗 Testing After Deployment

### Test Backend API:

```bash
curl https://your-backend.railway.app/api/health
```

Expected: `{"status": "ok"}`

### Test Analysis Endpoint:

```bash
curl -X POST https://your-backend.railway.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## 💰 Railway Pricing

- **Hobby Plan:** $5/month - Good for testing
- **Pro Plan:** $20/month - Better for production
- **Free Tier:** Limited (check current offerings)

**Note:** Playwright requires significant resources. Free tier may have limits.

---

## 📝 Next Steps After Deployment

1. Test the deployed API
2. Update frontend to use Railway backend URL
3. Deploy frontend (if separate)
4. Configure custom domain (optional)
5. Set up monitoring/alerts
6. Optimize costs (if needed)

---

## 🆘 Support

If deployment fails:
1. Check Railway logs
2. Verify all dependencies in requirements.txt
3. Test locally first
4. Check Railway documentation

**Railway Docs:** https://docs.railway.app/
