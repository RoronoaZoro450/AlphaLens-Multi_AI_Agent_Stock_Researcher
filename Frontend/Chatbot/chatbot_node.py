from Chatbot.chatbot_state import ChatState
from AlphaLens.config.llms import get_chatbot_llm


llm = get_chatbot_llm()

def chatbot(state: ChatState):
    
    return {"messages": [llm.invoke(state["messages"])]}