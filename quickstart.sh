#!/bin/bash

# ============================================================
# MathAI Quick Start Script
# ============================================================
# This script sets up everything with minimal user input
# ============================================================

set -e  # Exit on error

echo "🚀 MathAI Quick Start Setup"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    
    echo ""
    echo "⚠️  IMPORTANT: You need to add your API keys!"
    echo ""
    echo "1️⃣  Get Google Gemini API key (FREE):"
    echo "    👉 https://aistudio.google.com/apikey"
    echo ""
    echo "2️⃣  Get Tavily API key (FREE):"
    echo "    👉 https://tavily.com"
    echo ""
    
    read -p "Have you added your keys to .env? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Please add your API keys to .env and run this script again"
        exit 1
    fi
fi

# Check Python
echo "🔍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Check Node
echo "🔍 Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Setup Python virtual environment
echo ""
echo "🐍 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Python dependencies installed"

# Initialize database
echo ""
echo "🗄️  Initializing database..."
python scripts/init_db.py
echo "✅ Database initialized"

# Load knowledge base
echo ""
echo "📚 Loading knowledge base..."
python scripts/load_data.py
echo "✅ Knowledge base loaded"

# Setup frontend
echo ""
echo "⚛️  Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
    echo "✅ Frontend dependencies installed"
else
    echo "✅ Frontend dependencies exist"
fi
cd ..

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "📍 To start development servers:"
echo "   ./scripts/dev.sh"
echo ""
echo "📍 Or manually:"
echo "   Terminal 1: cd backend && uvicorn main:app --reload"
echo "   Terminal 2: cd frontend && npm run dev"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🎉 Happy coding!"