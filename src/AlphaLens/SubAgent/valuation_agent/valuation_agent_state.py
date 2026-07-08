from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class valuationState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    ticker: str
    computed_valuations: dict
    result: dict | None
