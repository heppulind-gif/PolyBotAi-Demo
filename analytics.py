# analytics.py
import time
import numpy as np
from collections import deque


class Analytics:
    def __init__(self):
        # Trade analytics
        self.recent_trades = deque(maxlen=200)

        # Market & crypto history
        self.polymarket_history = deque(maxlen=200)
        self.btc_history = deque(maxlen=200)
        self.eth_history = deque(maxlen=200)
        self.link_history = deque(maxlen=200)

    # -----------------------------
    # Trade logging
    # -----------------------------
    def log_trade(
        self,
        signal: str,
        stake: float,
        take_profit: float,
        stop_loss: float,
        profit_loss: float,
        confidence: float
    ):
        self.recent_trades.append({
            "signal": signal,
            "stake": stake,
            "tp": take_profit,
            "sl": stop_loss,
            "profit_loss": profit_loss,
            "confidence": confidence,
            "timestamp": time.time()
        })

    # -----------------------------
    # Market data updates
    # -----------------------------
    def update_market_data(
        self,
        polymarket_odds: float,
        btc_price: float,
        eth_price: float,
        link_price: float
    ):
        self.polymarket_history.append(polymarket_odds)
        self.btc_history.append(btc_price)
        self.eth_history.append(eth_price)
        self.link_history.append(link_price)

    # -----------------------------
    # Dashboard helpers
    # -----------------------------
    def get_dashboard(self) -> str:
        """
        Returns a Telegram-safe dashboard string
        """
        if not self.recent_trades:
            return "📊 PolyPulse Dashboard\n\nNo trades yet."

        profits = [t["profit_loss"] for t in self.recent_trades]
        wins = [1 for p in profits if p > 0]

        last = self.recent_trades[-1]
        avg_profit = np.mean(profits)
        win_rate = (len(wins) / len(profits)) * 100

        dashboard = (
            "📊 PolyPulse Dashboard\n\n"
            f"Last Trade: {last['signal']}\n"
            f"P/L: {last['profit_loss']:.6f}\n"
            f"Confidence: {last['confidence']:.2f}\n\n"
            f"Avg Profit: {avg_profit:.6f}\n"
            f"Win Rate: {win_rate:.1f}%\n"
            f"Total Trades: {len(self.recent_trades)}"
        )
        return dashboard

    # -----------------------------
    # Correlation & heatmap
    # -----------------------------
    def _safe_corr(self, a, b):
        if len(a) < 10 or len(b) < 10:
            return 0.0
        try:
            return float(np.corrcoef(a, b)[0, 1])
        except Exception:
            return 0.0

    def get_heatmap(self) -> dict:
        """
        Returns correlation values between BTC, ETH, LINK
        """
        return {
            "BTC_ETH": self._safe_corr(self.btc_history, self.eth_history),
            "BTC_LINK": self._safe_corr(self.btc_history, self.link_history),
            "ETH_LINK": self._safe_corr(self.eth_history, self.link_history)
        }

    def get_correlation_map(self) -> str:
        heatmap = self.get_heatmap()
        return (
            "📈 Correlation Map\n\n"
            f"BTC ↔ ETH: {heatmap['BTC_ETH']:.2f}\n"
            f"BTC ↔ LINK: {heatmap['BTC_LINK']:.2f}\n"
            f"ETH ↔ LINK: {heatmap['ETH_LINK']:.2f}"
        )

    # -----------------------------
    # Performance metrics
    # -----------------------------
    def get_performance_metrics(self) -> dict:
        if not self.recent_trades:
            return {
                "win_rate": 0.0,
                "avg_profit": 0.0,
                "max_drawdown": 0.0
            }

        profits = np.array([t["profit_loss"] for t in self.recent_trades])
        cumulative = np.cumsum(profits)
        peak = np.maximum.accumulate(cumulative)
        drawdown = cumulative - peak

        return {
            "win_rate": float((profits > 0).mean() * 100),
            "avg_profit": float(profits.mean()),
            "max_drawdown": float(drawdown.min())
        }
