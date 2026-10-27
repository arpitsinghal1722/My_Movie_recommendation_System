#!/bin/bash
# ─── CineAI Startup Script ───────────────────────────────────────────────────
echo ""
echo "🎬  CineAI — Movie ReAct Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check .env
if [ ! -f .env ]; then
  echo "❌  .env not found. Copy from template:"
  echo "    cp .env.example .env  →  then fill in your API keys"
  exit 1
fi

source .env

if [ -z "$TMDB_API_KEY" ] || [ "$TMDB_API_KEY" = "your_tmdb_api_key_here" ]; then
  echo "❌  TMDB_API_KEY not set in .env"
  echo "    Get a free key at: https://www.themoviedb.org/settings/api"
  exit 1
fi

echo "✅  TMDB key found"
[ -n "$OPENAI_API_KEY" ] && echo "✅  OpenAI key found (ReAct Agent enabled)" || echo "⚠️   No OpenAI key — using TMDB Direct mode only"
echo ""

# Start backend
echo "🚀  Starting FastAPI backend on http://localhost:8000 ..."
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

sleep 2

# Start frontend
echo "🎨  Starting React frontend on http://localhost:3000 ..."
cd frontend && npm start &
FRONTEND_PID=$!

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Frontend : http://localhost:3000"
echo "  Backend  : http://localhost:8000"
echo "  API Docs : http://localhost:8000/docs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Press Ctrl+C to stop both servers"
echo ""

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'" SIGINT SIGTERM
wait
