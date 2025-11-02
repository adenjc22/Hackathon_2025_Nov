"""
Test the AI utilities to ensure they are properly configured.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.azure_vision import azure_vision
from app.utils.azure_face import azure_face
from app.utils.openai_caption import openai_caption
from loguru import logger


def test_azure_vision():
    """Test Azure Computer Vision API."""
    print("\n" + "="*60)
    print("🔍 Testing Azure Computer Vision API")
    print("="*60)
    
    if not azure_vision.api_key or not azure_vision.endpoint:
        print("❌ Azure Vision not configured")
        print("   Set AZURE_VISION_KEY and AZURE_VISION_ENDPOINT in .env")
        return False
    
    print(f"✅ API Key: {azure_vision.api_key[:8]}...")
    print(f"✅ Endpoint: {azure_vision.endpoint}")
    
    # Test with a sample public image
    test_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"
    
    print(f"\n📸 Analyzing test image: {test_url}")
    result = azure_vision.analyze_image(test_url)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"\n✅ Success!")
    print(f"   Tags: {', '.join(result.get('tags', [])[:5])}")
    print(f"   Description: {result.get('description', 'N/A')}")
    return True


def test_azure_face():
    """Test Azure Face API."""
    print("\n" + "="*60)
    print("😊 Testing Azure Face API")
    print("="*60)
    
    if not azure_face.api_key or not azure_face.endpoint:
        print("❌ Azure Face not configured")
        print("   Set AZURE_FACE_KEY and AZURE_FACE_ENDPOINT in .env")
        return False
    
    print(f"✅ API Key: {azure_face.api_key[:8]}...")
    print(f"✅ Endpoint: {azure_face.endpoint}")
    
    # Test with a sample face image
    test_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/detection1.jpg"
    
    print(f"\n📸 Analyzing test image: {test_url}")
    result = azure_face.detect_emotion(test_url)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    face_count = result.get('face_count', 0)
    print(f"\n✅ Success!")
    print(f"   Faces detected: {face_count}")
    
    if face_count > 0:
        emotions = result.get('emotions', {})
        dominant = result.get('dominant_emotion', 'N/A')
        print(f"   Dominant emotion: {dominant}")
        if emotions:
            print(f"   Emotions: {dict(list(emotions.items())[:3])}")
    
    return True


def test_openai():
    """Test OpenAI API."""
    print("\n" + "="*60)
    print("🤖 Testing OpenAI API")
    print("="*60)
    
    if not openai_caption.api_key:
        print("❌ OpenAI not configured")
        print("   Set OPENAI_API_KEY in .env")
        return False
    
    print(f"✅ API Key: {openai_caption.api_key[:8]}...")
    
    # Test caption generation
    test_tags = ["dog", "beach", "sunset", "running"]
    test_emotions = {"happiness": 0.95, "neutral": 0.05}
    
    print(f"\n📝 Generating caption with:")
    print(f"   Tags: {', '.join(test_tags)}")
    print(f"   Emotions: {test_emotions}")
    
    try:
        caption = openai_caption.generate_caption(
            tags=test_tags,
            emotions=test_emotions,
            description="A dog running on the beach"
        )
        
        print(f"\n✅ Success!")
        print(f"   Caption: {caption}")
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🧪 AI Utilities Test Suite")
    print("="*60)
    
    # Load environment variables
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    
    print(f"\n📋 Environment file: {env_path}")
    print(f"   File exists: {env_path.exists()}")
    
    results = {
        "Azure Vision": test_azure_vision(),
        "Azure Face": test_azure_face(),
        "OpenAI": test_openai()
    }
    
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    for service, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {service}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! AI pipeline is ready.")
    else:
        print("\n⚠️  Some tests failed. Check API keys and endpoints in .env")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
