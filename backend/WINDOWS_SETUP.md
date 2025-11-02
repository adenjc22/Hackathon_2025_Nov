# Windows Setup Guide for Legacy Album Backend

## ⚠️ Windows-Specific Issues & Solutions

### Issue 1: Celery Prefork Pool Not Supported
**Problem**: Celery's default `prefork` pool doesn't work well on Windows due to permission issues.

**Solution**: Use the `solo` pool instead:
```powershell
celery -A app.ai_pipeline worker --pool=solo --loglevel=info
```

This is already configured in `app/celery_app.py` with `worker_pool="solo"`.

### Issue 2: Environment Variables Not Loading
**Problem**: `.env` file not automatically loaded by Celery workers.

**Solution**: Added explicit `.env` loading in `celery_app.py`:
```python
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)
```

## ✅ Verified Working Setup on Windows

### 1. Start Redis (via Docker or WSL)

**Option A - Docker Desktop:**
```powershell
docker run -d -p 6379:6379 redis
```

**Option B - WSL:**
```powershell
wsl
sudo service redis-server start
exit
```

**Verify Redis is running:**
```powershell
redis-cli ping
# Should return: PONG
```

### 2. Start FastAPI Backend

In Terminal 1:
```powershell
cd backend
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 3. Start Celery Worker (Windows-Compatible)

In Terminal 2:
```powershell
cd backend
celery -A app.ai_pipeline worker --pool=solo --loglevel=info
```

**Expected output:**
```
-------------- celery@YourPC v5.5.3 (immunity)
--- ***** ----- 
-- ******* ---- Windows-11-...
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         legacy_album:...
- ** ---------- .> transport:   redis://localhost:6379/0
- ** ---------- .> results:     redis://localhost:6379/0
- *** --- * --- .> concurrency: 1 (solo)
-- ******* ---- .> task events: OFF
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery

[tasks]
  . process_media_task

[INFO/MainProcess] Connected to redis://localhost:6379/0
[INFO/MainProcess] celery@YourPC ready.
```

✅ **No permission errors!**
✅ **API keys loaded from .env**

## 🧪 Test the Setup

### Quick Test
```powershell
cd backend
python tests/test_ai_utils.py
```

This will verify your Azure and OpenAI API keys are working.

### Full Integration Test

1. **Upload an image via API:**
```powershell
curl -X POST http://localhost:8000/api/upload/media/ -F "file=@C:\path\to\image.jpg"
```

2. **Check status (replace 1 with media ID from response):**
```powershell
curl http://localhost:8000/api/upload/media/status/1
```

3. **Watch the Celery worker logs** for processing:
```
[INFO] Starting AI pipeline for media 1: uploads/abc123.jpg
[INFO] Running Azure Vision analysis...
[INFO] Azure Vision found 5 tags
[INFO] Running Azure Face analysis...
[INFO] Azure Face detected 1 face(s)
[INFO] Generating caption with OpenAI
[INFO] ✅ Successfully processed media 1
```

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'gevent'"
If you try to use `--pool=gevent`, you need to install it:
```powershell
pip install gevent
```

But `solo` pool is simpler and works well for development.

### Error: "redis.exceptions.ConnectionError"
Redis is not running. Start it with:
```powershell
docker run -d -p 6379:6379 redis
```

### Warning: "Azure Vision API credentials not configured"
Check your `.env` file has the correct keys without extra quotes:
```env
AZURE_VISION_KEY=your_key_here
# NOT: AZURE_VISION_KEY="your_key_here"
```

Actually, the code handles both formats, but plain text is cleaner.

### API Keys Not Loading
1. Make sure `.env` is in the `backend/` directory
2. Restart the Celery worker after changing `.env`
3. Check the path is correct in `celery_app.py`

## 📊 Performance Notes

- **Solo pool** runs tasks sequentially (one at a time)
- Good for development and testing
- For production, consider deploying to Linux where prefork works better
- Or use `gevent` pool for concurrent processing on Windows

## 🚀 Alternative: Run Without Celery

If you just want to test the AI processing without Celery:

1. Comment out the Celery task in `media.py`:
```python
# process_media_task.delay(media_row.id, str(dest_path))
```

2. Call the sync version directly:
```python
from app.ai_pipeline import process_media_sync
process_media_sync(media_row.id, str(dest_path))
```

This will block the upload request but works without Redis/Celery.

## ✨ Success Checklist

- [ ] Redis running (docker or WSL)
- [ ] FastAPI backend running on port 8000
- [ ] Celery worker running with `--pool=solo`
- [ ] No permission errors in Celery logs
- [ ] API keys loaded (no warnings about missing config)
- [ ] Test upload returns status="pending"
- [ ] Celery worker processes the task
- [ ] Status endpoint shows status="done" with AI results

---

**You're all set for Windows development!** 🎉
