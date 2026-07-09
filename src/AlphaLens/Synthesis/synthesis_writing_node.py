from AlphaLens.Synthesis.synthesis_prompt import SYNTHESIS_SYSTEM_PROMPT
from AlphaLens.Synthesis.synthesis_model import InvestmentMemo
from langchain_core.messages import HumanMessage, SystemMessage
from AlphaLens.graph.state import OrchestratorState
from AlphaLens.config.llms import get_synthesis_llm
from langsmith import traceable

@traceable
async def synthesis_node(state: OrchestratorState) -> dict:
    payload = build_synthesis_input(state)

    messages = [
        SystemMessage(content=SYNTHESIS_SYSTEM_PROMPT),
        HumanMessage(content=f"Here are the 5 specialist reports for  ({state['ticker']}):\n\n{payload}"),
    ]

    synthesis_llm = get_synthesis_llm().with_structured_output(InvestmentMemo)
    response = await synthesis_llm.ainvoke(messages)

    return {"synthesis": response.model_dump()}

def build_synthesis_input(state: OrchestratorState) -> str:
    user_payload = f"""
        Ticker: {state['ticker']}

        --- FINANCIALS ---
        {state.get('financials')}

        --- SENTIMENT ---
        {state.get('sentiment')}

        --- TECHNICALS ---
        {state.get('technicals')}

        --- RISK ---
        {state.get('risk')}

        --- VALUATION ---
        {state.get('valuation')}

        --- ERRORS (agents that failed) ---
        {state.get('errors', {})}
        """

    return user_payload
