#!/bin/bash
# Railway installation script for backend
# Installs dependencies and Playwright browser

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browser..."
playwright install chromium --with-deps

echo "Installation complete!"
