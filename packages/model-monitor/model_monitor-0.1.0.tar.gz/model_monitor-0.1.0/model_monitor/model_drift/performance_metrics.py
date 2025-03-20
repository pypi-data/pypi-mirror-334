"""
Model performance metrics and drift detection.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional, Tuple, Any
from sklearn import metrics
import logging
import joblib
from pathlib import Path
import datetime

logger = logging.getLogger(__name__)


class ModelDrift:
    """
    Class for detecting drift in model performance metrics.

    This class provides methods for monitoring model performance over time
    and detecting significant degradation compared to a baseline.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the model drift detector.

        Args:
            config: Configuration for model drift detection. If None, default values are used.
        """
        self.config = config or {}

        # Performance metrics to track
        self.metrics = self.config.get(
            "metrics",
            ["accuracy", "f1", "precision", "recall", "roc_auc"]
        )

        # Window size for tracking performance
        self.window_size = self.config.get("window_size", 30)

        # Minimum samples required for performance evaluation
        self.min_samples = self.config.get("min_samples", 100)

        # Window type for performance monitoring
        self.performance_window_type = self.config.get("performance_window_type", "rolling")

        # Window type for reference (baseline) performance
        self.reference_window_type = self.config.get("reference_window_type", "fixed")

        # State variables
        self.model = None
        self.model_metadata = {}
        self.baseline_performance = {}
        self.performance_history = []
        self.prediction_history = []
        self.last_drift_check = None

        logger.info("Initialized ModelDrift detector")

    def set_model(self, model: Any, metadata: Optional[Dict] = None):
        """
        Set the model to be monitored.

        Args:
            model: Machine learning model
            metadata: Model metadata
        """
        self.model = model
        self.model_metadata = metadata or {}

        # Reset performance tracking
        self.baseline_performance = {}
        self.performance_history = []
        self.prediction_history = []

        logger.info(f"Model set: {self.model_metadata.get('name', 'unknown')}")

        return self

    def calculate_performance_metrics(
            self,
            y_true: np.ndarray,
            y_pred: np.ndarray,
            y_prob: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Calculate performance metrics for classification models.

        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_prob: Predicted probabilities (for ROC AUC)

        Returns:
            Dictionary of performance metrics
        """
        results = {}

        try:
            # Ensure we have enough samples
            if len(y_true) < self.min_samples:
                logger.warning(f"Not enough samples for reliable metrics: {len(y_true)} < {self.min_samples}")
                return {"error": f"Not enough samples: {len(y_true)} < {self.min_samples}"}

            # Basic classification metrics
            if "accuracy" in self.metrics:
                results["accuracy"] = metrics.accuracy_score(y_true, y_pred)

            # Handle binary vs multiclass
            is_binary = len(np.unique(y_true)) <= 2

            if is_binary:
                # Binary classification metrics
                if "precision" in self.metrics:
                    results["precision"] = metrics.precision_score(y_true, y_pred, zero_division=0)

                if "recall" in self.metrics:
                    results["recall"] = metrics.recall_score(y_true, y_pred, zero_division=0)

                if "f1" in self.metrics:
                    results["f1"] = metrics.f1_score(y_true, y_pred, zero_division=0)

                if "roc_auc" in self.metrics and y_prob is not None:
                    # For binary classification, use the probability of the positive class
                    if y_prob.ndim > 1 and y_prob.shape[1] > 1:
                        y_prob_pos = y_prob[:, 1]
                    else:
                        y_prob_pos = y_prob

                    try:
                        results["roc_auc"] = metrics.roc_auc_score(y_true, y_prob_pos)
                    except Exception as e:
                        logger.warning(f"Error calculating ROC AUC: {e}")
            else:
                # Multiclass classification metrics
                if "precision" in self.metrics:
                    results["precision"] = metrics.precision_score(y_true, y_pred, average='weighted', zero_division=0)

                if "recall" in self.metrics:
                    results["recall"] = metrics.recall_score(y_true, y_pred, average='weighted', zero_division=0)

                if "f1" in self.metrics:
                    results["f1"] = metrics.f1_score(y_true, y_pred, average='weighted', zero_division=0)

                if "roc_auc" in self.metrics and y_prob is not None:
                    try:
                        results["roc_auc"] = metrics.roc_auc_score(y_true, y_prob, average='weighted',
                                                                   multi_class='ovr')
                    except Exception as e:
                        logger.warning(f"Error calculating ROC AUC for multiclass: {e}")

            # Additional metrics that work for both binary and multiclass
            if "balanced_accuracy" in self.metrics:
                results["balanced_accuracy"] = metrics.balanced_accuracy_score(y_true, y_pred)

            if "log_loss" in self.metrics and y_prob is not None:
                try:
                    results["log_loss"] = metrics.log_loss(y_true, y_prob)
                except Exception as e:
                    logger.warning(f"Error calculating log loss: {e}")

            if "confusion_matrix" in self.metrics:
                cm = metrics.confusion_matrix(y_true, y_pred)
                results["confusion_matrix"] = cm.tolist()

            # Calculate a single performance score (weighted average of metrics)
            metric_weights = {
                "accuracy": 0.2,
                "precision": 0.2,
                "recall": 0.2,
                "f1": 0.2,
                "roc_auc": 0.2,
                "balanced_accuracy": 0.0,  # Not included in the performance score
                "log_loss": 0.0  # Not included in the performance score
            }

            # Calculate the weighted performance score
            performance_score = 0.0
            weight_sum = 0.0

            for metric, weight in metric_weights.items():
                if metric in results and metric != "confusion_matrix":
                    performance_score += results[metric] * weight
                    weight_sum += weight

            if weight_sum > 0:
                results["performance_score"] = performance_score / weight_sum

            return results

        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {"error": str(e)}

    def compare_performance(
            self,
            baseline_metrics: Dict[str, float],
            current_metrics: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Compare current performance with baseline performance.

        Args:
            baseline_metrics: Baseline performance metrics
            current_metrics: Current performance metrics

        Returns:
            Dictionary of performance differences
        """
        differences = {}

        for metric in baseline_metrics:
            if metric in current_metrics and metric != "confusion_matrix":
                baseline_value = baseline_metrics[metric]
                current_value = current_metrics[metric]

                differences[metric] = {
                    "baseline": baseline_value,
                    "current": current_value,
                    "absolute_diff": current_value - baseline_value,
                    "relative_diff": (
                                                 current_value - baseline_value) / baseline_value if baseline_value != 0 else float(
                        'inf')
                }

        return differences

    def detect(
            self,
            X: pd.DataFrame,
            y_pred: np.ndarray,
            y_true: np.ndarray,
            probabilities: Optional[np.ndarray] = None,
            timestamp: Optional[Union[str, datetime.datetime]] = None,
            compute_all: bool = True
    ) -> Dict[str, Any]:
        """
        Detect drift in model performance.

        Args:
            X: Feature matrix
            y_pred: Predicted labels
            y_true: True labels
            probabilities: Predicted probabilities (optional)
            timestamp: Timestamp for the data point
            compute_all: Whether to compute all drift metrics

        Returns:
            Dictionary containing performance drift detection results
        """
        # Set timestamp if not provided
        if timestamp is None:
            timestamp = datetime.datetime.now()
        elif isinstance(timestamp, str):
            timestamp = datetime.datetime.fromisoformat(timestamp)

        # Calculate performance metrics
        current_metrics = self.calculate_performance_metrics(y_true, y_pred, probabilities)

        # Record performance
        performance_record = {
            "timestamp": timestamp.isoformat(),
            "metrics": current_metrics,
            "n_samples": len(y_true)
        }

        self.performance_history.append(performance_record)

        # If we don't have baseline performance, set it
        if not self.baseline_performance:
            self.baseline_performance = current_metrics
            logger.info("Baseline performance set")

            return {
                "baseline_performance": self.baseline_performance,
                "current_performance": current_metrics,
                "performance_drift_detected": False,
                "performance_degradation": 0.0
            }

        # Compare with baseline
        differences = self.compare_performance(self.baseline_performance, current_metrics)

        # Calculate performance degradation
        degradation = 0.0
        metric_count = 0

        for metric, diff in differences.items():
            if metric in ["accuracy", "precision", "recall", "f1", "roc_auc", "performance_score"]:
                # For these metrics, negative differences indicate degradation
                degradation += max(0, -diff["absolute_diff"])
                metric_count += 1

        if metric_count > 0:
            avg_degradation = degradation / metric_count
        else:
            avg_degradation = 0.0

        # Determine if drift is detected based on threshold
        # A degradation of 0.05 (5%) or more is considered significant
        threshold = self.config.get("performance_threshold", 0.05)
        drift_detected = avg_degradation >= threshold

        # Put together results
        results = {
            "baseline_performance": self.baseline_performance,
            "current_performance": current_metrics,
            "differences": differences,
            "performance_degradation": avg_degradation,
            "performance_drift_detected": drift_detected,
            "timestamp": timestamp.isoformat()
        }

        # Add prediction distribution analysis if requested
        if compute_all and probabilities is not None:
            prediction_distribution = self.analyze_prediction_distribution(y_pred, probabilities)
            results["prediction_distribution"] = prediction_distribution

        # Update last drift check timestamp
        self.last_drift_check = timestamp

        return results

    def analyze_prediction_distribution(
            self,
            y_pred: np.ndarray,
            probabilities: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Analyze the distribution of model predictions.

        Args:
            y_pred: Predicted labels
            probabilities: Predicted probabilities

        Returns:
            Dictionary with prediction distribution analysis
        """
        results = {}

        # Analyze predicted labels
        unique_labels, counts = np.unique(y_pred, return_counts=True)
        label_distribution = {str(label): count / len(y_pred) for label, count in zip(unique_labels, counts)}

        results["label_distribution"] = label_distribution

        # Analyze predicted probabilities if available
        if probabilities is not None:
            try:
                # Check if we have binary or multiclass probabilities
                if probabilities.ndim == 1 or probabilities.shape[1] == 1:
                    # Binary case with single probability column
                    prob_data = probabilities.flatten()

                    # Calculate histogram
                    hist, bin_edges = np.histogram(prob_data, bins=10, range=(0, 1))

                    prob_histogram = {
                        "counts": hist.tolist(),
                        "bin_edges": bin_edges.tolist(),
                        "mean": float(np.mean(prob_data)),
                        "std": float(np.std(prob_data)),
                        "min": float(np.min(prob_data)),
                        "max": float(np.max(prob_data))
                    }

                    results["probability_distribution"] = {"class_1": prob_histogram}

                elif probabilities.ndim > 1 and probabilities.shape[1] > 1:
                    # Multiclass case
                    class_stats = {}

                    for i in range(probabilities.shape[1]):
                        prob_data = probabilities[:, i]

                        # Calculate histogram
                        hist, bin_edges = np.histogram(prob_data, bins=10, range=(0, 1))

                        class_stats[f"class_{i}"] = {
                            "counts": hist.tolist(),
                            "bin_edges": bin_edges.tolist(),
                            "mean": float(np.mean(prob_data)),
                            "std": float(np.std(prob_data)),
                            "min": float(np.min(prob_data)),
                            "max": float(np.max(prob_data))
                        }

                    results["probability_distribution"] = class_stats

                # Calculate confidence (max probability)
                if probabilities.ndim > 1 and probabilities.shape[1] > 1:
                    confidence = np.max(probabilities, axis=1)
                else:
                    confidence = np.maximum(probabilities, 1 - probabilities)

                results["confidence_stats"] = {
                    "mean": float(np.mean(confidence)),
                    "std": float(np.std(confidence)),
                    "min": float(np.min(confidence)),
                    "median": float(np.median(confidence)),
                    "max": float(np.max(confidence))
                }

            except Exception as e:
                logger.warning(f"Error analyzing prediction probabilities: {e}")
                results["probability_analysis_error"] = str(e)

        return results

    def save(self, path: Union[str, Path]):
        """
        Save the model drift detector to disk.

        Args:
            path: Path to save the detector
        """
        # Create a copy without the model (which might not be serializable)
        state_dict = {k: v for k, v in self.__dict__.items() if k != 'model'}

        joblib.dump(state_dict, path)
        logger.info(f"Model drift detector state saved to {path}")

    @classmethod
    def load(cls, path: Union[str, Path]) -> "ModelDrift":
        """
        Load a model drift detector from disk.

        Args:
            path: Path to the saved detector state

        Returns:
            ModelDrift instance
        """
        state_dict = joblib.load(path)

        # Create a new instance
        detector = cls()

        # Update the instance with the loaded state
        for k, v in state_dict.items():
            setattr(detector, k, v)

        logger.info(f"Model drift detector state loaded from {path}")
        return detector