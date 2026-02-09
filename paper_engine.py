# paper_engine.py
import asyncio
import random
import time
from crypto_data import CryptoData
from ml_engine import MLModel
from portfolio_manager import PortfolioManager
from orderbook_analyzer import OrderBookAnalyzer
from analytics import Analytics

class PaperEngine:
    def __init__(self):
        self.crypto_data = CryptoData()
        self.ml_model = MLModel()
        self.portfolio = PortfolioManager()
        self.orderbook = OrderBookAnalyzer()
        self.analytics = Analytics()
        self.running = False
        self.simulation_speed = 0.5  # seconds per micro-decision

    async def run_paper_loop(self):
        if self.running:
            return  # Already running
        self.running = True
        await self.crypto_data.connect_ws()

        while self.running:
            # Fetch latest market data
            odds = await self.crypto_data.get_polymarket_odds()
            btc, eth, link = await self.crypto_data.get_crypto_data()

            # Predict trade signal
            signal, confidence = self.ml_model.predict(odds, btc, eth, link)

            # Confirm signal using orderbook
            snapshot = await self.orderbook.fetch_orderbook()
            final_signal = self.orderbook.confirm_signal(signal, snapshot)

            # Calculate stake and TP/SL
            stake = self.portfolio.calculate_stake(confidence)
            tp, sl = self.portfolio.calculate_tp_sl(confidence)

            # Simulate trade outcome
            profit_loss = self._simulate_trade(final_signal, stake, tp, sl)

            # Update portfolio & analytics
            self.portfolio.update_balance(profit_loss)
            self.analytics.log_trade(final_signal, stake, tp, sl, profit_loss, confidence)
            self.analytics.update_market_data(odds, btc, eth, link)

            # Micro-decision speed
            await asyncio.sleep(self.simulation_speed)

    def _simulate_trade(self, signal, stake, tp, sl):
        """
        Simulate realistic P/L based on signal, stake, TP/SL.
        - Uses confidence and randomness to mimic human behavior
        """
        multiplier = 1.0
        if signal == "UP":
            multiplier = random.uniform(0.95, 1.05)
        elif signal == "DOWN":
            multiplier = random.uniform(0.95, 1.02)
        else:  # HOLD
            multiplier = 1.0
        return stake * (multiplier - 1)

    def stop(self):
        self.running = False
