from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ValuationModel(BaseModel):
    ticker: str
    current_price: Optional[float] = None
    price_target: Optional[float] = None
    upside_pct: Optional[float] = None
    verdict: str                          # "Undervalued" | "Fairly Valued" | "Overvalued" | "Unknown — missing current price"
    peers_used: List[str] = Field(default_factory=list)
    comps_target: Optional[float] = None
    dcf_target: Optional[float] = None
    graham_number: Optional[float] = None
    median_pe: Optional[float] = None
    median_pb: Optional[float] = None
    median_ev_ebitda: Optional[float] = None
    peer_multiples: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    peers_not_found: List[str] = Field(default_factory=list)
    confidence: float
    summary: str
