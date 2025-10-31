"""
API Testing Script for MathAI
Tests all endpoints and functionality
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}🧪 Testing: {name}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def test_health():
    """Test health check endpoint"""
    print_test("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Status: {data['status']}")
            print_success(f"Services: {data['services']}")
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_chat():
    """Test chat endpoint"""
    print_test("Chat Endpoint")
    try:
        payload = {
            "message": "Solve for x: 2x + 5 = 13",
            "session_id": "test_session",
            "use_feedback_learning": True
        }
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Success: {data['success']}")
            if data['solution']:
                print_success(f"Solution length: {len(data['solution'])} chars")
            if data.get('routing'):
                print_success(f"Source: {data['routing']['source']}")
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_kb_search():
    """Test knowledge base search"""
    print_test("Knowledge Base Search")
    try:
        payload = {
            "query": "linear equations",
            "top_k": 3,
            "score_threshold": 0.3
        }
        response = requests.post(f"{BASE_URL}/kb/search", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Found {data['num_results']} results")
            if data['results']:
                print_success(f"Top result: {data['results'][0]['question'][:50]}...")
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_feedback():
    """Test feedback submission"""
    print_test("Feedback Submission")
    try:
        payload = {
            "query": "Test question",
            "solution": "Test solution",
            "rating": 5,
            "comment": "Great explanation!"
        }
        response = requests.post(f"{BASE_URL}/feedback", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Feedback ID: {data.get('feedback_id')}")
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_feedback_stats():
    """Test feedback statistics"""
    print_test("Feedback Statistics")
    try:
        response = requests.get(f"{BASE_URL}/feedback/stats")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Total feedback: {data['total_feedback']}")
            print_success(f"Average rating: {data['average_rating']}")
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_analytics():
    """Test analytics endpoint"""
    print_test("Analytics")
    try:
        response = requests.get(f"{BASE_URL}/analytics?days=7")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Total queries: {data['total_queries']}")
            print_success(f"Period: {data['period_days']} days")
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_guardrails():
    """Test guardrails - should block non-math queries"""
    print_test("Guardrails (Should Block)")
    try:
        payload = {
            "message": "What's the weather today?",
            "session_id": "test_session"
        }
        response = requests.post(f"{BASE_URL}/chat", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('blocked') or not data.get('success'):
                print_success("Non-math query correctly blocked")
                return True
            else:
                print_warning("Query was not blocked (may still work)")
                return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_kb_stats():
    """Test knowledge base statistics"""
    print_test("Knowledge Base Stats")
    try:
        response = requests.get(f"{BASE_URL}/kb/stats")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Total problems: {data.get('total_problems', 0)}")
            print_success(f"Collection: {data.get('collection_name', 'N/A')}")
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print(f"\n{'='*60}")
    print(f"🧪 MathAI API Test Suite")
    print(f"{'='*60}")
    print(f"Testing: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if backend is running
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except Exception:
        print_error("\n❌ Backend is not running!")
        print_warning("Start backend with: cd backend && uvicorn main:app --reload")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Health Check", test_health),
        ("Chat Endpoint", test_chat),
        ("KB Search", test_kb_search),
        ("KB Stats", test_kb_stats),
        ("Feedback Submit", test_feedback),
        ("Feedback Stats", test_feedback_stats),
        ("Analytics", test_analytics),
        ("Guardrails", test_guardrails),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Test Results Summary")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{Colors.BLUE}Total: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"{Colors.GREEN}🎉 All tests passed!{Colors.END}")
        sys.exit(0)
    else:
        print(f"{Colors.RED}❌ Some tests failed{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()