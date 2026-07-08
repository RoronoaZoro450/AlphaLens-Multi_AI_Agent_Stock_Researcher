
from langchain_core.messages import HumanMessage,SystemMessage
from AlphaLens.SubAgent.valuation_agent.valuation_agent_prompt import VALUATION_AGENT_SYS_PROMPT
from AlphaLens.SubAgent.valuation_agent.valuation_agent_graph import valuation_workflow

async def run_valuation_agent(ticker:str)->dict:
    initial_state = {
        "messages": [
            SystemMessage(content=VALUATION_AGENT_SYS_PROMPT.format(ticker=ticker)),
            HumanMessage(content=f"Analyze the valuation of ticker: {ticker}")
        ],
        "ticker": ticker,
        "computed_valuations": {},
        "result": ""
    }

    response=await valuation_workflow.ainvoke(initial_state)

    return response["result"]


# Backwards-compatible alias for existing notebooks/tests.
run_Valuation_Agent = run_valuation_agent
