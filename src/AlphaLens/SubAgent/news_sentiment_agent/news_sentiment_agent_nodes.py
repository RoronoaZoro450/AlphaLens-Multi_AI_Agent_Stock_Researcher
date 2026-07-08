from AlphaLens.SubAgent.news_sentiment_agent.news_sentiment_model import NewsSentimentReport
from AlphaLens.SubAgent.news_sentiment_agent.news_sentiment_prompt import NEWS_SENTIMENT_REPORT_PROMPT
from AlphaLens.SubAgent.news_sentiment_agent.news_sentiment_state import NewsSentimentState
from AlphaLens.SubAgent.news_sentiment_agent.news_sentiment_tools import earning_call, get_earnings_history, get_insider_transactions, news_yfinance
from AlphaLens.config.llms import get_llm_for_tools, get_report_writer_llm
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()  


NewsSentiment_tools = [earning_call,news_yfinance,get_insider_transactions,get_earnings_history]
NewsSentiment_tool_node = ToolNode(NewsSentiment_tools)
NewsSentiment_llm_tools = get_llm_for_tools().bind_tools(NewsSentiment_tools)

def NewsSentimentAgent_node(state:NewsSentimentState)->NewsSentimentState:
    response = NewsSentiment_llm_tools.invoke(state["messages"])
    return {"messages": [response]}


def report_node(state: NewsSentimentState):
    """
    Report-writing LLM — receives ONLY plain text tool data.
    Builds a clean 2-message conversation so the API never
    sees tool_use/tool_result blocks → no BadRequestError.
    """
    raw_data = extract_tool_data(state["messages"])
 
    clean_messages = [
        SystemMessage(content=NEWS_SENTIMENT_REPORT_PROMPT),
        HumanMessage(content=f"Here is the collected sentiment data:\n\n{raw_data}"),
    ]
 
    report_writer_llm = get_report_writer_llm().with_structured_output(NewsSentimentReport)
    response = report_writer_llm.invoke(clean_messages)
    message_output = AIMessage(content=response.model_dump_json())
    
    return {"messages": [message_output], "report": response}

#====================================================================================================


def extract_tool_data(messages: list) -> str:
    """Extract tool results as plain text with truncation to stay under token limits."""
    
    # Max chars per tool — keeps total well under 12k tokens
    LIMITS = {
        "earning_call":              2000,  # transcripts are huge, trim hard
        "news_yfinance":             1500,  # headlines + summaries
        "get_earnings_history":      500,   # small structured data, keep all
        "get_insider_transactions":  500,   # small structured data, keep all
    }
    DEFAULT_LIMIT = 800

    parts = []
    for msg in messages:
        if isinstance(msg, ToolMessage):
            limit = LIMITS.get(msg.name, DEFAULT_LIMIT)
            content = msg.content[:limit]  # truncate
            parts.append(f"[{msg.name}]\n{content}")

    return "\n\n".join(parts)

