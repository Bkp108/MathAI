# 👨‍💻 MathAI Developer Guide

## Table of Contents

- [Getting Started](#getting-started)
- [Code Structure](#code-structure)
- [Development Workflow](#development-workflow)
- [Adding New Features](#adding-new-features)
- [Testing Guide](#testing-guide)
- [Debugging Tips](#debugging-tips)
- [Best Practices](#best-practices)

---

## Getting Started

### Prerequisites Knowledge

**Required:**

- Python 3.10+ (async/await, type hints)
- JavaScript ES6+ (async/await, destructuring)
- React Hooks (useState, useEffect, useCallback)
- REST API concepts
- Basic SQL

**Helpful:**

- Vector embeddings & similarity search
- Prompt engineering for LLMs
- Markdown & LaTeX syntax
- Docker & containerization

### Development Environment Setup

```bash
# 1. Clone and navigate
git clone <repo-url>
cd "13. MathAI (AI Planets)"

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\Activate.ps1 on Windows

# 3. Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# 4. Set up environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run verification
python complete_connection.py

# 6. Start development servers
# Terminal 1
cd backend && python -m uvicorn main:app --reload

# Terminal 2
cd frontend && npm run dev
```

### IDE Setup Recommendations

**VS Code Extensions:**

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss",
    "dsznajder.es7-react-js-snippets"
  ]
}
```

**Python Settings (settings.json):**

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

---

## Code Structure

### Backend Architecture

```
backend/
├── api/                    # API Layer
│   ├── __init__.py
│   ├── routes.py          # Main REST endpoints
│   └── websocket.py       # WebSocket support (future)
│
├── core/                   # Core Infrastructure
│   ├── __init__.py
│   ├── config.py          # Settings management (Pydantic)
│   ├── database.py        # Database operations (SQLite)
│   └── schemas.py         # Request/Response models
│
├── services/               # Business Logic
│   ├── __init__.py
│   ├── embeddings.py      # SentenceTransformers wrapper
│   ├── rag_engine.py      # Vector search + retrieval
│   ├── gemini_agent.py    # LLM integration
│   ├── web_search.py      # Tavily integration
│   ├── routing.py         # Smart routing logic
│   └── guardrails.py      # Safety & validation
│
└── main.py                 # FastAPI application
```

### Frontend Architecture

```
frontend/src/
├── components/             # React Components
│   ├── ChatWindow.jsx     # Main chat interface
│   ├── MessageBubble.jsx  # Message rendering
│   ├── InputArea.jsx      # User input
│   ├── Sidebar.jsx        # Navigation
│   ├── FeedbackModal.jsx  # Feedback collection
│   ├── AnalyticsView.jsx  # Statistics display
│   └── SettingsPanel.jsx  # User preferences
│
├── hooks/                  # Custom React Hooks
│   └── useChat.js         # Chat state management
│
├── services/               # API Communication
│   └── api.js             # Axios wrapper
│
├── styles/                 # CSS Files
│   ├── globals.css        # Global styles
│   └── components.css     # Component styles
│
├── App.jsx                 # Root component
└── main.jsx                # Entry point
```

---

## Development Workflow

### Daily Development Routine

```bash
# 1. Pull latest changes
git pull origin main

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install new dependencies (if any)
pip install -r requirements.txt
cd frontend && npm install && cd ..

# 4. Start backend (Terminal 1)
cd backend
python -m uvicorn main:app --reload

# 5. Start frontend (Terminal 2)
cd frontend
npm run dev

# 6. Make changes and test

# 7. Run tests before committing
pytest backend/tests/
cd frontend && npm test

# 8. Format code
black backend/
cd frontend && npm run lint:fix

# 9. Commit changes
git add .
git commit -m "feat: your feature description"
git push origin feature-branch
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit frequently
git add .
git commit -m "feat: add feature X"

# Push to remote
git push origin feature/your-feature-name

# Create Pull Request on GitHub

# After review, merge to main
# Delete feature branch
git branch -d feature/your-feature-name
```

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: fix bug in component
docs: update documentation
style: format code
refactor: refactor service
test: add tests
chore: update dependencies
```

---

## Adding New Features

### 1. Add New API Endpoint

**Example: Add a "Hint" endpoint**

**Step 1: Define Schema (core/schemas.py)**

```python
class HintRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    difficulty_level: str = Field("medium", regex="^(easy|medium|hard)$")

class HintResponse(BaseModel):
    success: bool
    hint: Optional[str] = None
    error: Optional[str] = None
```

**Step 2: Create Service (services/hint_service.py)**

```python
from core.schemas import HintRequest, HintResponse
from services.gemini_agent import gemini_agent

class HintService:
    """Generate hints for math problems"""

    def generate_hint(self, request: HintRequest) -> HintResponse:
        """Generate a hint without giving away the answer"""
        try:
            prompt = f"""
            Give a helpful HINT (not the full solution) for: {request.query}
            Difficulty level: {request.difficulty_level}

            The hint should:
            - Guide thinking without revealing the answer
            - Be appropriate for {request.difficulty_level} level
            - Be 1-2 sentences maximum
            """

            response = gemini_agent.model.generate_content(prompt)

            return HintResponse(
                success=True,
                hint=response.text,
                error=None
            )
        except Exception as e:
            return HintResponse(
                success=False,
                hint=None,
                error=str(e)
            )

hint_service = HintService()
```

**Step 3: Add Route (api/routes.py)**

```python
from services.hint_service import hint_service
from core.schemas import HintRequest, HintResponse

@router.post("/hint", response_model=HintResponse)
async def get_hint(request: HintRequest):
    """Get a hint for a math problem"""
    try:
        return hint_service.generate_hint(request)
    except Exception as e:
        logger.error(f"Hint generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Step 4: Test the Endpoint**

```bash
curl -X POST http://localhost:8000/api/hint \
  -H "Content-Type: application/json" \
  -d '{"query": "Solve x^2 - 4 = 0", "difficulty_level": "medium"}'
```

### 2. Add New Frontend Component

**Example: Add "Hint Button"**

**Step 1: Create Component (components/HintButton.jsx)**

```javascript
import React, { useState } from "react";
import { Lightbulb } from "lucide-react";
import apiService from "../services/api";

export default function HintButton({ query }) {
  const [hint, setHint] = useState(null);
  const [loading, setLoading] = useState(false);

  const getHint = async () => {
    setLoading(true);
    try {
      const response = await apiService.getHint(query);
      setHint(response.hint);
    } catch (error) {
      console.error("Failed to get hint:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button
        onClick={getHint}
        disabled={loading}
        className="flex items-center gap-2 px-3 py-2 bg-yellow-600 
                   hover:bg-yellow-700 rounded-lg transition-colors"
      >
        <Lightbulb size={16} />
        {loading ? "Getting hint..." : "Get Hint"}
      </button>

      {hint && (
        <div className="mt-2 p-3 bg-yellow-900/30 rounded-lg border border-yellow-800">
          <p className="text-sm text-yellow-200">{hint}</p>
        </div>
      )}
    </div>
  );
}
```

**Step 2: Add API Method (services/api.js)**

```javascript
export const apiService = {
  // ... existing methods ...

  getHint: (query, difficulty = "medium") =>
    api.post("/hint", { query, difficulty_level: difficulty }),
};
```

**Step 3: Use in Parent Component**

```javascript
import HintButton from "./HintButton";

// In your MessageBubble or InputArea
<HintButton query={currentQuery} />;
```

### 3. Add New Knowledge Base Topic

**Step 1: Add Problems (data/math_knowledge_base.json)**

```json
{
  "id": "trig_001",
  "question": "What is sin(30°)?",
  "solution": "sin(30°) is a standard trigonometric value. Using the unit circle or 30-60-90 triangle: sin(30°) = 1/2 = 0.5",
  "answer": "1/2 or 0.5",
  "topic": "Trigonometry",
  "difficulty": "easy"
}
```

**Step 2: Reload Knowledge Base**

```python
# In Python shell or script
from services.rag_engine import RAGEngine
from services.embeddings import EmbeddingService

embedding_service = EmbeddingService()
await embedding_service.initialize()

rag_engine = RAGEngine(embedding_service)
await rag_engine.initialize()

# The new problems will be automatically loaded and embedded
```

**Or restart the backend:**

```bash
# Backend automatically loads KB on startup
python -m uvicorn main:app --reload
```

### 4. Customize Response Style

**Edit Prompt Template (services/gemini_agent.py)**

```python
def _build_prompt(self, query: str, context: Optional[str] = None) -> str:
    # Add your custom instructions
    base_prompt = """
    You are a math tutor with these characteristics:
    - Patient and encouraging
    - Uses simple language
    - Provides visual explanations when helpful
    - Relates concepts to real-world examples
    """

    if context:
        prompt = f"{base_prompt}\n\nContext:\n{context}\n\nQuestion: {query}"
    else:
        prompt = f"{base_prompt}\n\nQuestion: {query}"

    # Add specific formatting instructions
    prompt += """

    Format your response:
    1. Quick Answer (if applicable)
    2. Detailed Explanation
    3. Step-by-step solution
    4. Final answer emphasized
    """

    return prompt
```

---

## Testing Guide

### Backend Testing

**Unit Tests (pytest)**

Create `backend/tests/test_routing.py`:

```python
import pytest
from services.routing import RoutingService
from core.schemas import ChatRequest

@pytest.mark.asyncio
async def test_routing_decision():
    # Setup
    request = ChatRequest(
        message="Solve 2x + 5 = 13",
        session_id="test_session"
    )

    # Mock dependencies
    mock_rag = MockRAGEngine()
    mock_gemini = MockGeminiAgent()
    routing_service = RoutingService(mock_rag, None, mock_gemini, None)

    # Execute
    response = await routing_service.process_query(request)

    # Assert
    assert response.success == True
    assert "x = 4" in response.solution
    assert response.routing.source == "knowledge_base"
```

**Integration Tests**

```python
# backend/tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post(
        "/api/chat",
        json={
            "message": "What is 2+2?",
            "session_id": "test"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "4" in data["solution"]
```

**Run Tests**

```bash
# All tests
pytest backend/tests/

# Specific file
pytest backend/tests/test_routing.py

# With coverage
pytest --cov=backend backend/tests/

# Verbose output
pytest -v backend/tests/
```

### Frontend Testing

**Component Tests (Jest + React Testing Library)**

Create `frontend/src/components/__tests__/MessageBubble.test.jsx`:

```javascript
import { render, screen, fireEvent } from "@testing-library/react";
import MessageBubble from "../MessageBubble";

describe("MessageBubble", () => {
  test("renders user message correctly", () => {
    const message = {
      id: 1,
      role: "user",
      content: "Test question",
      timestamp: "12:00 PM",
    };

    render(<MessageBubble message={message} />);

    expect(screen.getByText("Test question")).toBeInTheDocument();
  });

  test("shows action buttons for AI messages", () => {
    const message = {
      id: 2,
      role: "assistant",
      content: "Test answer",
      timestamp: "12:01 PM",
    };

    const mockAction = jest.fn();
    render(<MessageBubble message={message} onAction={mockAction} />);

    const likeButton = screen.getByTitle("Like");
    fireEvent.click(likeButton);

    expect(mockAction).toHaveBeenCalledWith(message, "like");
  });
});
```

**Run Tests**

```bash
cd frontend

# All tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

### Manual Testing Checklist

**Backend:**

- [ ] Health check returns 200
- [ ] Chat endpoint accepts valid queries
- [ ] Feedback endpoint stores data
- [ ] Analytics endpoint returns stats
- [ ] Invalid requests return proper errors
- [ ] Rate limiting works

**Frontend:**

- [ ] Chat interface loads
- [ ] Can send messages
- [ ] Receives and displays responses
- [ ] Like/dislike buttons work
- [ ] Feedback modal opens
- [ ] Analytics page shows data
- [ ] Sidebar navigation works
- [ ] Settings save correctly

---

## Debugging Tips

### Backend Debugging

**1. Enable Debug Logging**

```python
# backend/main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**2. Use FastAPI Debug Mode**

```python
# backend/main.py
app = FastAPI(debug=True)  # Shows detailed errors
```

**3. Print Debugging**

```python
# In any service
logger.debug(f"Query: {query}")
logger.debug(f"Embedding shape: {embedding.shape}")
logger.debug(f"Search results: {results}")
```

**4. Interactive Debugging (pdb)**

```python
import pdb

def my_function():
    x = calculate_something()
    pdb.set_trace()  # Debugger stops here
    y = process(x)
```

**5. VS Code Debugging**
Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "cwd": "${workspaceFolder}/backend",
      "env": { "PYTHONPATH": "${workspaceFolder}/backend" }
    }
  ]
}
```

### Frontend Debugging

**1. Browser Console**

```javascript
// In any component
console.log("Message sent:", message);
console.log("Response:", response);
console.error("Error occurred:", error);
```

**2. React DevTools**

- Install React DevTools extension
- Inspect component props and state
- View component hierarchy
- Track re-renders

**3. Network Tab**

- Check API requests
- Verify request/response data
- Check for errors (4xx, 5xx)
- Monitor request timing

**4. VS Code Debugging**
Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Chrome: Frontend",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

### Common Issues & Solutions

**Issue: "Module not found"**

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

**Issue: "Port already in use"**

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <process_id> /F

# Or change port in code
```

**Issue: "CORS error"**

```python
# backend/main.py
# Check CORS origins include your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Issue: "Gemini API error"**

```python
# Check API key
import os
print(os.getenv('GEMINI_API_KEY'))

# Test directly
import google.generativeai as genai
genai.configure(api_key="your_key")
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("test")
print(response.text)
```

---

## Best Practices

### Python Code Style

```python
# Use type hints
def process_query(query: str, top_k: int = 3) -> SearchResult:
    pass

# Use descriptive names
# Bad
def f(x, y):
    return x + y

# Good
def calculate_similarity_score(query_embedding: np.ndarray,
                               doc_embedding: np.ndarray) -> float:
    return np.dot(query_embedding, doc_embedding)

# Use docstrings
def search(self, query: str) -> SearchResponse:
    """
    Search knowledge base for similar problems.

    Args:
        query: User's math question

    Returns:
        SearchResponse with matched problems
    """
    pass

# Use list comprehensions
# Bad
results = []
for item in items:
    if item.score > 0.5:
        results.append(item)

# Good
results = [item for item in items if item.score > 0.5]

# Use context managers
# Good
with open('file.txt', 'r') as f:
    data = f.read()
```

### JavaScript/React Code Style

```javascript
// Use const/let, not var
const API_URL = "http://localhost:8000";
let count = 0;

// Use arrow functions
const handleClick = () => {
  console.log("Clicked");
};

// Use destructuring
const { messages, loading, error } = useChat();

// Use template literals
const url = `${API_URL}/api/chat`;

// Use optional chaining
const score = response?.routing?.confidence ?? 0;

// Use async/await
const fetchData = async () => {
  try {
    const response = await apiService.chat(message);
    setData(response);
  } catch (error) {
    console.error(error);
  }
};

// Memoize expensive calculations
const processedData = useMemo(() => expensiveCalculation(data), [data]);

// Use proper React hooks dependencies
useEffect(() => {
  fetchData();
}, [query]); // Include all dependencies
```

### Database Best Practices

```python
# Use parameterized queries (prevents SQL injection)
cursor.execute(
    "SELECT * FROM feedback WHERE rating >= ?",
    (min_rating,)
)

# Use transactions for multiple writes
conn = self._get_connection()
try:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO table1 ...")
    cursor.execute("UPDATE table2 ...")
    conn.commit()
except Exception as e:
    conn.rollback()
    raise
finally:
    conn.close()

# Index frequently queried columns
cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_session_id
    ON chat_history(session_id)
''')
```

### API Design Best Practices

```python
# Use proper HTTP methods
@router.get("/items")      # Read
@router.post("/items")     # Create
@router.put("/items/{id}") # Update
@router.delete("/items/{id}") # Delete

# Use proper status codes
return JSONResponse(
    status_code=201,  # Created
    content={"id": item_id}
)

# Validate input
class CreateItemRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    value: int = Field(..., ge=0, le=100)

# Return consistent responses
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

# Use pagination for large results
@router.get("/items")
async def get_items(skip: int = 0, limit: int = 10):
    items = db.get_items(skip=skip, limit=limit)
    return items
```

### Performance Optimization

```python
# Backend: Use async for I/O operations
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(x):
    return result

# Batch database operations
values = [(x, y, z) for x, y, z in data]
cursor.executemany(
    "INSERT INTO table VALUES (?, ?, ?)",
    values
)

# Use connection pooling
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL, pool_size=10)
```

```javascript
// Frontend: Lazy load components
const AnalyticsView = lazy(() => import("./components/AnalyticsView"));

// Debounce expensive operations
const debouncedSearch = useMemo(
  () => debounce((query) => performSearch(query), 300),
  []
);

// Virtualize long lists
import { FixedSizeList } from "react-window";

<FixedSizeList height={600} itemCount={messages.length} itemSize={100}>
  {MessageRow}
</FixedSizeList>;
```

---

## Contributing Checklist

Before submitting a PR:

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No console.log statements
- [ ] No commented-out code
- [ ] Dependencies minimized
- [ ] Environment variables in .env.example
- [ ] Commit messages follow convention
- [ ] PR description is clear

---

## Resources

### Learning Resources

- **FastAPI:** https://fastapi.tiangolo.com/tutorial/
- **React:** https://react.dev/learn
- **Tailwind CSS:** https://tailwindcss.com/docs
- **Qdrant:** https://qdrant.tech/documentation/
- **Gemini API:** https://ai.google.dev/docs

### Tools

- **Postman:** API testing
- **React DevTools:** Component debugging
- **DB Browser for SQLite:** Database inspection
- **Prettier:** Code formatting
- **ESLint:** JavaScript linting

### Community

- **Stack Overflow:** Questions and answers
- **GitHub Discussions:** Project discussions
- **Discord:** Real-time chat (if applicable)

---

Happy coding! 🚀
