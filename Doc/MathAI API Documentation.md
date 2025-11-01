# 📡 MathAI API Documentation

## Base URL

```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication

Currently no authentication required. Future versions will use JWT tokens.

---

## Table of Contents

- [Health Check](#health-check)
- [Chat Endpoints](#chat-endpoints)
- [Feedback Endpoints](#feedback-endpoints)
- [Knowledge Base](#knowledge-base-endpoints)
- [Analytics](#analytics-endpoints)
- [Web Search](#web-search)
- [Error Handling](#error-handling)

---

## Health Check

### GET /health

Check system health and service status.

**Request:**

```http
GET /api/health
```

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00",
  "services": {
    "rag_engine": true,
    "embedding_service": true,
    "gemini": true,
    "web_search": true,
    "database": true
  }
}
```

**Status Codes:**

- `200` - All services operational
- `503` - One or more services unavailable

---

## Chat Endpoints

### POST /chat

Send a math question and receive a step-by-step solution.

**Request:**

```http
POST /api/chat
Content-Type: application/json

{
  "message": "Solve for x: 2x + 5 = 13",
  "session_id": "optional-session-id",
  "use_feedback_learning": true
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | Math question (1-500 chars) |
| `session_id` | string | No | Session identifier for history |
| `use_feedback_learning` | boolean | No | Use feedback to improve (default: true) |

**Response:** `200 OK`

```json
{
  "success": true,
  "query": "Solve for x: 2x + 5 = 13",
  "solution": "### Step-by-Step Solution:\n\n**Step 1:** Subtract 5 from both sides\n2x = 8\n\n**Step 2:** Divide both sides by 2\nx = 4\n\n**Final Answer:** x = 4",
  "routing": {
    "use_kb": true,
    "confidence": 0.92,
    "reason": "High confidence match (score: 0.920)",
    "source": "knowledge_base"
  },
  "metadata": {
    "model": "gemini-1.5-flash",
    "source": "knowledge_base",
    "confidence": 0.92
  },
  "blocked": false,
  "error": null
}
```

**Error Response:** `400 Bad Request`

```json
{
  "success": false,
  "query": "How to hack?",
  "solution": null,
  "routing": null,
  "metadata": null,
  "blocked": true,
  "error": "Content policy violation. This system only handles mathematics questions."
}
```

**Status Codes:**

- `200` - Success
- `400` - Invalid request (guardrails blocked)
- `429` - Rate limit exceeded
- `500` - Server error

**Example (cURL):**

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the derivative of x^2?",
    "session_id": "my-session-123"
  }'
```

**Example (Python):**

```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "Find the area of a circle with radius 5",
        "session_id": "python-client"
    }
)

data = response.json()
print(data['solution'])
```

**Example (JavaScript):**

```javascript
const response = await fetch("http://localhost:8000/api/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    message: "Integrate sin(x)dx",
    session_id: "js-client",
  }),
});

const data = await response.json();
console.log(data.solution);
```

---

### GET /chat/history

Retrieve chat history for a session.

**Request:**

```http
GET /api/chat/history?session_id=my-session&limit=50
```

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `session_id` | string | Yes | - | Session identifier |
| `limit` | integer | No | 50 | Max messages to return |

**Response:** `200 OK`

```json
{
  "success": true,
  "session_id": "my-session",
  "messages": [
    {
      "timestamp": "2024-01-15T10:30:00",
      "role": "user",
      "content": "Solve 2x + 5 = 13",
      "metadata": null
    },
    {
      "timestamp": "2024-01-15T10:30:05",
      "role": "assistant",
      "content": "### Solution:\n...",
      "metadata": {
        "source": "knowledge_base",
        "confidence": 0.92
      }
    }
  ],
  "count": 2
}
```

**Status Codes:**

- `200` - Success
- `400` - Missing session_id
- `500` - Server error

---

## Feedback Endpoints

### POST /feedback

Submit feedback for a solution.

**Request:**

