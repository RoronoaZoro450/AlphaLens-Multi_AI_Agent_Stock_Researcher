import asyncio

from AlphaLens.SubAgent.FinancialAgent.run_financial_agent import run_financial_agent
from AlphaLens.SubAgent.news_sentiment_agent.run_news_sentiment import run_news_and_sentiment_agent
from AlphaLens.SubAgent.risk_agent.run_risk_agent import run_risk_agent
from AlphaLens.SubAgent.technical_agent.run_technical_agent import run_technical_Agent
from AlphaLens.SubAgent.valuation_agent.run_valuation_agent import run_valuation_agent
from AlphaLens.graph.state import OrchestratorState


async def orchestrator(ticker: str) -> dict:
    tasks = {
        "financials": run_financial_agent(ticker),
        "sentiment": run_news_and_sentiment_agent(ticker),
        "technicals": run_technical_Agent(ticker),
        "risk": run_risk_agent(ticker),
        "valuation": run_valuation_agent(ticker),
    }

    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    state = {"ticker": ticker, "errors": {}}
    for name, result in zip(tasks.keys(), results):
        if isinstance(result, Exception):
            state[name] = None
            state["errors"][name] = str(result)
        else:
            state[name] = result

    return state


async def orchestrator_work(state: OrchestratorState) -> dict:
    report = await orchestrator(state["ticker"])

    return {
        "financials": report["financials"],
        "sentiment":  report["sentiment"],
        "technicals": report["technicals"],
        "risk":       report["risk"],
        "valuation":  report["valuation"],
        "errors":     report["errors"],
    }

