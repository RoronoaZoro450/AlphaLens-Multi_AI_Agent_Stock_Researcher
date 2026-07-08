from pydantic import BaseModel
from typing import List, Literal


class RiskReport(BaseModel):
    overall_risk_level: Literal["Low", "Moderate", "High", "Very High"]
    market_risk_summary: str
    financial_risk_summary: str
    business_risk_summary: str
    liquidity_risk_summary: str
    red_flags: List[str]
    missing_data: List[str]
    confidence: float
    summary: str
