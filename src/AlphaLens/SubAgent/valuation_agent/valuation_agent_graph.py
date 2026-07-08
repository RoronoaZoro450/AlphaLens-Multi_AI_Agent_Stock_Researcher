from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition
from AlphaLens.SubAgent.valuation_agent.valuation_agent_nodes import (
    compute_val_node,
    report_node,
    valuation_agent_node,
    valuation_tools_node,
)
from AlphaLens.SubAgent.valuation_agent.valuation_agent_state import valuationState

graph = StateGraph(valuationState)
graph.add_node("ValuationAgent",valuation_agent_node)
graph.add_node("ValuationAgentTools",valuation_tools_node)
graph.add_node("compute_valuation",compute_val_node)
graph.add_node("ReportWriter",report_node)

graph.add_edge(START,"ValuationAgent")
graph.add_conditional_edges(
    "ValuationAgent",
    tools_condition,
    {"tools": "ValuationAgentTools", END: "compute_valuation"},
)
graph.add_edge("ValuationAgentTools","ValuationAgent")
graph.add_edge("compute_valuation","ReportWriter")
graph.add_edge("ReportWriter",END)

valuation_workflow=graph.compile()
