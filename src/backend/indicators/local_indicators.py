"""
Local Indicator Service
Calculates technical indicators (RSI, EMA, MACD) locally using raw price history.
Replaces external APIs (TAAPI) for zero-latency, unlimited usage.
"""

import math
import logging
from typing import List, Dict, Optional

class LocalIndicatorService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def fetch_and_calculate_all(self, exchange, asset: str) -> Dict[str, Dict]:
        """
        Fetch historical data for multiple timeframes and calculate all indicators.
        Returns structure compatible with BotEngine expectations.
        """
        results = {
            "5m": {},
            "1h": {},
            "4h": {}
        }
        
        try:
            # 1. Fetch data for all timeframes
            # Note: 100 candles is enough for EMA50, RSI14, MACD(26)
            tasks = [
                ("5m", "5m"),
                ("1h", "1h"),
                ("4h", "4h")
            ]
            
            for tf_key, interval in tasks:
                if not hasattr(exchange, 'get_historical_candles'):
                    self.logger.warning("Exchange does not support history fetching")
                    continue
                    
                candles = await exchange.get_historical_candles(asset, interval=interval, limit=100)
                if not candles:
                    continue
                    
                # Extract closing prices (chronological: old -> new)
                closes = [float(c['c']) for c in candles]
                
                # Calculate Indicators
                
                # EMA 20
                ema20 = self.ema(closes, 20)
                
                # EMA 50
                ema50 = self.ema(closes, 50)
                
                # RSI 7 (for 5m)
                rsi7 = self.rsi(closes, 7)
                
                # RSI 14
                rsi14 = self.rsi(closes, 14)
                
                # MACD (12, 26, 9)
                macd_res = self.macd(closes)
                
                # ATR (Needs High/Low/Close)
                atr14 = self.atr(candles, 14)
                atr3 = self.atr(candles, 3)
                
                # Populate result dict matching API structure
                data = {}
                data["ema20"] = ema20
                data["ema50"] = ema50
                data["rsi7"] = rsi7
                data["rsi14"] = rsi14
                data["macd"] = macd_res
                data["atr14"] = atr14
                data["atr3"] = atr3
                
                results[tf_key] = data

                # Calculate 24h stats from 1h candles
                if tf_key == "1h":
                    try:
                        # Extract Volume (v) and calculate 24h
                        # Note: candles is list of dicts from exchange
                        current_c = closes[-1]
                        # 24h ago is index -24 (if we have enough)
                        idx_24h = -24 if len(candles) >= 24 else 0
                        prev_c = float(candles[idx_24h]['o']) # Use OPEN of 24h ago? Or Close? Usually Close vs Close. 24h change = (Price - Price24hAgo)/Price24hAgo.
                        # Using Open of bar 24h ago covers the full 24h period?
                        # Bar -1 is current hour. Bar -24 is 23 hours ago. 
                        # Close of -25 is 24h ago?
                        # Let's simple use: Close[-1] vs Open[-24].
                        prev_c = float(candles[idx_24h]['o'])
                        
                        change_24h = ((current_c - prev_c) / prev_c) * 100
                        volume_24h = sum(float(c.get('v', 0)) for c in candles[idx_24h:])
                        
                        results["stats"] = {
                            "change_24h": change_24h,
                            "volume_24h": volume_24h
                        }
                    except Exception as e:
                        self.logger.error(f"Error calculating 24h stats: {e}")
                
        except Exception as e:
            self.logger.error(f"Error calculating local indicators for {asset}: {e}")
            
        return results

    # --- Calculation Engines ---

    def ema(self, prices: List[float], period: int) -> List[float]:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return []
            
        # Initial SMA
        sma = sum(prices[:period]) / period
        ema_values = [sma]
        multiplier = 2 / (period + 1)
        
        # Calculate rest
        for price in prices[period:]:
            new_ema = (price - ema_values[-1]) * multiplier + ema_values[-1]
            ema_values.append(new_ema)
            
        return ema_values # Note: Shorter than input by (period-1)

    def rsi(self, prices: List[float], period: int = 14) -> List[float]:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return []
            
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
            
        if len(gains) < period:
            return []
            
        # First Avg
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period
        
        rsis = []
        
        # Helper
        def calc_rsi(g, l):
            if l == 0: return 100.0
            rs = g / l
            return 100.0 - (100.0 / (1.0 + rs))
            
        rsis.append(calc_rsi(avg_gain, avg_loss))
        
        # Smoothed
        for i in range(period, len(gains)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            rsis.append(calc_rsi(avg_gain, avg_loss))
            
        return rsis

    def macd(self, prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> List[Dict[str, float]]:
        """Calculate MACD, Signal, Hist"""
        if len(prices) < slow + signal:
            return []
            
        ema_fast = self.ema(prices, fast)
        ema_slow = self.ema(prices, slow)
        
        # Match lengths to end
        ema_fast_subset = ema_fast[-len(ema_slow):]
        
        macd_line = [f - s for f, s in zip(ema_fast_subset, ema_slow)]
        
        # Signal Line
        signal_line = self.ema(macd_line, signal)
        
        # MACD Hist
        macd_line_subset = macd_line[-len(signal_line):]
        
        results = []
        for i in range(len(signal_line)):
            m = macd_line_subset[i]
            s = signal_line[i]
            h = m - s
            results.append({
                "valueMACD": m,
                "valueMACDSignal": s,
                "valueMACDHist": h
            })
            
        return results

    def atr(self, candles: List[Dict], period: int = 14) -> List[float]:
        """Calculate Average True Range (Wilder's Smoothing)"""
        if len(candles) < period + 1:
            return []
            
        highs = [float(c['h']) for c in candles]
        lows = [float(c['l']) for c in candles]
        closes = [float(c['c']) for c in candles]
        
        tr = []
        # First TR is H-L
        tr.append(highs[0] - lows[0])
        
        for i in range(1, len(candles)):
            h = highs[i]
            l = lows[i]
            prev_c = closes[i-1]
            val = max(h - l, abs(h - prev_c), abs(l - prev_c))
            tr.append(val)
            
        if len(tr) < period:
             return []
             
        # First ATR = SMA(TR, period)
        atr = [sum(tr[:period]) / period]
        
        # Wilder's Smoothing
        for i in range(period, len(tr)):
             current_tr = tr[i]
             prev_atr = atr[-1]
             # RMA formula
             new_atr = (prev_atr * (period - 1) + current_tr) / period
             atr.append(new_atr)
             
        return atr
