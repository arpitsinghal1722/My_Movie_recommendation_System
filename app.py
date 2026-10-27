"""app.py — Streamlit web UI."""
import os, sys
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="🎬 Movie ReAct Agent", page_icon="🎬", layout="wide")

with st.sidebar:
    st.title("⚙️ Settings")
    openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY",""))
    tmdb_key   = st.text_input("TMDB API Key",   type="password", value=os.getenv("TMDB_API_KEY",""))
    if openai_key: os.environ["OPENAI_API_KEY"] = openai_key
    if tmdb_key:   os.environ["TMDB_API_KEY"]   = tmdb_key
    st.divider()
    st.markdown("**Example Queries:**")
    examples = ["Horror movie from 90s rated R", "Top 3 sci-fi movies above 8 rating",
                "Japanese animated movie", "Hindi comedy film", "Korean thriller above 8"]
    for ex in examples:
        if st.button(ex): st.session_state["q"] = ex

st.title("🎬 Movie ReAct Agent")
st.caption("Real movie recommendations via TMDB API + LangChain ReAct")

if "history" not in st.session_state: st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

prefill = st.session_state.pop("q", "")
query   = st.chat_input("Ask for a movie…") or prefill

if query:
    with st.chat_message("user"): st.markdown(query)
    st.session_state.history.append({"role":"user","content":query})

    def get_agent():
        if "executor" not in st.session_state:
            from agents.movie_agent import build_movie_agent
            st.session_state.executor = build_movie_agent(verbose=False)
        return st.session_state.executor

    with st.chat_message("assistant"):
        with st.spinner("🤔 Searching TMDB…"):
            try:
                from agents.movie_agent import run_movie_agent
                result = run_movie_agent(query, get_agent())
                output = result.get("output","No results.")
            except Exception as e: output = f"Error: {e}"
        st.markdown(output)
        steps = result.get("intermediate_steps",[]) if "result" in dir() else []
        if steps:
            with st.expander("🧠 ReAct Trace"):
                for i,(action,obs) in enumerate(steps,1):
                    st.markdown(f"**Step {i} → Tool:** `{action.tool}`")
                    st.code(str(action.tool_input)[:300])
                    st.markdown(f"**Observation:** {str(obs)[:400]}")
    st.session_state.history.append({"role":"assistant","content":output})
