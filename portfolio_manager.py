# portfolio_manager.py
import time


class PortfolioManager:
    def __init__(self, starting_balance: float = 1.0):
        # Portfolio state
        self.balance = starting_balance
        self.starting_balance = starting_balance

        # Risk & protection settings
        self.stake_insurance_percent = 0.05   # 5% reserved
        self.max_stake_percent = 0.10          # max per trade
        self.max_consecutive_losses = 3
        self.daily_loss_limit_percent = 0.15  # 15% daily loss cap

        # Runtime tracking
        self.consecutive_losses = 0
        self.last_trade_time = 0
        self.cooldown_seconds = 300  # 5 minutes after losses
        self.daily_start_balance = starting_balance
        self.last_reset_day = self._current_day()

    # -----------------------------
    # Core helpers
    # -----------------------------
    def _current_day(self):
        return time.strftime("%Y-%m-%d")

    def _reset_daily_if_needed(self):
        today = self._current_day()
        if today != self.last_reset_day:
            self.daily_start_balance = self.balance
            self.consecutive_losses = 0
            self.last_reset_day = today

    # -----------------------------
    # Trade permission logic
    # -----------------------------
    def can_trade(self) -> bool:
        self._reset_daily_if_needed()

        # Cooldown after losses
        if self.consecutive_losses >= self.max_consecutive_losses:
            if time.time() - self.last_trade_time < self.cooldown_seconds:
                return False
            else:
                self.consecutive_losses = 0

        # Daily loss limit
        daily_loss = self.daily_start_balance - self.balance
        if daily_loss / self.daily_start_balance >= self.daily_loss_limit_percent:
            return False

        return True

    # -----------------------------
    # Stake calculation
    # -----------------------------
    def calculate_stake(self, confidence: float) -> float:
        """
        Determine how much to stake based on confidence and safety rules
        """
        insured_balance = self.balance * (1 - self.stake_insurance_percent)

        # Scale stake by confidence (0.6 → small, 0.9 → larger)
        stake = insured_balance * self.max_stake_percent * confidence

        # Never exceed available balance
        stake = min(stake, insured_balance)
        stake = max(stake, 0)

        return round(stake, 6)

    # -----------------------------
    # Trade result updates
    # -----------------------------
    def apply_trade_result(self, profit_loss: float):
        """
        Update balance and loss tracking after a trade
        """
        self.balance += profit_loss
        self.last_trade_time = time.time()

        if profit_loss < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

    # -----------------------------
    # Status reporting
    # -----------------------------
    def get_status(self) -> dict:
        self._reset_daily_if_needed()
        return {
            "balance": round(self.balance, 6),
            "starting_balance": round(self.starting_balance, 6),
            "daily_start_balance": round(self.daily_start_balance, 6),
            "consecutive_losses": self.consecutive_losses,
            "can_trade": self.can_trade()
        }
