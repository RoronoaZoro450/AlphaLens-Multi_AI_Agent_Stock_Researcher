from Query_Extraction.query_extraction_model import TickerExtraction
from AlphaLens.config.llms import get_report_writer_llm
from langchain_core.prompts import ChatPromptTemplate
from AlphaLens.utils.yf_utils import yf_search_with_retry
import logging

logger = logging.getLogger(__name__)


def ticker_extraction_tool(query: str) -> dict:
    """Used to find the official company and ticker of the company."""
    structured_llm = get_report_writer_llm().with_structured_output(TickerExtraction)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
                You are a financial data assistant. Extract the full official company name
                and its stock ticker symbol from the user's query.
                If the company cannot be identified, set company_name and ticker to 'UNKNOWN'.
                """),
        ("human", """
                    Analyze the following user query:
                    ---
                    Query: "{user_prompt}"
                    ---
                    """)
        ])

    chain = prompt | structured_llm
    llm_response = chain.invoke({"user_prompt": query})
    result = llm_response.model_dump()

    # LLM could not identify a company at all
    if result['company_name'] == 'UNKNOWN' or result['ticker'] == 'UNKNOWN':
        return {"status": "not_found", "message": "Could not identify a company from your query."}

    llm_ticker = result.get('ticker', '').strip().upper()

    # --- Try yf.Search for canonical ticker resolution ---
    try:
        quotes = yf_search_with_retry(result['company_name'], max_results=3)
    except RuntimeError as exc:
        # yf.Search exhausted retries (e.g. IP-level 429).
        # Fall back to the ticker the LLM already extracted — better than failing.
        logger.warning(
            "yf.Search failed (%s). Falling back to LLM-extracted ticker '%s'.",
            exc, llm_ticker,
        )
        if llm_ticker:
            return {
                "status": "resolved",
                "ticker": llm_ticker,
                "name": result.get('official_company_name') or result['company_name'],
                "source": "llm_fallback",   # signals downstream that search was skipped
            }
        return {"status": "error", "message": str(exc)}

    if not quotes:
        # Search succeeded but returned nothing — still use LLM ticker if available
        if llm_ticker:
            return {
                "status": "resolved",
                "ticker": llm_ticker,
                "name": result.get('official_company_name') or result['company_name'],
                "source": "llm_fallback",
            }
        return {"status": "not_found", "message": f"No ticker found for '{result['company_name']}'"}

    # Only ONE match
    if len(quotes) == 1:
        q = quotes[0]
        return {
            "status": "resolved",
            "ticker": q['symbol'],
            "name": q.get('longname') or q.get('shortname', q['symbol']),
        }

    # MULTIPLE matches — let user pick
    candidates = [
        {
            "ticker": q['symbol'],
            "name": q.get('longname') or q.get('shortname', q['symbol']),
            "exchange": q.get('exchange', 'Unknown'),
        }
        for q in quotes[:5]
    ]

    return {"status": "needs_confirmation", "candidates": candidates}
