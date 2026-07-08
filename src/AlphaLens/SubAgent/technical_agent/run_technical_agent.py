from AlphaLens.SubAgent.technical_agent.technical_agent_graph import technical_workflow

async def run_technical_Agent(ticker:str) -> dict:

    final_state = await technical_workflow.ainvoke({
        "ticker": ticker
    })
    
    report = final_state["report"]

    return report