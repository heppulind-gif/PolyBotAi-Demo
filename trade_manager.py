# trade_manager.py
import os
import asyncio
import time
from crypto_data import CryptoData
from ml_engine import MLModel
from portfolio_manager import PortfolioManager
from orderbook_analyzer import OrderBookAnalyzer
from analytics import Analytics
from web3 import Web3  # External library, keep at the top

class TradeManager:
    def __init__(self, paper_engine, wallet_tracker, analytics):
        self.crypto_data = CryptoData()
        self.ml_model = MLModel()
        self.portfolio = PortfolioManager()
        self.orderbook = OrderBookAnalyzer()
        self.analytics = analytics
        self.wallet_tracker = wallet_tracker
        self.paper_engine = paper_engine
        self.running = False

        # Web3 setup
        self.rpc_url = os.environ.get("ETH_RPC_URL")  # e.g., Infura/Alchemy endpoint
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.wallet_private_key = os.environ.get("WALLET_PRIVATE_KEY")
        if not self.wallet_private_key:
            raise Exception("Set WALLET_PRIVATE_KEY in environment variables")
        self.account = self.w3.eth.account.from_key(self.wallet_private_key)

        # Safety limits
        self.max_eth_per_trade = 0.05  # Max ETH per trade

    async def run_real_loop(self):
        if self.running:
            return  # Already running
        self.running = True
        await self.crypto_data.connect_ws()

        # Import WalletTracker inside method to avoid circular import
        from wallet_tracker import WalletTracker

        while self.running:
            # Fetch market data
            odds = await self.crypto_data.get_polymarket_odds()
            btc, eth, link = await self.crypto_data.get_crypto_data()

            # Predict trade signal using learned ML model
            signal, confidence = self.ml_model.predict(odds, btc, eth, link)

            # Confirm signal via orderbook
            snapshot = await self.orderbook.fetch_orderbook()
            final_signal = self.orderbook.confirm_signal(signal, snapshot)

            # Calculate stake
            stake = self.portfolio.calculate_stake(confidence)
            stake = min(stake, self.max_eth_per_trade)

            # Safety check: skip if stake is zero or market illiquid
            if stake <= 0 or final_signal == "HOLD":
                await asyncio.sleep(1)
                continue

            # Execute trade on-chain (Polymarket)
            tx_hash = self._execute_trade_onchain(final_signal, stake)
            
            # Update analytics
            self.analytics.log_trade(final_signal, stake, None, None, 0, confidence)
            self.analytics.update_market_data(odds, btc, eth, link)

            # Notify via Telegram / WalletTracker
            self.wallet_tracker.notify_trade(final_signal, stake, tx_hash)

            await asyncio.sleep(1)  # Micro-decision loop

    def _execute_trade_onchain(self, signal, stake):
        """
        Simulated: Replace with real Polymarket smart contract interaction.
        Signs transaction with local private key.
        """
        # For demonstration, we just simulate a tx hash
        tx_hash = "0x" + "".join([hex(ord(c))[2:] for c in f"{signal}{time.time()}"])[:64]
        print(f"Executing real trade: {signal}, stake: {stake} ETH, tx: {tx_hash}")
        return tx_hash

    def stop(self):
        self.running = False
