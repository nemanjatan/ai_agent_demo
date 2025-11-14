#!/bin/bash
# Railway startup script for frontend
# Uses PORT environment variable from Railway

PORT=${PORT:-4173}
echo "Starting frontend on port $PORT"
npx vite preview --host 0.0.0.0 --port $PORT
