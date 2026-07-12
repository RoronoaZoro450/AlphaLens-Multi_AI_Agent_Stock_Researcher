from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition 
from AlphaLens.SubAgent.FinancialAgent.financial_state import FinancialState
from AlphaLens.SubAgent.FinancialAgent.financial_agent_nodes import financial_tool_node , collect_financial_data_node , financial_report_node

graph = StateGraph(FinancialState)
graph.add_node("collect_financial_data", collect_financial_data_node)
graph.add_node("financial_report_writing", financial_report_node)
graph.add_node("financial_tool_node",financial_tool_node)
 
graph.add_edge(START, "collect_financial_data")

graph.add_conditional_edges("collect_financial_data",tools_condition,{"tools": "financial_tool_node", END: "financial_report_writing"})
graph.add_edge("financial_tool_node", "collect_financial_data")

graph.add_edge("financial_report_writing", END)
 
financial_workflow= graph.compile()
