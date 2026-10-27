"""agents/movie_agent.py — ReAct Agent using LangChain 0.1.x API."""
from __future__ import annotations
import logging, os
from typing import Optional
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from prompts.react_prompt import get_react_prompt
from tools.tmdb_tool import search_movies_tool

load_dotenv()
logger = logging.getLogger("movie_react_agent.agent")

class AgentLoggingCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kw):
        logger.info("── LLM CALLED ──")
    def on_tool_start(self, serialized, input_str, **kw):
        logger.info("── TOOL: %s | Input: %s", serialized.get("name","?"), input_str[:200])
    def on_tool_end(self, output, **kw):
        logger.info("── TOOL RESULT (first 300): %s", str(output)[:300])
    def on_tool_error(self, error, **kw):
        logger.error("── TOOL ERROR: %s", error)

def build_movie_agent(model_name=None, temperature=0.0, verbose=True,
                      max_iterations=10, max_execution_time=60.0) -> AgentExecutor:
    api_key = os.getenv("OPENAI_API_KEY","")
    if not api_key: raise EnvironmentError("OPENAI_API_KEY not set in .env")
    model = model_name or os.getenv("OPENAI_MODEL","gpt-4o-mini")
    llm   = ChatOpenAI(model=model, temperature=temperature, api_key=api_key)
    tools = [search_movies_tool]
    agent = create_react_agent(llm=llm, tools=tools, prompt=get_react_prompt())
    executor = AgentExecutor(
        agent=agent, tools=tools, verbose=verbose,
        max_iterations=max_iterations, max_execution_time=max_execution_time,
        handle_parsing_errors=True, callbacks=[AgentLoggingCallback()],
        return_intermediate_steps=True,
    )
    logger.info("Agent ready: model=%s", model)
    return executor

def run_movie_agent(query: str, executor: Optional[AgentExecutor] = None) -> dict:
    if executor is None:
        executor = build_movie_agent(verbose=os.getenv("AGENT_VERBOSE","true")=="true")
    logger.info("Query: '%s'", query)
    try:
        result = executor.invoke({"input": query})
        logger.info("Done. Output length: %d", len(result.get("output","")))
        return result
    except Exception as e:
        logger.exception(e)
        return {"output": f"Error: {e}", "intermediate_steps": []}
