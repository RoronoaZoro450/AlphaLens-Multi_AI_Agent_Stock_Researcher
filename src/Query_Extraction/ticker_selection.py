# only used when running in cli ====================================

from Query_Extraction.query_extraction import ticker_extraction_tool

def ticker_resolver(query: str) -> str:
    res = ticker_extraction_tool(query)

    status = res["status"]

    if status == "not_found":
        raise ValueError(f"Could not resolve ticker: {res['message']}")

    if status == "error":
        raise RuntimeError(f"Ticker lookup failed: {res['message']}")

    if status == "resolved":
        source = res.get("source", "yf_search")
        if source == "llm_fallback":
            print(f"[Warning] Yahoo Finance search unavailable — using LLM-inferred ticker: {res['ticker']}")
        return res["ticker"]

    if status == "needs_confirmation":
        print("Multiple matches found. Which company did you mean?")
        for i, c in enumerate(res["candidates"], 1):
            print(f"  {i}. {c['name']} ({c['ticker']}) — {c['exchange']}")
        choice = input("Enter number (or 'none' to cancel): ").strip()
        if not choice.isdigit() or choice.lower() == "none":
            userquery = input("\nTry again with a more specific company name: ")
            return ticker_resolver(userquery)
        idx = int(choice) - 1
        selected = res["candidates"][min(idx, len(res["candidates"]) - 1)]
        return selected["ticker"]

    raise RuntimeError(f"Unexpected ticker resolution status: '{status}'")