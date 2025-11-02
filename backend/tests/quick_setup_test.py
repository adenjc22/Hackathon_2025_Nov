"""
Quick test setup: Upload a test image and verify Phase 3 & 4 work
"""
import requests
from io import BytesIO
from PIL import Image
import time

BASE_URL = "http://127.0.0.1:8000"

def create_test_image():
    """Create a colorful test image"""
    img = Image.new('RGB', (200, 200), color='blue')
    # Add some variety
    for x in range(200):
        for y in range(100, 200):
            img.putpixel((x, y), (255, 200, 0))  # Orange bottom half
    
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG', quality=95)
    img_bytes.seek(0)
    return img_bytes

print("=" * 60)
print("🧪 QUICK TEST SETUP")
print("=" * 60)

# Step 1: Health check
print("\n1️⃣ Checking server health...")
try:
    r = requests.get(f"{BASE_URL}/api/health")
    if r.status_code == 200:
        print("   ✅ Server is running")
    else:
        print(f"   ❌ Server unhealthy: {r.status_code}")
        exit(1)
except:
    print("   ❌ Server not running. Start with: uvicorn main:app --reload")
    exit(1)

# Step 2: Upload test image
print("\n2️⃣ Uploading test image...")
try:
    img_bytes = create_test_image()
    files = {'file': ('test_sunset.jpg', img_bytes, 'image/jpeg')}
    r = requests.post(f"{BASE_URL}/api/media/", files=files)
    
    if r.status_code == 200:
        data = r.json()
        media_id = data.get('id')
        print(f"   ✅ Image uploaded (ID: {media_id})")
        print(f"   Status: {data.get('status')}")
    else:
        print(f"   ❌ Upload failed: {r.status_code}")
        print(f"   Response: {r.text}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Step 3: Wait for processing
print("\n3️⃣ Waiting for AI processing...")
max_wait = 30
for i in range(max_wait):
    try:
        r = requests.get(f"{BASE_URL}/api/media/status/{media_id}")
        if r.status_code == 200:
            data = r.json()
            status = data.get('status')
            has_caption = data.get('caption') is not None
            has_embedding = data.get('embedding') is not None
            
            if status == 'completed':
                print(f"   ✅ Processing complete!")
                print(f"   Caption: {data.get('caption', 'N/A')[:60]}")
                print(f"   Tags: {data.get('tags', [])[:5]}")
                print(f"   Has Embedding: {has_embedding}")
                break
            elif status == 'failed':
                print(f"   ❌ Processing failed: {data.get('error_message')}")
                break
            elif i % 5 == 0:
                print(f"   ⏳ Still processing... ({i+1}s)")
        
        time.sleep(1)
    except Exception as e:
        print(f"   ⚠️  Error checking status: {e}")
        break

# Step 4: Quick search test
print("\n4️⃣ Testing search endpoints...")
try:
    # Test semantic search
    r = requests.get(f"{BASE_URL}/api/search/search?query=blue+orange&search_type=semantic")
    if r.status_code == 200:
        results = r.json().get('total_results', 0)
        print(f"   ✅ Semantic search: {results} results")
    else:
        print(f"   ❌ Semantic search failed: {r.status_code}")
    
    # Test text search
    r = requests.get(f"{BASE_URL}/api/search/search?query=test&search_type=text")
    if r.status_code == 200:
        results = r.json().get('total_results', 0)
        print(f"   ✅ Text search: {results} results")
    else:
        print(f"   ❌ Text search failed: {r.status_code}")
    
    # Test hybrid search
    r = requests.get(f"{BASE_URL}/api/search/search?query=sunset&search_type=hybrid")
    if r.status_code == 200:
        results = r.json().get('total_results', 0)
        print(f"   ✅ Hybrid search: {results} results")
    else:
        print(f"   ❌ Hybrid search failed: {r.status_code}")
    
    # Test recommendations
    r = requests.get(f"{BASE_URL}/api/search/search/similar/{media_id}")
    if r.status_code == 200:
        results = r.json().get('total_results', 0)
        print(f"   ✅ Recommendations: {results} similar items")
    elif r.status_code == 404:
        print(f"   ⚠️  Recommendations: No embedding yet")
    else:
        print(f"   ❌ Recommendations failed: {r.status_code}")
        
except Exception as e:
    print(f"   ❌ Search test error: {e}")

print("\n" + "=" * 60)
print("✅ SETUP COMPLETE!")
print("=" * 60)
print("\nYou can now run full test suites:")
print("  python tests/phase4_test_search.py")
print("\nOr explore the API at:")
print("  http://127.0.0.1:8000/docs")
