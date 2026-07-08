import asyncio
from AlphaLens.SubAgent.technical_agent.run_technical_agent import run_technical_Agent

result= asyncio.run(run_technical_Agent("NVDA"))
print(result)
