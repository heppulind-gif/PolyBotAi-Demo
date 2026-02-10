# analytics.py
import time
import numpy as np
from collections import deque

class Analytics:
    def __init__(self):
        self.trades = deque(maxlen=200)
        self.market_history = deque(maxlen=200)
        self.crypto_history = deque(maxlen=200)

    # ---------- LOGGING ----------

    def log_trade(self, signal, stake, tp, sl, profit_loss, confidence):
        self.trades.append({
            "signal": signal,
            "stake": stake,
            "tp": tp,
            "sl": sl,
            "pnl": profit_loss,
            "confidence": confidence,
            "time": time.time()
        })

    def update_market_data(self, odds, btc, eth, link):
        self.market_history.append(odds)
        self.crypto_history.append([
            btc["price"],
            eth["price"],
            link["price"]
        ])

    # ---------- DASHBOARD ----------

    def get_dashboard(self):
        if not self.trades:
            return "📊 PolyPulse Dashboard\n\nNo trades yet."

        wins = [t for t in self.trades if t["pnl"] > 0]
        losses = [t for t in self.trades if t["pnl"] <= 0]

        win_rate = (len(wins) / len(self.trades)) * 100
        avg_pnl = np.mean([t["pnl"] for t in self.trades])
        last = self.trades[-1]

        return (
            "📊 PolyPulse Dashboard\n\n"
            f"Last Trade: {last['signal']}\n"
            f"P/L: {last['pnl']:.5f} ETH\n"
            f"Confidence: {last['confidence']:.2f}\n\n"
            f"Trades: {len(self.trades)}\n"
            f"Win Rate: {win_rate:.1f}%\n"
            f"Avg P/L: {avg_pnl:.5f} ETH"
        )

    # ---------- CORRELATION / HEATMAP ----------

    def get_heatmap(self):
        if len(self.crypto_history) < 10:
            return None

        data = np.array(self.crypto_history)
        corr = np.corrcoef(data.T)

        return {
            "BTC-ETH": corr[0][1],
            "BTC-LINK": corr[0][2],
            "ETH-LINK": corr[1][2]
        }

    def get_correlation_map(self):
        heat = self.get_heatmap()
        if not heat:
            return "📈 Correlation Map\n\nNot enough data yet."

        return (
            "📈 Correlation Map\n\n"
            f"BTC ↔ ETH: {heat['BTC-ETH']:.2f}\n"
            f"BTC ↔ LINK: {heat['BTC-LINK']:.2f}\n"
            f"ETH ↔ LINK: {heat['ETH-LINK']:.2f}"
        )

    # ---------- PERFORMANCE METRICS ----------

    def performance_score(self):
        if len(self.trades) < 10:
            return 0.0

        pnl = sum(t["pnl"] for t in self.trades)
        confidence_avg = np.mean([t["confidence"] for t in self.trades])
        win_rate = len([t for t in self.trades if t["pnl"] > 0]) / len(self.trades)

        # Risk-adjusted score
        return round((pnl * win_rate * confidence_avg), 4)
        
