# Development Setup Guide

## 🚀 Production (Railway) - Default

By default, the frontend is configured to connect to the Railway production backend.

**No additional setup needed!** Just run:

```bash
# Frontend
cd frontend
npm run dev

# Backend (if testing locally)
cd backend
uvicorn main:app --reload --port 8000
```

---

## 💻 Local Development Mode

To test everything locally, create `.env.local` files:

### Frontend Local Setup

```bash
cd frontend
cp .env.local.example .env.local
```

This creates a `.env.local` file that points to `http://localhost:8000`

### Backend Local Setup

```bash
cd backend
cp .env.local.example .env.local
```

This creates a `.env.local` file with `BACKEND_URL=http://localhost:8000`

### Start Both Servers

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## 🔄 Switching Back to Railway

Simply delete the `.env.local` files:

```bash
# Frontend
cd frontend
rm .env.local

# Backend
cd backend
rm .env.local
```

The app will use the default `.env` files which point to Railway.

---

## 📝 How It Works

### Backend URL Detection

The backend automatically detects the correct URL:

1. **If `BACKEND_URL` is set** → Uses that URL
2. **If not set** → Auto-detects from the request (Railway or localhost)

### Frontend API Configuration

- **`.env`** → Points to Railway (production)
- **`.env.local`** → Points to localhost (local dev)
- Vite prioritizes `.env.local` over `.env`

---

## ✅ Current Configuration

- **Frontend `.env`**: Uses Railway backend
- **Backend auto-detects**: Works on Railway and localhost
- **Local override**: Use `.env.local` files for local development
