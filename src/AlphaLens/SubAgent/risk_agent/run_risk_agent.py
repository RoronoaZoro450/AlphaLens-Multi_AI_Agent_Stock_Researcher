
from AlphaLens.SubAgent.risk_agent.risk_agent_graph import risk_agent_workflow


async def run_risk_agent(ticker: str) -> dict:
    initial_state = {
        "ticker": ticker,
        "report": None
    }
    state = await risk_agent_workflow.ainvoke(initial_state)
    return state["report"]
