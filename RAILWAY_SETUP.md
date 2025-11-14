# Railway Setup Instructions

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Code

```bash
cd ai_agent_demo
git init
git add .
git commit -m "AI Agent Demo ready for Railway"
```

### Step 2: Push to GitHub

```bash
# Create a new GitHub repository
# Then:
git remote add origin https://github.com/YOUR_USERNAME/ai-agent-demo.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Railway

#### A. Create New Project
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access GitHub
5. Select your repository: `ai-agent-demo`

#### B. Configure Backend Service

Railway should auto-detect Python project. Configure:

**Settings Tab:**
- **Root Directory:** `backend/` ⚠️ **IMPORTANT**
- **Build Command:** Leave empty (uses requirements.txt)
- **Start Command:** `python api_server.py`

**Variables Tab:**
Click **"New Variable"** and add:
```
OPENAI_API_KEY = sk-proj-...
```

**Optional Variables:**
```
PORT = 8000  # Railway auto-sets this
RAILWAY_ENVIRONMENT = production
```

#### C. Deploy

1. Railway auto-starts deployment
2. Wait 2-3 minutes for build
3. Check **Deploy** tab for logs
4. Get your public URL (e.g., `https://ai-agent-demo.railway.app`)

### Step 4: Test Deployment

```bash
# Health check
curl https://your-app.railway.app/api/health

# Should return: {"status": "ok"}
```

### Step 5: Deploy Frontend (Optional)

If you want to deploy the React frontend too:

1. In same Railway project, click **"+ New"**
2. Select **"Empty Service"**
3. **Settings:**
   - **Root Directory:** `frontend/`
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npx vite preview --host 0.0.0.0 --port $PORT`

4. **Variables:**
   ```
   VITE_API_URL = https://your-backend.railway.app
   PORT = 3000  # Railway auto-sets this
   ```

---

## 🔧 Railway Dashboard Configuration

### Backend Service Settings

```
Root Directory: backend/
Build Command: (leave empty - auto-detects)
Start Command: python api_server.py
Healthcheck Path: /api/health
```

### Environment Variables

Required:
- `OPENAI_API_KEY` - Your OpenAI API key

Auto-set by Railway:
- `PORT` - Port number (usually 8000+)
- `RAILWAY_ENVIRONMENT` - Set to "production"

---

## 🎯 Quick Test

Once deployed, test with:

```bash
curl -X POST https://your-app.railway.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://metro-manhattan.com"}'
```

---

## 📝 Important Notes

1. **Root Directory:** Must be `backend/` (not project root)
2. **Playwright:** May take extra time to install browser
3. **Memory:** Railway free tier may have limits with Playwright
4. **CORS:** Already configured to allow all origins in Railway
5. **Environment:** API detects Railway environment automatically

---

## 🐛 Troubleshooting

### Build fails: "Playwright not found"
- Add custom build command: `pip install -r requirements.txt && playwright install chromium`
- Or check `.railway/install.sh` is being used

### API returns 500
- Check Railway logs
- Verify OPENAI_API_KEY is set
- Test `/api/health` endpoint first

### Memory limit exceeded
- Playwright needs significant memory
- Consider upgrading Railway plan
- Or optimize Playwright settings

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Repository connected
- [ ] Root directory set to `backend/`
- [ ] OPENAI_API_KEY added as variable
- [ ] Deployed successfully
- [ ] `/api/health` returns `{"status": "ok"}`
- [ ] `/api/analyze` endpoint works
- [ ] Frontend configured (if deployed)

---

**Need help?** Check Railway logs in dashboard → Deploy tab
