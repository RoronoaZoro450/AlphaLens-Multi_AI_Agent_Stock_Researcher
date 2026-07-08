from typing import TypedDict

class RiskState(TypedDict):
    ticker: str
    computed_risks: dict | None
    report: dict | None
