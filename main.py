"""main.py — CLI for Movie ReAct Agent."""
import argparse, sys
from dotenv import load_dotenv
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Movie ReAct Agent CLI")
    parser.add_argument("--query","-q", type=str, help="Single query")
    parser.add_argument("--demo", "-d", action="store_true", help="Run 5 demo queries")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    print("\n🎬 Movie ReAct Agent | LangChain + TMDB + OpenAI\n" + "="*50)

    try:
        from agents.movie_agent import build_movie_agent, run_movie_agent
        executor = build_movie_agent(verbose=not args.quiet)
    except EnvironmentError as e:
        print(f"\n❌ Setup Error: {e}")
        print("→ Add OPENAI_API_KEY and TMDB_API_KEY to your .env file")
        sys.exit(1)

    demos = [
        "Recommend a horror movie from the 90s rated R.",
        "Give me top 3 sci-fi movies from the 2010s above 7 rating.",
        "Suggest a Japanese animated movie.",
        "Recommend a Hindi comedy above 8 rating.",
        "Give me a PG-13 family adventure movie.",
    ]

    if args.query:
        result = run_movie_agent(args.query, executor)
        print(f"\n✅ ANSWER:\n{result['output']}\n")
    elif args.demo:
        for q in demos:
            print(f"\n📌 Query: {q}")
            result = run_movie_agent(q, executor)
            print(f"✅ {result['output']}\n{'─'*50}")
    else:
        print("Type your movie request (or 'quit' to exit):\n")
        while True:
            try: q = input("You: ").strip()
            except (EOFError, KeyboardInterrupt): print("\nBye!"); break
            if not q: continue
            if q.lower() in ("quit","exit","q"): print("Bye!"); break
            r = run_movie_agent(q, executor)
            print(f"\n🤖 {r['output']}\n")

if __name__ == "__main__":
    main()
