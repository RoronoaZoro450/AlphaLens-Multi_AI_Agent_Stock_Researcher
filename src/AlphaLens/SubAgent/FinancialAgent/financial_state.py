from langgraph.graph import add_messages
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from AlphaLens.SubAgent.FinancialAgent.financial_model import FinancialReport

class FinancialState(TypedDict):                                                                                                                                                                      
    messages: Annotated[list[BaseMessage], add_messages]
    ticker: str
    report: FinancialReport | None 
