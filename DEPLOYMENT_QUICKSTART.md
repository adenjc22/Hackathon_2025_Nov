# 🚀 Quick Start: Railway Deployment

## What We Just Did

I've prepared your Memory Lane app for Railway deployment. Here's what changed:

### Backend Changes:
✅ Added `Procfile` - tells Railway how to run your app
✅ Added `railway.json` - Railway configuration
✅ Added `runtime.txt` - specifies Python 3.11
✅ Updated `main.py` - CORS now uses environment variables
✅ Added `.env.example` - template for environment variables

### Frontend Changes:
✅ Updated `api.js` - now uses `VITE_API_URL` environment variable
✅ Updated `vite.config.js` - production preview settings
✅ Added `.env.example` - template for frontend config

### Documentation:
✅ Created `RAILWAY_DEPLOYMENT.md` - complete step-by-step guide

---

## 🎯 Next Steps (Takes ~15 minutes)

### 1. Push to GitHub (5 min)
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push
```

### 2. Deploy on Railway (10 min)
1. Go to https://railway.app (sign up with GitHub)
2. Create new project from your GitHub repo
3. Deploy **Backend** first:
   - Set root directory: `/backend`
   - Add environment variables (see below)
   - Generate domain
4. Deploy **Frontend**:
   - Set root directory: `/frontend`
   - Add `VITE_API_URL` (your backend URL)
   - Generate domain
5. Update backend's `FRONTEND_URL` with frontend domain

### 3. Test Your Live App! 🎉

---

## 📝 Environment Variables You'll Need

### Backend:
```
FRONTEND_URL=https://your-frontend.railway.app
AZURE_FACE_KEY=your_azure_key
AZURE_FACE_ENDPOINT=your_azure_endpoint
OPENAI_API_KEY=your_openai_key
```

### Frontend:
```
VITE_API_URL=https://your-backend.railway.app
```

---

## 📖 Full Instructions

See `RAILWAY_DEPLOYMENT.md` for detailed step-by-step guide with screenshots descriptions.

---

## ⚠️ Important Notes

1. **File Uploads**: Railway has ephemeral storage. Uploaded files reset on redeploy.
   - **Solution**: Add a Railway Volume (persistent storage) in backend settings
   - Mount path: `/app/uploads`

2. **Free Tier**: Railway gives you $5/month credit (~500 hours)
   - Monitor usage in Railway dashboard

3. **Auto-Deploy**: Every `git push` will auto-deploy to Railway

---

## 🆘 Common Issues

**CORS errors?**
- Make sure `FRONTEND_URL` in backend matches your frontend domain exactly

**API not connecting?**
- Verify `VITE_API_URL` in frontend matches your backend domain

**Build failing?**
- Check Railway logs in the "Deployments" tab
- Verify root directory is set correctly (`/backend` or `/frontend`)

---

## 🎓 Railway Resources

- Dashboard: https://railway.app/dashboard
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

---

Ready to deploy? Follow `RAILWAY_DEPLOYMENT.md`! 🚀
