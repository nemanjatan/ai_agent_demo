#!/bin/bash
# Railway build script for backend

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

echo "🌐 Installing Playwright browser..."
playwright install chromium --with-deps || playwright install chromium

echo "✅ Build complete!"
