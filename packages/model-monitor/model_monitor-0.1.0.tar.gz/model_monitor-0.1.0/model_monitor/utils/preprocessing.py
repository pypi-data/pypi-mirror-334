"""
Data preprocessing utilities for model monitoring.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Union, Optional, Any, Tuple
from pathlib import Path
import joblib

logger = logging.getLogger(__name__)


class Preprocessor:
    """
    Class for preprocessing data for model monitoring.

    This class provides methods for handling missing values, encoding categorical
    features, scaling numerical features, etc.
    """

    def __init__(self):
        """Initialize the preprocessor."""
        # Transformers
        self.encoders = {}
        self.scalers = {}
        self.imputers = {}

        # Feature lists
        self.numerical_features = []
        self.categorical_features = []
        self.all_features = []

        # Fitted flag
        self.is_fitted = False

        logger.info("Initialized Preprocessor")

    def preprocess(self,
                   data: pd.DataFrame,
                   categorical_features: Optional[List[str]] = None,
                   numerical_features: Optional[List[str]] = None,
                   fit: bool = False) -> pd.DataFrame:
        """
        Preprocess data for model monitoring.

        Args:
            data: DataFrame to preprocess
            categorical_features: List of categorical feature names
            numerical_features: List of numerical feature names
            fit: Whether to fit the preprocessor on this data

        Returns:
            Preprocessed DataFrame
        """
        # Make a copy to avoid modifying the original DataFrame
        df = data.copy()

        # Identify categorical and numerical features if not provided
        if fit:
            self._identify_features(df, categorical_features, numerical_features)

        # Handle missing values
        df = self._handle_missing_values(df, fit=fit)

        # Encode categorical features
        df = self._encode_categorical_features(df, fit=fit)

        # Scale numerical features
        # Commented out as we typically don't scale in drift detection
        # df = self._scale_numerical_features(df, fit=fit)

        if fit:
            self.is_fitted = True

        return df

    def _identify_features(self,
                           df: pd.DataFrame,
                           categorical_features: Optional[List[str]] = None,
                           numerical_features: Optional[List[str]] = None):
        """
        Identify categorical and numerical features.

        Args:
            df: DataFrame to analyze
            categorical_features: List of categorical feature names
            numerical_features: List of numerical feature names
        """
        # Use provided feature lists if available
        if categorical_features is not None:
            self.categorical_features = [col for col in categorical_features if col in df.columns]

        if numerical_features is not None:
            self.numerical_features = [col for col in numerical_features if col in df.columns]

        # If either list is not provided, infer from data types
        if not self.categorical_features and not self.numerical_features:
            self.categorical_features = []
            self.numerical_features = []

            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Check if this is a categorical feature encoded as numbers
                    n_unique = df[col].nunique()
                    if n_unique <= 10 or (n_unique <= 20 and n_unique / len(df) < 0.05):
                        self.categorical_features.append(col)
                    else:
                        self.numerical_features.append(col)
                else:
                    self.categorical_features.append(col)

        # Store all features
        self.all_features = self.categorical_features + self.numerical_features

        logger.info(
            f"Identified {len(self.categorical_features)} categorical features and {len(self.numerical_features)} numerical features")

    def _handle_missing_values(self, df: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.

        Args:
            df: DataFrame to process
            fit: Whether to fit the imputers on this data

        Returns:
            DataFrame with handled missing values
        """
        # Make a copy to avoid modifying the original DataFrame
        df_out = df.copy()

        # For categorical features, fill with the most frequent value
        for col in self.categorical_features:
            if col not in df_out.columns:
                continue

            if fit:
                # Get the most frequent value
                most_frequent = df_out[col].mode().iloc[0] if not df_out[col].isnull().all() else "MISSING"
                self.imputers[col] = most_frequent

            if col in self.imputers:
                # Fill missing values
                df_out[col] = df_out[col].fillna(self.imputers[col])

        # For numerical features, fill with the median
        for col in self.numerical_features:
            if col not in df_out.columns:
                continue

            if fit:
                # Get the median value
                median = df_out[col].median() if not df_out[col].isnull().all() else 0
                self.imputers[col] = median

            if col in self.imputers:
                # Fill missing values
                df_out[col] = df_out[col].fillna(self.imputers[col])

        return df_out

    def _encode_categorical_features(self, df: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """
        Encode categorical features.

        Args:
            df: DataFrame to process
            fit: Whether to fit the encoders on this data

        Returns:
            DataFrame with encoded categorical features
        """
        # Make a copy to avoid modifying the original DataFrame
        df_out = df.copy()

        # One-hot encode categorical features
        for col in self.categorical_features:
            if col not in df_out.columns:
                continue

            if fit:
                # Get unique values (excluding NaN)
                unique_values = df_out[col].dropna().unique()
                self.encoders[col] = {val: i for i, val in enumerate(unique_values)}

            if col in self.encoders:
                # Apply label encoding
                encoder = self.encoders[col]

                # Handle values not seen during fitting
                df_out[col] = df_out[col].apply(lambda x: encoder.get(x, -1) if pd.notna(x) else -1)

        return df_out

    def _scale_numerical_features(self, df: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """
        Scale numerical features.

        Args:
            df: DataFrame to process
            fit: Whether to fit the scalers on this data

        Returns:
            DataFrame with scaled numerical features
        """
        # Make a copy to avoid modifying the original DataFrame
        df_out = df.copy()

        # StandardScaler for numerical features
        for col in self.numerical_features:
            if col not in df_out.columns:
                continue

            if fit:
                # Calculate mean and std
                mean = df_out[col].mean()
                std = df_out[col].std()
                if std == 0:
                    std = 1.0

                self.scalers[col] = (mean, std)

            if col in self.scalers:
                # Apply scaling
                mean, std = self.scalers[col]
                df_out[col] = (df_out[col] - mean) / std

        return df_out

    def save(self, path: Union[str, Path]):
        """
        Save the preprocessor to disk.

        Args:
            path: Path to save the preprocessor
        """
        # Create state dictionary
        state = {
            'encoders': self.encoders,
            'scalers': self.scalers,
            'imputers': self.imputers,
            'numerical_features': self.numerical_features,
            'categorical_features': self.categorical_features,
            'all_features': self.all_features,
            'is_fitted': self.is_fitted
        }

        # Save to disk
        joblib.dump(state, path)
        logger.info(f"Preprocessor saved to {path}")

    @classmethod
    def load(cls, path: Union[str, Path]) -> "Preprocessor":
        """
        Load a preprocessor from disk.

        Args:
            path: Path to the saved preprocessor

        Returns:
            Loaded Preprocessor instance
        """
        # Load state dictionary
        state = joblib.load(path)

        # Create new instance
        preprocessor = cls()

        # Restore state
        preprocessor.encoders = state['encoders']
        preprocessor.scalers = state['scalers']
        preprocessor.imputers = state['imputers']
        preprocessor.numerical_features = state['numerical_features']
        preprocessor.categorical_features = state['categorical_features']
        preprocessor.all_features = state['all_features']
        preprocessor.is_fitted = state['is_fitted']

        logger.info(f"Preprocessor loaded from {path}")
        return preprocessor