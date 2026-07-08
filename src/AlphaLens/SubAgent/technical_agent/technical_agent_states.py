from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class TechnicalState(TypedDict):
    ticker: str
    report: str
    data: dict