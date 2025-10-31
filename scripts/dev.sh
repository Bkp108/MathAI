#!/bin/bash

# ============================================================
# MathAI Development Server Launcher
# ============================================================

set -e  # Exit on error

echo "🚀 Starting MathAI Development Servers..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please create .env from .env.example and add your API keys"
    exit 1
fi

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;93m'
NC='\033[0m' # No Color

# Kill any existing processes on our ports
echo "🧹 Cleaning up existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

echo ""
echo -e "${BLUE}📦 Starting Backend (FastAPI on port 8000)...${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment and start backend
cd backend
source ../venv/bin/activate 2>/dev/null || . ../venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

echo ""
echo -e "${BLUE}⚛️  Starting Frontend (React on port 5173)...${NC}"

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait a bit
sleep 3

echo ""
echo -e "${GREEN}✅ Development servers started!${NC}"
echo ""
echo "📍 Backend API:  http://localhost:8000"
echo "📍 API Docs:     http://localhost:8000/docs"
echo "📍 Frontend UI:  http://localhost:5173"
echo ""
echo "💡 Tips:"
echo "   - Backend logs will appear in this terminal"
echo "   - Frontend logs in a separate window"
echo "   - Press Ctrl+C to stop all servers"
echo ""

# Trap to kill both processes on Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# Wait for user to stop
wait