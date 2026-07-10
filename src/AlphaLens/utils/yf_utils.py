"""
Utility helpers for yfinance requests.

Provides:
- yf_search_with_retry: wraps yf.Search with exponential back-off,
  jitter, and an in-process LRU cache to survive Yahoo Finance
  429 / rate-limit responses without blind fixed sleeps.
- yf_delay: kept for backward compatibility with other callers.
"""

import time
import random
import logging
import functools
import requests
import yfinance as yf

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rotating User-Agent pool — reduces fingerprinting risk
# ---------------------------------------------------------------------------
_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
]


def _make_session() -> requests.Session:
    """Return a requests.Session with a randomly chosen User-Agent."""
    session = requests.Session()
    session.headers.update({"User-Agent": random.choice(_USER_AGENTS)})
    return session


# ---------------------------------------------------------------------------
# LRU cache — same company name → no network call
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=256)
def _cached_search(company_name: str, max_results: int) -> tuple:
    """
    Internal cached wrapper around yf.Search.
    Returns a tuple of quote dicts (hashable, so lru_cache works).
    Raises on failure so the retry layer can catch it.
    """
    session = _make_session()
    search = yf.Search(company_name, max_results=max_results, session=session)
    return tuple(search.quotes)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def yf_search_with_retry(
    company_name: str,
    max_results: int = 5,
    max_attempts: int = 4,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
) -> list[dict]:
    """
    Search Yahoo Finance for *company_name* with exponential back-off retry.

    Strategy
    --------
    - Attempt 1: immediate (no delay).
    - On 429 / connection error: wait ``base_delay * 2^attempt + jitter``
      seconds (capped at *max_delay*), then retry.
    - Results are cached per (company_name, max_results) pair for the
      lifetime of the process so repeated identical queries are free.

    Returns
    -------
    list[dict]  — the ``quotes`` list from yf.Search (may be empty).

    Raises
    ------
    RuntimeError  — if all *max_attempts* are exhausted.
    """
    last_exc: Exception | None = None

    for attempt in range(max_attempts):
        try:
            # lru_cache returns the same tuple on cache hit — no network call
            quotes = list(_cached_search(company_name, max_results))
            if attempt > 0:
                logger.info("yf_search succeeded on attempt %d", attempt + 1)
            return quotes

        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            is_rate_limit = (
                "429" in str(exc)
                or "Too Many Requests" in str(exc)
                or "rate limit" in str(exc).lower()
            )
            # Invalidate the cache entry so the next attempt actually retries
            _cached_search.cache_clear()

            if attempt + 1 >= max_attempts:
                break

            # Exponential back-off with full jitter
            sleep_time = min(base_delay * (2 ** attempt), max_delay)
            sleep_time += random.uniform(0, sleep_time * 0.3)  # ±30 % jitter

            if is_rate_limit:
                logger.warning(
                    "Yahoo Finance rate-limited (429). "
                    "Retrying in %.1fs (attempt %d/%d)…",
                    sleep_time, attempt + 1, max_attempts,
                )
            else:
                logger.warning(
                    "yf.Search failed: %s. Retrying in %.1fs (attempt %d/%d)…",
                    exc, sleep_time, attempt + 1, max_attempts,
                )

            time.sleep(sleep_time)

    raise RuntimeError(
        f"yf.Search for '{company_name}' failed after {max_attempts} attempts. "
        f"Last error: {last_exc}"
    )


def yf_delay() -> None:
    """Backward-compatible: sleep 1–3 s. Prefer yf_search_with_retry for new code."""
    time.sleep(random.uniform(1, 3))
