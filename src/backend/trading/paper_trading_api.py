"""
Paper Trading API - Simulated Hyperliquid Exchange
Ingen ekte penger, ingen ekte exchange - perfekt for læring!
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
import requests
import json
import os
from dataclasses import dataclass, field


@dataclass
class Position:
    """Simulert trading position."""
    coin: str
    entry_px: float
    size: float  # Positive = long, negative = short
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def side(self) -> str:
        return "long" if self.size > 0 else "short"

    @property
    def notional(self) -> float:
        return abs(self.size) * self.entry_px


@dataclass
class Order:
    """Simulert order."""
    oid: str
    coin: str
    side: str  # "B" (buy) or "A" (sell/ask)
    sz: float
    limit_px: float
    order_type: dict
    reduce_only: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PaperTradingAPI:
    """
    Simulert Hyperliquid exchange API.

    Features:
    - Henter real-time prices fra Binance
    - Simuler market orders
    - Simuler TP/SL trigger orders
    - Beregn PnL
    - Track balance og positions
    - Ingen ekte penger involvert!
    """

    def __init__(self, starting_balance: float = 10000.0):
        """
        Initialize paper trading API.

        Args:
            starting_balance: Starting USDC balance (default: $10,000)
        """
        self.balance = starting_balance
        self.initial_balance = starting_balance
        self.positions: Dict[str, Position] = {}
        self.orders: List[Order] = []
        self.fills: List[dict] = []
        self.order_counter = 0

        # Price cache (to avoid too many API calls)
        self._price_cache: Dict[str, tuple[float, datetime]] = {}
        self._cache_ttl = 2  # seconds (Increased slightly to avoid API/Hold errors)

        # Mock wallet (for compatibility)
        self.wallet = type('Wallet', (), {'address': '0xPaperTradingWallet'})()
        self.base_url = "https://api.binance.com/api/v3"

        logging.info(f"Paper Trading API initialized with ${starting_balance:,.2f}")
        
        # Load state if exists
        self._load_state()

    def _save_state(self):
        """Save state to file"""
        try:
            os.makedirs("data", exist_ok=True)
            state = {
                "balance": self.balance,
                "positions": [
                    {
                        "coin": p.coin, "entry_px": p.entry_px, "size": p.size,
                        "timestamp": p.timestamp.isoformat()
                    } for p in self.positions.values()
                ],
                "fills": self.fills,
                "orders": [
                    {
                        "oid": o.oid, "coin": o.coin, "side": o.side, "sz": o.sz,
                        "limit_px": o.limit_px, "order_type": o.order_type,
                        "reduce_only": o.reduce_only,
                        "timestamp": o.timestamp.isoformat()
                    } for o in self.orders
                ]
            }
            with open("data/paper_trading_state.json", "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save paper state: {e}")

    def _load_state(self):
        """Load state from file"""
        try:
            if not os.path.exists("data/paper_trading_state.json"):
                return
            with open("data/paper_trading_state.json", "r") as f:
                state = json.load(f)
            
            self.balance = state.get("balance", self.initial_balance)
            self.fills = state.get("fills", [])
            
            # Restore positions
            for p_data in state.get("positions", []):
                self.positions[p_data["coin"]] = Position(
                    coin=p_data["coin"],
                    entry_px=p_data["entry_px"],
                    size=p_data["size"],
                    timestamp=datetime.fromisoformat(p_data["timestamp"])
                )
                
            # Restore orders
            for o_data in state.get("orders", []):
                self.orders.append(Order(
                    oid=o_data["oid"],
                    coin=o_data["coin"],
                    side=o_data["side"],
                    sz=o_data["sz"],
                    limit_px=o_data["limit_px"],
                    order_type=o_data["order_type"],
                    reduce_only=o_data["reduce_only"],
                    timestamp=datetime.fromisoformat(o_data["timestamp"])
                ))
            
            logging.info(f"Loaded paper state: {len(self.positions)} positions")
        except Exception as e:
            logging.error(f"Failed to load state: {e}")

    def _get_next_oid(self) -> str:
        """Generate unique order ID."""
        self.order_counter += 1
        return f"paper_{self.order_counter}_{int(datetime.now(timezone.utc).timestamp())}"

    async def get_current_price(self, asset: str) -> float:
        """
        Hent real-time pris fra Binance.

        Args:
            asset: Asset symbol (e.g., "BTC", "ETH")

        Returns:
            Current price in USDT
        """
        # Check cache
        now = datetime.now(timezone.utc)
        if asset in self._price_cache:
            price, timestamp = self._price_cache[asset]
            if (now - timestamp).total_seconds() < self._cache_ttl:
                return price

        try:
            # Binance symbol format: BTCUSDT, ETHUSDT
            symbol = f"{asset}USDT"

            response = await asyncio.to_thread(
                requests.get,
                f"{self.base_url}/ticker/price",
                params={"symbol": symbol},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            price = float(data['price'])

            # Update cache
            self._price_cache[asset] = (price, now)

            logging.debug(f"Fetched {asset} price: ${price:,.2f}")
            return price

        except Exception as e:
            logging.error(f"Failed to fetch price for {asset}: {e}")
            # Fallback to cached price if available
            if asset in self._price_cache:
                price, _ = self._price_cache[asset]
                logging.warning(f"Using cached price for {asset}: ${price:,.2f}")
                return price
            # Default fallback prices
            fallback_prices = {
                "BTC": 98000.0,
                "ETH": 3400.0,
                "SOL": 180.0,
                "AVAX": 35.0,
            }
            return fallback_prices.get(asset, 100.0)

    async def get_historical_candles(self, asset: str, interval: str = "5m", limit: int = 100) -> List[Dict]:
        """
        Fetch historical candles from Binance to populate charts.
        
        Args:
            asset: Asset symbol
            interval: Timeframe (5m, 1h, 4h)
            limit: Number of candles
            
        Returns:
            List of candles {'t': ms_timestamp, 'o': open, 'h': high, 'l': low, 'c': close}
        """
        try:
            symbol = f"{asset}USDT"
            response = await asyncio.to_thread(
                requests.get,
                f"{self.base_url}/klines",
                params={"symbol": symbol, "interval": interval, "limit": limit},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            candles = []
            for k in data:
                # Binance kline: [open_time, open, high, low, close, vol, ...]
                candles.append({
                    't': k[0], # ms timestamp
                    'o': float(k[1]),
                    'h': float(k[2]),
                    'l': float(k[3]),
                    'c': float(k[4]),
                    'v': float(k[5])
                })
            return candles
            
        except Exception as e:
            logging.error(f"Failed to fetch historical candles for {asset}: {e}")
            return []

    def round_size(self, asset: str, amount: float) -> float:
        """
        Round order size to asset precision.

        Args:
            asset: Asset symbol
            amount: Desired size

        Returns:
            Rounded size
        """
        # BTC: 4 decimals, ETH: 3 decimals, others: 2 decimals
        decimals = {
            "BTC": 4,
            "ETH": 3,
            "SOL": 2,
        }.get(asset, 2)

        return round(amount, decimals)

    async def place_buy_order(self, asset: str, amount: float, slippage: float = 0.01) -> dict:
        """
        Simuler market buy order (open LONG position).

        Args:
            asset: Asset to buy
            amount: Contract size
            slippage: Simulated slippage (default 1%)

        Returns:
            Order result
        """
        amount = self.round_size(asset, amount)
        current_price = await self.get_current_price(asset)

        # Simulate slippage (worse fill for market buy)
        fill_price = current_price * (1 + slippage)

        cost = fill_price * amount

        if cost > self.balance:
            logging.error(f"Insufficient balance: ${self.balance:,.2f} < ${cost:,.2f}")
            return {
                "status": "error",
                "response": {
                    "type": "error",
                    "data": {"message": "Insufficient balance"}
                }
            }

        # Execute trade
        self.balance -= cost

        # Update or create position
        if asset in self.positions:
            # Add to existing position
            existing = self.positions[asset]
            total_size = existing.size + amount
            
            if abs(total_size) < 0.0001:
                # Position closed
                del self.positions[asset]
            else:
                # Only update Avg Entry if increasing exposure (same side)
                # If reducing (e.g. Closing Short), Entry Price represents original entry.
                if (existing.size > 0 and amount > 0) or (existing.size < 0 and amount < 0):
                     existing.entry_px = (existing.entry_px * existing.size + fill_price * amount) / total_size
                
                existing.size = total_size
        else:
            self.positions[asset] = Position(
                coin=asset,
                entry_px=fill_price,
                size=amount
            )

        # Record fill
        oid = self._get_next_oid()
        self.fills.append({
            "oid": oid,
            "coin": asset,
            "side": "B",
            "px": fill_price,
            "sz": amount,
            "time": datetime.now(timezone.utc).isoformat(),
            "fee": cost * 0.0002,  # 0.02% taker fee
        })

        logging.info(f"PAPER TRADE: BUY {amount} {asset} @ ${fill_price:,.2f} (cost: ${cost:,.2f})")

        result = {
            "status": "ok",
            "response": {
                "type": "order",
                "data": {
                    "statuses": [{
                        "filled": {
                            "oid": oid,
                            "totalSz": str(amount),
                            "avgPx": str(fill_price)
                        }
                    }]
                }
            }
        }
        
        self._save_state()
        return result

    async def place_sell_order(self, asset: str, amount: float, slippage: float = 0.01) -> dict:
        """
        Simuler market sell order (open SHORT position).

        Args:
            asset: Asset to sell
            amount: Contract size
            slippage: Simulated slippage

        Returns:
            Order result
        """
        amount = self.round_size(asset, amount)
        current_price = await self.get_current_price(asset)

        # Simulate slippage (worse fill for market sell)
        fill_price = current_price * (1 - slippage)

        # For short: we receive USDC
        received = fill_price * amount
        self.balance += received

        # Update or create position (negative size = short)
        if asset in self.positions:
            existing = self.positions[asset]
            total_size = existing.size - amount

            if abs(total_size) < 0.0001:
                # Position closed
                del self.positions[asset]
            else:
                # Update position
                avg_entry = (existing.entry_px * existing.size - fill_price * amount) / total_size
                existing.size = total_size
                existing.entry_px = avg_entry
        else:
            self.positions[asset] = Position(
                coin=asset,
                entry_px=fill_price,
                size=-amount  # Negative = short
            )

        # Record fill
        oid = self._get_next_oid()
        self.fills.append({
            "oid": oid,
            "coin": asset,
            "side": "A",
            "px": fill_price,
            "sz": amount,
            "time": datetime.now(timezone.utc).isoformat(),
            "fee": received * 0.0002,
        })

        logging.info(f"PAPER TRADE: SELL {amount} {asset} @ ${fill_price:,.2f} (received: ${received:,.2f})")

        result = {
            "status": "ok",
            "response": {
                "type": "order",
                "data": {
                    "statuses": [{
                        "filled": {
                            "oid": oid,
                            "totalSz": str(amount),
                            "avgPx": str(fill_price)
                        }
                    }]
                }
            }
        }
        
        self._save_state()
        return result

    async def place_take_profit(self, asset: str, is_buy: bool, amount: float, tp_price: float) -> dict:
        """
        Simuler take-profit trigger order.

        Args:
            asset: Asset
            is_buy: True if original position is long
            amount: Size to close
            tp_price: Trigger price

        Returns:
            Order result
        """
        amount = self.round_size(asset, amount)
        oid = self._get_next_oid()

        order = Order(
            oid=oid,
            coin=asset,
            side="A" if is_buy else "B",  # Opposite of position
            sz=amount,
            limit_px=tp_price,
            order_type={"trigger": {"triggerPx": tp_price, "isMarket": True, "tpsl": "tp"}},
            reduce_only=True
        )

        self.orders.append(order)

        logging.info(f"PAPER ORDER: TP for {amount} {asset} @ ${tp_price:,.2f}")

        result = {
            "status": "ok",
            "response": {
                "type": "order",
                "data": {
                    "statuses": [{
                        "resting": {
                            "oid": oid
                        }
                    }]
                }
            }
        }
        
        self._save_state()
        return result

    async def place_stop_loss(self, asset: str, is_buy: bool, amount: float, sl_price: float) -> dict:
        """
        Simuler stop-loss trigger order.

        Args:
            asset: Asset
            is_buy: True if original position is long
            amount: Size to close
            sl_price: Trigger price

        Returns:
            Order result
        """
        amount = self.round_size(asset, amount)
        oid = self._get_next_oid()

        order = Order(
            oid=oid,
            coin=asset,
            side="A" if is_buy else "B",  # Opposite of position
            sz=amount,
            limit_px=sl_price,
            order_type={"trigger": {"triggerPx": sl_price, "isMarket": True, "tpsl": "sl"}},
            reduce_only=True
        )

        self.orders.append(order)

        logging.info(f"PAPER ORDER: SL for {amount} {asset} @ ${sl_price:,.2f}")

        result = {
            "status": "ok",
            "response": {
                "type": "order",
                "data": {
                    "statuses": [{
                        "resting": {
                            "oid": oid
                        }
                    }]
                }
            }
        }
        
        self._save_state()
        return result

    async def cancel_order(self, asset: str, oid: str) -> dict:
        """Cancel specific order."""
        self.orders = [o for o in self.orders if o.oid != oid]
        logging.info(f"PAPER ORDER: Cancelled {oid}")
        self._save_state()
        return {"status": "ok"}

    async def cancel_all_orders(self, asset: str) -> dict:
        """Cancel all orders for asset."""
        count = len([o for o in self.orders if o.coin == asset])
        self.orders = [o for o in self.orders if o.coin != asset]
        logging.info(f"PAPER ORDER: Cancelled {count} orders for {asset}")
        return {"status": "ok", "cancelled_count": count}

    async def get_open_orders(self) -> List[dict]:
        """
        Get open orders.

        Returns:
            List of open orders
        """
        return [{
            "coin": o.coin,
            "side": o.side,
            "sz": o.sz,
            "limitPx": o.limit_px,
            "oid": o.oid,
            "orderType": o.order_type,
            "reduceOnly": o.reduce_only,
            "timestamp": o.timestamp.isoformat(),
        } for o in self.orders]

    async def get_recent_fills(self, limit: int = 50) -> List[dict]:
        """Get recent fills."""
        return self.fills[-limit:]

    def extract_oids(self, order_result: dict) -> List[str]:
        """Extract order IDs from order result."""
        oids = []
        try:
            statuses = order_result["response"]["data"]["statuses"]
            for st in statuses:
                if "resting" in st and "oid" in st["resting"]:
                    oids.append(st["resting"]["oid"])
                if "filled" in st and "oid" in st["filled"]:
                    oids.append(st["filled"]["oid"])
        except (KeyError, TypeError):
            pass
        return oids

    async def get_user_state(self) -> dict:
        """
        Get account state with positions and PnL.

        Returns:
            Account state dict
        """
        enriched_positions = []
        total_unrealized_pnl = 0.0

        for asset, pos in self.positions.items():
            current_price = await self.get_current_price(asset)

            # Calculate PnL
            if pos.side == "long":
                unrealized_pnl = (current_price - pos.entry_px) * pos.size
            else:
                unrealized_pnl = (pos.entry_px - current_price) * abs(pos.size)

            total_unrealized_pnl += unrealized_pnl

            enriched_positions.append({
                "symbol": asset,
                "quantity": pos.size,
                "entry_price": pos.entry_px,
                "current_price": current_price,
                "unrealized_pnl": unrealized_pnl,
                "pnl_pct": (unrealized_pnl / pos.notional * 100) if pos.notional > 0 else 0.0,
                "leverage": 1,
                "liquidation_price": 0,
                "side": "LONG" if pos.size > 0 else "SHORT",
                # Keep raw keys for compatibility if needed elsewhere
                "coin": asset,
                "szi": str(pos.size),
                "entryPx": str(pos.entry_px),
                "positionValue": str(abs(pos.size) * current_price),
                "unrealizedPnl": str(unrealized_pnl),
                "returnOnEquity": str((unrealized_pnl / pos.notional) * 100) if pos.notional > 0 else "0",
                "pnl": unrealized_pnl,
                "notional_entry": pos.notional,
            })

        # Calculate Total Equity
        # For Paper Trading (Spot-like model):
        # Long:  Equity = Cash Balance + (Size * Current Price)
        # Short: Equity = Cash Balance - (|Size| * Current Price) (Since cash increased on sell)
        # Unified: Equity = Cash Balance + (Size * Current Price)
        
        position_equity = 0.0
        for p in enriched_positions:
            # pos.size is signed (+ for Long, - for Short)
            # enriched_positions stores quantity as signed size
            position_equity += (p["quantity"] * p["current_price"])

        total_value = self.balance + position_equity

        return {
            "balance": self.balance,
            "total_value": total_value,
            "withdrawable": self.balance,
            "accountValue": str(total_value),
            "assetPositions": [{"position": pos} for pos in enriched_positions],
            "positions": enriched_positions,
        }

    async def get_meta_and_ctxs(self) -> List[dict]:
        """
        Mock metadata (for compatibility).

        Returns:
            [meta, asset_ctxs]
        """
        meta = {
            "universe": [
                {"name": "BTC", "szDecimals": 4},
                {"name": "ETH", "szDecimals": 3},
                {"name": "SOL", "szDecimals": 2},
                {"name": "AVAX", "szDecimals": 2},
                {"name": "SUI", "szDecimals": 1},
                {"name": "AAVE", "szDecimals": 2},
                {"name": "DOGE", "szDecimals": 0},
                {"name": "ARB", "szDecimals": 1},
                {"name": "OP", "szDecimals": 1},
                {"name": "MATIC", "szDecimals": 1},
                {"name": "LINK", "szDecimals": 2},
                {"name": "ADA", "szDecimals": 1},
                {"name": "DOT", "szDecimals": 2},
            ]
        }

        asset_ctxs = [
            {"funding": "0.0001", "openInterest": "12500000"},  # BTC
            {"funding": "0.0005", "openInterest": "8700000"},   # ETH
            {"funding": "-0.0002", "openInterest": "4500000"},  # SOL
            {"funding": "0.0001", "openInterest": "200000"},   # AVAX
            {"funding": "0.0003", "openInterest": "500000"},   # SUI
            {"funding": "0.0002", "openInterest": "150000"},   # AAVE
            {"funding": "0.0001", "openInterest": "10000000"}, # DOGE
            {"funding": "0.0001", "openInterest": "800000"},   # ARB
            {"funding": "0.0002", "openInterest": "600000"},   # OP
            {"funding": "0.0001", "openInterest": "1200000"},  # MATIC
            {"funding": "0.0001", "openInterest": "300000"},   # LINK
            {"funding": "0.0001", "openInterest": "2500000"},  # ADA
            {"funding": "0.0004", "openInterest": "400000"},   # DOT
        ]

        return [meta, asset_ctxs]

    async def get_funding_rate(self, asset: str) -> Optional[float]:
        """Mock funding rate."""
        # Returns small positive funding by default for unknown assets
        rates = {
            "BTC": 0.0001,
            "ETH": 0.0005,
            "SOL": -0.0002,
        }
        return rates.get(asset, 0.0001)

    async def get_open_interest(self, asset: str) -> Optional[float]:
        """Mock open interest."""
        oi = {
            "BTC": 12500000,
            "ETH": 8700000,
            "SOL": 4500000,
        }
        # Return a generic OI if not found, to imply liquidity
        return oi.get(asset, 500000.0)

    async def check_trigger_orders(self):
        """
        Check if any trigger orders should execute.
        Called periodically by bot engine.
        """
        executed_orders = []

        for order in self.orders[:]:  # Copy to avoid modification during iteration
            current_price = await self.get_current_price(order.coin)
            trigger_px = order.order_type.get("trigger", {}).get("triggerPx")

            if not trigger_px:
                continue

            tpsl = order.order_type.get("trigger", {}).get("tpsl")
            should_trigger = False

            if tpsl == "tp":
                # Take profit: trigger when price reaches target
                if order.side == "A":  # Closing long
                    should_trigger = current_price >= trigger_px
                else:  # Closing short
                    should_trigger = current_price <= trigger_px

            elif tpsl == "sl":
                # Stop loss: trigger when price goes against position
                if order.side == "A":  # Closing long
                    should_trigger = current_price <= trigger_px
                else:  # Closing short
                    should_trigger = current_price >= trigger_px

            if should_trigger:
                logging.info(f"PAPER TRIGGER: {tpsl.upper()} triggered for {order.coin} @ ${current_price:,.2f}")

                # Execute market close
                if order.side == "A":
                    await self.place_sell_order(order.coin, order.sz, slippage=0.005)
                else:
                    await self.place_buy_order(order.coin, order.sz, slippage=0.005)

                executed_orders.append(order.oid)
                self.orders.remove(order)

        return executed_orders

    def get_statistics(self) -> dict:
        """
        Get trading statistics.

        Returns:
            Performance metrics
        """
        total_value = self.balance + sum(
            pos.entry_px * abs(pos.size) for pos in self.positions.values()
        )

        return {
            "starting_balance": self.initial_balance,
            "current_balance": self.balance,
            "total_value": total_value,
            "total_return": total_value - self.initial_balance,
            "total_return_pct": ((total_value / self.initial_balance) - 1) * 100,
            "total_trades": len(self.fills),
            "active_positions": len(self.positions),
            "pending_orders": len(self.orders),
        }
