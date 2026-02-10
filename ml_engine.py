# ml_engine.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import BayesianRidge

class MLModel:
    def __init__(self):
        # Historical data storage
        self.market_history = []
        self.crypto_history = []

        # ML models
        self.pattern_model = RandomForestClassifier(n_estimators=50)
        self.bayesian_model = BayesianRidge()

        # Feature importance / auto feature selection
        self.feature_weights = {}

        # Auto parameter tuning
        self.tp_percent = 0.05  # default 5%
        self.sl_percent = 0.03  # default 3%
        self.max_stake_percent = 0.1

    def predict(self, market_odds, btc_data, eth_data, link_data):
        """
        Returns a trade signal and confidence %
        """
        # Update histories
        self._update_histories(market_odds, btc_data, eth_data, link_data)

        # Extract features
        features = self._extract_features(market_odds, btc_data, eth_data, link_data)

        # Pattern discovery prediction
        pattern_signal = (
            self.pattern_model.predict([features])[0]
            if len(self.market_history) > 10
            else "UP"
        )

        # Bayesian adjustment
        confidence = (
            self.bayesian_model.predict([features])[0]
            if len(self.market_history) > 10
            else 0.7
        )

        # Apply feature weighting
        weighted_confidence = confidence * self._feature_weight(features)

        # Signal confirmation logic
        final_signal = pattern_signal if weighted_confidence > 0.6 else "HOLD"

        # Auto parameter tuning
        self._auto_tune_params(weighted_confidence)

        return final_signal, weighted_confidence

    def _update_histories(self, market_odds, btc_data, eth_data, link_data):
        self.market_history.append(market_odds)
        self.crypto_history.append([btc_data["price"], eth_data["price"], link_data["price"]])
        # Keep history limited
        if len(self.market_history) > 500:
            self.market_history.pop(0)
            self.crypto_history.pop(0)

    def _extract_features(self, market_odds, btc_data, eth_data, link_data):
        # Example simple feature vector
        features = [
            market_odds["up_prob"],
            market_odds["down_prob"],
            btc_data["price_change"],
            eth_data["price_change"],
            link_data["price_change"]
        ]
        return features

    def _feature_weight(self, features):
        # Simple weighted average if feature_weights exists
        if not self.feature_weights:
            return 1.0
        weighted = sum(f * self.feature_weights.get(i, 1.0) for i, f in enumerate(features)) / len(features)
        return weighted

    def _auto_tune_params(self, confidence):
        # Adjust TP/SL based on confidence
        if confidence > 0.8:
            self.tp_percent = 0.06
            self.sl_percent = 0.02
        elif confidence < 0.5:
            self.tp_percent = 0.03
            self.sl_percent = 0.05
        else:
            self.tp_percent = 0.05
            self.sl_percent = 0.03
