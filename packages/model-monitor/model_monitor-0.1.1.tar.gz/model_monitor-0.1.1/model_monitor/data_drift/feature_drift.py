"""
Feature drift detection for Model Monitor.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional, Tuple, Any
import logging
import joblib
from pathlib import Path

from model_monitor.data_drift.statistical_tests import (
    ks_test,
    chi2_test,
    wasserstein_distance,
    jensen_shannon_divergence,
    population_stability_index
)
from model_monitor.data_drift.distribution_metrics import (
    calculate_descriptive_stats,
    compare_distributions,
    calculate_drift_score,
    detect_feature_correlations,
    detect_multivariate_drift
)

logger = logging.getLogger(__name__)


class DataDrift:
    """
    Class for detecting data drift in features.

    This class provides methods for detecting and quantifying drift in
    feature distributions between a baseline dataset and a current dataset.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the data drift detector.

        Args:
            config: Configuration for data drift detection. If None, default values are used.
        """
        self.config = config or {}

        # Set default test types if not specified
        self.test_types = self.config.get(
            "test_types",
            ["ks", "psi", "js_divergence", "wasserstein"]
        )

        # Set categorical test
        self.categorical_test = self.config.get("categorical_test", "chi2")

        # Sample size
        self.sample_size = self.config.get("sample_size", None)

        # Features to ignore
        self.ignore_features = self.config.get("ignore_features", [])

        # Correlation threshold
        self.correlation_threshold = self.config.get("correlation_threshold", 0.7)

        # PCA components for multivariate drift
        self.pca_components = self.config.get("pca_components", 2)

        # State variables
        self.baseline_data = None
        self.categorical_features = []
        self.numerical_features = []
        self.baseline_stats = {}
        self.baseline_timestamp = None

        logger.info("Initialized DataDrift detector")

    def set_baseline(self,
                     data: pd.DataFrame,
                     categorical_features: Optional[List[str]] = None,
                     numerical_features: Optional[List[str]] = None):
        """
        Set the baseline data for drift detection.

        Args:
            data: DataFrame containing the baseline data
            categorical_features: List of categorical feature names
            numerical_features: List of numerical feature names
        """
        self.baseline_data = data.copy()

        # Identify categorical and numerical features if not provided
        if categorical_features is None and numerical_features is None:
            self.categorical_features = []
            self.numerical_features = []

            for col in data.columns:
                if col in self.ignore_features:
                    continue

                if pd.api.types.is_numeric_dtype(data[col]):
                    self.numerical_features.append(col)
                else:
                    self.categorical_features.append(col)
        else:
            # Use provided feature lists
            self.categorical_features = [] if categorical_features is None else categorical_features
            self.numerical_features = [] if numerical_features is None else numerical_features

        # Apply sample size limit if needed
        if self.sample_size is not None and len(data) > self.sample_size:
            self.baseline_data = data.sample(self.sample_size, random_state=42)

        # Calculate baseline statistics
        self.baseline_stats = {}

        for col in self.categorical_features:
            if col in self.ignore_features:
                continue
            self.baseline_stats[col] = calculate_descriptive_stats(
                self.baseline_data[col].values,
                is_categorical=True
            )

        for col in self.numerical_features:
            if col in self.ignore_features:
                continue
            self.baseline_stats[col] = calculate_descriptive_stats(
                self.baseline_data[col].values,
                is_categorical=False
            )

        import datetime
        self.baseline_timestamp = datetime.datetime.now()

        logger.info(f"Baseline set with {len(self.baseline_data)} samples")
        logger.info(f"Categorical features: {len(self.categorical_features)}")
        logger.info(f"Numerical features: {len(self.numerical_features)}")

        return self

    def detect(self,
               data: pd.DataFrame,
               compute_all: bool = False) -> Dict[str, Any]:
        """
        Detect drift in the provided data compared to the baseline.

        Args:
            data: DataFrame containing the current data
            compute_all: Whether to compute all drift metrics (can be slow for large datasets)

        Returns:
            Dictionary containing drift detection results
        """
        if self.baseline_data is None:
            raise ValueError("Baseline data not set. Call set_baseline() first.")

        # Apply sample size limit if needed
        current_data = data.copy()
        if self.sample_size is not None and len(current_data) > self.sample_size:
            current_data = current_data.sample(self.sample_size, random_state=42)

        # Initialize results
        results = {
            "feature_drift": {},
            "drift_detected": {},
            "statistics": {},
            "drift_scores": {},
            "pvalues": {},
            "comparison": {}
        }

        # Check for missing columns
        missing_columns = set(self.baseline_data.columns) - set(current_data.columns)
        extra_columns = set(current_data.columns) - set(self.baseline_data.columns)

        if missing_columns:
            logger.warning(f"Missing columns in current data: {missing_columns}")
            results["warnings"] = {"missing_columns": list(missing_columns)}

        if extra_columns:
            logger.warning(f"Extra columns in current data: {extra_columns}")
            if "warnings" not in results:
                results["warnings"] = {}
            results["warnings"]["extra_columns"] = list(extra_columns)

        # Detect drift for each feature
        all_drifts = {}

        # Process categorical features
        for col in self.categorical_features:
            if col in self.ignore_features or col not in current_data.columns:
                continue

            baseline_values = self.baseline_data[col].values
            current_values = current_data[col].values

            # Run chi-square test for categorical features
            if self.categorical_test == "chi2":
                statistic, p_value, is_drift = chi2_test(baseline_values, current_values)

                results["feature_drift"][col] = {
                    "test": "chi2",
                    "statistic": statistic,
                    "p_value": p_value,
                    "drift_detected": is_drift
                }

                results["drift_detected"][col] = is_drift
                results["statistics"][col] = statistic
                results["pvalues"][col] = p_value

            # Run PSI for categorical features
            psi, psi_drift = population_stability_index(baseline_values, current_values)

            results["feature_drift"][col]["psi"] = psi
            results["feature_drift"][col]["psi_drift"] = psi_drift

            # Compare distributions
            comparison = compare_distributions(baseline_values, current_values, is_categorical=True)
            results["comparison"][col] = comparison

            # Calculate drift score
            drift_score = calculate_drift_score(comparison, is_categorical=True)
            results["drift_scores"][col] = drift_score

            all_drifts[col] = is_drift

        # Process numerical features
        for col in self.numerical_features:
            if col in self.ignore_features or col not in current_data.columns:
                continue

            baseline_values = self.baseline_data[col].values
            current_values = current_data[col].values

            # Initialize feature results
            results["feature_drift"][col] = {}

            # Run all configured tests for numerical features
            is_drift = False

            if "ks" in self.test_types:
                statistic, p_value, ks_drift = ks_test(baseline_values, current_values)

                results["feature_drift"][col]["ks"] = {
                    "statistic": statistic,
                    "p_value": p_value,
                    "drift_detected": ks_drift
                }

                if ks_drift:
                    is_drift = True

                results["pvalues"][col] = p_value
                results["statistics"][col] = statistic

            if "wasserstein" in self.test_types:
                distance, w_drift = wasserstein_distance(baseline_values, current_values)

                results["feature_drift"][col]["wasserstein"] = {
                    "distance": distance,
                    "drift_detected": w_drift
                }

                if w_drift:
                    is_drift = True

            if "js_divergence" in self.test_types:
                divergence, js_drift = jensen_shannon_divergence(baseline_values, current_values)

                results["feature_drift"][col]["js_divergence"] = {
                    "divergence": divergence,
                    "drift_detected": js_drift
                }

                if js_drift:
                    is_drift = True

            if "psi" in self.test_types:
                psi, psi_drift = population_stability_index(baseline_values, current_values)

                results["feature_drift"][col]["psi"] = {
                    "index": psi,
                    "drift_detected": psi_drift
                }

                if psi_drift:
                    is_drift = True

            # Set overall drift detection result
            results["drift_detected"][col] = is_drift

            # Compare distributions
            comparison = compare_distributions(baseline_values, current_values, is_categorical=False)
            results["comparison"][col] = comparison

            # Calculate drift score
            drift_score = calculate_drift_score(comparison, is_categorical=False)
            results["drift_scores"][col] = drift_score

            all_drifts[col] = is_drift

        # Calculate overall drift score (mean of individual scores)
        if results["drift_scores"]:
            results["overall_drift_score"] = np.mean(list(results["drift_scores"].values()))
        else:
            results["overall_drift_score"] = 0.0

        # Determine if any drift is detected
        results["any_drift_detected"] = any(all_drifts.values())

        # Calculate additional metrics if requested
        if compute_all:
            # Detect feature correlation changes
            numerical_df_baseline = self.baseline_data[self.numerical_features]
            numerical_df_current = current_data[self.numerical_features]

            correlation_changes = detect_feature_correlations(
                numerical_df_baseline,
                numerical_df_current,
                threshold=self.correlation_threshold
            )

            results["correlation_changes"] = correlation_changes

            # Detect multivariate drift if we have enough numerical features
            if len(self.numerical_features) >= 2:
                multivariate_drift = detect_multivariate_drift(
                    numerical_df_baseline,
                    numerical_df_current,
                    n_components=min(self.pca_components, len(self.numerical_features))
                )

                results["multivariate_drift"] = multivariate_drift

        return results

    def save(self, path: Union[str, Path]):
        """
        Save the data drift detector to disk.

        Args:
            path: Path to save the detector
        """
        joblib.dump(self, path)
        logger.info(f"Data drift detector saved to {path}")

    @classmethod
    def load(cls, path: Union[str, Path]) -> "DataDrift":
        """
        Load a data drift detector from disk.

        Args:
            path: Path to the saved detector

        Returns:
            DataDrift instance
        """
        detector = joblib.load(path)
        logger.info(f"Data drift detector loaded from {path}")
        return detector