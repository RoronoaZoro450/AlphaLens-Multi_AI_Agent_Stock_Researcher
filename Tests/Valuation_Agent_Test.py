import asyncio
from AlphaLens.SubAgent.valuation_agent.run_valuation_agent import run_Valuation_Agent

result = asyncio.run(run_Valuation_Agent("NVDA"))
print(result)
