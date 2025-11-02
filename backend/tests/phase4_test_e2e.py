"""
PHASE 4 TEST: End-to-End Integration Test
Tests: User registration → Login → Upload → AI Processing → Search → Recommendations
Complete workflow test for Phase 4 semantic search functionality.
"""
import requests
import json
import time
from io import BytesIO
from PIL import Image

BASE_URL = "http://127.0.0.1:8000"

# Test credentials
TEST_USER = {
    "email": "test@example.com",
    "password": "testpass123"
}

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def register_and_login():
    """Register and login a test user"""
    print("\n1️⃣ Registering test user...")
    try:
        r = requests.post(f"{BASE_URL}/api/auth/register", data=TEST_USER)
        if r.status_code == 200:
            data = r.json()
            token = data.get("accessToken")
            print("   ✅ User registered and logged in")
            return token
        elif r.status_code == 400:
            print("   ℹ️  User already exists, logging in...")
        else:
            print(f"   ⚠️  Registration response: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"   ⚠️  Registration error: {str(e)}")
    
    print("\n2️⃣ Logging in...")
    try:
        r = requests.post(f"{BASE_URL}/api/auth/login", data=TEST_USER)
        if r.status_code == 200:
            data = r.json()
            token = data.get("accessToken")
            print(f"   ✅ Logged in successfully")
            return token
        else:
            print(f"   ❌ Login failed: {r.status_code} - {r.text}")
            return None
    except Exception as e:
        print(f"   ❌ Login error: {str(e)}")
        return None

def upload_test_image(token):
    """Upload a test image"""
    print("\n3️⃣ Uploading test image...")
    try:
        img_bytes = create_test_image()
        files = {'file': ('test_beach.png', img_bytes, 'image/png')}
        headers = {'Authorization': f'Bearer {token}'}
        
        r = requests.post(
            f"{BASE_URL}/api/media/",
            files=files,
            headers=headers
        )
        
        if r.status_code == 200 or r.status_code == 201:
            data = r.json()
            media_id = data.get('id')
            print(f"   ✅ Image uploaded (ID: {media_id})")
            print(f"   Status: {data.get('status')}")
            return media_id
        else:
            print(f"   ❌ Upload failed: {r.status_code} - {r.text}")
            return None
    except Exception as e:
        print(f"   ❌ Upload error: {str(e)}")
        return None

def wait_for_processing(media_id, token, max_wait=30):
    """Wait for AI processing to complete"""
    print("\n4️⃣ Waiting for AI processing (embeddings)...")
    headers = {'Authorization': f'Bearer {token}'}
    
    for i in range(max_wait):
        try:
            r = requests.get(f"{BASE_URL}/api/media/status/{media_id}", headers=headers)
            if r.status_code == 200:
                data = r.json()
                status = data.get('status')
                has_embedding = data.get('embedding') is not None
                
                print(f"   [{i+1}s] Status: {status}, Embedding: {has_embedding}")
                
                if status == 'completed' and has_embedding:
                    print(f"   ✅ Processing complete!")
                    print(f"   Caption: {data.get('caption', 'N/A')[:50]}...")
                    print(f"   Tags: {data.get('tags', [])}")
                    return True
                elif status == 'failed':
                    print(f"   ❌ Processing failed: {data.get('error_message')}")
                    return False
                
                time.sleep(1)
        except Exception as e:
            print(f"   ⚠️  Status check error: {str(e)}")
    
    print("   ⏱️  Timeout waiting for processing")
    return False

def test_search(token):
    """Test search functionality"""
    print("\n5️⃣ Testing search...")
    headers = {'Authorization': f'Bearer {token}'}
    
    queries = [
        ("beach sunset", "semantic"),
        ("blue", "text"),
        ("ocean", "hybrid")
    ]
    
    for query, search_type in queries:
        try:
            r = requests.get(
                f"{BASE_URL}/api/search/search?query={query}&search_type={search_type}",
                headers=headers
            )
            if r.status_code == 200:
                data = r.json()
                count = data.get('total_results', 0)
                print(f"   ✅ {search_type.capitalize()} search '{query}': {count} results")
            else:
                print(f"   ❌ {search_type.capitalize()} search failed: {r.status_code}")
        except Exception as e:
            print(f"   ❌ Search error: {str(e)}")

def test_recommendations(media_id, token):
    """Test similar media recommendations"""
    print("\n6️⃣ Testing recommendations...")
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        r = requests.get(
            f"{BASE_URL}/api/search/search/similar/{media_id}",
            headers=headers
        )
        if r.status_code == 200:
            data = r.json()
            count = data.get('total_results', 0)
            print(f"   ✅ Found {count} similar items")
        else:
            print(f"   ❌ Recommendations failed: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"   ❌ Recommendations error: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 PHASE 4: END-TO-END INTEGRATION TEST")
    print("=" * 60)
    print(f"\nTesting server at: {BASE_URL}")
    
    # Authenticate
    token = register_and_login()
    if not token:
        print("\n❌ Cannot continue without authentication")
        exit(1)
    
    # Upload image
    media_id = upload_test_image(token)
    if not media_id:
        print("\n❌ Cannot continue without uploaded image")
        exit(1)
    
    # Wait for processing
    success = wait_for_processing(media_id, token)
    if not success:
        print("\n⚠️  Processing incomplete, but continuing tests...")
    
    # Test search
    test_search(token)
    
    # Test recommendations
    test_recommendations(media_id, token)
    
    print("\n" + "=" * 60)
    print("🎉 End-to-End Test Complete!")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("1. Visit http://127.0.0.1:8000/docs to explore the API")
    print("2. Try different search queries")
    print("3. Upload more images to improve search results")
