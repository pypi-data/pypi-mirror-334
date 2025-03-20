"""
Distribution metrics for comparing datasets and detecting drift.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional, Tuple
from scipy import stats
import logging

logger = logging.getLogger(__name__)


def calculate_descriptive_stats(
        data: np.ndarray,
        is_categorical: bool = False
) -> Dict[str, Union[float, int, str]]:
    """
    Calculate descriptive statistics for a feature.

    Args:
        data: Data for a feature
        is_categorical: Whether the feature is categorical

    Returns:
        Dictionary of descriptive statistics
    """
    # Handle NaN values
    non_nan_data = data[~pd.isna(data)]

    stats_dict = {
        "count": len(data),
        "missing_count": len(data) - len(non_nan_data),
        "missing_percentage": (len(data) - len(non_nan_data)) / len(data) * 100 if len(data) > 0 else 0
    }

    if len(non_nan_data) == 0:
        return stats_dict

    if is_categorical:
        # Categorical statistics
        value_counts = pd.Series(non_nan_data).value_counts(normalize=True)
        most_frequent = value_counts.index[0] if not value_counts.empty else None

        stats_dict.update({
            "unique_count": len(value_counts),
            "most_frequent": most_frequent,
            "most_frequent_percentage": value_counts.iloc[0] * 100 if not value_counts.empty else 0,
            "entropy": stats.entropy(value_counts) if len(value_counts) > 1 else 0
        })
    else:
        # Numerical statistics
        try:
            numeric_data = non_nan_data.astype(float)
            stats_dict.update({
                "mean": float(np.mean(numeric_data)),
                "std": float(np.std(numeric_data)),
                "min": float(np.min(numeric_data)),
                "25%": float(np.percentile(numeric_data, 25)),
                "50%": float(np.median(numeric_data)),
                "75%": float(np.percentile(numeric_data, 75)),
                "max": float(np.max(numeric_data)),
                "skewness": float(stats.skew(numeric_data)),
                "kurtosis": float(stats.kurtosis(numeric_data))
            })
        except (ValueError, TypeError) as e:
            logger.warning(f"Error calculating numerical statistics: {e}")
            stats_dict.update({
                "error": str(e)
            })

    return stats_dict


def compare_distributions(
        baseline: np.ndarray,
        current: np.ndarray,
        is_categorical: bool = False
) -> Dict[str, Union[float, Dict[str, float]]]:
    """
    Compare distributions between baseline and current data.

    Args:
        baseline: Baseline data for a feature
        current: Current data for the same feature
        is_categorical: Whether the feature is categorical

    Returns:
        Dictionary of distribution comparison metrics
    """
    # Calculate stats for both datasets
    baseline_stats = calculate_descriptive_stats(baseline, is_categorical)
    current_stats = calculate_descriptive_stats(current, is_categorical)

    # Initialize results
    comparison = {
        "baseline_stats": baseline_stats,
        "current_stats": current_stats,
        "differences": {}
    }

    # Compare common numerical stats if available
    for stat in ["count", "missing_percentage"]:
        if stat in baseline_stats and stat in current_stats:
            comparison["differences"][stat] = current_stats[stat] - baseline_stats[stat]

    if not is_categorical:
        for stat in ["mean", "std", "min", "25%", "50%", "75%", "max", "skewness", "kurtosis"]:
            if stat in baseline_stats and stat in current_stats:
                comparison["differences"][stat] = current_stats[stat] - baseline_stats[stat]
                # Calculate percentage change for key metrics
                if stat in ["mean", "std", "50%"] and baseline_stats[stat] != 0:
                    comparison["differences"][f"{stat}_pct_change"] = (
                            (current_stats[stat] - baseline_stats[stat]) / abs(baseline_stats[stat]) * 100
                    )
    else:
        # For categorical, calculate difference in entropy and unique counts
        if "entropy" in baseline_stats and "entropy" in current_stats:
            comparison["differences"]["entropy"] = current_stats["entropy"] - baseline_stats["entropy"]

        if "unique_count" in baseline_stats and "unique_count" in current_stats:
            comparison["differences"]["unique_count"] = current_stats["unique_count"] - baseline_stats["unique_count"]

        # Compare distributions of categories
        if len(baseline) > 0 and len(current) > 0:
            # Get unique categories across both datasets
            baseline_series = pd.Series(baseline).replace({np.nan: "NaN"})
            current_series = pd.Series(current).replace({np.nan: "NaN"})

            baseline_counts = baseline_series.value_counts(normalize=True)
            current_counts = current_series.value_counts(normalize=True)

            # Get all categories from both distributions
            all_categories = set(baseline_counts.index).union(set(current_counts.index))

            # Calculate absolute differences in frequencies
            category_diffs = {}
            for category in all_categories:
                baseline_freq = baseline_counts.get(category, 0)
                current_freq = current_counts.get(category, 0)
                category_diffs[str(category)] = current_freq - baseline_freq

            comparison["category_differences"] = category_diffs

            # Calculate L1 (total variation) distance
            l1_distance = sum(abs(current_counts.get(cat, 0) - baseline_counts.get(cat, 0))
                              for cat in all_categories) / 2
            comparison["l1_distance"] = l1_distance

    return comparison


def calculate_drift_score(
        comparison: Dict[str, Union[float, Dict[str, float]]],
        is_categorical: bool = False
) -> float:
    """
    Calculate an overall drift score based on distribution differences.

    Args:
        comparison: Distribution comparison metrics
        is_categorical: Whether the feature is categorical

    Returns:
        Drift score between 0 and 1
    """
    diffs = comparison["differences"]

    if is_categorical:
        # For categorical features, use L1 distance (ranges from 0 to 1)
        if "l1_distance" in comparison:
            return comparison["l1_distance"]
        return 0.0
    else:
        # For numerical features, use a weighted combination of changes
        weights = {
            "mean_pct_change": 0.4,  # Higher weight to mean shift
            "std_pct_change": 0.3,  # Medium weight to variance change
            "50%_pct_change": 0.3  # Medium weight to median shift
        }

        # Calculate weighted score from percent changes (normalized by 100)
        score = 0.0

        for metric, weight in weights.items():
            if metric in diffs:
                # Convert percentage to 0-1 scale with sigmoid-like function
                change = abs(diffs[metric]) / 100
                normalized_change = min(1.0, change / (1.0 + change))
                score += weight * normalized_change

        return score


def detect_feature_correlations(
        baseline_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.2
) -> Dict[str, float]:
    """
    Detect changes in feature correlations between datasets.

    Args:
        baseline_df: Baseline dataframe
        current_df: Current dataframe
        threshold: Threshold for significant correlation change

    Returns:
        Dictionary of correlation changes that exceed the threshold
    """
    # Calculate correlation matrices
    try:
        baseline_corr = baseline_df.corr(method='spearman', numeric_only=True)
        current_corr = current_df.corr(method='spearman', numeric_only=True)

        # Ensure we have same columns
        common_cols = set(baseline_corr.columns).intersection(set(current_corr.columns))
        baseline_corr = baseline_corr.loc[common_cols, common_cols]
        current_corr = current_corr.loc[common_cols, common_cols]

        # Calculate absolute differences
        diff_corr = (current_corr - baseline_corr).abs()

        # Find significant changes
        significant_changes = {}

        for i in range(len(common_cols)):
            for j in range(i + 1, len(common_cols)):
                col1, col2 = list(common_cols)[i], list(common_cols)[j]
                diff = diff_corr.loc[col1, col2]

                if diff > threshold:
                    pair = f"{col1}_{col2}"
                    significant_changes[pair] = {
                        "baseline_corr": baseline_corr.loc[col1, col2],
                        "current_corr": current_corr.loc[col1, col2],
                        "difference": diff,
                        "abs_difference": abs(diff)
                    }

        return significant_changes

    except Exception as e:
        logger.warning(f"Error detecting correlation changes: {e}")
        return {}


def detect_multivariate_drift(
        baseline_df: pd.DataFrame,
        current_df: pd.DataFrame,
        n_components: int = 2
) -> Dict[str, Union[float, bool]]:
    """
    Detect multivariate drift using PCA projection and then comparing distributions.

    Args:
        baseline_df: Baseline dataframe (numerical features only)
        current_df: Current dataframe (numerical features only)
        n_components: Number of PCA components to use

    Returns:
        Dictionary with multivariate drift metrics
    """
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    try:
        # Ensure we have the same columns
        common_cols = list(set(baseline_df.columns).intersection(set(current_df.columns)))

        # Select only numerical columns
        numerical_cols = [col for col in common_cols if pd.api.types.is_numeric_dtype(baseline_df[col])]

        if len(numerical_cols) < 2:
            return {"error": "Not enough numerical features for multivariate analysis"}

        baseline_num = baseline_df[numerical_cols].select_dtypes(include=['number'])
        current_num = current_df[numerical_cols].select_dtypes(include=['number'])

        # Handle missing values
        baseline_num = baseline_num.fillna(baseline_num.mean())
        current_num = current_num.fillna(current_num.mean())

        # Standardize the data
        scaler = StandardScaler()
        baseline_scaled = scaler.fit_transform(baseline_num)
        current_scaled = scaler.transform(current_num)

        # Apply PCA
        pca = PCA(n_components=min(n_components, len(numerical_cols)))
        pca.fit(baseline_scaled)

        # Project both datasets
        baseline_pca = pca.transform(baseline_scaled)
        current_pca = pca.transform(current_scaled)

        # Compare distributions of principal components
        results = {}
        drift_detected = False

        for i in range(pca.n_components_):
            # Check if distributions are significantly different (KS test)
            from model_monitor.data_drift.statistical_tests import ks_test

            statistic, p_value, is_drift = ks_test(
                baseline_pca[:, i],
                current_pca[:, i],
                significance_level=0.05
            )

            results[f"PC{i + 1}"] = {
                "statistic": statistic,
                "p_value": p_value,
                "drift_detected": is_drift,
                "variance_explained": pca.explained_variance_ratio_[i]
            }

            if is_drift:
                drift_detected = True

        # Calculate overall multivariate drift score (weighted by variance explained)
        weights = pca.explained_variance_ratio_ / np.sum(pca.explained_variance_ratio_)

        drift_score = 0
        for i in range(pca.n_components_):
            component_drift = 1.0 if results[f"PC{i + 1}"]["drift_detected"] else 0.0
            drift_score += weights[i] * component_drift

        results["overall_drift_score"] = drift_score
        results["overall_drift_detected"] = drift_detected

        return results

    except Exception as e:
        logger.warning(f"Error in multivariate drift detection: {e}")
        return {"error": str(e)}