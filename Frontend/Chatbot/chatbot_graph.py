from langgraph.graph import StateGraph, START, END
from Chatbot.chatbot_state import ChatState
from Chatbot.chatbot_node import chatbot 
from langgraph.checkpoint.memory import MemorySaver


memory = MemorySaver()
config = {"configurable": {"thread_id": "user-1"}}

graph_builder = StateGraph(ChatState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot",END)

graph = graph_builder.compile(checkpointer=memory)