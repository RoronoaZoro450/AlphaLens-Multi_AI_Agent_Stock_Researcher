import asyncio
from AlphaLens.SubAgent.FinancialAgent.run_financial_agent import run_financial_agent

result= asyncio.run(run_financial_agent("NVDA"))

print(result)
