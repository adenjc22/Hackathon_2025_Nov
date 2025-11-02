"""
Simple script to test media upload and AI processing
"""
import requests
import time
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def test_upload():
    print("=" * 60)
    print("Testing Media Upload and AI Processing")
    print("=" * 60)
    
    # Find an image file to upload
    uploads_dir = Path("uploads")
    image_files = list(uploads_dir.glob("*.jpg")) + list(uploads_dir.glob("*.png"))
    
    if not image_files:
        print("\n❌ No images found in uploads/ directory")
        print("Please add a .jpg or .png file to the uploads/ folder and try again")
        return
    
    test_file = image_files[0]
    print(f"\n📁 Using test file: {test_file.name}")
    
    # Upload the file
    print("\n⬆️  Uploading file...")
    with open(test_file, "rb") as f:
        files = {"file": (test_file.name, f, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/api/upload/media/", files=files)
    
    if response.status_code != 200:
        print(f"\n❌ Upload failed with status {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    media_id = data["id"]
    print(f"✅ Upload successful! Media ID: {media_id}")
    print(f"   Status: {data['status']}")
    print(f"   File URL: {data['file_url']}")
    
    # Poll for processing status
    print("\n🔄 Checking processing status...")
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        response = requests.get(f"{BASE_URL}/api/upload/media/status/{media_id}")
        data = response.json()
        status = data["status"]
        
        print(f"   [{attempt+1}/{max_attempts}] Status: {status}", end="")
        
        if status == "done":
            print(" ✅")
            print("\n" + "=" * 60)
            print("AI Processing Results:")
            print("=" * 60)
            
            print(f"\n📝 Caption:")
            print(f"   {data.get('caption', 'N/A')}")
            
            print(f"\n🏷️  Tags:")
            tags = data.get('tags', [])
            if tags:
                for tag in tags:
                    print(f"   - {tag}")
            else:
                print("   N/A")
            
            print(f"\n😊 Emotions:")
            emotion = data.get('emotion')
            if emotion and isinstance(emotion, dict) and len(emotion) > 0:
                print(json.dumps(emotion, indent=2))
            else:
                print(f"   Raw data: {emotion}")
                print("   (No emotion data detected - may require Azure Limited Access approval)")
            
            print("\n" + "=" * 60)
            print("✅ Test Complete!")
            print("=" * 60)
            return
        
        elif status == "error":
            print(" ❌")
            print(f"\n⚠️  Processing failed with error:")
            print(f"   {data.get('error_message', 'Unknown error')}")
            return
        
        else:
            print()
        
        attempt += 1
        time.sleep(2)
    
    print(f"\n⏱️  Timeout: Processing took longer than {max_attempts * 2} seconds")
    print(f"   Last status: {status}")
    print("\n💡 Tips:")
    print("   - Check if Celery worker is running")
    print("   - Check if Azure API keys are configured in .env")
    print("   - Check Celery terminal for error messages")

if __name__ == "__main__":
    try:
        test_upload()
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server at http://127.0.0.1:8000")
        print("Make sure uvicorn is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
