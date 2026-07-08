from langgraph.graph import StateGraph, START, END

from AlphaLens.SubAgent.risk_agent.risk_agent_state import RiskState
from AlphaLens.SubAgent.risk_agent.risk_agent_nodes import risk_report_node,risk_agent_node

graph = StateGraph(RiskState)
    
graph.add_node("risk_agent", risk_agent_node)
graph.add_node("risk_report", risk_report_node)

graph.add_edge(START, "risk_agent")
graph.add_edge("risk_agent", "risk_report")
graph.add_edge("risk_report", END)

risk_agent_workflow = graph.compile()