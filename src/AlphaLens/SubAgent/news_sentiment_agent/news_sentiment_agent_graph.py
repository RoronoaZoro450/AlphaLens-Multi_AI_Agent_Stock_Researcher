from langgraph.graph import StateGraph, START, END
from AlphaLens.SubAgent.news_sentiment_agent.news_sentiment_state import NewsSentimentState
from langgraph.prebuilt import tools_condition 
from AlphaLens.SubAgent.news_sentiment_agent.news_sentiment_agent_nodes import NewsSentimentAgent_node, report_node, NewsSentiment_tool_node

graph = StateGraph(NewsSentimentState)
graph.add_node("NewsSentimentAgent",NewsSentimentAgent_node)
graph.add_node("NewsSentimentTools",NewsSentiment_tool_node)
graph.add_node("ReportWriter",report_node)

graph.add_edge(START,"NewsSentimentAgent")
graph.add_conditional_edges("NewsSentimentAgent",tools_condition,{"tools": "NewsSentimentTools",END:"ReportWriter" })
graph.add_edge("NewsSentimentTools","NewsSentimentAgent")
graph.add_edge("ReportWriter",END)

NewsSentimentWorkflow=graph.compile()