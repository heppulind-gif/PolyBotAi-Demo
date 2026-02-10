# wallet_tracker.py
import os
import time
from web3 import Web3

class WalletTracker:
    def __init__(self):
        self.rpc_url = os.environ.get("ETH_RPC_URL")
        self.private_key = os.environ.get("WALLET_PRIVATE_KEY")

        self.enabled = bool(self.rpc_url and self.private_key)

        if self.enabled:
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            self.account = self.w3.eth.account.from_key(self.private_key)
            self.address = self.account.address
        else:
            self.w3 = None
            self.address = None

        self.last_balance = None
        self.last_check = time.time()

    # ---------- BALANCE ----------

    def get_balance(self):
        if not self.enabled:
            return None

        balance_wei = self.w3.eth.get_balance(self.address)
        balance_eth = self.w3.from_wei(balance_wei, "ether")
        return float(balance_eth)

    # ---------- STATUS ----------

    def get_status(self):
        if not self.enabled:
            return "👛 Wallet Tracker\n\nWallet not connected."

        balance = self.get_balance()
        delta = ""
        if self.last_balance is not None:
            diff = balance - self.last_balance
            if abs(diff) > 0.00001:
                delta = f"\nChange: {diff:+.5f} ETH"

        self.last_balance = balance

        return (
            "👛 Wallet Tracker\n\n"
            f"Address:\n{self.address}\n\n"
            f"Balance: {balance:.5f} ETH"
            f"{delta}"
        )

    # ---------- TRADE NOTIFICATION ----------

    def notify_trade(self, signal, stake, tx_hash):
        """
        Used by TradeManager.
        """
        if not self.enabled:
            return

        print(
            f"[REAL TRADE]\n"
            f"Signal: {signal}\n"
            f"Stake: {stake} ETH\n"
            f"TX: {tx_hash}"
        )

    # ---------- WATCH LOOP (OPTIONAL) ----------

    def check_balance_change(self, interval=30):
        """
        Optional periodic balance watcher.
        """
        if not self.enabled:
            return

        while True:
            bal = self.get_balance()
            if self.last_balance and abs(bal - self.last_balance) > 0.001:
                print(f"[WALLET CHANGE] {bal:.5f} ETH")
            self.last_balance = bal
            time.sleep(interval)
