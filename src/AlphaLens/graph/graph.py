from langgraph.graph import StateGraph, START, END
from AlphaLens.Orchestrator.orchestrator import orchestrator_work

from AlphaLens.graph.state import OrchestratorState
from AlphaLens.Synthesis.synthesis_writing_node import synthesis_node

graph = StateGraph(OrchestratorState)

graph.add_node("Orchestrator", orchestrator_work)
graph.add_node("Synthesis", synthesis_node)

graph.add_edge(START, "Orchestrator")
graph.add_edge("Orchestrator", "Synthesis")
graph.add_edge("Synthesis", END)

workflow = graph.compile()
