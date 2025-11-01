# 🏗️ MathAI Architecture Documentation

## Table of Contents

- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Component Details](#component-details)
- [Data Flow](#data-flow)
- [Technology Decisions](#technology-decisions)
- [Scaling Considerations](#scaling-considerations)

---

## System Overview

MathAI is a **microservices-based** intelligent tutoring system that combines multiple AI techniques to provide accurate, educational math solutions.

### Key Architectural Principles

1. **Separation of Concerns** - Frontend, Backend, and AI services are decoupled
2. **Smart Routing** - Intelligent decision-making between data sources
3. **Fail-Safe Design** - Graceful degradation when services fail
4. **Stateless Backend** - Easy horizontal scaling
5. **Event-Driven** - Feedback loop for continuous improvement

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Browser    │  │    Mobile    │  │   Desktop    │         │
│  │   (React)    │  │  (Future)    │  │   (Future)   │         │
│  └──────┬───────┘  └──────────────┘  └──────────────┘         │
└─────────┼──────────────────────────────────────────────────────┘
          │
          │ HTTP/REST
          │
┌─────────▼──────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                          │
│  ┌───────────────────────────────────────────────────┐         │
│  │              FastAPI Application                   │         │
│  │  ┌─────────────────────────────────────────────┐  │         │
│  │  │         CORS Middleware                     │  │         │
│  │  │         Rate Limiting                       │  │         │
│  │  │         Authentication (Future)             │  │         │
│  │  │         Logging & Monitoring                │  │         │
│  │  └─────────────────────────────────────────────┘  │         │
│  └───────────────────────────────────────────────────┘         │
└─────────┬──────────────────────────────────────────────────────┘
          │
          │
┌─────────▼──────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              INPUT GUARDRAILS SERVICE                     │  │
│  │  • Content validation     • Math detection               │  │
│  │  • Length check           • Safety filtering             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 ROUTING SERVICE                          │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Decision Engine:                                  │  │  │
│  │  │  1. Query embedding generation                     │  │  │
│  │  │  2. Knowledge Base similarity search               │  │  │
│  │  │  3. Confidence scoring                             │  │  │
│  │  │  4. Source selection (KB vs Web vs Direct)        │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│           │                    │                    │           │
│           ▼                    ▼                    ▼           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │  RAG ENGINE    │  │  WEB SEARCH    │  │  DIRECT LLM    │   │
│  │   (Qdrant)     │  │   (Tavily)     │  │   (Gemini)     │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
│           │                    │                    │           │
│           └────────────────────┴────────────────────┘           │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              SOLUTION GENERATION SERVICE                 │  │
│  │               (Google Gemini 1.5 Flash)                  │  │
│  │  • Context assembly    • Prompt engineering              │  │
│  │  • Response generation • Markdown formatting             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              OUTPUT GUARDRAILS SERVICE                   │  │
│  │  • Quality check       • Content safety                  │  │
│  │  • Format validation   • Length verification             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────┬──────────────────────────────────────────────────────┘
          │
          │
┌─────────▼──────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │  Vector Store  │  │   Relational   │  │    Cache       │   │
│  │   (Qdrant)     │  │    (SQLite)    │  │  (In-Memory)   │   │
│  │                │  │                │  │                │   │
│  │  • Embeddings  │  │  • Feedback    │  │  • Sessions    │   │
│  │  • Knowledge   │  │  • Analytics   │  │  • Temp data   │   │
│  │    Base        │  │  • Chat logs   │  │                │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
          │
          │ Feedback Loop
          │
┌─────────▼──────────────────────────────────────────────────────┐
│                    LEARNING LAYER                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FEEDBACK PROCESSING SERVICE                 │  │
│  │  • Rating analysis    • Pattern detection                │  │
│  │  • Solution ranking   • Continuous improvement           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Frontend Layer (React)

**Purpose:** User interface and experience

**Components:**

```javascript
src/
├── components/          # UI components
│   ├── ChatWindow      # Main conversation interface
│   ├── MessageBubble   # Individual message display
│   ├── InputArea       # User input with validation
│   ├── Sidebar         # Navigation & history
│   ├── FeedbackModal   # Feedback collection
│   └── Analytics       # Performance dashboard
├── hooks/              # Custom React hooks
│   └── useChat         # Chat state management
└── services/           # API communication
    └── api.js          # Axios client with interceptors
```

**Key Features:**

- **Real-time updates:** WebSocket-ready architecture
- **Markdown rendering:** KaTeX for math formulas
- **Responsive design:** Mobile-first approach
- **Error boundaries:** Graceful error handling
- **State management:** React hooks + local storage

**Technology Choices:**

- **React 18:** Latest features (concurrent rendering)
- **Vite:** Fast build tool (HMR in <50ms)
- **Tailwind CSS:** Utility-first styling (< 10KB gzipped)
- **Axios:** Promise-based HTTP client

---

### 2. API Gateway Layer (FastAPI)

**Purpose:** Request routing, validation, and security

**Endpoints Structure:**

```python
/api
├── /chat                # Main chat interface
│   ├── POST /          # Send message
│   └── GET /history    # Get history
├── /feedback           # Feedback system
│   ├── POST /          # Submit feedback
│   ├── GET /stats      # Get statistics
│   └── GET /positive   # Get positive feedback
├── /kb                 # Knowledge base
│   ├── POST /search    # Search directly
│   └── GET /stats      # KB statistics
├── /analytics          # Usage analytics
│   └── GET /           # Get metrics
└── /health             # System health
    └── GET /           # Health check
```

**Middleware Stack:**

```
Request
  ↓
CORS Middleware (origin validation)
  ↓
Rate Limiting Middleware (30 req/min)
  ↓
Logging Middleware (structured logging)
  ↓
Error Handler Middleware (exception catching)
  ↓
Route Handler
  ↓
Response
```

**Features:**

- **Automatic OpenAPI docs:** /docs and /redoc
- **Request validation:** Pydantic schemas
- **Async support:** Non-blocking I/O
- **Error handling:** Comprehensive exception handlers
- **CORS:** Configurable origins

---

### 3. Routing Service (Brain of the System)

**Purpose:** Intelligent decision-making for query handling

**Decision Algorithm:**

```python
def route_query(query: str) -> Decision:
    # Step 1: Generate embedding
    embedding = embedding_service.encode(query)

    # Step 2: Search knowledge base
    results = qdrant.search(embedding, top_k=3)

    # Step 3: Calculate confidence
    best_score = results[0].score if results else 0.0

    # Step 4: Make decision
    if best_score >= CONFIDENCE_THRESHOLD:
        return Decision(
            source="knowledge_base",
            confidence=best_score,
            context=results[0]
        )
    else:
        # Fallback to web search
        return Decision(
            source="web_search",
            confidence=best_score,
            context=None
        )
```

**Decision Flow:**

```
Query: "Solve 2x + 5 = 13"
  ↓
Generate Embedding (384-dim vector)
  ↓
Search Qdrant (cosine similarity)
  ↓
Results: [(0.92, "2x+5=13 example"), (0.45, "linear eq")]
  ↓
Best Score: 0.92 >= 0.5 threshold
  ↓
Decision: Use Knowledge Base + Context
  ↓
Generate solution with Gemini using KB context
```

**Confidence Calculation:**

- **Cosine similarity:** Between query and KB items
- **Range:** 0.0 to 1.0
- **Threshold:** 0.5 (configurable)
- **Factors:**
  - Semantic similarity
  - Topic match
  - Difficulty alignment

---

### 4. RAG Engine (Knowledge Base)

**Purpose:** Semantic search over curated math problems

**Architecture:**

```
Knowledge Base JSON
        ↓
    Embeddings
        ↓
   Qdrant Store
        ↓
    Vector Search
        ↓
   Top-K Results
```

**Vector Database (Qdrant):**

```python
Collection: "math_problems"
├── Vectors: 384-dimensional (all-MiniLM-L6-v2)
├── Payload: {
│     question: str,
│     solution: str,
│     answer: str,
│     topic: str,
│     difficulty: str
│   }
└── Index: HNSW (Hierarchical Navigable Small World)
```

**Search Process:**

1. **Input:** User query
2. **Embedding:** Convert to 384-dim vector
3. **Search:** Find K most similar vectors
4. **Filter:** Apply score threshold
5. **Return:** Matched problems with metadata

**Performance:**

- **Search time:** < 10ms for 1000 items
- **Accuracy:** 90%+ for similar problems
- **Scalability:** Handles 100K+ vectors

---

### 5. Web Search Service (Tavily)

**Purpose:** Fallback for unknown or current topics

**Integration:**

```python
def search(query: str) -> SearchResult:
    # Tavily API call
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=3,
        include_answer=True
    )

    return SearchResult(
        answer=response.answer,        # AI summary
        results=response.results,      # Top sources
        sources=[r.url for r in results]
    )
```

**When Used:**

- KB confidence < 50%
- Current events in math
- Specialized topics not in KB
- User explicitly requests web search

**Features:**

- **AI-generated summary:** Quick answer
- **Source citations:** Transparent sourcing
- **Deep search:** Advanced mode for better results
- **Rate limiting:** 1000 requests/month (FREE)

---

### 6. LLM Service (Google Gemini)

**Purpose:** Natural language solution generation

**Prompt Engineering:**

```python
# For simple calculations
prompt = """
Question: {query}
Provide a BRIEF solution (2-3 sentences):
1. State the calculation
2. Show the result
"""

# For complex problems
prompt = """
Context: {kb_or_web_context}
Question: {query}
Provide step-by-step solution:
1. Break down the problem
2. Explain reasoning
3. Show calculations
4. Give final answer
"""
```

**Response Generation:**

```
User Query + Context
        ↓
   Prompt Assembly
        ↓
   Gemini API Call
        ↓
   Markdown Response
        ↓
  Format & Return
```

**Optimization:**

- **Temperature:** 0.3 (focused, deterministic)
- **Max tokens:** 2048 (sufficient for explanations)
- **Model:** gemini-1.5-flash (fast, free)
- **Caching:** Disabled (dynamic responses)

---

### 7. Guardrails System

**Purpose:** Ensure safety and quality

**Input Guardrails:**

```python
def check_input(query: str) -> bool:
    # Length check
    if len(query) > MAX_LENGTH:
        return False

    # Math detection
    if not is_math_related(query):
        return False

    # Safety check
    if contains_inappropriate(query):
        return False

    return True
```

**Math Detection Algorithm:**

```python
def is_math_related(query: str) -> bool:
    score = 0

    # Check math keywords
    if has_math_keywords(query):
        score += 2

    # Check numbers
    if has_numbers(query):
        score += 1

    # Check math symbols
    if has_math_symbols(query):
        score += 2

    # Check patterns (x^2, 2x, sin(x))
    if has_math_patterns(query):
        score += 2

    return score >= 2
```

**Output Guardrails:**

- Quality check (steps present?)
- Length validation (not too short)
- Content safety (appropriate?)
- Format verification (proper markdown?)

---

### 8. Feedback Learning System

**Purpose:** Continuous improvement through user feedback

**Feedback Loop:**

```
User Provides Feedback
        ↓
   Store in Database
        ↓
   Analyze Patterns
        ↓
  Update Knowledge Base (future)
        ↓
   Improve Future Responses
```

**Feedback Types:**

1. **Quick Feedback:** 👍/👎 (rating 5 or 2)
2. **Detailed Feedback:**
   - Rating (1-5 stars)
   - Comments
   - Improved solution suggestion

**Learning Process:**

```python
def learn_from_feedback():
    # Get positive feedback (4-5 stars)
    positive = db.get_positive_feedback(min_rating=4)

    # Extract patterns
    patterns = analyze_patterns(positive)

    # Update prompts (future)
    update_prompt_templates(patterns)

    # Add to knowledge base (future)
    add_to_kb(high_quality_solutions)
```

**Analytics:**

- Average rating tracking
- Rating distribution analysis
- Common issues identification
- Topic popularity trends

---

## Data Flow

### Complete Request Flow

```
1. USER ENTERS QUERY
   "Solve 2x + 5 = 13"
        ↓

2. FRONTEND (useChat Hook)
   • Validate input locally
   • Add to messages state
   • Show loading indicator
   • POST to /api/chat
        ↓

3. API GATEWAY
   • CORS check
   • Rate limit check
   • Parse JSON body
   • Validate with Pydantic
        ↓

4. INPUT GUARDRAILS
   • Check length (< 500 chars) ✓
   • Detect math keywords ("solve") ✓
   • Safety check (no inappropriate) ✓
   • Sanitize input
        ↓

5. ROUTING SERVICE
   • Generate embedding
     [0.23, -0.45, 0.67, ... 384 dims]
   • Search Qdrant
     Result: 92% match found
   • Decision: Use KB + Gemini
        ↓

6. RAG ENGINE
   • Retrieve matched problem:
     {
       "question": "Solve 2x+5=13",
       "solution": "Step 1: Subtract 5...",
       "answer": "x=4"
     }
        ↓

7. GEMINI SERVICE
   • Build prompt with context
   • Call Gemini API
   • Get response:
     """
     ### Solution:
     **Step 1:** Subtract 5 from both sides
     2x = 8

     **Step 2:** Divide by 2
     x = 4
     """
        ↓

8. OUTPUT GUARDRAILS
   • Quality check ✓
   • Safety check ✓
   • Format validation ✓
        ↓

9. DATABASE
   • Save user message
   • Save assistant response
   • Log analytics event
        ↓

10. API RESPONSE
    {
      "success": true,
      "solution": "### Solution:\n...",
      "routing": {
        "source": "knowledge_base",
        "confidence": 0.92
      },
      "metadata": {...}
    }
        ↓

11. FRONTEND
    • Parse response
    • Render markdown
    • Show action buttons
    • Update chat history
        ↓

12. USER SEES SOLUTION
    (With like/dislike/feedback options)
        ↓

13. USER PROVIDES FEEDBACK (Optional)
    • Click 👍 (rating=5)
    • Stored in database
    • Used for future learning
```

---

## Technology Decisions

### Why These Technologies?

#### Frontend: React

**Chosen because:**

- ✅ Component reusability
- ✅ Large ecosystem
- ✅ Virtual DOM performance
- ✅ Hooks for state management
- ✅ Great developer experience

**Alternatives considered:**

- Vue.js (lighter but smaller ecosystem)
- Svelte (faster but less mature)
- Angular (too heavy for this use case)

#### Backend: FastAPI

**Chosen because:**

- ✅ Async support (non-blocking I/O)
- ✅ Automatic OpenAPI docs
- ✅ Type safety with Pydantic
- ✅ Fast performance (on par with Node.js)
- ✅ Modern Python features

**Alternatives considered:**

- Flask (too basic, no async)
- Django (overkill for API-only)
- Express.js (would need TypeScript)

#### Vector DB: Qdrant

**Chosen because:**

- ✅ Pure vector search (specialized)
- ✅ In-memory mode (dev-friendly)
- ✅ Excellent Python client
- ✅ Fast search (< 10ms)
- ✅ Easy to use

**Alternatives considered:**

- Pinecone (paid service)
- Weaviate (more complex setup)
- FAISS (no managed features)

#### LLM: Google Gemini

**Chosen because:**

- ✅ Completely FREE (60 req/min)
- ✅ Good quality responses
- ✅ Fast inference
- ✅ Easy API integration
- ✅ No credit card required

**Alternatives considered:**

- OpenAI GPT (expensive, $0.002/1K tokens)
- Claude (limited free tier)
- Llama (requires hosting)

#### Embeddings: SentenceTransformers

**Chosen because:**

- ✅ Open source & free
- ✅ Runs locally (no API costs)
- ✅ Good quality (384-dim)
- ✅ Fast inference (< 50ms)
- ✅ Easy to use

**Alternatives considered:**

- OpenAI embeddings (paid)
- Cohere embeddings (limited free)
- Custom trained (too complex)

---

## Scaling Considerations

### Current Capacity

- **Users:** 10-50 concurrent users
- **Requests:** 30/minute (rate limited)
- **Storage:** Limited by disk (SQLite + Qdrant files)
- **Response time:** 2-5 seconds average

### Bottlenecks

1. **Gemini API rate limit** (60 req/min)

   - Solution: Implement queue system
   - Alternative: Add caching layer

2. **SQLite concurrent writes** (limited)

   - Solution: Move to PostgreSQL
   - Alternative: Use write-ahead logging

3. **In-memory Qdrant** (lost on restart)

   - Solution: Use persistent storage
   - Alternative: Regular backups

4. **Single server** (no redundancy)
   - Solution: Load balancer + multiple instances
   - Alternative: Containerized deployment

### Scaling Strategy

#### Phase 1: Vertical Scaling (100-500 users)

```
Current: 2 CPU, 4GB RAM
Upgrade: 4 CPU, 8GB RAM

Changes:
• Add Redis caching
• Use persistent Qdrant
• Migrate to PostgreSQL
• Add request queue
```

#### Phase 2: Horizontal Scaling (500-5000 users)

```
Architecture:
• Load balancer (Nginx)
• 3x API servers
• Separate DB server
• Separate Qdrant server
• Redis cluster
• CDN for frontend
```

#### Phase 3: Distributed System (5000+ users)

```
Architecture:
• Kubernetes cluster
• Auto-scaling (5-20 pods)
• Managed PostgreSQL (RDS)
• Managed Redis (ElastiCache)
• Qdrant Cloud
• CloudFlare CDN
• API Gateway (Kong)
```

### Cost Estimates

#### Current (Free Tier):

- **Gemini:** $0/month (60 req/min)
- **Tavily:** $0/month (1000 req/month)
- **Hosting:** $0 (local development)
- **Total:** $0/month

#### Production (500 users):

- **Server:** $20/month (2GB VPS)
- **Database:** $10/month (managed DB)
- **Gemini:** $0 (still free)
- **Tavily:** $20/month (pro plan)
- **CDN:** $5/month (CloudFlare)
- **Total:** $55/month

#### Scale (5000 users):

- **Kubernetes:** $100/month (3 nodes)
- **Database:** $50/month (larger instance)
- **Qdrant Cloud:** $40/month
- **Redis:** $30/month
- **Gemini:** $50/month (API costs)
- **Tavily:** $50/month (enterprise)
- **CDN:** $20/month
- **Monitoring:** $30/month
- **Total:** $370/month

---

## Security Considerations

### Current Security Measures

1. **Input Validation**

   - Length limits (500 chars)
   - Content filtering
   - SQL injection prevention (Pydantic)
   - XSS prevention (React escaping)

2. **Rate Limiting**

   - 30 requests/minute per IP
   - Prevents DoS attacks
   - Configurable limits

3. **CORS**

   - Whitelisted origins only
   - Credentials not allowed
   - Preflight handling

4. **API Keys**
   - Stored in .env (not in code)
   - Server-side only (not exposed)
   - Rotation capability

### Future Security Enhancements

1. **Authentication**

   - JWT tokens
   - OAuth integration
   - Session management

2. **Authorization**

   - Role-based access
   - API key per user
   - Rate limits per user

3. **Encryption**

   - HTTPS only
   - Database encryption
   - API key encryption

4. **Monitoring**
   - Suspicious activity detection
   - Failed login tracking
   - Unusual query patterns

---

## Monitoring & Observability

### Current Monitoring

1. **Logging**

   - Structured JSON logs
   - Log levels (INFO, WARNING, ERROR)
   - Request/response logging
   - Error stack traces

2. **Analytics**

   - Total queries
   - Average ratings
   - Response times
   - Error rates

3. **Health Checks**
   - /api/health endpoint
   - Service status checks
   - Component availability

### Future Monitoring

1. **APM (Application Performance Monitoring)**

   - New Relic or DataDog
   - Request tracing
   - Performance metrics
   - Error tracking

2. **Metrics**

   - Prometheus + Grafana
   - Custom dashboards
   - Alert rules
   - SLA monitoring

3. **User Analytics**
   - Google Analytics
   - Hotjar (heatmaps)
   - User session recording
   - Conversion funnels

---

## Deployment Architecture

### Development

```
Local Machine
├── Backend (localhost:8000)
├── Frontend (localhost:5173)
├── SQLite (local file)
└── Qdrant (in-memory)
```

### Staging

```
Single VPS
├── Nginx (reverse proxy)
├── Backend (127.0.0.1:8000)
├── Frontend (static files via Nginx)
├── PostgreSQL (local)
└── Qdrant (persistent)
```

### Production

```
Cloud Infrastructure
├── Load Balancer (AWS ALB)
├── Backend Cluster (ECS/EKS)
│   ├── Container 1
│   ├── Container 2
│   └── Container 3
├── Frontend (CloudFront + S3)
├── Database (RDS PostgreSQL)
├── Cache (ElastiCache Redis)
└── Vector Store (Qdrant Cloud)
```

---

## Conclusion

MathAI's architecture is designed to be:

- **Modular:** Easy to modify components
- **Scalable:** Ready for growth
- **Maintainable:** Clear separation of concerns
- **Performant:** Optimized for speed
- **Reliable:** Fault-tolerant design
- **Secure:** Multiple layers of protection

This architecture provides a solid foundation for an intelligent tutoring system while remaining flexible enough to adapt to future requirements.
