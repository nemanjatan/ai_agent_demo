# 🚂 Railway Deployment - Quick Start

## Fastest Way to Deploy

### 1. Push to GitHub
```bash
cd ai_agent_demo
git init
git add .
git commit -m "AI Agent Demo for Railway"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway auto-detects Python project

### 3. Configure

**In Railway Dashboard:**

**Settings Tab:**
- **Root Directory:** `backend/`

**Variables Tab:**
Add environment variable:
```
OPENAI_API_KEY=sk-proj-...
```

**Deploy Tab:**
- Build will auto-start
- Wait ~2-3 minutes

### 4. Get Your URL

After deployment:
- Railway provides a public URL
- Example: `https://ai-agent-demo.railway.app`
- Test: `https://your-url.railway.app/api/health`

### 5. Update Frontend (If deploying frontend)

Create `frontend/.env.production`:
```
VITE_API_URL=https://your-backend.railway.app
```

---

## 🎯 Two-Service Setup (Backend + Frontend)

### Service 1: Backend API

1. **New Service** → **Deploy from GitHub**
2. **Root Directory:** `backend/`
3. **Variables:** `OPENAI_API_KEY=...`
4. **Get Backend URL**

### Service 2: Frontend

1. **New Service** → **Deploy from GitHub**
2. **Root Directory:** `frontend/`
3. **Variables:** `VITE_API_URL=https://your-backend.railway.app`
4. **Build Command:** `npm install && npm run build`
5. **Start Command:** `npx vite preview --host 0.0.0.0 --port $PORT`

---

## ✅ After Deployment

1. **Test Backend:**
```bash
curl https://your-backend.railway.app/api/health
```

2. **Test Analysis:**
```bash
curl -X POST https://your-backend.railway.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://metro-manhattan.com"}'
```

3. **Update Frontend** with backend URL if needed

---

## 🐛 Common Issues

**Playwright not installing?**
- Railway may need custom build script
- Check `backend/.railway/install.sh`

**Memory limits?**
- Playwright is resource-intensive
- Consider Railway Pro plan

**CORS errors?**
- Backend already configured for Railway
- Check frontend URL is correct

---

**Full guide:** See `RAILWAY_DEPLOYMENT.md` for detailed instructions.
