"""
The main Monitor class that provides a unified interface for model monitoring.
"""

import logging
import os
import datetime
from typing import Dict, List, Optional, Union, Any, Callable, Tuple
import pandas as pd
import numpy as np
from pathlib import Path
import json
import joblib
from tqdm import tqdm

from model_monitor.config import Config
from model_monitor.data_drift import DataDrift
from model_monitor.model_drift import ModelDrift
from model_monitor.visualization.drift_plots import DriftVisualizer
from model_monitor.alerting.notification import AlertManager
from model_monitor.utils.data_loader import DataLoader
from model_monitor.utils.preprocessing import Preprocessor

logger = logging.getLogger(__name__)


class Monitor:
    """
    Main class for monitoring machine learning models and data.

    This class provides a unified interface for detecting data drift,
    model performance degradation, and prediction distribution changes.
    It also includes visualization tools and alerting systems.

    Attributes:
        config (Config): Configuration object for the monitor
        data_drift (DataDrift): Component for detecting data drift
        model_drift (ModelDrift): Component for detecting model drift
        visualizer (DriftVisualizer): Component for visualizing drift
        alert_manager (AlertManager): Component for managing alerts
    """

    def __init__(self, config: Optional[Union[Config, Dict, str, Path]] = None):
        """
        Initialize the monitor with a configuration.

        Args:
            config: Configuration for the monitor. Can be a Config object,
                   a dictionary of configuration values, or a path to a YAML file.
                   If None, the default configuration is used.
        """
        if config is None:
            self.config = Config.default()
        elif isinstance(config, Config):
            self.config = config
        elif isinstance(config, dict):
            self.config = Config().update(config)
        elif isinstance(config, (str, Path)):
            self.config = Config.from_yaml(config)
        else:
            raise TypeError("config must be None, Config, dict, str, or Path")

        # Initialize components
        self.data_drift = DataDrift(self.config.data_drift)
        self.model_drift = ModelDrift(self.config.model_drift)
        self.visualizer = DriftVisualizer(self.config.visualization)
        self.alert_manager = AlertManager(self.config.alerting)
        self.data_loader = DataLoader()
        self.preprocessor = Preprocessor()

        # State variables
        self.baseline_data = None
        self.baseline_metadata = {}
        self.baseline_timestamp = None
        self.model = None
        self.model_metadata = {}
        self.monitoring_history = []
        self.features = None
        self.target = None

        # Create monitoring directory if it doesn't exist
        os.makedirs(self.config.storage.local_dir, exist_ok=True)

        logger.info(f"Initialized Monitor with configuration: {self.config.name}")

    def set_baseline(self,
                     data: Union[pd.DataFrame, str, Path],
                     target: Optional[str] = None,
                     features: Optional[List[str]] = None,
                     timestamp_column: Optional[str] = None,
                     categorical_features: Optional[List[str]] = None,
                     numerical_features: Optional[List[str]] = None,
                     metadata: Optional[Dict] = None,
                     preprocess: bool = True):
        """
        Set the baseline data for drift detection.

        Args:
            data: DataFrame or path to a CSV file containing the baseline data
            target: Name of the target column (if applicable)
            features: List of feature columns to use (if None, all columns except target)
            timestamp_column: Name of the timestamp column (if any)
            categorical_features: List of categorical features (if None, auto-detected)
            numerical_features: List of numerical features (if None, auto-detected)
            metadata: Additional metadata about the baseline data
            preprocess: Whether to preprocess the data (normalization, encoding, etc.)
        """
        if isinstance(data, (str, Path)):
            data = self.data_loader.load(data)

        # Validate the data
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame or a path to a data file")

        # Store features and target information
        self.target = target

        if features is None:
            if target is not None:
                self.features = [col for col in data.columns if col != target]
            else:
                self.features = list(data.columns)
        else:
            self.features = features

        # Preprocess the data if needed
        if preprocess:
            data = self.preprocessor.preprocess(
                data,
                categorical_features=categorical_features,
                numerical_features=numerical_features,
                fit=True
            )

        # Store the baseline data
        self.baseline_data = data
        self.baseline_timestamp = datetime.datetime.now()

        # Add metadata
        self.baseline_metadata = {
            "timestamp": self.baseline_timestamp.isoformat(),
            "n_samples": len(data),
            "n_features": len(self.features),
            "features": self.features,
            "target": target,
            "timestamp_column": timestamp_column,
            "categorical_features": categorical_features or self.preprocessor.categorical_features,
            "numerical_features": numerical_features or self.preprocessor.numerical_features,
        }

        if metadata:
            self.baseline_metadata.update(metadata)

        # Initialize drift detectors with baseline data
        self.data_drift.set_baseline(
            data[self.features] if self.features else data,
            categorical_features=categorical_features or self.preprocessor.categorical_features,
            numerical_features=numerical_features or self.preprocessor.numerical_features
        )

        # Save baseline metadata
        self._save_baseline_metadata()

        logger.info(f"Baseline set with {len(data)} samples and {len(self.features)} features")
        return self

    def set_model(self,
                  model: Any,
                  model_name: str,
                  model_version: str = "1.0.0",
                  metadata: Optional[Dict] = None):
        """
        Set the model to be monitored.

        Args:
            model: The trained model object
            model_name: Name of the model
            model_version: Version of the model
            metadata: Additional metadata about the model
        """
        self.model = model
        self.model_metadata = {
            "name": model_name,
            "version": model_version,
            "timestamp": datetime.datetime.now().isoformat(),
        }

        if metadata:
            self.model_metadata.update(metadata)

        # Initialize model drift detector with the model
        self.model_drift.set_model(model, self.model_metadata)

        # Save model metadata
        self._save_model_metadata()

        logger.info(f"Model set: {model_name} (version: {model_version})")
        return self

    def detect_drift(self,
                     data: Union[pd.DataFrame, str, Path],
                     target_actual: Optional[pd.Series] = None,
                     timestamp: Optional[Union[str, datetime.datetime]] = None,
                     preprocess: bool = True,
                     compute_all: bool = True) -> Dict:
        """
        Detect drift in new data compared to the baseline.

        Args:
            data: DataFrame or path to a CSV file containing the new data
            target_actual: Actual target values (for model performance evaluation)
            timestamp: Timestamp for the data (if None, current time is used)
            preprocess: Whether to preprocess the data
            compute_all: Whether to compute all drift metrics or only basic ones

        Returns:
            Dictionary containing drift detection results
        """
        if self.baseline_data is None:
            raise ValueError("Baseline data not set. Call set_baseline() first.")

        if isinstance(data, (str, Path)):
            data = self.data_loader.load(data)

        # Validate the data
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame or a path to a data file")

        # Preprocess the data if needed
        if preprocess:
            data = self.preprocessor.preprocess(data, fit=False)

        # Use only the features that were in the baseline
        if self.features:
            missing_features = set(self.features) - set(data.columns)
            if missing_features:
                raise ValueError(f"Missing features in new data: {missing_features}")
            data_features = data[self.features]
        else:
            data_features = data

        # Set timestamp
        if timestamp is None:
            timestamp = datetime.datetime.now()
        elif isinstance(timestamp, str):
            timestamp = datetime.datetime.fromisoformat(timestamp)

        # Compute data drift
        data_drift_results = self.data_drift.detect(data_features, compute_all=compute_all)

        # Compute model drift if model and actual targets are provided
        model_drift_results = {}
        if self.model is not None and target_actual is not None:
            # Get model predictions
            predictions = self.model.predict(data_features)
            probabilities = None
            if hasattr(self.model, "predict_proba"):
                try:
                    probabilities = self.model.predict_proba(data_features)
                except:
                    logger.warning("Model has predict_proba method but it failed")

            # Compute model drift
            model_drift_results = self.model_drift.detect(
                data_features,
                predictions,
                target_actual,
                probabilities=probabilities,
                compute_all=compute_all
            )

        # Compile results
        results = {
            "timestamp": timestamp.isoformat(),
            "n_samples": len(data),
            "data_drift": data_drift_results,
            "model_drift": model_drift_results,
            "summary": {
                "data_drift_detected": any(data_drift_results.get("drift_detected", {}).values()),
                "model_drift_detected": model_drift_results.get("performance_drift_detected", False),
                "overall_drift_score": data_drift_results.get("overall_drift_score", 0),
            }
        }

        # Add to monitoring history
        self.monitoring_history.append(results)

        # Check if we need to alert
        if self.config.alerting.enabled:
            self._check_alerts(results)

        logger.info(f"Drift detection completed at {timestamp.isoformat()}")
        return results

    def generate_report(self,
                        output_path: Union[str, Path],
                        results: Optional[Dict] = None,
                        include_history: bool = False) -> str:
        """
        Generate a comprehensive drift report.

        Args:
            output_path: Path to save the report
            results: Drift detection results (if None, uses the latest results)
            include_history: Whether to include historical drift data

        Returns:
            Path to the generated report
        """
        if not results and not self.monitoring_history:
            raise ValueError("No drift detection results available")

        if not results:
            results = self.monitoring_history[-1]

        # Generate visualizations
        figs = self.visualizer.create_drift_dashboard(
            results,
            self.baseline_data,
            monitoring_history=self.monitoring_history if include_history else None
        )

        # Export the report
        report_path = self.visualizer.export_report(
            figs,
            results,
            self.baseline_metadata,
            self.model_metadata,
            output_path
        )

        logger.info(f"Report generated at {report_path}")
        return report_path

    def schedule(self,
                 data_source: str,
                 frequency: str = "daily",
                 alert_threshold: Optional[float] = None,
                 notification_email: Optional[Union[str, List[str]]] = None) -> Dict:
        """
        Schedule automated monitoring.

        Note: This creates the configuration for scheduled monitoring but actual
        scheduling depends on the execution environment. In a production setting,
        this would be integrated with a task scheduler (e.g., Airflow, cron).

        Args:
            data_source: URI for the data source (e.g., file path, database URI)
            frequency: Monitoring frequency ('hourly', 'daily', 'weekly')
            alert_threshold: Override the default drift threshold for alerts
            notification_email: Email address(es) for alert notifications

        Returns:
            Dictionary with the scheduling configuration
        """
        if alert_threshold is not None:
            self.config.alerting.drift_threshold = alert_threshold

        if notification_email is not None:
            if isinstance(notification_email, str):
                self.config.alerting.email_recipients = [notification_email]
            else:
                self.config.alerting.email_recipients = notification_email

        # Enable alerting if not already enabled
        self.config.alerting.enabled = True

        # Create scheduling configuration
        schedule_config = {
            "data_source": data_source,
            "frequency": frequency,
            "last_updated": datetime.datetime.now().isoformat(),
            "alert_threshold": self.config.alerting.drift_threshold,
            "notification_email": self.config.alerting.email_recipients,
        }

        # Save the configuration
        schedule_path = os.path.join(self.config.storage.local_dir, "schedule_config.json")
        with open(schedule_path, 'w') as f:
            json.dump(schedule_config, f, indent=2)

        logger.info(f"Scheduled monitoring configured with frequency: {frequency}")
        return schedule_config

    def _save_baseline_metadata(self):
        """Save baseline metadata to disk."""
        metadata_path = os.path.join(self.config.storage.local_dir, "baseline_metadata.json")
        with open(metadata_path, 'w') as f:
            # Convert any non-serializable objects to strings
            metadata = {k: str(v) if not isinstance(v, (str, int, float, bool, list, dict, type(None)))
            else v for k, v in self.baseline_metadata.items()}
            json.dump(metadata, f, indent=2)

    def _save_model_metadata(self):
        """Save model metadata to disk."""
        metadata_path = os.path.join(self.config.storage.local_dir, "model_metadata.json")
        with open(metadata_path, 'w') as f:
            # Convert any non-serializable objects to strings
            metadata = {k: str(v) if not isinstance(v, (str, int, float, bool, list, dict, type(None)))
            else v for k, v in self.model_metadata.items()}
            json.dump(metadata, f, indent=2)

    def _check_alerts(self, results: Dict):
        """Check if alerts should be triggered based on drift results."""
        # Check data drift
        if results["summary"]["data_drift_detected"] and \
                results["summary"]["overall_drift_score"] > self.config.alerting.drift_threshold:
            self.alert_manager.send_data_drift_alert(
                drift_score=results["summary"]["overall_drift_score"],
                drift_details=results["data_drift"],
                timestamp=results["timestamp"]
            )

        # Check model drift
        if results.get("model_drift", {}).get("performance_drift_detected", False) and \
                results.get("model_drift", {}).get("performance_degradation",
                                                   0) > self.config.alerting.performance_threshold:
            self.alert_manager.send_model_drift_alert(
                performance_degradation=results["model_drift"]["performance_degradation"],
                performance_details=results["model_drift"],
                timestamp=results["timestamp"]
            )

    def save(self, path: Optional[Union[str, Path]] = None):
        """
        Save the monitor state to disk.

        Args:
            path: Directory to save the monitor state (if None, uses the config's local_dir)
        """
        if path is None:
            path = self.config.storage.local_dir

        os.makedirs(path, exist_ok=True)

        # Save the config
        config_path = os.path.join(path, "config.yaml")
        self.config.to_yaml(config_path)

        # Save metadata
        if self.baseline_metadata:
            metadata_path = os.path.join(path, "baseline_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(self.baseline_metadata, f, indent=2)

        if self.model_metadata:
            metadata_path = os.path.join(path, "model_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(self.model_metadata, f, indent=2)

        # Save monitoring history
        if self.monitoring_history:
            history_path = os.path.join(path, "monitoring_history.json")
            with open(history_path, 'w') as f:
                json.dump(self.monitoring_history, f, indent=2)

        # Save preprocessor
        if hasattr(self.preprocessor, 'save'):
            preprocessor_path = os.path.join(path, "preprocessor.joblib")
            self.preprocessor.save(preprocessor_path)

        # Save data drift detector
        if hasattr(self.data_drift, 'save'):
            data_drift_path = os.path.join(path, "data_drift.joblib")
            self.data_drift.save(data_drift_path)

        # Save model drift detector
        if hasattr(self.model_drift, 'save'):
            model_drift_path = os.path.join(path, "model_drift.joblib")
            self.model_drift.save(model_drift_path)

        logger.info(f"Monitor state saved to {path}")
        return path

    @classmethod
    def load(cls, path: Union[str, Path]) -> "Monitor":
        """
        Load a monitor from disk.

        Args:
            path: Directory containing the saved monitor state

        Returns:
            A Monitor instance with the loaded state
        """
        # Load the config
        config_path = os.path.join(path, "config.yaml")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}")

        config = Config.from_yaml(config_path)
        monitor = cls(config)

        # Load metadata
        baseline_metadata_path = os.path.join(path, "baseline_metadata.json")
        if os.path.exists(baseline_metadata_path):
            with open(baseline_metadata_path, 'r') as f:
                monitor.baseline_metadata = json.load(f)

        model_metadata_path = os.path.join(path, "model_metadata.json")
        if os.path.exists(model_metadata_path):
            with open(model_metadata_path, 'r') as f:
                monitor.model_metadata = json.load(f)

        # Load monitoring history
        history_path = os.path.join(path, "monitoring_history.json")
        if os.path.exists(history_path):
            with open(history_path, 'r') as f:
                monitor.monitoring_history = json.load(f)

        # Load preprocessor
        preprocessor_path = os.path.join(path, "preprocessor.joblib")
        if os.path.exists(preprocessor_path):
            monitor.preprocessor = joblib.load(preprocessor_path)

        # Load data drift detector
        data_drift_path = os.path.join(path, "data_drift.joblib")
        if os.path.exists(data_drift_path):
            monitor.data_drift = joblib.load(data_drift_path)

        # Load model drift detector
        model_drift_path = os.path.join(path, "model_drift.joblib")
        if os.path.exists(model_drift_path):
            monitor.model_drift = joblib.load(model_drift_path)

        logger.info(f"Monitor loaded from {path}")
        return monitor