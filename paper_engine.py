# paper_engine.py
import asyncio
import random
from crypto_data import CryptoData
from ml_engine import MLModel
from portfolio_manager import PortfolioManager
from analytics import Analytics

class PaperEngine:
    def __init__(self, crypto_data: CryptoData, ml_model: MLModel,
                 portfolio: PortfolioManager, analytics: Analytics):
        self.crypto_data = crypto_data
        self.ml_model = ml_model
        self.portfolio = portfolio
        self.analytics = analytics
        self.running = False
        self.simulation_speed = 0.2  # seconds per micro-decision

    async def run_simulations(self):
        """Main paper trading loop"""
        if self.running:
            return  # Already running

        self.running = True
        print("🧪 PaperEngine started in background...")

        while self.running:
            try:
                polymarket_odds = await self.crypto_data.get_polymarket_odds()
                btc, eth, link = await self.crypto_data.get_crypto_data()

                signal, confidence = self.ml_model.predict(
                    polymarket_odds, btc, eth, link
                )

                stake = self.portfolio.calculate_stake(confidence)
                tp, sl = self.portfolio.calculate_tp_sl(confidence)

                profit_loss = self._simulate_trade(signal, stake, tp, sl)

                self.portfolio.update_balance(profit_loss)
                self.analytics.log_trade(signal, stake, tp, sl, profit_loss, confidence)
                self.analytics.update_market_data(polymarket_odds, btc, eth, link)

                await asyncio.sleep(self.simulation_speed)
            except Exception as e:
                print(f"[PaperEngine Error] {e}")
                await asyncio.sleep(1)

    def _simulate_trade(self, signal, stake, tp, sl):
        multiplier = 1.0
        if signal == "UP":
            multiplier = random.uniform(0.95, 1.05)
        elif signal == "DOWN":
            multiplier = random.uniform(0.95, 1.02)
        return stake * (multiplier - 1)
