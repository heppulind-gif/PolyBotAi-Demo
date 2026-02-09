# ml_engine.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import BayesianRidge

class MLModel:
    def __init__(self):
        # Historical data storage
        self.market_history = []
        self.btc_history = []
        self.eth_history = []
        self.link_history = []

        # ML models
        self.pattern_model = RandomForestClassifier(n_estimators=50)
        self.bayesian_model = BayesianRidge()

        # Feature importance / auto feature selection
        self.feature_weights = {}

        # Auto parameter tuning
        self.tp_percent = 0.05  # 5% take profit
        self.sl_percent = 0.03  # 3% stop loss
        self.max_stake_percent = 0.1  # max % of balance per trade

    def predict(self, market_odds, btc_data, eth_data, link_data):
        """
        Returns a trade signal ('UP', 'DOWN', 'HOLD') and confidence %
        """
        # Update histories
        self._update_histories(market_odds, btc_data, eth_data, link_data)

        # Extract features for ML models
        features = self._extract_features(market_odds, btc_data, eth_data, link_data)

        # Pattern model prediction
        if len(self.market_history) > 10:
            pattern_signal = self.pattern_model.predict([features])[0]
            confidence = self.bayesian_model.predict([features])[0]
        else:
            pattern_signal = "UP"
            confidence = 0.7

        # Apply feature weighting
        weighted_confidence = confidence * self._feature_weight(features)

        # Final signal decision
        final_signal = pattern_signal if weighted_confidence > 0.6 else "HOLD"

        # Adjust TP/SL automatically
        self._auto_tune_params(weighted_confidence)

        return final_signal, weighted_confidence

    def _update_histories(self, market_odds, btc_data, eth_data, link_data):
        self.market_history.append(market_odds)
        self.btc_history.append(btc_data)
        self.eth_history.append(eth_data)
        self.link_history.append(link_data)

        # Limit history size to prevent memory issues
        max_len = 500
        self.market_history = self.market_history[-max_len:]
        self.btc_history = self.btc_history[-max_len:]
        self.eth_history = self.eth_history[-max_len:]
        self.link_history = self.link_history[-max_len:]

    def _extract_features(self, market_odds, btc_data, eth_data, link_data):
        """
        Convert raw data to ML features
        """
        features = [
            market_odds,
            btc_data,
            eth_data,
            link_data,
            np.mean(self.market_history[-10:]),
            np.mean(self.btc_history[-10:]),
            np.mean(self.eth_history[-10:]),
            np.mean(self.link_history[-10:])
        ]
        return features

    def _feature_weight(self, features):
        """
        Placeholder for feature weighting logic
        """
        # For now, simple equal weight
        return 1.0

    def _auto_tune_params(self, confidence):
        """
        Adjust take profit / stop loss based on confidence
        """
        if confidence > 0.8:
            self.tp_percent = min(0.1, self.tp_percent + 0.01)
            self.sl_percent = max(0.01, self.sl_percent - 0.005)
        elif confidence < 0.5:
            self.tp_percent = max(0.02, self.tp_percent - 0.01)
            self.sl_percent = min(0.05, self.sl_percent + 0.005)
