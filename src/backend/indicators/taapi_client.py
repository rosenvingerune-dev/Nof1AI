"""Client helper for interacting with the TAAPI technical analysis API (Async)."""

import aiohttp
import asyncio
import logging
import time
from src.backend.config_loader import CONFIG
from src.backend.indicators.taapi_cache import get_cache


class TAAPIClient:
    """Fetches TA indicators with retry/backoff semantics for resilience (Async)."""

    def __init__(self, enable_cache: bool = True, cache_ttl: int = 60):
        """
        Initialize TAAPI credentials and base URL.
        
        Args:
            enable_cache: Enable caching to reduce API calls
            cache_ttl: Cache time-to-live in seconds (default: 60s)
        """
        self.api_key = CONFIG["taapi_api_key"]
        self.base_url = "https://api.taapi.io/"
        self.bulk_url = "https://api.taapi.io/bulk"
        self.enable_cache = enable_cache
        self.cache = get_cache(ttl=cache_ttl) if enable_cache else None

    async def _get_with_retry(self, url, params, retries=3, backoff=0.5):
        """Perform a GET request with exponential backoff retry logic."""
        async with aiohttp.ClientSession() as session:
            for attempt in range(retries):
                try:
                    async with session.get(url, params=params, timeout=10) as resp:
                        if resp.status == 200:
                            return await resp.json()
                        
                        # Retry on rate limit (429) or server errors (500+)
                        if (resp.status == 429 or resp.status >= 500) and attempt < retries - 1:
                            wait = backoff * (2 ** attempt)
                            if resp.status == 429:
                                logging.warning(f"TAAPI rate limit (429) hit, retrying in {wait}s (attempt {attempt + 1}/{retries})")
                            else:
                                logging.warning(f"TAAPI {resp.status}, retrying in {wait}s")
                            await asyncio.sleep(wait)
                        else:
                            resp.raise_for_status()
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    if attempt < retries - 1:
                        wait = backoff * (2 ** attempt)
                        logging.warning(f"TAAPI connection error: {e}, retrying in {wait}s")
                        await asyncio.sleep(wait)
                    else:
                        raise
            raise RuntimeError("Max retries exceeded")

    async def _post_with_retry(self, url, payload, retries=3, backoff=0.5):
        """Perform a POST request with exponential backoff retry logic."""
        async with aiohttp.ClientSession() as session:
            for attempt in range(retries):
                try:
                    async with session.post(url, json=payload, timeout=15) as resp:
                        if resp.status == 200:
                            return await resp.json()
                        
                        # Retry on rate limit (429) or server errors (500+)
                        if (resp.status == 429 or resp.status >= 500) and attempt < retries - 1:
                            wait = backoff * (2 ** attempt)
                            if resp.status == 429:
                                logging.warning(f"TAAPI Bulk rate limit (429), retrying in {wait}s (attempt {attempt + 1}/{retries})")
                            else:
                                logging.warning(f"TAAPI Bulk {resp.status}, retrying in {wait}s")
                            await asyncio.sleep(wait)
                        else:
                            resp.raise_for_status()
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    if attempt < retries - 1:
                        wait = backoff * (2 ** attempt)
                        logging.warning(f"TAAPI connection error: {e}, retrying in {wait}s")
                        await asyncio.sleep(wait)
                    else:
                        raise
            raise RuntimeError("Max retries exceeded")

    async def fetch_bulk_indicators(self, symbol, interval, indicators_config):
        """
        Fetch multiple indicators in one bulk request to TAAPI.
        """
        try:
            # Build bulk request payload
            indicators = []
            for config in indicators_config:
                indicator_def = {
                    "id": config.get("id", config["indicator"]),
                    "indicator": config["indicator"]
                }

                # Add optional parameters
                if "period" in config:
                    indicator_def["period"] = config["period"]
                if "results" in config:
                    indicator_def["results"] = config["results"]
                if "backtrack" in config:
                    indicator_def["backtrack"] = config["backtrack"]

                indicators.append(indicator_def)

            payload = {
                "secret": self.api_key,
                "construct": {
                    "exchange": "binance",
                    "symbol": symbol,
                    "interval": interval,
                    "indicators": indicators
                }
            }

            # Make bulk POST request
            response = await self._post_with_retry(self.bulk_url, payload)

            # Parse results by ID
            results = {}
            if isinstance(response, dict) and "data" in response:
                for item in response["data"]:
                    indicator_id = item.get("id")
                    if indicator_id:
                        results[indicator_id] = item.get("result")

            return results

        except Exception as e:
            logging.error(f"TAAPI bulk fetch exception for {symbol} {interval}: {e}")
            return {}

    async def fetch_asset_indicators(self, asset):
        """
        Fetch all required indicators for an asset using bulk requests (Async).
        Makes 2 requests total (5m + 4h) instead of 10 individual requests.
        """
        # Check cache first (for current interval from config)
        interval = CONFIG.get("interval", "1h")
        
        # Try to get cached data for both intervals
        if self.enable_cache and self.cache:
            cached_5m = self.cache.get(asset, "5m")
            cached_interval = self.cache.get(asset, interval)
            
            if cached_5m and cached_interval:
                logging.info(f"Using cached indicators for {asset} (5m + {interval})")
                return {"5m": cached_5m, interval: cached_interval}
        
        symbol = f"{asset}/USDT"
        result = {"5m": {}, interval: {}}

        # Bulk request for 5m indicators
        indicators_5m = [
            {"id": "ema20", "indicator": "ema", "period": 20, "results": 20},
            {"id": "macd", "indicator": "macd", "results": 20},
            {"id": "rsi7", "indicator": "rsi", "period": 7, "results": 20},
            {"id": "rsi14", "indicator": "rsi", "period": 14, "results": 20}
        ]

        bulk_5m = await self.fetch_bulk_indicators(symbol, "5m", indicators_5m)

        # Extract series data from bulk response
        result["5m"]["ema20"] = self._extract_series(bulk_5m.get("ema20"), "value")
        result["5m"]["macd"] = self._extract_series(bulk_5m.get("macd"), "valueMACD")
        result["5m"]["rsi7"] = self._extract_series(bulk_5m.get("rsi7"), "value")
        result["5m"]["rsi14"] = self._extract_series(bulk_5m.get("rsi14"), "value")

        # Wait 15 seconds to respect Free plan rate limit (1 request per 15 seconds)
        logging.info(f"Waiting 15s for TAAPI rate limit (Free plan: 1 req/15s)...")
        await asyncio.sleep(15)

        # Bulk request for 4h indicators
        indicators_4h = [
            {"id": "ema20", "indicator": "ema", "period": 20},
            {"id": "ema50", "indicator": "ema", "period": 50},
            {"id": "atr3", "indicator": "atr", "period": 3},
            {"id": "atr14", "indicator": "atr", "period": 14},
            {"id": "macd", "indicator": "macd", "results": 5},
            {"id": "rsi14", "indicator": "rsi", "period": 14, "results": 5}
        ]

        bulk_4h = await self.fetch_bulk_indicators(symbol, "4h", indicators_4h)

        # Extract values and series
        result[interval]["ema20"] = self._extract_value(bulk_4h.get("ema20"))
        result[interval]["ema50"] = self._extract_value(bulk_4h.get("ema50"))
        result[interval]["atr3"] = self._extract_value(bulk_4h.get("atr3"))
        result[interval]["atr14"] = self._extract_value(bulk_4h.get("atr14"))
        result[interval]["macd"] = self._extract_series(bulk_4h.get("macd"), "valueMACD")
        result[interval]["rsi14"] = self._extract_series(bulk_4h.get("rsi14"), "value")

        # Cache the results
        if self.enable_cache and self.cache:
            self.cache.set(asset, "5m", result["5m"])
            self.cache.set(asset, interval, result[interval])
            logging.info(f"Cached indicators for {asset} (5m + {interval})")

        return result

    def _extract_series(self, data, value_key="value"):
        """Extract and normalize series data from TAAPI response."""
        if not data:
            return []
        
        # Handle list of results (historical)
        if isinstance(data, list):
            series = []
            # TAAPI returns oldest first or newest first? Usually newest first by default unless 'backtrack' is used?
            # actually usually it returns dicts. 
            # We want a list of values.
            # Let's preserve order from API.
            for item in data:
                if isinstance(item, dict) and value_key in item:
                    val = item[value_key]
                    series.append(round(val, 4) if isinstance(val, (int, float)) else val)
            # If API returns newest first, charts usually want oldest first (left to right).
            # TAAPI documentation says results are returned from newest to oldest.
            # So we should REVERSE the list for plotting.
            return series[::-1] 

        # Handle single result (latest) wrapped in dict, or weird structure
        if isinstance(data, dict):
            if value_key in data:
                val = data[value_key]
                if isinstance(val, list): # If value itself is list?
                     return [round(v, 4) if isinstance(v, (int, float)) else v for v in val]
                else:
                     val = round(val, 4) if isinstance(val, (int, float)) else val
                     return [val]
                     
        return []

    def _extract_value(self, data, value_key="value"):
        """Extract and normalize single value from TAAPI response."""
        if not data:
            return None
        if isinstance(data, dict) and value_key in data:
            val = data[value_key]
            return round(val, 4) if isinstance(val, (int, float)) else val
        return None

    # Helper methods for basic fetch (kept for backward compatibility but made async)
    async def get_indicators(self, asset, interval):
        params = {
            "secret": self.api_key,
            "exchange": "binance",
            "symbol": f"{asset}/USDT",
            "interval": interval
        }
        # Parallel fetch would be better but keeping simple for now
        rsi = await self._get_with_retry(f"{self.base_url}rsi", params)
        macd = await self._get_with_retry(f"{self.base_url}macd", params)
        sma = await self._get_with_retry(f"{self.base_url}sma", params)
        ema = await self._get_with_retry(f"{self.base_url}ema", params)
        bbands = await self._get_with_retry(f"{self.base_url}bbands", params)
        return {
            "rsi": rsi.get("value"),
            "macd": macd,
            "sma": sma.get("value"),
            "ema": ema.get("value"),
            "bbands": bbands
        }
    
    async def get_historical_indicator(self, indicator, symbol, interval, results=10, params=None):
        """Fetch historical indicator data with optional overrides."""
        base_params = {
            "secret": self.api_key,
            "exchange": "binance",
            "symbol": symbol,
            "interval": interval,
            "results": results
        }
        if params:
            base_params.update(params)
        response = await self._get_with_retry(f"{self.base_url}{indicator}", base_params)
        return response

    async def fetch_value(self, indicator: str, symbol: str, interval: str, params: dict | None = None, key: str = "value"):
        """Fetch a single indicator value for the latest candle."""
        try:
            base_params = {
                "secret": self.api_key,
                "exchange": "binance",
                "symbol": symbol,
                "interval": interval
            }
            if params:
                base_params.update(params)
            data = await self._get_with_retry(f"{self.base_url}{indicator}", base_params)
            if isinstance(data, dict):
                val = data.get(key)
                return round(val, 4) if isinstance(val, (int, float)) else val
            return None
        except Exception:
            return None
