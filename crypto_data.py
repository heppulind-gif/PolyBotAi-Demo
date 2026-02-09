# crypto_data.py
import asyncio
import random
from collections import deque

class CryptoData:
    def __init__(self):
        # Historical data caches (maxlen=500)
        self.polymarket_history = deque(maxlen=500)
        self.btc_history = deque(maxlen=500)
        self.eth_history = deque(maxlen=500)
        self.link_history = deque(maxlen=500)

        # Simulated WebSocket connection flag
        self.ws_connected = False

    async def connect_ws(self):
        """
        Simulate establishing a low-latency WebSocket connection
        """
        await asyncio.sleep(0.1)
        self.ws_connected = True
        print("[CryptoData] WebSocket connected.")

    async def fetch_polymarket(self):
        """
        Fetch simulated Polymarket odds (0-1)
        """
        odds = round(random.uniform(0.4, 0.6), 3)
        self.polymarket_history.append(odds)
        return odds

    async def fetch_btc(self):
        """
        Fetch simulated BTC price
        """
        price = round(random.uniform(26000, 28000), 2)
        self.btc_history.append(price)
        return price

    async def fetch_eth(self):
        """
        Fetch simulated ETH price
        """
        price = round(random.uniform(1600, 1800), 2)
        self.eth_history.append(price)
        return price

    async def fetch_link(self):
        """
        Fetch simulated LINK price
        """
        price = round(random.uniform(6.5, 8.5), 2)
        self.link_history.append(price)
        return price

    async def get_latest_data(self):
        """
        Fetch all latest market data simultaneously
        """
        polymarket = await self.fetch_polymarket()
        btc = await self.fetch_btc()
        eth = await self.fetch_eth()
        link = await self.fetch_link()

        return {
            "polymarket": polymarket,
            "btc": btc,
            "eth": eth,
            "link": link
        }

    def get_history(self, market: str):
        """
        Return historical data for a given market
        """
        if market.lower() == "polymarket":
            return list(self.polymarket_history)
        elif market.lower() == "btc":
            return list(self.btc_history)
        elif market.lower() == "eth":
            return list(self.eth_history)
        elif market.lower() == "link":
            return list(self.link_history)
        else:
            return []
