from typing import TypedDict

class OrchestratorState(TypedDict):
    ticker: str
    company_name: str
    financials:   dict | None
    sentiment:    dict | None
    technicals:   dict | None
    risk:         dict | None
    valuation:    dict | None
    errors:       dict

    synthesis : dict | None