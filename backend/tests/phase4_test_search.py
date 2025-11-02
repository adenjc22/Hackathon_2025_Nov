"""
PHASE 4 TEST: Smart Search Comprehensive Test Suite
Tests: Semantic search, text search, hybrid search, embeddings, recommendations
Run this to verify that Phase 4 semantic search is working correctly.
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"


def print_header(text):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def test_embedding_generation():
    """Test 1: Verify embedding generation works."""
    print_header("Test 1: Embedding Generation")
    
    test_text = "A beautiful sunset over the ocean with warm colors"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/search/embeddings",
            json={"text": test_text},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Embedding generated successfully!")
            print(f"   Text: {data['text'][:50]}...")
            print(f"   Dimension: {data['dimension']}")
            print(f"   First 5 values: {data['embedding'][:5]}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_media_list():
    """Test 2: Check if any media exists."""
    print_header("Test 2: Media Inventory")
    
    try:
        response = requests.get(f"{BASE_URL}/api/upload/media/", timeout=10)
        
        if response.status_code == 200:
            media_items = response.json()
            print(f"✅ Found {len(media_items)} media items")
            
            # Show details of items with embeddings
            with_embeddings = [m for m in media_items if m.get('embedding')]
            without_embeddings = [m for m in media_items if not m.get('embedding')]
            
            print(f"   With embeddings: {len(with_embeddings)}")
            print(f"   Without embeddings: {len(without_embeddings)}")
            
            if media_items:
                print("\n   Sample media:")
                for item in media_items[:3]:
                    has_emb = "✓" if item.get('embedding') else "✗"
                    print(f"   [{has_emb}] ID {item['id']}: {item['filename']}")
                    print(f"       Caption: {item.get('caption', 'N/A')[:60]}")
                    print(f"       Status: {item.get('status', 'unknown')}")
            
            return len(with_embeddings) > 0
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_reindex():
    """Test 3: Reindex existing media to generate embeddings."""
    print_header("Test 3: Reindexing Media")
    
    try:
        print("🔄 Starting reindex (this may take a moment)...")
        response = requests.post(
            f"{BASE_URL}/api/search/search/reindex",
            params={"force": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reindexing complete!")
            print(f"   Total: {data['total']}")
            print(f"   Success: {data['success']}")
            print(f"   Failed: {data['failed']}")
            return data['success'] > 0
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_search(query, search_type="hybrid"):
    """Test 4: Perform various search queries."""
    print_header(f"Test 4: Search Query - '{query}' ({search_type})")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/search/search",
            params={
                "query": query,
                "search_type": search_type,
                "limit": 5
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search completed: {data['search_type']}")
            print(f"   Query: {data['query']}")
            print(f"   Total results: {data['total_results']}")
            
            if data['results']:
                print("\n   Top Results:")
                for i, result in enumerate(data['results'][:5], 1):
                    print(f"\n   {i}. {result['filename']} (score: {result['score']:.3f})")
                    print(f"      Caption: {result.get('caption', 'N/A')[:70]}")
                    print(f"      Match type: {result['match_type']}")
                    if result.get('tags'):
                        print(f"      Tags: {', '.join(result['tags'][:5])}")
            else:
                print("\n   No results found")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_similar_media():
    """Test 5: Find similar media."""
    print_header("Test 5: Similar Media Recommendations")
    
    try:
        # First get a media ID
        response = requests.get(f"{BASE_URL}/api/upload/media/", timeout=10)
        if response.status_code != 200:
            print("❌ Could not fetch media list")
            return False
        
        media_items = response.json()
        if not media_items:
            print("⚠️  No media items available")
            return False
        
        # Use first item
        reference_id = media_items[0]['id']
        print(f"Finding similar items to ID {reference_id}: {media_items[0]['filename']}")
        
        response = requests.get(
            f"{BASE_URL}/api/search/similar/{reference_id}",
            params={"limit": 5},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total_results']} similar items")
            
            if data['results']:
                print("\n   Similar Media:")
                for i, result in enumerate(data['results'], 1):
                    print(f"\n   {i}. {result['filename']} (similarity: {result['score']:.3f})")
                    print(f"      Caption: {result.get('caption', 'N/A')[:70]}")
            
            return True
        elif response.status_code == 404:
            print("⚠️  Media not found or has no embedding")
            return False
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_filters():
    """Test 6: Search with filters."""
    print_header("Test 6: Search with Filters")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/search/search",
            params={
                "query": "photos",
                "has_people": True,
                "limit": 5
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Filtered search completed")
            print(f"   Results with people: {data['total_results']}")
            print(f"   Filters applied: {data['filters_applied']}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "🚀" * 30)
    print("  PHASE 4: SMART SEARCH - COMPREHENSIVE TEST SUITE")
    print("🚀" * 30)
    
    results = {
        "Embedding Generation": test_embedding_generation(),
        "Media Inventory": test_media_list(),
        "Reindexing": test_reindex(),
        "Semantic Search": test_search("happy moments", "semantic"),
        "Text Search": test_search("photo", "text"),
        "Hybrid Search": test_search("beautiful sunset", "hybrid"),
        "Similar Media": test_similar_media(),
        "Filtered Search": test_filters()
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'=' * 60}")
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print(f"{'=' * 60}\n")
    
    if passed == total:
        print("🎉 All tests passed! Phase 4 is working correctly!")
    elif passed >= total * 0.7:
        print("⚠️  Most tests passed, but some issues detected.")
    else:
        print("❌ Several tests failed. Please check the logs above.")
    
    return passed == total


if __name__ == "__main__":
    print("\n💡 Make sure the backend is running on http://localhost:8000")
    print("   Start it with: uvicorn main:app --reload\n")
    
    input("Press Enter to start tests...")
    
    success = run_all_tests()
    
    if not success:
        print("\n🔧 Troubleshooting Tips:")
        print("   1. Verify OPENAI_API_KEY is set in .env")
        print("   2. Upload at least one test image")
        print("   3. Wait for AI processing to complete")
        print("   4. Check backend logs for errors")
    
    print("\n👋 Tests complete!\n")
