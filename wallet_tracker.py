# wallet_tracker.py
import os
from web3 import Web3
import requests

class WalletTracker:
    def __init__(self):
        # Web3 setup (if you need it here too)
        self.rpc_url = os.environ.get("ETH_RPC_URL")  # optional
        if self.rpc_url:
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        else:
            self.w3 = None

        # Telegram bot setup (example)
        self.telegram_token = os.environ.get("TELEGRAM_TOKEN")
        self.telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    def notify_trade(self, signal, stake, tx_hash):
        """
        Notify user about a trade via Telegram.
        """
        message = f"Trade executed:\nSignal: {signal}\nStake: {stake} ETH\nTx: {tx_hash}"

        if self.telegram_token and self.telegram_chat_id:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {"chat_id": self.telegram_chat_id, "text": message}
            try:
                requests.post(url, data=data)
            except Exception as e:
                print(f"Telegram notification failed: {e}")
        else:
            print(message)  # fallback: print to console

    def track_wallet_balance(self, wallet_address):
        """
        Optional: Check ETH balance of a wallet.
        """
        if not self.w3:
            print("Web3 not initialized, cannot track balance")
            return None
        try:
            balance = self.w3.eth.get_balance(wallet_address)
            eth_balance = self.w3.fromWei(balance, 'ether')
            return eth_balance
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None

    # If you need TradeManager inside here, import inside a method to avoid circular import
    def example_trade_usage(self):
        from trade_manager import TradeManager  # import inside method
        # Example: just to show you can access it safely
        print("TradeManager can be used here if needed")
