# orderbook_analyzer.py
import asyncio
import random
from collections import deque
from time import time


class OrderBookAnalyzer:
    def __init__(self):
        # Store recent orderbook snapshots (max 500)
        self.orderbook_history = deque(maxlen=500)

        # Liquidity & safety thresholds
        self.max_spread = 0.05          # Max acceptable spread
        self.min_bid_ask_ratio = 0.95   # Used for confirmation
        self.max_bid_ask_ratio = 1.05

    async def fetch_orderbook(self, market: str = "POLY"):
        """
        Simulate fetching order book data.
        Returns a snapshot dictionary.
        """
        bids = random.uniform(0.45, 0.55)
        asks = random.uniform(0.45, 0.55)
        spread = abs(bids - asks)

        snapshot = {
            "market": market,
            "bids": bids,
            "asks": asks,
            "spread": spread,
            "timestamp": time()
        }

        self.orderbook_history.append(snapshot)
        return snapshot

    def is_liquid(self, snapshot: dict) -> bool:
        """
        Determine if the market is liquid enough to trade safely.
        """
        if snapshot["spread"] > self.max_spread:
            return False
        return True

    def confirm_signal(self, signal: str, snapshot: dict) -> str:
        """
        Confirm or reject a trade signal based on order book conditions.
        Returns: 'UP', 'DOWN', or 'HOLD'
        """
        if signal == "HOLD":
            return "HOLD"

        if not self.is_liquid(snapshot):
            return "HOLD"

        bid_ask_ratio = snapshot["bids"] / max(snapshot["asks"], 0.0001)

        if signal == "UP" and bid_ask_ratio < self.min_bid_ask_ratio:
            return "HOLD"

        if signal == "DOWN" and bid_ask_ratio > self.max_bid_ask_ratio:
            return "HOLD"

        return signal

    async def get_confirmed_signal(self, signal: str, market: str = "POLY"):
        """
        Fetch orderbook and confirm ML signal in one call.
        """
        snapshot = await self.fetch_orderbook(market)
        confirmed_signal = self.confirm_signal(signal, snapshot)
        return confirmed_signal, snapshot

    async def background_monitor(self, interval: float = 0.5):
        """
        Background monitoring loop (non-blocking).
        Optional: run as asyncio task.
        """
        while True:
            try:
                await self.fetch_orderbook()
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"[OrderBookAnalyzer] Error: {e}")
                await asyncio.sleep(1)
