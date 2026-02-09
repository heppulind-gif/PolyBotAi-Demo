# sandbox.py
import asyncio
import random
from crypto_data import CryptoData
from ml_engine import MLModel
from portfolio_manager import PortfolioManager
from analytics import Analytics


class Sandbox:
    def __init__(self):
        self.crypto_data = CryptoData()
        self.ml_model = MLModel()
        self.portfolio = PortfolioManager()
        self.analytics = Analytics()

        self.running = False
        self.simulation_speed = 0.5  # seconds per decision loop

    async def start(self):
        """
        Start sandbox paper trading
        """
        self.running = True
        await self.crypto_data.connect_ws()
        await self.run_simulation_loop()

    async def stop(self):
        self.running = False

    async def run_simulation_loop(self):
        """
        Continuous paper trading loop
        """
        while self.running:
            try:
                # 1️⃣ Fetch latest market data
                data = await self.crypto_data.get_latest_data()
                polymarket = data["polymarket"]
                btc = data["btc"]
                eth = data["eth"]
                link = data["link"]

                # 2️⃣ ML prediction
                signal, confidence = self.ml_model.predict(
                    polymarket, btc, eth, link
                )

                if signal == "HOLD":
                    await asyncio.sleep(self.simulation_speed)
                    continue

                # 3️⃣ Risk checks
                if not self.portfolio.can_trade():
                    await asyncio.sleep(self.simulation_speed)
                    continue

                # 4️⃣ Stake calculation
                stake = self.portfolio.calculate_stake(confidence)
                if stake <= 0:
                    await asyncio.sleep(self.simulation_speed)
                    continue

                # 5️⃣ TP / SL from ML model
                tp = stake * self.ml_model.tp_percent
                sl = stake * self.ml_model.sl_percent

                # 6️⃣ Simulate trade outcome
                profit_loss = self._simulate_trade(
                    signal, stake, confidence, tp, sl
                )

                # 7️⃣ Update portfolio
                self.portfolio.apply_trade_result(profit_loss)

                # 8️⃣ Log analytics
                self.analytics.log_trade(
                    signal=signal,
                    stake=stake,
                    take_profit=tp,
                    stop_loss=sl,
                    profit_loss=profit_loss,
                    confidence=confidence
                )

                self.analytics.update_market_data(
                    polymarket, btc, eth, link
                )

                await asyncio.sleep(self.simulation_speed)

            except Exception as e:
                print(f"[Sandbox] Error: {e}")
                await asyncio.sleep(1)

    def _simulate_trade(self, signal, stake, confidence, tp, sl):
        """
        Realistic paper trade simulation
        """
        # Base win probability influenced by confidence
        win_prob = min(max(confidence, 0.55), 0.75)

        if random.random() < win_prob:
            return round(random.uniform(0.5, 1.0) * tp, 6)
        else:
            return round(-random.uniform(0.5, 1.0) * sl, 6)
