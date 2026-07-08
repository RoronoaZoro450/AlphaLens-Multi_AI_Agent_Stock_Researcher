import asyncio

from AlphaLens.Orchestrator.orchestrator import orchestrator_work
from AlphaLens.graph.state import OrchestratorState


def run_orchestrator_node(ticker: str) -> OrchestratorState:
    state: OrchestratorState = {
        "ticker":     ticker,
        "financials": None,
        "sentiment":  None,
        "technicals": None,
        "risk":       None,
        "valuation":  None,
        "errors":     {},
    }
    return asyncio.run(orchestrator_work(state))