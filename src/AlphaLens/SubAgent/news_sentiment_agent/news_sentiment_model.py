from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class NewsSentimentReport(BaseModel):
    sentiment: str                  # "Bullish" | "Bearish" | "Neutral"
    sentiment_score: float          # -1.0 to 1.0
    earnings_call_summary: str
    earnings_surprise_trend: str
    insider_signal: str             # "Bullish" | "Bearish" | "Neutral"
    insider_summary: str
    news_summary: str
    key_events: List[str]
    red_flags: List[str]
    confidence: float
    sources: List[str]