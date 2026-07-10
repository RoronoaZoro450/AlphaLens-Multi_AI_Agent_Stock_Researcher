from AlphaLens.graph.graph import workflow
from Query_Extraction.ticker_selection import ticker_resolver
import asyncio
import json
from langsmith import traceable

@traceable
async def main(userquery: str):
    try:
        ticker = ticker_resolver(userquery)
    except (ValueError, RuntimeError) as exc:
        print(f"\n[Error] {exc}")
        return

    orchestrator_state = await workflow.ainvoke({"ticker": ticker})
    memo = orchestrator_state["synthesis"]
    ticker = orchestrator_state["ticker"]
    f_memo = json.dumps(memo, indent=2)
    print(f_memo)

if __name__ == "__main__":
    query = input("query: ")
    asyncio.run(main(query))