"""
Centralized yfinance proxy configuration.

Import this module ONCE at app startup (e.g. in AlphaLens.__init__) to route
ALL yfinance HTTP traffic through the proxy defined in YFINANCE_PROXY env var.

How it works:
  1. Creates a requests.Session with proxy + retry settings.
  2. Monkey-patches yf.Ticker and yf.Search so every call automatically
     uses the proxied session — zero changes needed in tool files.
"""

import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()

PROXY_URL = os.getenv("YFINANCE_PROXY", "")


def _build_proxied_session() -> requests.Session:
    """Build a requests.Session pre-configured with proxy & retry logic."""
    session = requests.Session()

    if PROXY_URL:
        session.proxies = {
            "http": PROXY_URL,
            "https": PROXY_URL,
        }

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        )
    })

    # Retry on 429 (rate-limit) and 5xx errors with exponential back-off
    retry = Retry(
        total=3,
        backoff_factor=1,          # 1s, 2s, 4s
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


# ---------------------------------------------------------------------------
# Monkey-patch yf.Ticker and yf.Search to inject the proxied session
# ---------------------------------------------------------------------------
_OriginalTicker = yf.Ticker
_OriginalSearch = yf.Search


class _ProxiedTicker(_OriginalTicker):
    """Thin wrapper that injects the proxy session automatically."""

    def __init__(self, ticker, session=None, **kwargs):
        if session is None:
            session = _build_proxied_session()
        super().__init__(ticker, session=session, **kwargs)


class _ProxiedSearch(_OriginalSearch):
    """Thin wrapper that injects the proxy session automatically."""

    def __init__(self, query, *args, session=None, **kwargs):
        if session is None:
            session = _build_proxied_session()
        super().__init__(query, *args, session=session, **kwargs)


# Apply patches
yf.Ticker = _ProxiedTicker
yf.Search = _ProxiedSearch
