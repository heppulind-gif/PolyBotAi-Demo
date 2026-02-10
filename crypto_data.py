# crypto_data.py
import asyncio
import random
import time
from collections import deque

class CryptoData:
    def __init__(self):
        # Historical caches
        self.polymarket_history = deque(maxlen=500)
        self.btc_history = deque(maxlen=500)
        self.eth_history = deque(maxlen=500)
        self.link_history = deque(maxlen=500)

        self.ws_connected = False

    # ---------- CONNECTION ----------

    async def connect_ws(self):
        """
        Simulated low-latency websocket connection.
        Keeps async structure compatible with real APIs later.
        """
        await asyncio.sleep(0.1)
        self.ws_connected = True

    # ---------- POLYMARKET (15 MIN UP/DOWN) ----------

    async def get_polymarket_odds(self):
        """
        Returns simulated Polymarket odds.
        Replace later with real Polymarket API.
        """
        up_prob = random.uniform(0.45, 0.55)
        down_prob = 1 - up_prob

        odds = {
            "up_prob": round(up_prob, 4),
            "down_prob": round(down_prob, 4),
            "timestamp": time.time()
        }

        self.polymarket_history.append(odds)
        return odds

    # ---------- CRYPTO PRICES ----------

    async def get_crypto_data(self):
        """
        Returns BTC, ETH, LINK price + price change.
        """
        btc = self._generate_price(self.btc_history, base=65000)
        eth = self._generate_price(self.eth_history, base=3200)
        link = self._generate_price(self.link_history, base=18)

        return btc, eth, link

    # ---------- INTERNAL HELPERS ----------

    def _generate_price(self, history, base):
        """
        Generates realistic micro price movement.
        """
        if not history:
            price = base
        else:
            price = history[-1]["price"]

        change = random.uniform(-0.003, 0.003)
        new_price = price * (1 + change)

        data = {
            "price": round(new_price, 4),
            "price_change": round(change, 6),
            "time": time.time()
        }

        history.append(data)
        return data
