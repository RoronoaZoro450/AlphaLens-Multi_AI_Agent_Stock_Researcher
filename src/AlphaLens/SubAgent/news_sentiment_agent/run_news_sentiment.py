from langchain_core.messages import HumanMessage, SystemMessage
from AlphaLens.SubAgent.news_sentiment_agent.news_sentiment_agent_graph import NewsSentimentWorkflow
from AlphaLens.SubAgent.news_sentiment_agent.news_sentiment_prompt import NEWS_SENTIMENT_SYS_PROMPT
from AlphaLens.graph.state import OrchestratorState

async def run_news_and_sentiment_agent (ticker:str) -> OrchestratorState:
    """
    Kicks off the LangGraph workflow for news and sentiment analysis.
    """
    # Initialize the state with the System Prompt and the Human's request
    initial_state = {
        "messages": [
            SystemMessage(content=NEWS_SENTIMENT_SYS_PROMPT),
            HumanMessage(content=f"Analyze the current news and earnings sentiment for ticker: {ticker}")
        ],
        "ticker": ticker,
        "result": ""
    }
    
    # Run the graph
    final_state = await NewsSentimentWorkflow.ainvoke(initial_state)
    
    message = final_state["messages"][-1].content

    return message

