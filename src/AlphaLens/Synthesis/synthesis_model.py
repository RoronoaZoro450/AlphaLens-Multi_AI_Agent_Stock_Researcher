from pydantic import BaseModel
from typing import List, Optional


class InvestmentMemo(BaseModel):
    ticker: str
    company_name: str
    exchange: str
    recommendation: str              # "Buy" | "Hold" | "Sell"
    conviction: str                  # "High" | "Medium" | "Low"
    price_target: Optional[float] = None
    current_price: Optional[float] = None
    time_horizon: str                # e.g. "6-12 months"
    executive_summary: str
    investment_thesis: str
    fundamentals_section: str
    valuation_section: str
    sentiment_section: str
    technicals_section: str
    risk_section: str
    key_risks_ranked: List[str]
    conflicting_signals: List[str]
    data_gaps: List[str]
    confidence: float