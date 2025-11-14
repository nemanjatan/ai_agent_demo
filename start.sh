#!/bin/bash

# AI Agent Demo Startup Script

echo "🚀 Starting AI Agent Demo..."
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "❌ ERROR: backend/.env file not found!"
    echo "Please create it with: OPENAI_API_KEY=your_key_here"
    exit 1
fi

# Start backend in background
echo "📡 Starting backend server..."
cd backend
python api_server.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Demo started!"
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
