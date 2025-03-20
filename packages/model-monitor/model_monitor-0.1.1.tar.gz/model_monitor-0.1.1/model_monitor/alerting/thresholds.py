"""
Thresholds for alert detection in model monitoring.
"""

from typing import Dict, List, Union, Optional, Any
import numpy as np
import logging

logger = logging.getLogger(__name__)


class ThresholdManager:
    """
    Manager for alert thresholds in model monitoring.

    This class provides methods for setting and evaluating thresholds
    for data drift and model performance metrics.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the threshold manager.

        Args:
            config: Configuration for thresholds
        """
        self.config = config or {}

        # Set default thresholds
        self.drift_threshold = self.config.get("drift_threshold", 0.05)
        self.performance_threshold = self.config.get("performance_threshold", 0.1)

        # Feature-specific thresholds
        self.feature_thresholds = self.config.get("feature_thresholds", {})

        # Metric-specific thresholds
        self.metric_thresholds = self.config.get("metric_thresholds", {})

        logger.info("Initialized ThresholdManager")

    def set_drift_threshold(self,
                            threshold: float,
                            feature: Optional[str] = None):
        """
        Set drift threshold.

        Args:
            threshold: Threshold value (0-1)
            feature: Feature name (if None, sets the global threshold)
        """
        if feature is None:
            self.drift_threshold = threshold
        else:
            self.feature_thresholds[feature] = threshold

    def set_performance_threshold(self,
                                  threshold: float,
                                  metric: Optional[str] = None):
        """
        Set performance threshold.

        Args:
            threshold: Threshold value (0-1)
            metric: Metric name (if None, sets the global threshold)
        """
        if metric is None:
            self.performance_threshold = threshold
        else:
            self.metric_thresholds[metric] = threshold

    def get_drift_threshold(self, feature: Optional[str] = None) -> float:
        """
        Get drift threshold for a feature.

        Args:
            feature: Feature name (if None, returns the global threshold)

        Returns:
            Threshold value
        """
        if feature is not None and feature in self.feature_thresholds:
            return self.feature_thresholds[feature]
        return self.drift_threshold

    def get_performance_threshold(self, metric: Optional[str] = None) -> float:
        """
        Get performance threshold for a metric.

        Args:
            metric: Metric name (if None, returns the global threshold)

        Returns:
            Threshold value
        """
        if metric is not None and metric in self.metric_thresholds:
            return self.metric_thresholds[metric]
        return self.performance_threshold

    def check_drift_alert(self,
                          feature: str,
                          drift_score: float) -> bool:
        """
        Check if a drift alert should be triggered for a feature.

        Args:
            feature: Feature name
            drift_score: Drift score (0-1)

        Returns:
            True if alert should be triggered, False otherwise
        """
        threshold = self.get_drift_threshold(feature)
        return drift_score > threshold

    def check_performance_alert(self,
                                metric: str,
                                baseline_value: float,
                                current_value: float) -> bool:
        """
        Check if a performance alert should be triggered for a metric.

        Args:
            metric: Metric name
            baseline_value: Baseline metric value
            current_value: Current metric value

        Returns:
            True if alert should be triggered, False otherwise
        """
        threshold = self.get_performance_threshold(metric)

        # For metrics where higher is better (accuracy, precision, recall, f1, etc.)
        if metric in ["accuracy", "precision", "recall", "f1", "roc_auc", "mcc", "r2"]:
            return (baseline_value - current_value) > threshold

        # For metrics where lower is better (error, loss, etc.)
        else:
            return (current_value - baseline_value) > threshold

    def validate_thresholds(self) -> Dict[str, Any]:
        """
        Validate that all thresholds are within reasonable ranges.

        Returns:
            Dictionary with validation results
        """
        validation = {"valid": True, "warnings": []}

        # Check global thresholds
        if not 0 <= self.drift_threshold <= 1:
            validation["warnings"].append(f"Global drift threshold {self.drift_threshold} outside range [0,1]")
            validation["valid"] = False

        if not 0 <= self.performance_threshold <= 1:
            validation["warnings"].append(
                f"Global performance threshold {self.performance_threshold} outside range [0,1]")
            validation["valid"] = False

        # Check feature thresholds
        for feature, threshold in self.feature_thresholds.items():
            if not 0 <= threshold <= 1:
                validation["warnings"].append(f"Feature '{feature}' threshold {threshold} outside range [0,1]")
                validation["valid"] = False

        # Check metric thresholds
        for metric, threshold in self.metric_thresholds.items():
            if not 0 <= threshold <= 1:
                validation["warnings"].append(f"Metric '{metric}' threshold {threshold} outside range [0,1]")
                validation["valid"] = False

        return validation