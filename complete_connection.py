"""
Complete Connection Verification Script
Run this to test all connections in your project
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
if backend_path.exists():
    sys.path.insert(0, str(backend_path))

print("=" * 70)
print("🔍 MathAI CONNECTION VERIFICATION")
print("=" * 70)

# Test 1: Environment Variables
print("\n1️⃣ Testing Environment Variables...")
try:
    from dotenv import load_dotenv
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

    if not gemini_key or gemini_key == "your-gemini-api-key-here":
        print("   ❌ GEMINI_API_KEY not set properly")
    else:
        print(f"   ✅ GEMINI_API_KEY set ({gemini_key[:10]}...)")

    if not tavily_key or tavily_key == "your-tavily-api-key-here":
        print("   ❌ TAVILY_API_KEY not set properly")
    else:
        print(f"   ✅ TAVILY_API_KEY set ({tavily_key[:10]}...)")

except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Config Loading
print("\n2️⃣ Testing Configuration...")
try:
    from core.config import settings
    print(f"   ✅ Config loaded")
    print(f"   - Backend Port: {settings.BACKEND_PORT}")
    print(f"   - Frontend Port: {settings.FRONTEND_PORT}")
    print(f"   - CORS Origins: {len(settings.cors_origins_list)} domains")
except Exception as e:
    print(f"   ❌ Config error: {e}")

# Test 3: Database Connection
print("\n3️⃣ Testing Database...")
try:
    from core.database import db

    # Test save and retrieve
    test_id = db.save_message(
        session_id="test_verification",
        role="user",
        content="Test message"
    )

    history = db.get_chat_history("test_verification", limit=1)

    if len(history) > 0:
        print(f"   ✅ Database working (ID: {test_id})")
    else:
        print(f"   ⚠️ Database write/read issue")

except Exception as e:
    print(f"   ❌ Database error: {e}")

# Test 4: Gemini API
print("\n4️⃣ Testing Gemini API...")
try:
    import google.generativeai as genai
    from backend.core.config import settings

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

    response = model.generate_content("What is 2+2?")

    if response.text:
        print(f"   ✅ Gemini API working")
        print(f"   Response: {response.text[:50]}...")
    else:
        print(f"   ⚠️ No response from Gemini")

except Exception as e:
    print(f"   ❌ Gemini error: {e}")

# Test 5: Tavily Search
print("\n5️⃣ Testing Tavily Search...")
try:
    from tavily import TavilyClient
    from core.config import settings

    client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    response = client.search(query="What is calculus?", max_results=1)

    if response and 'results' in response:
        print(f"   ✅ Tavily API working")
        print(f"   Found {len(response['results'])} results")
    else:
        print(f"   ⚠️ No results from Tavily")

except Exception as e:
    print(f"   ❌ Tavily error: {e}")

# Test 6: Embeddings
print("\n6️⃣ Testing Embeddings...")
try:
    from sentence_transformers import SentenceTransformer
    from core.config import settings

    model = SentenceTransformer(settings.EMBEDDING_MODEL)
    embedding = model.encode("test query")

    if len(embedding) == settings.EMBEDDING_DIM:
        print(f"   ✅ Embeddings working (dim: {len(embedding)})")
    else:
        print(
            f"   ⚠️ Dimension mismatch: {len(embedding)} vs {settings.EMBEDDING_DIM}")

except Exception as e:
    print(f"   ❌ Embeddings error: {e}")

# Test 7: Qdrant
print("\n7️⃣ Testing Qdrant...")
try:
    from qdrant_client import QdrantClient

    client = QdrantClient(":memory:")
    collections = client.get_collections()

    print(f"   ✅ Qdrant working (in-memory mode)")

except Exception as e:
    print(f"   ❌ Qdrant error: {e}")

# Test 8: FastAPI Imports
print("\n8️⃣ Testing FastAPI Setup...")
try:
    from fastapi import FastAPI
    from api.routes import router

    app = FastAPI()
    app.include_router(router)

    print(f"   ✅ FastAPI setup working")
    print(f"   Routes: {len(app.routes)} registered")

except Exception as e:
    print(f"   ❌ FastAPI error: {e}")

# Test 9: Guardrails
print("\n9️⃣ Testing Guardrails...")
try:
    from services.guardrails import guardrails

    test_cases = [
        ("Solve 2x + 5 = 13", True),
        ("How to hack", False),
        ("What is weather", False)
    ]

    passed = 0
    for query, should_pass in test_cases:
        result = guardrails.check_input_guardrail(query)

        # Handle both dict and Pydantic model
        if hasattr(result, 'dict'):
            result_dict = result.dict()
        elif hasattr(result, 'model_dump'):
            result_dict = result.model_dump()
        else:
            result_dict = result

        if result_dict['allowed'] == should_pass:
            passed += 1

    if passed == len(test_cases):
        print(
            f"   ✅ Guardrails working ({passed}/{len(test_cases)} tests passed)")
    else:
        print(
            f"   ⚠️ Guardrails partial: {passed}/{len(test_cases)} tests passed")

except Exception as e:
    print(f"   ❌ Guardrails error: {e}")

# Test 10: Knowledge Base File
print("\n🔟 Testing Knowledge Base File...")
try:
    # Try multiple possible locations
    possible_paths = [
        Path("data/math_knowledge_base.json"),
        Path("backend/data/math_knowledge_base.json"),
        Path("../data/math_knowledge_base.json")
    ]

    kb_path = None
    for path in possible_paths:
        if path.exists():
            kb_path = path
            break

    if kb_path:
        import json
        with open(kb_path, 'r') as f:
            kb = json.load(f)
        print(f"   ✅ Knowledge base found ({len(kb)} problems)")
    else:
        print(f"   ⚠️ Knowledge base not found")
        print(f"   Run notebook 01 to create it")

except Exception as e:
    print(f"   ❌ KB error: {e}")

# Summary
print("\n" + "=" * 70)
print("📊 VERIFICATION SUMMARY")
print("=" * 70)
print("\n✅ = Working correctly")
print("⚠️ = Needs attention")
print("❌ = Critical issue")
print("\nIf you see ❌, fix those issues before running the application.")
print("=" * 70)
