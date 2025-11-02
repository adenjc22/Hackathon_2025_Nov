# Legacy Album - Quick Start Guide 🚀

AI-powered photo management application with automatic image analysis and caption generation.

## Prerequisites

- Python 3.8+ 
- Node.js 16+
- Redis (for background processing)

## 🏃 Quick Start

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment (edit backend/.env with your API keys)
cd backend
cp .env.example .env

# Start Redis (via Docker)
docker run -d -p 6379:6379 redis

# Start FastAPI server
uvicorn main:app --reload

# In a new terminal: Start Celery worker
celery -A app.ai_pipeline worker --loglevel=info
```

Backend runs at: **http://localhost:8000**

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: **http://localhost:5173**

## 🎯 Features Implemented

### Phase 1 ✅
- FastAPI backend structure
- JWT authentication
- User registration/login
- React frontend with routing
- Dark/light mode toggle

### Phase 2 ✅
- Image upload with validation
- File storage system
- Media database model
- Upload UI with drag & drop

### Phase 3 ✅ (NEW!)
- **Background AI Processing**
  - Azure Computer Vision integration
  - Azure Face API for emotion detection
  - OpenAI GPT-4 caption generation
  - Celery task queue
  - Redis message broker
  - Status tracking endpoint

## 🧠 AI Processing Flow

```
User Upload → Backend API → Celery Queue → AI Pipeline Worker
                ↓                ↓
            Database ←     Results ← Azure + OpenAI APIs
```

When you upload an image:
1. File saved with status="pending"
2. Background task queued
3. Azure Vision extracts tags
4. Azure Face detects emotions
5. OpenAI generates natural caption
6. Status updates to "done"

## 🔑 API Keys Required

Create accounts and get keys from:

- **OpenAI**: https://platform.openai.com/api-keys
- **Azure Computer Vision**: https://portal.azure.com/ → Cognitive Services → Computer Vision
- **Azure Face API**: https://portal.azure.com/ → Cognitive Services → Face

Add them to `backend/.env`:

```env
OPENAI_API_KEY=your_key_here
AZURE_VISION_KEY=your_key_here
AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_FACE_KEY=your_key_here
AZURE_FACE_ENDPOINT=https://your-resource.cognitiveservices.azure.com
REDIS_URL=redis://localhost:6379/0
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Sign in
- `GET /api/auth/me` - Get current user

### Media
- `POST /api/upload/media/` - Upload image (triggers AI)
- `GET /api/upload/media/` - List all media
- `GET /api/upload/media/status/{id}` - Check processing status
- `DELETE /api/upload/media/{id}` - Delete media

### Health
- `GET /api/health` - System health check

## 🧪 Testing the AI Pipeline

1. **Upload an image** via the UI or API
2. **Check the status** - it will show "pending" → "processing" → "done"
3. **View results** - tags, emotions, and generated caption

Example with curl:

```bash
# Upload
curl -X POST http://localhost:8000/api/upload/media/ \
  -F "file=@photo.jpg"

# Check status (replace 1 with media ID)
curl http://localhost:8000/api/upload/media/status/1
```

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI entry point
├── app/
│   ├── ai_pipeline.py     # Celery task orchestration
│   ├── celery_app.py      # Celery configuration
│   ├── api/routes/        # API endpoints
│   ├── database/          # SQLAlchemy models
│   ├── utils/             # AI service integrations
│   │   ├── azure_vision.py
│   │   ├── azure_face.py
│   │   └── openai_caption.py
│   └── services/          # Business logic

frontend/
├── src/
│   ├── pages/            # React pages
│   ├── components/       # Reusable components
│   ├── context/          # Auth context
│   └── utils/            # API client
```

## 🐛 Troubleshooting

### Redis Not Running
```bash
# Check if Redis is up
redis-cli ping
# Should return: PONG

# Start Redis with Docker
docker run -d -p 6379:6379 redis
```

### Celery Worker Not Starting
Make sure you're in the backend directory and Redis is running:
```bash
cd backend
celery -A app.ai_pipeline worker --loglevel=info
```

### Azure API Errors
- Verify API keys in `.env`
- Check Azure portal for quota limits
- Ensure endpoints don't have trailing slashes

### Frontend Can't Connect
- Backend must be running on port 8000
- Check CORS settings in `main.py`
- Verify `VITE_API_URL` in frontend

## 📊 Monitoring

### View Celery Tasks (Optional)
```bash
cd backend
celery -A app.ai_pipeline flower
```

Dashboard at: http://localhost:5555

### Check Logs
- Backend logs show in the terminal where uvicorn runs
- Celery logs show AI processing progress
- Frontend logs in browser console

## 🚢 Next Steps

- [ ] Add image search by tags/captions
- [ ] Implement albums/collections
- [ ] Add image editing features
- [ ] Deploy to cloud (Azure/AWS)
- [ ] Add more AI models (object detection, OCR)
- [ ] Implement sharing and permissions

## 📚 Documentation

- Backend API docs: http://localhost:8000/docs
- [Backend README](backend/README.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## 💡 Tips

- Use **http://localhost:8000/docs** to explore and test the API interactively
- The AI processing can take 5-15 seconds per image
- Frontend polls `/status/{id}` every 2 seconds to update the UI
- SQLite database is stored at `~/.legacy_album/legacy_album.db`

---

**Built with** ❤️ **using FastAPI, React, Azure AI, and OpenAI**
