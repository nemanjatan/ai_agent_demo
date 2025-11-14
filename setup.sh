#!/bin/bash

# AI Agent Demo Setup Script

echo "🔧 Setting up AI Agent Demo..."
echo ""

# Backend setup
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt

echo "🌐 Installing Playwright browser..."
playwright install chromium

if [ ! -f .env ]; then
    echo "⚠️  Creating .env.example (please add your OPENAI_API_KEY)"
    cp .env.example .env 2>/dev/null || echo "OPENAI_API_KEY=your_key_here" > .env
fi

cd ..

# Frontend setup
echo "📦 Installing Node dependencies..."
cd frontend
npm install

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your OPENAI_API_KEY to backend/.env"
echo "2. Run: ./start.sh (or start backend/frontend separately)"
echo ""
