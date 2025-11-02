# Backend Test Suite

This folder contains organized tests for Phase 3 and Phase 4 functionality.

## Test Organization

### Phase 3 Tests (AI Processing Pipeline)
- **`phase3_test_upload.py`** - Integration test for media upload and AI processing
  - Tests: Upload → Azure Vision → OpenAI Caption → Storage
  - Monitors processing status and displays results
  
- **`phase3_test_face_detection.py`** - Direct Azure Face API test
  - Tests: Face detection and emotion analysis
  - Verifies Azure Face API integration

### Phase 4 Tests (Smart Search)
- **`phase4_test_search.py`** - Comprehensive search test suite ⭐ **MAIN TEST**
  - Tests: Embeddings, semantic search, text search, hybrid search
  - Tests: Reindexing, recommendations, filtered search
  - Runs 8 different test scenarios
  
- **`phase4_test_e2e.py`** - End-to-end integration test
  - Tests: Registration → Login → Upload → Processing → Search
  - Complete workflow validation

## Running Tests

### Prerequisites
1. **Start the backend server:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Verify environment variables:**
   - `OPENAI_API_KEY` - For embeddings and captions
   - `AZURE_VISION_KEY` - For image analysis
   - `AZURE_FACE_KEY` - For face detection

### Run Individual Tests

**Phase 3 - Upload & AI Processing:**
```bash
python tests/phase3_test_upload.py
```

**Phase 3 - Face Detection:**
```bash
python tests/phase3_test_face_detection.py
```

**Phase 4 - Search (Recommended):**
```bash
python tests/phase4_test_search.py
```

**Phase 4 - End-to-End:**
```bash
python tests/phase4_test_e2e.py
```

## Test Requirements

### Phase 3 Tests
- At least one image file in `uploads/` directory
- Valid Azure API keys

### Phase 4 Tests
- Backend server running on `http://localhost:8000`
- Valid OpenAI API key for embeddings
- At least one media item uploaded (or will upload test image)

## Expected Results

### ✅ All Tests Passing
- Phase 3: Successful upload, AI processing, caption generation
- Phase 4: 8/8 tests passing (100%)

### ⚠️ Common Issues
1. **Connection Error** - Server not running
2. **API Key Error** - Missing or invalid environment variables
3. **No Media Found** - Upload at least one image first
4. **Timeout** - AI processing taking longer than expected

## Test Coverage

| Feature | Phase 3 | Phase 4 |
|---------|---------|---------|
| Upload | ✅ | ✅ |
| Azure Vision | ✅ | - |
| Azure Face | ✅ | - |
| OpenAI Caption | ✅ | - |
| OpenAI Embeddings | - | ✅ |
| Semantic Search | - | ✅ |
| Text Search | - | ✅ |
| Hybrid Search | - | ✅ |
| Recommendations | - | ✅ |
| Filtered Search | - | ✅ |

## Quick Test Script

Run all tests in sequence:
```bash
# Phase 3
python tests/phase3_test_upload.py
python tests/phase3_test_face_detection.py

# Phase 4
python tests/phase4_test_search.py
python tests/phase4_test_e2e.py
```

## Troubleshooting

**Server not responding:**
```bash
# Check if uvicorn is running
curl http://localhost:8000/api/health
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**Database issues:**
```bash
# Reinitialize database
python -c "from app.database.init_database import init_db; init_db()"
```

---

**Note:** These tests are for development and integration testing. For production deployment, consider adding pytest-based unit tests.
