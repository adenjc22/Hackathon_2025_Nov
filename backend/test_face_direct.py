"""Direct test of Azure Face API with smile detection"""
from app.utils.azure_face import azure_face
from pathlib import Path

# Find a test image
uploads = Path("uploads")
images = list(uploads.glob("*.jpg"))

if images:
    test_image = images[0]
    print(f"Testing Azure Face with: {test_image}")
    print("="*60)
    
    result = azure_face.detect_emotion_from_file(str(test_image))
    
    print(f"\nFace count: {result.get('face_count', 0)}")
    print(f"\nEmotions: {result.get('emotions', {})}")
    print(f"\nDominant emotion: {result.get('dominant_emotion')}")
    print(f"\nFaces: {result.get('faces', [])}")
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
else:
    print("No test images found in uploads/")
