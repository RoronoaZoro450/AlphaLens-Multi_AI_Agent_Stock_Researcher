from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class FinancialReport(BaseModel):
    company_name:   Optional[str]
    exchange:       Optional[str]
    sector:         Optional[str]
    reasoning:      str = Field(description="Show your step-by-step math for the health_score and confidence penalties here BEFORE outputting the final numbers.")
    health_score:   float                                            
    confidence:     float                                            
    recommendation: Literal["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]
    summary:        str        
    report_summary: str        
    positives:      List[str]
    red_flags:      List[str]
    data_gaps:      List[str]
    key_metrics:    Dict[str, Any]  # PE, EPS, FCF, D/E, margins, ROE, target price
    sources:        List[str]
