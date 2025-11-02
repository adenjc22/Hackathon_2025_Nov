# Railway Deployment Guide for Memory Lane

## Prerequisites
- GitHub account
- Railway account (sign up at https://railway.app with GitHub)
- Your API keys ready (Azure Face API, OpenAI)

---

## Part 1: Push Your Code to GitHub

1. **Initialize Git (if not already done):**
```bash
git init
git add .
git commit -m "Prepare for Railway deployment"
```

2. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name it "memory-lane" or similar
   - Don't initialize with README (you already have one)

3. **Push your code:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

## Part 2: Deploy Backend on Railway

### Step 1: Create New Project
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your `memory-lane` repository

### Step 2: Configure Backend Service
1. Railway will detect multiple buildable directories
2. Click **"Add Service"** → **"GitHub Repo"**
3. Select your repository
4. In **"Settings"**:
   - **Root Directory**: `/backend`
   - **Build Command**: (leave empty, Railway auto-detects)
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables
1. Go to your backend service
2. Click **"Variables"** tab
3. Click **"+ New Variable"** and add:

```
FRONTEND_URL=https://your-frontend-url.railway.app
AZURE_FACE_KEY=your_azure_face_api_key
AZURE_FACE_ENDPOINT=your_azure_endpoint
OPENAI_API_KEY=your_openai_api_key
```

**Note:** You'll update `FRONTEND_URL` after deploying frontend (Step 4)

### Step 4: Generate Domain
1. Go to **"Settings"** tab
2. Scroll to **"Domains"**
3. Click **"Generate Domain"**
4. Copy the URL (e.g., `https://backend-production-abc123.railway.app`)

### Step 5: Deploy
- Railway will automatically deploy
- Wait 2-3 minutes for build to complete
- Check **"Deployments"** tab for status
- Once deployed, visit your backend URL - you should see the FastAPI welcome page

---

## Part 3: Deploy Frontend on Railway

### Step 1: Add Frontend Service
1. In the same Railway project, click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose the same repository

### Step 2: Configure Frontend Service
1. In **"Settings"**:
   - **Root Directory**: `/frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables
1. Click **"Variables"** tab
2. Add:

```
VITE_API_URL=https://your-backend-url.railway.app
```

Replace with your actual backend URL from Part 2, Step 4

### Step 4: Generate Domain
1. Go to **"Settings"** → **"Domains"**
2. Click **"Generate Domain"**
3. Copy the URL (e.g., `https://frontend-production-xyz789.railway.app`)

### Step 5: Update Backend CORS
1. Go back to **Backend service**
2. Click **"Variables"** tab
3. Update `FRONTEND_URL` with your frontend URL from Step 4
4. Backend will auto-redeploy with new CORS settings

---

## Part 4: Verify Deployment

### Test Your App:
1. **Visit your frontend URL**
2. **Create an account** (signup)
3. **Upload a photo**
4. **Check the dashboard**

### Troubleshooting:
- **Check logs**: Each service has a "Logs" tab - check for errors
- **CORS errors**: Make sure `FRONTEND_URL` in backend matches your frontend domain
- **API errors**: Verify `VITE_API_URL` in frontend matches your backend domain
- **Build fails**: Check "Deployments" tab for build logs

---

## Part 5: File Upload Storage (Important!)

⚠️ **Railway uses ephemeral storage** - uploaded files will be lost on redeployment!

### Solutions:

**Option A: Use Railway Volumes (Persistent Storage)**
1. In backend service, go to **"Volumes"** tab
2. Click **"+ New Volume"**
3. Mount path: `/app/uploads`
4. This persists your `backend/uploads/` folder

**Option B: Use Cloud Storage (Recommended for Production)**
- Use AWS S3, Cloudflare R2, or Backblaze B2
- Update `backend/app/services/storage.py` to upload to cloud
- Much more reliable for production

---

## Environment Variables Reference

### Backend Variables:
```
FRONTEND_URL=https://your-frontend.railway.app
AZURE_FACE_KEY=your_key_here
AZURE_FACE_ENDPOINT=https://your-region.api.cognitive.microsoft.com/
OPENAI_API_KEY=sk-proj-...
```

### Frontend Variables:
```
VITE_API_URL=https://your-backend.railway.app
```

---

## Railway Tips

- **Free Tier**: $5/month credit (~500 hours of runtime)
- **Auto-deploys**: Push to GitHub → automatically deploys
- **Logs**: Click any service → "Logs" tab for real-time logs
- **Cost**: Monitor usage in "Usage" tab
- **Custom Domain**: Add your own domain in Settings → Domains

---

## Quick Commands Cheat Sheet

### Redeploy:
```bash
git add .
git commit -m "Update"
git push
# Railway auto-deploys on push!
```

### View Logs Locally:
```bash
railway logs
```

### Open Service:
```bash
railway open
```

---

## Success Checklist

- [ ] Backend deployed with domain
- [ ] Frontend deployed with domain
- [ ] Environment variables set for both services
- [ ] Backend `FRONTEND_URL` matches frontend domain
- [ ] Frontend `VITE_API_URL` matches backend domain
- [ ] Can sign up and log in
- [ ] Can upload photos
- [ ] Photos appear in dashboard
- [ ] (Optional) Volume mounted for persistent uploads

---

## Next Steps After Deployment

1. **Share your live link!** 🎉
2. **Monitor Railway usage** - watch your $5 credit
3. **Add custom domain** (optional)
4. **Set up cloud storage** for production reliability
5. **Configure AI processing** with your colleague's API

---

Need help? Check Railway docs: https://docs.railway.app
