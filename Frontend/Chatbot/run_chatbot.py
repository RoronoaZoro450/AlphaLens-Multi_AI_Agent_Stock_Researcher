from Chatbot.chatbot_graph import graph
from Chatbot.chatbot_prompt import CHAT_SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage

config = {"configurable": {"thread_id": "user-2"}}

def run_chatbot(memo: str, ticker: str, user_input: str) -> str:

    if user_input.lower() in ["exit", "quit"]:
        return "Chat ended."

    formatted_system_text = CHAT_SYSTEM_PROMPT.format(
        Ticker=ticker,
        memo_json=memo
    )

    state_payload = {
        "messages": [
            SystemMessage(content=formatted_system_text),
            HumanMessage(content=user_input),
        ],
    }

    result = graph.invoke(state_payload, config=config)
    
    return result["messages"][-1].content
