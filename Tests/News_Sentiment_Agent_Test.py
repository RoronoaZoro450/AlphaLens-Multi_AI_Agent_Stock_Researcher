from AlphaLens.SubAgent.news_sentiment_agent.run_news_sentiment import run_news_and_sentiment_agent
import asyncio

result= asyncio.run(run_news_and_sentiment_agent("TCS.NS"))
print(result)