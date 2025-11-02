"""
Integration test for media upload and AI processing pipeline.
Tests the complete flow: upload -> Azure Vision analysis -> OpenAI caption generation.
"""
import requests
import time
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def test_upload():
    print("=" * 70)
    print("MEDIA UPLOAD AND AI PROCESSING - INTEGRATION TEST")
    print("=" * 70)
    
    # Find an image file to upload
    uploads_dir = Path("uploads")
    image_files = list(uploads_dir.glob("*.jpg")) + list(uploads_dir.glob("*.png"))
    
    if not image_files:
        print("\n[ERROR] No images found in uploads/ directory")
        print("Please add a .jpg or .png file to the uploads/ folder and try again")
        return
    
    test_file = image_files[0]
    print(f"\nTest file: {test_file.name}")
    
    # Upload the file
    print("\n[STEP 1] Uploading file to API...")
    with open(test_file, "rb") as f:
        files = {"file": (test_file.name, f, "image/jpeg")}
        response = requests.post(f"{BASE_URL}/api/upload/media/", files=files)
    
    if response.status_code != 200:
        print(f"\n[ERROR] Upload failed with status {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    media_id = data["id"]
    print(f"[SUCCESS] Upload completed")
    print(f"          Media ID: {media_id}")
    print(f"          Status: {data['status']}")
    print(f"          File URL: {data['file_url']}")
    
    # Poll for processing status
    print(f"\n[STEP 2] Monitoring AI processing status...")
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        response = requests.get(f"{BASE_URL}/api/upload/media/status/{media_id}")
        data = response.json()
        status = data["status"]
        
        print(f"          Attempt {attempt+1}/{max_attempts}: Status = {status}", end="")
        
        if status == "done":
            print(" [COMPLETE]")
            print("\n" + "=" * 70)
            print("AI PROCESSING RESULTS")
            print("=" * 70)
            
            print(f"\nGenerated Caption:")
            print(f"  {data.get('caption', 'N/A')}")
            
            print(f"\nDetected Tags:")
            tags = data.get('tags', [])
            if tags:
                for tag in tags:
                    print(f"  - {tag}")
            else:
                print("  N/A")
            
            print(f"\nEmotion Analysis:")
            emotion = data.get('emotion')
            if emotion and isinstance(emotion, dict) and len(emotion) > 0:
                for key, value in emotion.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {emotion}")
                print("  Note: Full emotion detection requires Azure Limited Access approval")
            
            print("\n" + "=" * 70)
            print("TEST COMPLETED SUCCESSFULLY")
            print("=" * 70)
            return
        
        elif status == "error":
            print(" [FAILED]")
            print(f"\n[ERROR] Processing failed:")
            print(f"        {data.get('error_message', 'Unknown error')}")
            return
        
        else:
            print()
        
        attempt += 1
        time.sleep(2)
    
    print(f"\n[WARNING] Timeout: Processing exceeded {max_attempts * 2} seconds")
    print(f"          Last status: {status}")
    print("\nTroubleshooting:")
    print("  - Verify Azure API keys are configured in .env")
    print("  - Check uvicorn terminal for error messages")
    print("  - Ensure network connectivity to Azure services")

if __name__ == "__main__":
    try:
        test_upload()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Cannot connect to server at http://127.0.0.1:8000")
        print("        Make sure uvicorn is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
