"""
PHASE 3 TEST: Direct Azure Face API Test
Tests: Azure Face API smile/emotion detection
"""
from app.utils.azure_face import azure_face
from pathlib import Path

# Find a test image
uploads = Path("uploads")
images = list(uploads.glob("*.jpg"))

if images:
    test_image = images[0]
    print("=" * 60)
    print("PHASE 3: AZURE FACE API - DIRECT TEST")
    print("=" * 60)
    print(f"\nTesting Azure Face with: {test_image}")
    print("="*60)
    
    result = azure_face.detect_emotion_from_file(str(test_image))
    
    print(f"\nFace count: {result.get('face_count', 0)}")
    print(f"\nEmotions: {result.get('emotions', {})}")
    print(f"\nDominant emotion: {result.get('dominant_emotion')}")
    print(f"\nFaces: {result.get('faces', [])}")
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
else:
    print("No test images found in uploads/")
