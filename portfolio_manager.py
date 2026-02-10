# portfolio_manager.py
class PortfolioManager:
    def __init__(self):
        # Starting balances
        self.balance_eth = 1.0          # paper balance default
        self.initial_balance = 1.0

        # Risk controls
        self.max_stake_percent = 0.10   # max 10% per trade
        self.stake_insurance = 0.05     # 5% reserved (never touched)
        self.max_consecutive_losses = 3
        self.consecutive_losses = 0

        # Dynamic parameters (updated by ML)
        self.tp_percent = 0.05
        self.sl_percent = 0.03

        # Kill switch
        self.trading_paused = False

    # ---------- STAKE LOGIC ----------

    def calculate_stake(self, confidence: float) -> float:
        """
        Risk-adjusted stake sizing.
        Higher confidence = larger stake (but capped).
        """
        if self.trading_paused:
            return 0.0

        usable_balance = self.balance_eth * (1 - self.stake_insurance)
        base_stake = usable_balance * self.max_stake_percent

        # Confidence weighting (human-like)
        stake = base_stake * max(0.3, min(confidence, 1.0))

        return round(stake, 6)

    # ---------- TP / SL ----------

    def calculate_tp_sl(self, confidence: float):
        """
        Dynamic TP/SL adjusted by confidence.
        """
        if confidence > 0.8:
            tp = self.tp_percent * 1.2
            sl = self.sl_percent * 0.8
        elif confidence < 0.5:
            tp = self.tp_percent * 0.7
            sl = self.sl_percent * 1.3
        else:
            tp = self.tp_percent
            sl = self.sl_percent

        return round(tp, 4), round(sl, 4)

    # ---------- BALANCE UPDATE ----------

    def update_balance(self, profit_loss: float):
        """
        Update portfolio balance and loss tracking.
        """
        self.balance_eth += profit_loss

        if profit_loss < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

        # Emergency pause if losing streak
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.trading_paused = True

    # ---------- CONTROL ----------

    def resume_trading(self):
        self.consecutive_losses = 0
        self.trading_paused = False

    def get_status(self):
        return {
            "balance_eth": round(self.balance_eth, 4),
            "pnl": round(self.balance_eth - self.initial_balance, 4),
            "paused": self.trading_paused,
            "loss_streak": self.consecutive_losses
        }
