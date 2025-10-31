# MathAI - Intelligent Math Problem Solver

A full-stack AI-powered math tutor with RAG (Retrieval-Augmented Generation), web search, and human-in-the-loop feedback.

## Features

- 🧮 **Step-by-step Math Solutions** - Clear explanations for algebra, calculus, geometry, and more
- 🔍 **Smart Routing** - Uses knowledge base first, falls back to web search
- 🛡️ **Guardrails** - Input/output validation for safety
- 💬 **Feedback Learning** - Improves from user corrections
- 📊 **Analytics Dashboard** - Track performance and usage
- 🎨 **Modern UI** - ChatGPT-style interface

## Tech Stack

**Backend:**

- FastAPI (Python 3.9+)
- Qdrant Vector Database
- Google Gemini 1.5 Flash (FREE)
- Tavily Web Search API
- SentenceTransformers for embeddings
- SQLite for feedback storage

**Frontend:**

- React 18
- Vite
- Tailwind CSS
- Lucide Icons

## Quick Start

### Prerequisites

```bash
# Required
Python 3.9+
Node.js 18+
npm or yarn

# API Keys (both FREE)
Google Gemini API: https://aistudio.google.com/apikey
Tavily API: https://tavily.com
```

### Installation

1. **Clone the repository**

```bash
git clone <your-repo>
cd MathAI
```

2. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here
```

3. **Install backend dependencies**

```bash
pip install -r requirements.txt
```

4. **Install frontend dependencies**

```bash
cd frontend
npm install
cd ..
```

5. **Initialize database and load knowledge base**

```bash
python scripts/init_db.py
python scripts/load_data.py
```

6. **Start development servers**

```bash
# Option 1: Use convenience script
bash scripts/dev.sh

# Option 2: Manual (2 terminals)
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

7. **Open browser**

```
Frontend: http://localhost:5173
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

## Project Structure

```
MathAI/
├── backend/          # FastAPI backend
│   ├── api/         # API routes
│   ├── core/        # Config & database
│   ├── services/    # Business logic
│   └── utils/       # Helpers
├── frontend/         # React frontend
│   └── src/
│       ├── components/
│       ├── hooks/
│       └── services/
├── data/            # Knowledge base & configs
├── notebooks/       # Original Jupyter notebooks
└── scripts/         # Utility scripts
```

## API Endpoints

### Chat

- `POST /api/chat` - Send math question, get solution
- `GET /api/chat/history` - Get chat history

### Feedback

- `POST /api/feedback` - Submit feedback for a solution
- `GET /api/feedback/stats` - Get analytics

### System

- `GET /api/health` - Health check
- `GET /api/kb/search` - Search knowledge base directly

## Configuration

Edit `.env` file:

```env
# Required
GEMINI_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key

# Optional
DATABASE_URL=sqlite:///./data/feedback.db
QDRANT_MEMORY=true
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
```

## Usage Examples

### Sample Questions

```
✅ Good questions:
- "Solve for x: 2x + 5 = 13"
- "Find the derivative of 3x² + 2x - 1"
- "What is the area of a circle with radius 5 cm?"
- "Prove the Pythagorean theorem"

❌ Will be blocked:
- "What's the weather today?" (not math)
- "How to hack a website?" (inappropriate)
```

### Feedback System

1. Ask a question
2. Review the solution
3. Click feedback buttons (👍/👎)
4. Optionally provide:
   - Rating (1-5 stars)
   - Comments
   - Improved solution

The system learns from your feedback!

## Development

### Run tests

```bash
# Backend
pytest backend/tests/

# Frontend
cd frontend
npm test
```

### Code formatting

```bash
# Backend
black backend/
isort backend/

# Frontend
cd frontend
npm run lint
```

### Build for production

```bash
# Backend
docker build -f docker/Dockerfile.backend -t mathai-backend .

# Frontend
cd frontend
npm run build
```

## Docker Deployment

```bash
# Start all services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

## Troubleshooting

### "API key not configured"

- Make sure `.env` file exists in project root
- Check that `GEMINI_API_KEY` is set correctly
- Restart backend server

### "Knowledge base not found"

- Run `python scripts/load_data.py`
- Check that `data/math_knowledge_base.json` exists

### "Port already in use"

- Backend: Change port in `backend/main.py`
- Frontend: Set `PORT=3000` in `frontend/.env`

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file

## Acknowledgments

- Google Gemini for free LLM API
- Tavily for web search
- Qdrant for vector database
- SentenceTransformers for embeddings

## Support

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](your-repo/issues)
- 📖 Docs: [Full Documentation](your-docs-link)

---

Built with ❤️ for students and educators
