from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from AlphaLens.SubAgent.FinancialAgent.financial_state import FinancialState
from AlphaLens.SubAgent.FinancialAgent.financial_tools import get_company_info, get_income_statement, get_balance_sheet, get_cash_flow, get_key_ratios      
from AlphaLens.SubAgent.FinancialAgent.financial_model import FinancialReport
from AlphaLens.SubAgent.FinancialAgent.financial_prompts import FINANCIAL_REPORT_PROMPT
from AlphaLens.config.llms import get_llm_for_tools,get_report_writer_llm

financial_tools = [get_company_info, get_income_statement, get_balance_sheet, get_cash_flow, get_key_ratios]
financial_tool_node = ToolNode(financial_tools)


def collect_financial_data_node(state: FinancialState)->FinancialState:

    financial_tool_llm = get_llm_for_tools().bind_tools(financial_tools)
    response = financial_tool_llm.invoke(state["messages"])
    return {"messages": [response]}
    
    
def financial_report_node(state: FinancialState)->FinancialState:
    """
    Report-writing LLM — receives ONLY plain text data, no tool blocks.
    Builds a clean 2-message conversation: system prompt + all tool data.
    """

    financial_report_llm=get_report_writer_llm().with_structured_output(FinancialReport)

    cleaned_context = "\n".join(
        f"{msg.type.capitalize()}: {msg.content}"
        for msg in state["messages"]
        if msg.content
    )
 
    clean_messages = [
        SystemMessage(content=FINANCIAL_REPORT_PROMPT),
        HumanMessage(content=f"Here is the collected financial data:\n\n{cleaned_context}"),
    ]
 
    response = financial_report_llm.invoke(clean_messages)
    message_output = AIMessage(content=response.model_dump_json())
    
    return {"messages": [message_output], "report": response}
