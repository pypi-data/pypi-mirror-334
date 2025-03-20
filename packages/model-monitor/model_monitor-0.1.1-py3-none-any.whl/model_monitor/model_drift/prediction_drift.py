"""
Prediction drift detection for model monitoring.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional, Tuple, Any
import logging
from scipy import stats

logger = logging.getLogger(__name__)


def detect_prediction_drift(
        baseline_predictions: np.ndarray,
        current_predictions: np.ndarray,
        significance_level: float = 0.05
) -> Dict[str, Any]:
    """
    Detect drift in model predictions.

    Args:
        baseline_predictions: Baseline model predictions
        current_predictions: Current model predictions
        significance_level: Significance level for statistical tests

    Returns:
        Dictionary with prediction drift detection results
    """
    results = {}

    # Check if predictions are numeric or categorical
    is_numeric = np.issubdtype(baseline_predictions.dtype, np.number) and np.issubdtype(current_predictions.dtype,
                                                                                        np.number)

    if is_numeric:
        # For regression models or probability outputs

        # Descriptive statistics
        baseline_stats = {
            "mean": float(np.mean(baseline_predictions)),
            "std": float(np.std(baseline_predictions)),
            "min": float(np.min(baseline_predictions)),
            "25%": float(np.percentile(baseline_predictions, 25)),
            "median": float(np.median(baseline_predictions)),
            "75%": float(np.percentile(baseline_predictions, 75)),
            "max": float(np.max(baseline_predictions))
        }

        current_stats = {
            "mean": float(np.mean(current_predictions)),
            "std": float(np.std(current_predictions)),
            "min": float(np.min(current_predictions)),
            "25%": float(np.percentile(current_predictions, 25)),
            "median": float(np.median(current_predictions)),
            "75%": float(np.percentile(current_predictions, 75)),
            "max": float(np.max(current_predictions))
        }

        # Kolmogorov-Smirnov test
        ks_statistic, ks_pvalue = stats.ks_2samp(baseline_predictions, current_predictions)

        # Mann-Whitney U test
        mw_statistic, mw_pvalue = stats.mannwhitneyu(baseline_predictions, current_predictions, alternative='two-sided')

        # Determine if drift is detected
        drift_detected = ks_pvalue < significance_level or mw_pvalue < significance_level

        results = {
            "baseline_stats": baseline_stats,
            "current_stats": current_stats,
            "ks_test": {
                "statistic": float(ks_statistic),
                "p_value": float(ks_pvalue),
                "drift_detected": ks_pvalue < significance_level
            },
            "mann_whitney_test": {
                "statistic": float(mw_statistic),
                "p_value": float(mw_pvalue),
                "drift_detected": mw_pvalue < significance_level
            },
            "drift_detected": drift_detected
        }
    else:
        # For classification models with class labels

        # Get unique classes
        unique_classes = np.unique(np.concatenate([baseline_predictions, current_predictions]))

        # Calculate class distribution
        baseline_dist = {str(cls): np.mean(baseline_predictions == cls) for cls in unique_classes}
        current_dist = {str(cls): np.mean(current_predictions == cls) for cls in unique_classes}

        # Chi-square test
        baseline_counts = np.array([np.sum(baseline_predictions == cls) for cls in unique_classes])
        current_counts = np.array([np.sum(current_predictions == cls) for cls in unique_classes])

        # Handle zeros with smoothing
        baseline_counts = baseline_counts + 0.5
        current_counts = current_counts + 0.5

        # Normalize to same sample size for chi-square test
        baseline_counts = baseline_counts / np.sum(baseline_counts) * len(baseline_predictions)
        current_counts = current_counts / np.sum(current_counts) * len(current_predictions)

        try:
            chi2_statistic, chi2_pvalue = stats.chisquare(current_counts, baseline_counts)
            drift_detected = chi2_pvalue < significance_level
        except Exception as e:
            logger.warning(f"Error in Chi-square test: {e}")
            chi2_statistic, chi2_pvalue = np.nan, np.nan
            drift_detected = False

        results = {
            "baseline_distribution": baseline_dist,
            "current_distribution": current_dist,
            "chi2_test": {
                "statistic": float(chi2_statistic) if not np.isnan(chi2_statistic) else None,
                "p_value": float(chi2_pvalue) if not np.isnan(chi2_pvalue) else None,
                "drift_detected": drift_detected
            },
            "drift_detected": drift_detected
        }

    return results


def detect_probability_drift(
        baseline_probabilities: np.ndarray,
        current_probabilities: np.ndarray,
        threshold: float = 0.1
) -> Dict[str, Any]:
    """
    Detect drift in predicted probabilities for classification models.

    Args:
        baseline_probabilities: Baseline predicted probabilities
        current_probabilities: Current predicted probabilities
        threshold: Threshold for drift detection

    Returns:
        Dictionary with probability drift detection results
    """
    results = {}

    # Check if we have binary or multiclass probabilities
    if baseline_probabilities.ndim == 1 or baseline_probabilities.shape[1] == 1:
        # Binary case
        baseline_probs = baseline_probabilities.flatten()
        current_probs = current_probabilities.flatten()

        # Descriptive statistics
        baseline_stats = {
            "mean": float(np.mean(baseline_probs)),
            "std": float(np.std(baseline_probs)),
            "min": float(np.min(baseline_probs)),
            "median": float(np.median(baseline_probs)),
            "max": float(np.max(baseline_probs))
        }

        current_stats = {
            "mean": float(np.mean(current_probs)),
            "std": float(np.std(current_probs)),
            "min": float(np.min(current_probs)),
            "median": float(np.median(current_probs)),
            "max": float(np.max(current_probs))
        }

        # Kolmogorov-Smirnov test
        ks_statistic, ks_pvalue = stats.ks_2samp(baseline_probs, current_probs)

        # Jensen-Shannon divergence
        # Create histograms
        hist_baseline, bin_edges = np.histogram(baseline_probs, bins=20, range=(0, 1), density=True)
        hist_current, _ = np.histogram(current_probs, bins=20, range=(0, 1), density=True)

        # Add small value to avoid zeros
        hist_baseline = hist_baseline + 1e-10
        hist_current = hist_current + 1e-10

        # Normalize
        hist_baseline = hist_baseline / np.sum(hist_baseline)
        hist_current = hist_current / np.sum(hist_current)

        # Calculate JS divergence
        m = 0.5 * (hist_baseline + hist_current)
        js_divergence = 0.5 * (stats.entropy(hist_baseline, m) + stats.entropy(hist_current, m))

        # Drift detection
        drift_detected = ks_pvalue < 0.05 or js_divergence > threshold

        results = {
            "class_positive": {
                "baseline_stats": baseline_stats,
                "current_stats": current_stats,
                "ks_test": {
                    "statistic": float(ks_statistic),
                    "p_value": float(ks_pvalue)
                },
                "js_divergence": float(js_divergence),
                "drift_detected": drift_detected
            },
            "drift_detected": drift_detected
        }

    elif baseline_probabilities.ndim > 1 and baseline_probabilities.shape[1] > 1:
        # Multiclass case
        class_results = {}
        any_drift = False

        for i in range(baseline_probabilities.shape[1]):
            baseline_probs = baseline_probabilities[:, i]
            current_probs = current_probabilities[:, i]

            # Descriptive statistics
            baseline_stats = {
                "mean": float(np.mean(baseline_probs)),
                "std": float(np.std(baseline_probs)),
                "min": float(np.min(baseline_probs)),
                "median": float(np.median(baseline_probs)),
                "max": float(np.max(baseline_probs))
            }

            current_stats = {
                "mean": float(np.mean(current_probs)),
                "std": float(np.std(current_probs)),
                "min": float(np.min(current_probs)),
                "median": float(np.median(current_probs)),
                "max": float(np.max(current_probs))
            }

            # Kolmogorov-Smirnov test
            ks_statistic, ks_pvalue = stats.ks_2samp(baseline_probs, current_probs)

            # Jensen-Shannon divergence
            # Create histograms
            hist_baseline, bin_edges = np.histogram(baseline_probs, bins=20, range=(0, 1), density=True)
            hist_current, _ = np.histogram(current_probs, bins=20, range=(0, 1), density=True)

            # Add small value to avoid zeros
            hist_baseline = hist_baseline + 1e-10
            hist_current = hist_current + 1e-10

            # Normalize
            hist_baseline = hist_baseline / np.sum(hist_baseline)
            hist_current = hist_current / np.sum(hist_current)

            # Calculate JS divergence
            m = 0.5 * (hist_baseline + hist_current)
            js_divergence = 0.5 * (stats.entropy(hist_baseline, m) + stats.entropy(hist_current, m))

            # Drift detection for this class
            class_drift = ks_pvalue < 0.05 or js_divergence > threshold

            if class_drift:
                any_drift = True

            class_results[f"class_{i}"] = {
                "baseline_stats": baseline_stats,
                "current_stats": current_stats,
                "ks_test": {
                    "statistic": float(ks_statistic),
                    "p_value": float(ks_pvalue)
                },
                "js_divergence": float(js_divergence),
                "drift_detected": class_drift
            }

        # Calculate confidence drift (max probability)
        baseline_confidence = np.max(baseline_probabilities, axis=1)
        current_confidence = np.max(current_probabilities, axis=1)

        ks_statistic, ks_pvalue = stats.ks_2samp(baseline_confidence, current_confidence)
        confidence_drift = ks_pvalue < 0.05

        if confidence_drift:
            any_drift = True

        results = {
            "class_probabilities": class_results,
            "confidence": {
                "baseline_mean": float(np.mean(baseline_confidence)),
                "current_mean": float(np.mean(current_confidence)),
                "ks_test": {
                    "statistic": float(ks_statistic),
                    "p_value": float(ks_pvalue)
                },
                "drift_detected": confidence_drift
            },
            "drift_detected": any_drift
        }

    return results


def detect_concept_drift(
        baseline_data: Tuple[np.ndarray, np.ndarray],
        current_data: Tuple[np.ndarray, np.ndarray],
        threshold: float = 0.05
) -> Dict[str, Any]:
    """
    Detect concept drift by comparing model errors across datasets.

    Concept drift occurs when the relationship between input features and the target variable changes.

    Args:
        baseline_data: Tuple of (predictions, actuals) for baseline data
        current_data: Tuple of (predictions, actuals) for current data
        threshold: Threshold for drift detection

    Returns:
        Dictionary with concept drift detection results
    """
    baseline_preds, baseline_actuals = baseline_data
    current_preds, current_actuals = current_data

    # Check if we're dealing with classification or regression
    is_classification = len(np.unique(np.concatenate([baseline_actuals, current_actuals]))) < 10

    if is_classification:
        # For classification, compare error rates
        baseline_errors = (baseline_preds != baseline_actuals).astype(int)
        current_errors = (current_preds != current_actuals).astype(int)

        baseline_error_rate = np.mean(baseline_errors)
        current_error_rate = np.mean(current_errors)

        # Use a proportion test to see if error rates are significantly different
        from statsmodels.stats.proportion import proportions_ztest

        count = [np.sum(current_errors), np.sum(baseline_errors)]
        nobs = [len(current_errors), len(baseline_errors)]

        try:
            z_stat, p_value = proportions_ztest(count, nobs)
            drift_detected = p_value < threshold
        except Exception as e:
            logger.warning(f"Error in proportion test: {e}")
            z_stat, p_value = np.nan, np.nan
            drift_detected = abs(current_error_rate - baseline_error_rate) > threshold

        results = {
            "baseline_error_rate": float(baseline_error_rate),
            "current_error_rate": float(current_error_rate),
            "absolute_difference": float(abs(current_error_rate - baseline_error_rate)),
            "relative_difference": float(
                abs(current_error_rate - baseline_error_rate) / baseline_error_rate) if baseline_error_rate > 0 else float(
                'inf'),
            "proportion_test": {
                "z_statistic": float(z_stat) if not np.isnan(z_stat) else None,
                "p_value": float(p_value) if not np.isnan(p_value) else None,
            },
            "drift_detected": drift_detected
        }
    else:
        # For regression, compare error distributions
        baseline_errors = np.abs(baseline_preds - baseline_actuals)
        current_errors = np.abs(current_preds - current_actuals)

        # Descriptive statistics
        baseline_stats = {
            "mean": float(np.mean(baseline_errors)),
            "std": float(np.std(baseline_errors)),
            "median": float(np.median(baseline_errors)),
            "mae": float(np.mean(baseline_errors)),
            "rmse": float(np.sqrt(np.mean(np.square(baseline_errors))))
        }

        current_stats = {
            "mean": float(np.mean(current_errors)),
            "std": float(np.std(current_errors)),
            "median": float(np.median(current_errors)),
            "mae": float(np.mean(current_errors)),
            "rmse": float(np.sqrt(np.mean(np.square(current_errors))))
        }

        # Kolmogorov-Smirnov test
        ks_statistic, ks_pvalue = stats.ks_2samp(baseline_errors, current_errors)

        # Mann-Whitney U test
        mw_statistic, mw_pvalue = stats.mannwhitneyu(baseline_errors, current_errors, alternative='two-sided')

        # Determine if drift is detected
        drift_detected = ks_pvalue < threshold or mw_pvalue < threshold or \
                         (current_stats["mae"] - baseline_stats["mae"]) / baseline_stats["mae"] > threshold

        results = {
            "baseline_stats": baseline_stats,
            "current_stats": current_stats,
            "absolute_difference_mae": float(current_stats["mae"] - baseline_stats["mae"]),
            "relative_difference_mae": float((current_stats["mae"] - baseline_stats["mae"]) / baseline_stats["mae"]),
            "ks_test": {
                "statistic": float(ks_statistic),
                "p_value": float(ks_pvalue),
            },
            "mann_whitney_test": {
                "statistic": float(mw_statistic),
                "p_value": float(mw_pvalue),
            },
            "drift_detected": drift_detected
        }

    return results