```http
POST /api/feedback
Content-Type: application/json

{
  "query": "Solve 2x + 5 = 13",
  "solution": "The complete solution text...",
  "rating": 5,
  "comment": "Clear explanation!",
  "improved_solution": null
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | Original question |
| `solution` | string | Yes | AI-generated solution |
| `rating` | integer | No | Rating 1-5 (null for like/dislike) |
| `comment` | string | No | User comments |
| `improved_solution` | string | No | User's suggested improvement |

**Response:** `200 OK`

```json
{
  "success": true,
  "message": "Feedback submitted successfully",
  "feedback_id": 42
}
```

**Status Codes:**

- `200` - Success
- `400` - Invalid rating (must be 1-5)
- `500` - Server error

**Example (Quick Feedback - Like):**

```javascript
await fetch("http://localhost:8000/api/feedback", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: userQuestion,
    solution: aiResponse,
    rating: 5, // Like
  }),
});
```

**Example (Detailed Feedback):**

```javascript
await fetch("http://localhost:8000/api/feedback", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "Find derivative of x^2",
    solution: "The derivative is 2x",
    rating: 4,
    comment: "Good but could explain power rule",
    improved_solution:
      "Using the power rule (d/dx)[x^n] = nx^(n-1), we get 2x^1 = 2x",
  }),
});
```

---

### GET /feedback/stats

Get feedback statistics.

**Request:**

```http
GET /api/feedback/stats
```

**Response:** `200 OK`

```json
{
  "total_feedback": 150,
  "average_rating": 4.2,
  "rating_distribution": {
    "5": 80,
    "4": 40,
    "3": 20,
    "2": 7,
    "1": 3
  },
  "recent_feedback": [
    {
      "timestamp": "2024-01-15T10:30:00",
      "query": "Solve x^2 = 16",
      "rating": 5,
      "comment": "Perfect explanation!"
    }
  ]
}
```

**Status Codes:**

- `200` - Success
- `500` - Server error

---

### GET /feedback/positive

Get positive feedback for learning.

**Request:**

```http
GET /api/feedback/positive?min_rating=4
```

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `min_rating` | integer | No | 4 | Minimum rating to include |

**Response:** `200 OK`

```json
{
  "success": true,
  "count": 25,
  "feedback": [
    {
      "query": "Factor x^2 - 9",
      "solution": "Using difference of squares...",
      "improved_solution": "Recognize this as a^2 - b^2...",
      "rating": 5,
      "comment": "Excellent explanation"
    }
  ]
}
```

---

## Knowledge Base Endpoints

### POST /kb/search

Search knowledge base directly.

**Request:**

```http
POST /api/kb/search
Content-Type: application/json

{
  "query": "quadratic equation",
  "top_k": 3,
  "score_threshold": 0.5
}
```

**Parameters:**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query |
| `top_k` | integer | No | 3 | Number of results |
| `score_threshold` | float | No | 0.5 | Minimum similarity score |

**Response:** `200 OK`

```json
{
  "success": true,
  "query": "quadratic equation",
  "results": [
    {
      "id": "alg_005",
      "question": "Solve x^2 + 5x + 6 = 0",
      "solution": "Step-by-step solution...",
      "answer": "x = -2 or x = -3",
      "topic": "Quadratic Equations",
      "difficulty": "medium",
      "score": 0.89
    }
  ],
  "num_results": 1
}
```

**Status Codes:**

- `200` - Success
- `400` - Invalid parameters
- `500` - Server error

---

### GET /kb/stats

Get knowledge base statistics.

**Request:**

```http
GET /api/kb/stats
```

**Response:** `200 OK`

```json
{
  "success": true,
  "total_problems": 20,
  "collection_name": "math_problems",
  "topics": [
    "Linear Equations",
    "Derivatives",
    "Circle Area",
    "Quadratic Equations"
  ],
  "difficulties": ["easy", "medium", "hard"]
}
```

---

## Analytics Endpoints

### GET /analytics

Get usage analytics.

**Request:**

```http
GET /api/analytics?days=7
```

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `days` | integer | No | 7 | Number of days to analyze |

**Response:** `200 OK`

```json
{
  "period_days": 7,
  "total_queries": 342,
  "total_feedback": 150,
  "average_rating": 4.2,
  "rating_distribution": {
    "5": 80,
    "4": 40,
    "3": 20,
    "2": 7,
    "1": 3
  },
  "events": {
    "query": 342,
    "feedback_submitted": 150,
    "error": 5
  },
  "top_topics": []
}
```

**Status Codes:**

- `200` - Success
- `400` - Invalid days parameter
- `500` - Server error

---

## Web Search

### POST /web/search

Perform web search directly (debugging/testing only).

**Request:**

```http
POST /api/web/search
Content-Type: application/json

{
  "query": "latest developments in calculus"
}
```

**Response:** `200 OK`

```json
{
  "success": true,
  "query": "latest developments in calculus",
  "answer": "AI-generated summary of search results",
  "results": [
    {
      "title": "Advanced Calculus Techniques",
      "url": "https://example.com/calculus",
      "content": "Excerpt from the page...",
      "score": 0.95
    }
  ],
  "num_results": 3,
  "error": null
}
```

**Note:** This endpoint is primarily for testing. Normal chat flow uses web search automatically when needed.

---

## Utility Endpoints

### POST /improve

Generate improved solution based on feedback.

**Request:**

```http
POST /api/improve
Content-Type: application/json

