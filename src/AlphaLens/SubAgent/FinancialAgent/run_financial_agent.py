
from AlphaLens.SubAgent.FinancialAgent.financial_prompts import FINANCIAL_SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage
from AlphaLens.SubAgent.FinancialAgent.financial_agent_graph import financial_workflow
from AlphaLens.graph.state import OrchestratorState

async def run_financial_agent(ticker: str) -> OrchestratorState:
    """Run the fundamentals agent for a ticker and return a validated report."""
 
    initial_state = {
        "ticker": ticker,
        "messages": [
            SystemMessage(content=FINANCIAL_SYSTEM_PROMPT),
            HumanMessage(content=f"Research the fundamentals for ticker: {ticker.upper()}"),
        ],
    }
    report = await financial_workflow.ainvoke(initial_state)
    message = report["messages"][-1].content
    return message
 
