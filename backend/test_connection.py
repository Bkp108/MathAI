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
        print(f"📝 Solution: {data.get('solution', 'No solution')[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("MathAI Backend Connection Test")
    print("=" * 60)

    health_ok = test_health()
    chat_ok = test_chat()

    print("\n" + "=" * 60)
    if health_ok and chat_ok:
        print("✅ All tests passed! Backend is working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print("=" * 60)