{
  "query": "Find derivative of x^2",
  "solution": "The derivative is 2x",
  "feedback": "Could you explain the power rule?",
  "improved_suggestion": null
}
```

**Response:** `200 OK`

```json
{
  "success": true,
  "improved_solution": "Using the power rule, which states that d/dx[x^n] = nx^(n-1), we can find the derivative of x^2:\n\nd/dx[x^2] = 2x^(2-1) = 2x^1 = 2x\n\nSo the derivative of x^2 is 2x."
}
```

---

### GET /

API root - shows available endpoints.

**Request:**

```http
GET /api/
```

**Response:** `200 OK`

```json
{
  "name": "MathAI API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/api/health",
    "chat": "/api/chat",
    "feedback": "/api/feedback",
    "search": "/api/kb/search",
    "analytics": "/api/analytics",
    "docs": "/docs"
  }
}
```

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

| Code  | Meaning               | Common Causes                     |
| ----- | --------------------- | --------------------------------- |
| `400` | Bad Request           | Invalid input, guardrails blocked |
| `404` | Not Found             | Endpoint doesn't exist            |
| `422` | Validation Error      | Pydantic validation failed        |
| `429` | Too Many Requests     | Rate limit exceeded               |
| `500` | Internal Server Error | Server-side error                 |
| `503` | Service Unavailable   | Service temporarily down          |

### Error Examples

**Validation Error (422):**

```json
{
  "detail": [
    {
      "loc": ["body", "rating"],
      "msg": "ensure this value is less than or equal to 5",
      "type": "value_error.number.not_le"
    }
  ]
}
```

**Guardrails Block (400):**

```json
{
  "success": false,
  "error": "Please ask a mathematics question. This system specializes in math problems.",
  "blocked": true
}
```

**Rate Limit (429):**

```json
{
  "detail": "Rate limit exceeded. Please wait before making more requests."
}
```

---

## Rate Limiting

### Current Limits

- **Default:** 30 requests per minute per IP
- **Burst:** Up to 10 requests in rapid succession
- **Window:** Rolling 60-second window

### Rate Limit Headers

```http
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1705320600
```

### Handling Rate Limits

**Best Practices:**

```javascript
async function makeRequestWithRetry(url, data, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (response.status === 429) {
        // Rate limited, wait and retry
        const retryAfter = response.headers.get("Retry-After") || 60;
        await sleep(retryAfter * 1000);
        continue;
      }

      return await response.json();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
    }
  }
}
```

---

## Interactive API Documentation

**Swagger UI:** `http://localhost:8000/docs`

- Interactive API exploration
- Try endpoints directly
- See request/response schemas
- Download OpenAPI spec

**ReDoc:** `http://localhost:8000/redoc`

- Clean, readable documentation
- Better for reading/printing
- Same content as Swagger

---

## SDK Examples

### Python SDK (requests)

```python
import requests
from typing import Optional, Dict

class MathAIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()

    def chat(self, message: str, session_id: Optional[str] = None) -> Dict:
        """Send a math question and get solution."""
        response = self.session.post(
            f"{self.base_url}/chat",
            json={
                "message": message,
                "session_id": session_id
            }
        )
        response.raise_for_status()
        return response.json()

    def submit_feedback(self, query: str, solution: str, rating: int) -> Dict:
        """Submit feedback for a solution."""
        response = self.session.post(
            f"{self.base_url}/feedback",
            json={
                "query": query,
                "solution": solution,
                "rating": rating
            }
        )
        response.raise_for_status()
        return response.json()

# Usage
client = MathAIClient()
result = client.chat("What is 2+2?")
print(result['solution'])
```

### JavaScript SDK (axios)

```javascript
class MathAIClient {
  constructor(baseURL = "http://localhost:8000/api") {
    this.client = axios.create({ baseURL });
  }

  async chat(message, sessionId = null) {
    const response = await this.client.post("/chat", {
      message,
      session_id: sessionId,
    });
    return response.data;
  }

  async submitFeedback(query, solution, rating) {
    const response = await this.client.post("/feedback", {
      query,
      solution,
      rating,
    });
    return response.data;
  }

  async getAnalytics(days = 7) {
    const response = await this.client.get("/analytics", {
      params: { days },
    });
    return response.data;
  }
}

// Usage
const client = new MathAIClient();
const result = await client.chat("Solve x^2 = 16");
console.log(result.solution);
```

---

## Webhooks (Future)

_Coming soon: Real-time notifications for events_

### Planned Webhook Events

- `solution.generated` - When solution is created
- `feedback.received` - When feedback is submitted
- `error.occurred` - When errors happen

---

## Changelog

### Version 1.0.0 (Current)

- Initial release
- Chat endpoint with intelligent routing
- Feedback system
- Knowledge base search
- Analytics dashboard

### Roadmap

- v1.1.0: WebSocket support for real-time chat
- v1.2.0: User authentication (JWT)
- v1.3.0: File upload (solve from images)
- v2.0.0: Multi-language support

---

## Support

- **API Issues:** Open GitHub issue
- **Questions:** Check documentation or ask in discussions
- **Security:** Email brijeshkpurohit04@gmail.com
