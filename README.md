# 🎬 CineAI — Movie ReAct Agent v3.0

> AI-powered movie recommendations | LangChain ReAct | Live TMDB | React UI | SQLite Persistent DB

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **ReAct Agent** | LangChain Thought→Action→Observation reasoning |
| 🎬 **100+ Movies** | Auto-fetched from TMDB, cached in SQLite |
| ➕ **Add My Movie** | Add any movie manually — AI can recommend it |
| ⭐ **Rate My Movie** | AI analyzes and generates rating + review |
| 💾 **Persistent DB** | SQLite — survives restarts |
| ⚡ **TMDB Direct Mode** | No OpenAI key needed for basic use |
| 📱 **Responsive UI** | Mobile + tablet + desktop |

---

## 🚀 Quick Setup (5 mins)

### Step 1 — Install Python deps
```bash
pip install -r requirements.txt
```

### Step 2 — Get FREE API Keys

**TMDB (required, always free):**
1. Go to https://www.themoviedb.org/signup
2. Settings → API → Request API Key → Developer
3. Copy "API Key (v3 auth)"

**OpenAI (optional — for ReAct Agent mode):**
1. Go to https://platform.openai.com/api-keys

### Step 3 — Configure .env
```bash
# Edit the .env file:
TMDB_API_KEY=paste_your_tmdb_key_here
OPENAI_API_KEY=paste_your_openai_key_here   # optional
OPENAI_MODEL=gpt-4o-mini
```

### Step 4 — Start Backend
```bash
uvicorn api_server:app --reload --port 8000
```
Backend auto-fetches 100+ movies from TMDB on first start!

### Step 5 — Start Frontend (new terminal)
```bash
cd frontend
npm install        # first time only
npm start
```

### Step 6 — Open Browser
```
http://localhost:3000
```

---

## 📁 Project Structure

```
movie_react_agent/
├── api_server.py          ← FastAPI backend (all endpoints)
├── main.py                ← CLI entry point
├── start.sh               ← One-command startup script
├── .env                   ← YOUR API KEYS (fill this in)
├── requirements.txt
│
├── agents/
│   └── movie_agent.py     ← LangChain ReAct Agent
├── tools/
│   └── tmdb_tool.py       ← TMDB @tool + LangChain integration
├── prompts/
│   └── react_prompt.py    ← ReAct system prompt
├── utils/
│   └── helpers.py         ← Constraint extraction
│
├── data/
│   ├── database.py        ← SQLite operations (persistent)
│   ├── tmdb_fetcher.py    ← Batch fetch 100+ movies
│   └── movies.db          ← Auto-created SQLite database
│
├── frontend/
│   ├── src/App.js         ← Complete React app
│   └── public/index.html
│
└── evaluation/            ← DeepEval test suite (50+ cases)
```

---

## 🌐 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/health` | Status + DB movie count |
| POST | `/recommend` | AI recommendation |
| GET | `/trending` | TMDB trending |
| GET | `/genres` | All genres |
| GET | `/movies/db` | Browse 100+ cached movies |
| GET | `/movies/user` | Your added movies |
| POST | `/movies/add` | Add a movie |
| POST | `/movies/rate` | AI rates a movie |
| POST | `/movies/save-rating` | Save AI rating to collection |
| GET | `/docs` | Swagger UI |

---

## 💬 Example Queries

```
"Horror movie from the 90s rated R"
"Top 3 sci-fi from 2010s above 8 rating"
"Japanese animated movie"
"Hindi comedy above 8 rating"
"Korean thriller 2019"
"PG-13 family adventure"
"Classic drama above 9 rating"
```

---

## 🧪 Run Evaluation Suite
```bash
pytest evaluation/test_eval_suite.py -v
```

---

*Built with LangChain · FastAPI · React · SQLite · TMDB API*
