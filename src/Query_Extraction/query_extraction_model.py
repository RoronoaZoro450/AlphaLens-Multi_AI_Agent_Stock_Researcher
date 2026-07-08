from pydantic import BaseModel, Field


class TickerExtraction(BaseModel):
    company_name: str = Field(description="The comapany name extracted form query. ")
    official_company_name : str = Field(description= "The standardized, clean name of the corporation. Return 'UNKNOWN' if not identifiable.")
    ticker : str =Field(description= "The official Ticker of the company ")