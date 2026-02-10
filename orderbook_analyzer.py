# orderbook_analyzer.py
import asyncio
import random
import time
from collections import deque

class OrderBookAnalyzer:
    def __init__(self):
        # Store recent orderbook snapshots
        self.orderbook_history = deque(maxlen=300)

        # Liquidity & safety thresholds
        self.max_spread = 0.08          # too wide = bad market
        self.min_liquidity_score = 0.4  # below = skip trade

    # ---------- FETCH ORDERBOOK ----------

    async def fetch_orderbook(self, market="POLY"):
        """
        Simulated orderbook snapshot.
        Structure matches real exchanges / Polymarket adapters.
        """
        bids = random.uniform(0.4, 0.6)
        asks = random.uniform(0.4, 0.6)
        spread = abs(bids - asks)

        liquidity_score = min(bids, asks) / max(bids, asks)

        snapshot = {
            "bids": round(bids, 4),
            "asks": round(asks, 4),
            "spread": round(spread, 4),
            "liquidity": round(liquidity_score, 4),
            "time": time.time()
        }

        self.orderbook_history.append(snapshot)
        return snapshot

    # ---------- LIQUIDITY CHECK ----------

    def is_liquid(self, snapshot):
        if snapshot["spread"] > self.max_spread:
            return False
        if snapshot["liquidity"] < self.min_liquidity_score:
            return False
        return True

    # ---------- SIGNAL CONFIRMATION ----------

    def confirm_signal(self, signal, snapshot):
        """
        Confirms or cancels ML signal based on orderbook.
        """
        if signal == "HOLD":
            return "HOLD"

        if not self.is_liquid(snapshot):
            return "HOLD"

        bid_ask_ratio = snapshot["bids"] / max(snapshot["asks"], 0.0001)

        if signal == "UP" and bid_ask_ratio < 1:
            return "HOLD"

        if signal == "DOWN" and bid_ask_ratio > 1:
            return "HOLD"

        return signal

    # ---------- FAST MONITOR LOOP ----------

    async def monitor(self, interval=0.3):
        """
        Optional continuous monitoring loop.
        """
        while True:
            await self.fetch_orderbook()
            await asyncio.sleep(interval)
