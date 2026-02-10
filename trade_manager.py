# trade_manager.py
import asyncio
from crypto_data import CryptoData
from ml_engine import MLModel
from portfolio_manager import PortfolioManager
from analytics import Analytics
from wallet_tracker import WalletTracker
import random

class TradeManager:
    def __init__(self, crypto_data: CryptoData, ml_model: MLModel,
                 portfolio: PortfolioManager, analytics: Analytics,
                 wallet_tracker: WalletTracker):
        self.crypto_data = crypto_data
        self.ml_model = ml_model
        self.portfolio = portfolio
        self.analytics = analytics
        self.wallet_tracker = wallet_tracker
        self.running = False
        self.simulation_speed = 0.2  # micro-decision speed

    async def run_real_trading(self):
        """Main loop for real trading"""
        if self.running:
            return  # Already running

        if not self.wallet_tracker.enabled:
            print("⚠️ Wallet not enabled. Cannot run real trades.")
            return

        self.running = True
        print("💰 TradeManager started in REAL mode...")

        while self.running:
            try:
                # Fetch market & crypto data
                polymarket_odds = await self.crypto_data.get_polymarket_odds()
                btc, eth, link = await self.crypto_data.get_crypto_data()

                # Predict trade signal
                signal, confidence = self.ml_model.predict(
                    polymarket_odds, btc, eth, link
                )

                # Calculate stake, TP/SL
                stake = self.portfolio.calculate_stake(confidence)
                tp, sl = self.portfolio.calculate_tp_sl(confidence)

                # Execute trade via wallet tracker
                profit_loss = await self.wallet_tracker.execute_trade(signal, stake, tp, sl)

                # Update analytics & portfolio
                self.portfolio.update_balance(profit_loss)
                self.analytics.log_trade(signal, stake, tp, sl, profit_loss, confidence)
                self.analytics.update_market_data(polymarket_odds, btc, eth, link)

                await asyncio.sleep(self.simulation_speed)
            except Exception as e:
                print(f"[TradeManager Error] {e}")
                await asyncio.sleep(1)            
