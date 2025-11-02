"""
PHASE  TEST: Smart Search Comprehensive Test Suite
Tests: Semantic search, text search, hybrid search, embeddings, recommendations
Run this to verify that Phase  semantic search is working correctly.
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:"


def print_header(text):
    """Print a formatted section header."""
    print("\n" + "=" * )
    print(f"  {text}")
    print("=" *  + "\n")


def test_embedding_generation():
    """Test : Verify embedding generation works."""
    print_header("Test : Embedding Generation")
    
    test_text = "A beautiful sunset over the ocean with warm colors"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/search/embeddings",
            json={"text": test_text},
            timeout=
        )
        
        if response.status_code == :
            data = response.json()
            print(f"âœ… Embedding generated successfully!")
            print(f"   Text: {data['text'][:]}...")
            print(f"   Dimension: {data['dimension']}")
            print(f"   First  values: {data['embedding'][:]}")
            return True
        else:
            print(f"âŒ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"âŒ Error: {str(e)}")
        return False


def test_media_list():
    """Test : Check if any media exists."""
    print_header("Test : Media Inventory")
    
    try:
        response = requests.get(f"{BASE_URL}/api/upload/media/", timeout=)
        
        if response.status_code == :
            media_items = response.json()
            print(f"âœ… Found {len(media_items)} media items")
            
            # Show details of items with embeddings
            with_embeddings = [m for m in media_items if m.get('embedding')]
            without_embeddings = [m for m in media_items if not m.get('embedding')]
            
            print(f"   With embeddings: {len(with_embeddings)}")
            print(f"   Without embeddings: {len(without_embeddings)}")
            
            if media_items:
                print("\n   Sample media:")
                for item in media_items[:]:
                    has_emb = "âœ“" if item.get('embedding') else "âœ—"
                    print(f"   [{has_emb}] ID {item['id']}: {item['filename']}")
                    print(f"       Caption: {item.get('caption', 'N/A')[:]}")
                    print(f"       Status: {item.get('status', 'unknown')}")
            
            return len(with_embeddings) > 
        else:
            print(f"âŒ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"âŒ Error: {str(e)}")
        return False


def test_reindex():
    """Test : Reindex existing media to generate embeddings."""
    print_header("Test : Reindexing Media")
    
    try:
        print("ðŸ”„ Starting reindex (this may take a moment)...")
        response = requests.post(
            f"{BASE_URL}/api/search/search/reindex",
            params={"force": True},
            timeout=
        )
        
        if response.status_code == :
            data = response.json()
            print(f"âœ… Reindexing complete!")
            print(f"   Total: {data['total']}")
            print(f"   Success: {data['success']}")
            print(f"   Failed: {data['failed']}")
            return data['success'] > 
        else:
            print(f"âŒ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"âŒ Error: {str(e)}")
        return False


def test_search(query, search_type="hybrid"):
    """Test : Perform various search queries."""
    print_header(f"Test : Search Query - '{query}' ({search_type})")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/search/search",
            params={
                "query": query,
                "search_type": search_type,
                "limit": 
            },
            timeout=
        )
        
        if response.status_code == :
            data = response.json()
            print(f"âœ… Search completed: {data['search_type']}")
            print(f"   Query: {data['query']}")
            print(f"   Total results: {data['total_results']}")
            
            if data['results']:
                print("\n   Top Results:")
                for i, result in enumerate(data['results'][:], ):
                    print(f"\n   {i}. {result['filename']} (score: {result['score']:.f})")
                    print(f"      Caption: {result.get('caption', 'N/A')[:]}")
                    print(f"      Match type: {result['match_type']}")
                    if result.get('tags'):
                        print(f"      Tags: {', '.join(result['tags'][:])}")
            else:
                print("\n   No results found")
            
            return True
        else:
            print(f"âŒ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"âŒ Error: {str(e)}")
        return False


def test_similar_media():
    """Test : Find similar media."""
    print_header("Test : Similar Media Recommendations")
    
    try:
        # First get a media ID
        response = requests.get(f"{BASE_URL}/api/upload/media/", timeout=)
        if response.status_code != :
            print("âŒ Could not fetch media list")
            return False
        
        media_items = response.json()
        if not media_items:
            print("âš ï¸  No media items available")
            return False
        
        # Use first item
        reference_id = media_items[]['id']
        print(f"Finding similar items to ID {reference_id}: {media_items[]['filename']}")
        
        response = requests.get(
            f"{BASE_URL}/api/search/similar/{reference_id}",
            params={"limit": },
            timeout=
        )
        
        if response.status_code == :
            data = response.json()
            print(f"âœ… Found {data['total_results']} similar items")
            
            if data['results']:
                print("\n   Similar Media:")
                for i, result in enumerate(data['results'], ):
                    print(f"\n   {i}. {result['filename']} (similarity: {result['score']:.f})")
                    print(f"      Caption: {result.get('caption', 'N/A')[:]}")
            
            return True
        elif response.status_code == :
            print("âš ï¸  Media not found or has no embedding")
            return False
        else:
            print(f"âŒ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"âŒ Error: {str(e)}")
        return False


def test_filters():
    """Test : Search with filters."""
    print_header("Test : Search with Filters")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/search/search",
            params={
                "query": "photos",
                "has_people": True,
                "limit": 
            },
            timeout=
        )
        
        if response.status_code == :
            data = response.json()
            print(f"âœ… Filtered search completed")
            print(f"   Results with people: {data['total_results']}")
            print(f"   Filters applied: {data['filters_applied']}")
            return True
        else:
            print(f"âŒ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"âŒ Error: {str(e)}")
        return False


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "ðŸš€" * )
    print("  PHASE : SMART SEARCH - COMPREHENSIVE TEST SUITE")
    print("ðŸš€" * )
    
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
    
    passed = sum( for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "âœ… PASS" if result else "âŒ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'=' * }")
    print(f"Total: {passed}/{total} tests passed ({passed/total*:.f}%)")
    print(f"{'=' * }\n")
    
    if passed == total:
        print("ðŸŽ‰ All tests passed! Phase  is working correctly!")
    elif passed >= total * .:
        print("âš ï¸  Most tests passed, but some issues detected.")
    else:
        print("âŒ Several tests failed. Please check the logs above.")
    
    return passed == total


if __name__ == "__main__":
    print("\nðŸ’¡ Make sure the backend is running on http://localhost:")
    print("   Start it with: uvicorn main:app --reload\n")
    
    input("Press Enter to start tests...")
    
    success = run_all_tests()
    
    if not success:
        print("\nðŸ”§ Troubleshooting Tips:")
        print("   . Verify OPENAI_API_KEY is set in .env")
        print("   . Upload at least one test image")
        print("   . Wait for AI processing to complete")
        print("   . Check backend logs for errors")
    
    print("\nðŸ‘‹ Tests complete!\n")
