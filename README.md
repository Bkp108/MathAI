# 🧮 MathAI - Intelligent Math Problem Solver

<div align="center">

![MathAI Banner](https://img.shields.io/badge/MathAI-AI%20Powered%20Tutor-blue?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.10+-green?style=flat-square)](https://python.org)
[![React](https://img.shields.io/badge/React-18-blue?style=flat-square)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal?style=flat-square)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**A full-stack AI-powered math tutor with RAG, web search, and intelligent routing**

[🚀 Quick Start](#quick-start) • [📚 Documentation](#documentation) • [🎯 Features](#features) • [💻 Tech Stack](#tech-stack)

</div>

---

## ✨ Features

- 🧠 **Intelligent AI Tutor** - Step-by-step solutions with clear explanations
- 🔄 **Smart Routing** - Automatic decision: Knowledge Base → Web Search → Direct LLM
- 🎯 **Adaptive Responses** - Concise for simple questions, detailed for complex problems
- 🛡️ **Safety Guardrails** - Input/output validation for appropriate content
- 💬 **Feedback Learning** - Improves continuously from user feedback
- 📊 **Analytics Dashboard** - Track performance, ratings, and usage patterns
- 🎨 **Modern ChatGPT-style UI** - Beautiful, responsive interface with markdown & LaTeX
- ⚡ **Real-time Processing** - Fast responses with loading indicators
- 📝 **Session Management** - Maintains conversation history
- 🔍 **Web Search Integration** - Falls back to Tavily when needed

---

## 🎯 What Makes MathAI Special?

### Intelligent Multi-Source System

```
User Question
      ↓
Input Guardrails ✓
      ↓
Knowledge Base Search
      ↓
Confidence >= 50%?
   ├─ YES → Use KB Context + Gemini
   └─ NO  → Web Search + Gemini
      ↓
Output Guardrails ✓
      ↓
Beautiful Response with Steps
```

### Response Optimization

- **Simple calculations** (2+2) → Quick, concise answer
- **Standard problems** (solve x) → Key steps highlighted
- **Complex topics** (proofs) → Comprehensive explanation

---

## 💻 Tech Stack

### Backend

- **Framework:** FastAPI (Python 3.10+)
- **AI Model:** Google Gemini 2.5 Flash (FREE - 60 req/min)
- **Vector DB:** Qdrant (in-memory/persistent)
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)
- **Web Search:** Tavily API (FREE - 1000 req/month)
- **Database:** SQLite (feedback & analytics)

### Frontend

- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Markdown:** react-markdown with KaTeX support
- **HTTP Client:** Axios

---

## 🚀 Quick Start

### Prerequisites

```bash
✅ Python 3.10 or higher
✅ Node.js 18 or higher
✅ npm or yarn
✅ Internet connection
```

### 🔑 Get FREE API Keys

1. **Google Gemini API** (FREE)

   - Visit: https://aistudio.google.com/apikey
   - Click "Create API Key"
   - Copy your key (starts with `AIza...`)

2. **Tavily Search API** (FREE)
   - Visit: https://tavily.com
   - Sign up for free account
   - Get API key from dashboard (starts with `tvly-...`)

### 📦 Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd "13. MathAI (AI Planets)"

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Install frontend dependencies
cd frontend
npm install
cd ..

# 5. Configure environment variables
# Edit .env file and add your API keys:
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### ✅ Verify Installation

```bash
# Test all connections
python complete_connection.py

# You should see all ✅ for:
# ✅ Gemini API working
# ✅ Tavily API working
# ✅ Embeddings working
# ✅ Qdrant working
# ✅ Database working
# ✅ Knowledge Base loaded
```

### 🎬 Start the Application

**1: Manual Start**

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Wait for: "✅ Application startup complete!"

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 🌐 Access the Application

- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

---

## 📁 Project Structure

```
MathAI/
├── 📁 backend/                 # FastAPI Backend
│   ├── 📁 api/
│   │   ├── routes.py          # REST API endpoints
│   │   └── websocket.py       # Real-time support
│   ├── 📁 core/
│   │   ├── config.py          # Environment settings
│   │   ├── database.py        # SQLite operations
│   │   └── schemas.py         # Pydantic models
│   ├── 📁 services/
│   │   ├── embeddings.py      # SentenceTransformers
│   │   ├── rag_engine.py      # Vector search
│   │   ├── gemini_agent.py    # Gemini API integration
│   │   ├── web_search.py      # Tavily integration
│   │   ├── routing.py         # Intelligent routing
│   │   └── guardrails.py      # Safety checks
│   └── main.py                # FastAPI app entry
│
├── 📁 frontend/                # React Frontend
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── ChatWindow.jsx      # Main chat UI
│   │   │   ├── MessageBubble.jsx   # Message display
│   │   │   ├── InputArea.jsx       # User input
│   │   │   ├── Sidebar.jsx         # Navigation
│   │   │   ├── FeedbackModal.jsx   # Feedback form
│   │   │   ├── AnalyticsView.jsx   # Statistics
│   │   │   └── SettingsPanel.jsx   # Preferences
│   │   ├── 📁 hooks/
│   │   │   └── useChat.js          # Chat logic
│   │   ├── 📁 services/
│   │   │   └── api.js              # API client
│   │   └── App.jsx                 # Root component
│   ├── package.json
│   └── vite.config.js
│
├── 📁 data/                    # Data & Storage
│   ├── math_knowledge_base.json   # Problem database
│   ├── feedback.db                # User feedback
│   └── qdrant_storage/            # Vector embeddings
│
├── 📁 scripts/                 # Utility Scripts
│   ├── start.ps1              # Automated startup
│   └── start-frontend.ps1     # Frontend starter
│
├── 📁 Doc/
│   ├── start.ps1
│   └── start-frontend.ps1
│
├── 📁 image/
│   ├── Chat.png
│   └── Feedback.png
│   └── Out of Topic.png
│
├── 📁 video/
│   ├── MathAI - Improvement feadback.mp4
│   └── MathAI - Out of Context question.mp4
│   └── MathAI - Update Improvement.mp4

├── .env                        # Environment config
├── requirements.txt            # Python dependencies
├── complete_connection.py      # System verification
├── README.md                   # This file
├── USER_GUIDE.md              # Usage guide
├── TROUBLESHOOTING.md         # Problem solutions
└── PROJECT_SUMMARY.md         # Technical overview
```

---

## 🎓 Usage Examples

### ✅ Great Questions to Ask

**Simple Calculations**

```
What is 15 + 27?
Calculate 20% of 150
What is √64?
```

**Algebra**

```
Solve for x: 2x + 5 = 13
Factor x² + 5x + 6
Simplify (x² - 9)/(x - 3)
```

**Calculus**

```
Find the derivative of x³ + 2x
Integrate sin(x)dx
What is the limit of (x² - 1)/(x - 1) as x → 1?
```

**Geometry**

```
Find the area of a circle with radius 5
Calculate the volume of a sphere (r=3)
What is the Pythagorean theorem?
```

### ❌ Questions That Will Be Blocked

```
❌ "What's the weather today?" (not math)
❌ "How to hack a website?" (inappropriate)
❌ "Tell me about history" (off-topic)
```

---

## 🔧 API Endpoints

### Chat Operations

```http
POST   /api/chat              # Send question, get solution
GET    /api/chat/history      # Get session history
```

### Feedback System

```http
POST   /api/feedback          # Submit feedback
GET    /api/feedback/stats    # Get analytics
GET    /api/feedback/positive # Get positive feedback
```

### Knowledge Base

```http
POST   /api/kb/search        # Search knowledge base
GET    /api/kb/stats         # KB statistics
```

### System

```http
GET    /api/health           # Health check
GET    /api/analytics        # Usage analytics
POST   /api/improve          # Improve solution
```

### Full API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# ============================================================
# REQUIRED: AI APIs (Both FREE)
# ============================================================
GEMINI_API_KEY=AIza...              # Get: https://aistudio.google.com/apikey
TAVILY_API_KEY=tvly-dev-...         # Get: https://tavily.com

# ============================================================
# DATABASE
# ============================================================
DATABASE_URL=sqlite:///./data/feedback.db

# ============================================================
# VECTOR DATABASE
# ============================================================
QDRANT_MEMORY=true                  # true=in-memory, false=persistent
QDRANT_PATH=./data/qdrant_storage   # If persistent

# ============================================================
# EMBEDDINGS
# ============================================================
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIM=384

# ============================================================
# RAG CONFIGURATION
# ============================================================
KB_CONFIDENCE_THRESHOLD=0.5         # Minimum confidence for KB usage
KB_TOP_K=3                          # Number of similar problems
WEB_SEARCH_MAX_RESULTS=3            # Max web results

# ============================================================
# SERVER
# ============================================================
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=5173
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# ============================================================
# GUARDRAILS
# ============================================================
ENABLE_GUARDRAILS=true
MAX_QUERY_LENGTH=500

# ============================================================
# LOGGING
# ============================================================
LOG_LEVEL=INFO                      # DEBUG, INFO, WARNING, ERROR
```

---

## 💡 Key Features Explained

### 🔄 Intelligent Routing

The system automatically decides the best source:

1. **Knowledge Base** (confidence ≥ 50%) → Fast, accurate
2. **Web Search** (confidence < 50%) → Current, comprehensive
3. **Direct LLM** (fallback) → Always available

### 🛡️ Safety Guardrails

**Input Validation:**

- ✅ Math-related queries only
- ✅ Appropriate content filter
- ✅ Length limits (max 500 chars)

**Output Validation:**

- ✅ Educational content check
- ✅ Quality verification
- ✅ No inappropriate material

### 💬 Feedback Learning System

1. User gets solution
2. Provides feedback (👍/👎 or detailed)
3. System stores feedback
4. Future responses improve based on patterns

### 📊 Analytics Dashboard

Track:

- Total queries processed
- Average response rating
- Rating distribution (1-5 stars)
- Popular topics
- Usage patterns

---

## 🧪 Testing

### Run All Tests

```bash
# Backend connection test
cd backend
python test_connection.py

# Expected output:
# ✅ Health endpoint working
# ✅ Chat endpoint working
# ✅ Feedback endpoint working

# Complete system verification
python complete_connection.py

# Expected: All 10 tests pass ✅
```

### Manual Testing

1. Visit http://localhost:5173
2. Ask: "Solve 2x + 5 = 13"
3. Verify you get a step-by-step solution
4. Test like/dislike buttons
5. Test feedback modal (··· button)
6. Check analytics dashboard

---

## 🐛 Troubleshooting

### Common Issues & Solutions

**Issue: Backend won't start**

```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Solution: Kill the process or change port
```

**Issue: "Gemini API 404 error"**

```bash
# Make sure model name is correct in backend/services/gemini_agent.py
# Should be: 'gemini-2.5-flash' (not 'gemini-2.5-flash-latest')
```

**Issue: "No response" or blank chat**

```bash
# 1. Check backend is running (Terminal 1)
# 2. Check frontend is running (Terminal 2)
# 3. Open browser console (F12) for errors
# 4. Verify API keys in .env
```

**Issue: Like/Dislike buttons don't work**

```bash
# 1. Check browser console for errors
# 2. Verify frontend files are updated
# 3. Hard refresh browser (Ctrl + F5)
```

### Full Troubleshooting Guide

See **TROUBLESHOOTING.md** for comprehensive solutions

---

## 📚 Documentation

- **USER_GUIDE.md** - How to use MathAI effectively
- **TROUBLESHOOTING.md** - Fix common issues
- **PROJECT_SUMMARY.md** - Technical architecture & overview
- **API Docs** - http://localhost:8000/docs (when running)

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Checklist

- [ ] Set strong `SECRET_KEY` in .env
- [ ] Use persistent Qdrant (`QDRANT_MEMORY=false`)
- [ ] Set `DEBUG_MODE=false`
- [ ] Configure production CORS origins
- [ ] Set up proper logging
- [ ] Enable rate limiting
- [ ] Use environment-specific configs
- [ ] Set up monitoring (optional)

---

## 🎯 Performance

### Current Performance Metrics

- **Response Time:** 2-5 seconds (depends on Gemini API)
- **Accuracy:** High (verified solutions + Gemini)
- **Knowledge Base:** 20 pre-loaded problems (expandable)
- **Concurrent Users:** Supports multiple sessions

### API Rate Limits (FREE Tier)

- **Gemini:** 60 requests/minute
- **Tavily:** 1000 requests/month
- **Backend:** 30 requests/minute (configurable)

---

## 🛠️ Development

### Code Quality

```bash
# Format Python code
black backend/
isort backend/

# Lint frontend
cd frontend
npm run lint
```

### Add New Features

**1. Add to Knowledge Base:**
Edit `data/math_knowledge_base.json`:

```json
{
  "id": "custom_001",
  "question": "Your question here",
  "solution": "Step-by-step solution",
  "answer": "Final answer",
  "topic": "Topic name",
  "difficulty": "easy"
}
```

**2. Customize Prompts:**
Edit `backend/services/gemini_agent.py` → `_build_prompt()`

**3. Adjust Guardrails:**
Edit `backend/services/guardrails.py` → Add/remove keywords

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push** to your branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Contribution Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Ensure all tests pass

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini** - Free, powerful LLM API
- **Tavily** - Excellent web search API
- **Qdrant** - Fast vector database
- **SentenceTransformers** - Quality embeddings
- **FastAPI** - Modern Python web framework
- **React** - Powerful UI library

---

## 📞 Support & Contact

- 📧 **Email:** brijeshkpurohit04@gmail.com
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/your-repo/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/your-repo/discussions)
- 📖 **Full Docs:** [Documentation Site](https://github.com/Bkp108/MathAI/tree/main/Doc)

---

## 🌟 Star History

If you find MathAI helpful, please consider giving it a star! ⭐

---

## 🎓 Educational Use

MathAI is designed for:

- ✅ Learning and understanding math concepts
- ✅ Homework help with explanations
- ✅ Exam preparation
- ✅ Concept verification

**Important:** Use MathAI to _learn_, not just to get answers. Understanding the steps is key to mastering mathematics!

---

## 🚀 Future Roadmap

- [ ] **More Subjects:** Physics, Chemistry integration
- [ ] **Image Input:** Solve problems from photos
- [ ] **Voice I/O:** Speak questions, hear answers
- [ ] **Multi-language:** Support for multiple languages
- [ ] **Progress Tracking:** Monitor learning journey
- [ ] **Collaborative:** Study with friends
- [ ] **Mobile App:** iOS/Android applications
- [ ] **Custom Study Plans:** Personalized learning paths

---

<div align="center">

**Built with ❤️ for students and educators worldwide**

Made with [FastAPI](https://fastapi.tiangolo.com) • [React](https://reactjs.org) • [Gemini AI](https://ai.google.dev)

[⬆ Back to Top](#-mathai---intelligent-math-problem-solver)

</div>
