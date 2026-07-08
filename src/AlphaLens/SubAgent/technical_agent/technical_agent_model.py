from pydantic import BaseModel
from typing import List

class KeyLevels(BaseModel):
    resistance: float
    support: float

class TechnicalReport(BaseModel):
    overall_signal: str          # "Bullish" | "Bearish" | "Neutral"
    confidence: float            # 0 to 1
    trend_verdict: str           # SMA cross, EMA, Bollinger interpretation
    momentum_verdict: str        # RSI, MACD, Stoch interpretation
    volume_verdict: str          # OBV, volume spike, ADL interpretation
    volatility_verdict: str      # ATR, hist_vol, 52w position interpretation
    key_signals: List[str]       # e.g. ["Golden cross confirmed", "RSI approaching overbought"]
    risks: List[str]             # e.g. ["RSI at 72 — overbought risk", "Volume declining on rally"]
    entry_zone: str              # e.g. "Wait for RSI pullback to 55 before entering"
    key_levels: KeyLevels        # resistance and support prices
    summary: str