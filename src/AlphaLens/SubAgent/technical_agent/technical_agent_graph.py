from langgraph.graph import END, START, StateGraph
from AlphaLens.SubAgent.technical_agent.technical_agent_nodes import technical_Agent_node, technical_report_node
from AlphaLens.SubAgent.technical_agent.technical_agent_states import TechnicalState


graph = StateGraph(TechnicalState)
graph.add_node("technical_Agent",technical_Agent_node)
graph.add_node("ReportWriter",technical_report_node)

graph.add_edge(START,"technical_Agent")
graph.add_edge("technical_Agent","ReportWriter")
graph.add_edge("ReportWriter",END)

technical_workflow=graph.compile()