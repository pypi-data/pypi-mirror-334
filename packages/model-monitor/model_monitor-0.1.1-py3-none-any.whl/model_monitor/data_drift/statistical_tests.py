"""
Statistical tests for data drift detection.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Union, Optional, List
from scipy import stats
import logging

logger = logging.getLogger(__name__)


def ks_test(
        baseline: np.ndarray,
        current: np.ndarray,
        significance_level: float = 0.05
) -> Tuple[float, float, bool]:
    """
    Perform a Kolmogorov-Smirnov test to detect drift in numerical features.

    The KS test compares the empirical distribution functions of two samples
    to determine if they come from the same distribution.

    Args:
        baseline: Baseline data for a feature
        current: Current data for the same feature
        significance_level: Alpha level for hypothesis testing

    Returns:
        Tuple of (statistic, p-value, drift_detected)
    """
    # Handle NaN values
    baseline = baseline[~np.isnan(baseline)]
    current = current[~np.isnan(current)]

    if len(baseline) == 0 or len(current) == 0:
        logger.warning("Empty array in KS test after removing NaN values")
        return 0.0, 1.0, False

    # Perform KS test
    statistic, p_value = stats.ks_2samp(baseline, current)
    drift_detected = p_value < significance_level

    return statistic, p_value, drift_detected


def chi2_test(
        baseline: np.ndarray,
        current: np.ndarray,
        significance_level: float = 0.05
) -> Tuple[float, float, bool]:
    """
    Perform a Chi-Square test to detect drift in categorical features.

    Args:
        baseline: Baseline data for a feature (categorical)
        current: Current data for the same feature (categorical)
        significance_level: Alpha level for hypothesis testing

    Returns:
        Tuple of (statistic, p-value, drift_detected)
    """
    # Get unique categories across both datasets
    categories = np.unique(np.concatenate([baseline, current]))

    # Count occurrences in each dataset
    baseline_counts = np.array([np.sum(baseline == cat) for cat in categories])
    current_counts = np.array([np.sum(current == cat) for cat in categories])

    # Handle zeros by adding a small value (smoothing)
    baseline_counts = baseline_counts + 0.5
    current_counts = current_counts + 0.5

    # Normalize to the same sample size
    baseline_counts = baseline_counts / np.sum(baseline_counts) * len(baseline)
    current_counts = current_counts / np.sum(current_counts) * len(current)

    # Perform Chi-Square test
    try:
        statistic, p_value = stats.chisquare(current_counts, baseline_counts)
        drift_detected = p_value < significance_level
    except Exception as e:
        logger.warning(f"Error in Chi-Square test: {e}")
        statistic, p_value, drift_detected = 0.0, 1.0, False

    return statistic, p_value, drift_detected


def wasserstein_distance(
        baseline: np.ndarray,
        current: np.ndarray,
        threshold: float = 0.1
) -> Tuple[float, bool]:
    """
    Calculate the Wasserstein distance (Earth Mover's Distance) between distributions.

    Args:
        baseline: Baseline data for a feature
        current: Current data for the same feature
        threshold: Threshold for determining drift

    Returns:
        Tuple of (distance, drift_detected)
    """
    # Handle NaN values
    baseline = baseline[~np.isnan(baseline)]
    current = current[~np.isnan(current)]

    if len(baseline) == 0 or len(current) == 0:
        logger.warning("Empty array in Wasserstein distance after removing NaN values")
        return 0.0, False

    # Calculate distance
    distance = stats.wasserstein_distance(baseline, current)
    drift_detected = distance > threshold

    return distance, drift_detected


def jensen_shannon_divergence(
        baseline: np.ndarray,
        current: np.ndarray,
        bins: int = 30,
        threshold: float = 0.1
) -> Tuple[float, bool]:
    """
    Calculate the Jensen-Shannon divergence between distributions.

    Args:
        baseline: Baseline data for a feature
        current: Current data for the same feature
        bins: Number of bins for histogram
        threshold: Threshold for determining drift

    Returns:
        Tuple of (divergence, drift_detected)
    """
    # Handle NaN values
    baseline = baseline[~np.isnan(baseline)]
    current = current[~np.isnan(current)]

    if len(baseline) == 0 or len(current) == 0:
        logger.warning("Empty array in JS divergence after removing NaN values")
        return 0.0, False

    # For categorical data
    if baseline.dtype == object or current.dtype == object:
        # Get unique categories
        categories = np.unique(np.concatenate([baseline, current]))

        # Calculate probabilities
        p = np.array([np.mean(baseline == cat) for cat in categories])
        q = np.array([np.mean(current == cat) for cat in categories])

        # Handle zeros with smoothing
        p = p + 1e-10
        q = q + 1e-10

        # Normalize
        p = p / np.sum(p)
        q = q / np.sum(q)
    else:
        # For numerical data, create histograms with same bins
        min_val = min(np.min(baseline), np.min(current))
        max_val = max(np.max(baseline), np.max(current))

        hist_baseline, bin_edges = np.histogram(baseline, bins=bins, range=(min_val, max_val), density=True)
        hist_current, _ = np.histogram(current, bins=bins, range=(min_val, max_val), density=True)

        # Convert to probabilities and handle zeros
        p = hist_baseline + 1e-10
        q = hist_current + 1e-10

        # Normalize
        p = p / np.sum(p)
        q = q / np.sum(q)

    # Calculate JS divergence
    m = 0.5 * (p + q)
    divergence = 0.5 * (stats.entropy(p, m) + stats.entropy(q, m))

    # Handle numerical issues
    if np.isnan(divergence):
        logger.warning("NaN value in JS divergence calculation")
        return 0.0, False

    drift_detected = divergence > threshold

    return divergence, drift_detected


def population_stability_index(
        baseline: np.ndarray,
        current: np.ndarray,
        bins: int = 10,
        threshold: float = 0.25
) -> Tuple[float, bool]:
    """
    Calculate the Population Stability Index (PSI) between distributions.

    PSI = sum((actual_pct - expected_pct) * ln(actual_pct / expected_pct))

    Args:
        baseline: Baseline data for a feature
        current: Current data for the same feature
        bins: Number of bins for numerical data
        threshold: Threshold for determining drift

    Returns:
        Tuple of (psi, drift_detected)
    """
    # Handle NaN values
    baseline = baseline[~np.isnan(baseline)]
    current = current[~np.isnan(current)]

    if len(baseline) == 0 or len(current) == 0:
        logger.warning("Empty array in PSI calculation after removing NaN values")
        return 0.0, False

    # For categorical data
    if baseline.dtype == object or current.dtype == object:
        # Get unique categories
        categories = np.unique(np.concatenate([baseline, current]))

        # Calculate percentages
        expected_pct = np.array([np.mean(baseline == cat) for cat in categories])
        actual_pct = np.array([np.mean(current == cat) for cat in categories])
    else:
        # For numerical data, create binned distributions

        # Define bin edges based on baseline quantiles for more robust binning
        bin_edges = np.linspace(
            np.min(baseline),
            np.max(baseline),
            bins + 1
        )

        # Count observations in each bin
        expected_counts, _ = np.histogram(baseline, bins=bin_edges)
        actual_counts, _ = np.histogram(current, bins=bin_edges)

        # Convert to percentages
        expected_pct = expected_counts / len(baseline)
        actual_pct = actual_counts / len(current)

    # Handle zeros with smoothing
    expected_pct = expected_pct + 1e-6
    actual_pct = actual_pct + 1e-6

    # Normalize percentages to sum to 1
    expected_pct = expected_pct / np.sum(expected_pct)
    actual_pct = actual_pct / np.sum(actual_pct)

    # Calculate PSI
    psi_values = (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)
    psi = np.sum(psi_values)

    # Handle numerical issues
    if np.isnan(psi):
        logger.warning("NaN value in PSI calculation")
        return 0.0, False

    # Interpret PSI
    # < 0.1: No significant change
    # 0.1-0.25: Moderate change
    # > 0.25: Significant change
    drift_detected = psi > threshold

    return psi, drift_detected