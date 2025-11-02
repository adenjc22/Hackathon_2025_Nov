# Legacy Album - Backend API

AI-powered photo management backend with automatic image analysis and caption generation.

## 🎯 Features

- **FastAPI Backend** - Modern async Python web framework
- **JWT Authentication** - Secure user authentication
- **Image Upload & Storage** - File handling with metadata extraction
- **Background AI Processing** - Asynchronous analysis with Celery
- **Azure Computer Vision** - Image tagging and scene detection
- **Azure Face API** - Emotion and face attribute detection
- **OpenAI GPT-4** - Natural language caption generation

## 🏗️ Architecture

```
Upload → FastAPI → Celery Queue → AI Pipeline Worker
           ↓             ↓
       SQLite ←    Results ← Azure + OpenAI APIs
```

## 📦 Installation

### 1. Install Python Dependencies

```bash
pip install -r ../requirements.txt
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required for AI Processing
OPENAI_API_KEY=your_openai_key_here
AZURE_VISION_KEY=your_azure_vision_key
AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_FACE_KEY=your_azure_face_key
AZURE_FACE_ENDPOINT=https://your-resource.cognitiveservices.azure.com

# Required for Background Processing
REDIS_URL=redis://localhost:6379/0

# Authentication
SECRET_KEY=your-secret-key-min-32-characters
```

### 3. Install Redis (for Celery)

**Windows (via WSL or Docker):**
```bash
docker run -d -p 6379:6379 redis
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

## 🚀 Running the Backend

### Start the FastAPI Server

```bash
cd backend
uvicorn main:app --reload
```

API will be available at: `http://localhost:8000`

### Start the Celery Worker (Background Processing)

In a separate terminal:

```bash
cd backend
celery -A app.ai_pipeline worker --loglevel=info
```

### Optional: Monitor Celery with Flower

```bash
celery -A app.ai_pipeline flower
```

Dashboard at: `http://localhost:5555`

## 📚 API Endpoints

### Health Check
```
GET /api/health
```

### Authentication
```
POST /api/auth/register - Create account
POST /api/auth/login    - Sign in
POST /api/auth/logout   - Sign out
GET  /api/auth/me       - Get current user
```

### Media Management
```
POST   /api/upload/media/           - Upload image (triggers AI processing)
GET    /api/upload/media/           - List all media
GET    /api/upload/media/status/{id} - Check processing status
DELETE /api/upload/media/{id}       - Delete media
```

## 🧠 AI Processing Pipeline

When an image is uploaded:

1. **File is saved** to local storage
2. **Database record created** with status="pending"
3. **Celery task enqueued** for background processing
4. **AI Analysis runs:**
   - Azure Vision extracts tags and description
   - Azure Face detects emotions (if faces present)
   - OpenAI GPT-4 generates natural caption
5. **Database updated** with results, status="done"

Frontend can poll `/api/upload/media/status/{id}` to get updates.

## 🗄️ Database Schema

### Media Table
```python
id           - Integer (primary key)
owner_id     - Integer (foreign key to users)
filename     - String
stored_path  - String (unique)
mime_type    - String
size_bytes   - Integer
status       - Enum: pending, processing, done, error
tags         - JSON (list of strings)
emotion      - JSON (emotion scores)
caption      - Text (generated caption)
error_message - Text (if status=error)
created_at   - DateTime
updated_at   - DateTime
```

## 🧪 Testing

Run backend tests:

```bash
pytest tests/backend/
```

Test the API with curl:

```bash
# Upload an image
curl -X POST http://localhost:8000/api/upload/media/ \
  -F "file=@path/to/image.jpg"

# Check status
curl http://localhost:8000/api/upload/media/status/1
```

## 🔧 Configuration

### Core Settings (`app/core/config.py`)
- Database connection
- JWT settings
- CORS configuration

### Storage (`app/services/storage.py`)
- File upload handling
- Metadata extraction
- Path management

### AI Utilities (`app/utils/`)
- `azure_vision.py` - Vision API integration
- `azure_face.py` - Face API integration
- `openai_caption.py` - Caption generation

## 📝 Development Notes

### Running Without Celery

If Redis/Celery is not set up, the API will still work but skip background processing. Check logs for:
```
WARNING: Celery not available, skipping AI processing
```

### Database Migrations

Database is auto-created on first run. To reset:

```bash
rm ~/.legacy_album/legacy_album.db
```

Then restart the server.

### Logging

Logs use `loguru` for structured logging. Check console output for:
- Upload events
- AI processing progress
- API errors

## 🚢 Deployment Considerations

For production:

1. **Use PostgreSQL** instead of SQLite
2. **Use Azure Redis Cache** for managed Redis
3. **Store files in Azure Blob Storage**
4. **Secure API keys in Azure Key Vault**
5. **Enable HTTPS** and proper CORS
6. **Set up monitoring** with Application Insights

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [Azure Vision API](https://learn.microsoft.com/azure/cognitive-services/computer-vision/)
- [Azure Face API](https://learn.microsoft.com/azure/cognitive-services/face/)
- [OpenAI API](https://platform.openai.com/docs/)

## 🐛 Troubleshooting

### Redis Connection Error
Make sure Redis is running:
```bash
redis-cli ping
# Should return: PONG
```

### Azure API Errors
Check your API keys and endpoints in `.env`. Verify quota limits in Azure portal.

### Database Locked
SQLite can have concurrency issues. Consider switching to PostgreSQL for production.
