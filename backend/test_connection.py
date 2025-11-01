"""
Test script to verify backend is working
Run from backend directory: python test_connection.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"✅ Status: {response.status_code}")
        print(f"📝 Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_chat():
    """Test chat endpoint"""
    print("\n💬 Testing chat endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={
                "message": "Solve for x: 2x + 5 = 13",
                "session_id": "test_session",
                "use_feedback_learning": True
            }
        )
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        
        # Better error handling
        if data.get('success'):
            solution = data.get('solution', 'No solution')
            print(f"📝 Solution: {solution[:200]}...")
            if len(solution) > 200:
                print(f"   (Total length: {len(solution)} chars)")
            return True
        else:
            print(f"❌ Request failed: {data.get('error', 'Unknown error')}")
            if data.get('blocked'):
                print(f"   Blocked: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_feedback():
    """Test feedback endpoint"""
    print("\n👍 Testing feedback endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/feedback",
            json={
                "query": "Test question",
                "solution": "Test solution",
                "rating": 5,
                "comment": "Great explanation!"
            }
        )
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        
        if data.get('success'):
            print(f"📝 Feedback ID: {data.get('feedback_id')}")
            return True
        else:
            print(f"❌ Feedback failed: {data.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("MathAI Backend Connection Test")
    print("=" * 60)

    health_ok = test_health()
    chat_ok = test_chat()
    feedback_ok = test_feedback()

    print("\n" + "=" * 60)
    if health_ok and chat_ok and feedback_ok:
        print("✅ All tests passed! Backend is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    print("=" * 60)