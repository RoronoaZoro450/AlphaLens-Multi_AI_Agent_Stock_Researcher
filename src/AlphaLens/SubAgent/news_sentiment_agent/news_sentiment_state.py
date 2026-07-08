from langgraph.graph import add_messages
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage



class NewsSentimentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    ticker: str
    report: str | None