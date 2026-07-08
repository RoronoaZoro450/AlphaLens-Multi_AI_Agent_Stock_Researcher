import asyncio
from AlphaLens.SubAgent.risk_agent.run_risk_agent import run_risk_agent

result= asyncio.run(run_risk_agent("NVDA"))
print(result)