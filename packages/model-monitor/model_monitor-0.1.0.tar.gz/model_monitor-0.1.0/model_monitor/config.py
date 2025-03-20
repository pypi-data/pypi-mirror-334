"""
Configuration module for model monitoring parameters and settings.
"""

from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, validator
import yaml
import os
from pathlib import Path


class AlertConfig(BaseModel):
    """Configuration for alert thresholds and notification settings."""

    enabled: bool = True
    drift_threshold: float = Field(0.05, ge=0, le=1)
    performance_threshold: float = Field(0.1, ge=0, le=1)
    notification_channels: List[str] = ["email"]
    email_recipients: Optional[List[str]] = None
    slack_webhook: Optional[str] = None
    notification_frequency: str = "immediate"  # immediate, daily, weekly

    @validator("notification_frequency")
    def validate_frequency(cls, v):
        allowed = ["immediate", "daily", "weekly"]
        if v not in allowed:
            raise ValueError(f"notification_frequency must be one of {allowed}")
        return v


class VisualizationConfig(BaseModel):
    """Configuration for visualization settings."""

    plot_style: str = "seaborn"
    color_palette: str = "viridis"
    default_width: int = 10
    default_height: int = 6
    interactive: bool = True
    export_format: str = "html"

    @validator("plot_style")
    def validate_style(cls, v):
        allowed = ["seaborn", "ggplot", "classic", "bmh", "dark_background"]
        if v not in allowed:
            raise ValueError(f"plot_style must be one of {allowed}")
        return v


class DataDriftConfig(BaseModel):
    """Configuration for data drift detection."""

    test_types: List[str] = ["ks", "psi", "js_divergence", "wasserstein"]
    categorical_test: str = "chi2"
    sample_size: Optional[int] = None
    ignore_features: List[str] = []
    correlation_threshold: float = Field(0.7, ge=0, le=1)
    pca_components: Optional[int] = None


class ModelDriftConfig(BaseModel):
    """Configuration for model drift detection."""

    metrics: List[str] = ["accuracy", "f1", "precision", "recall", "roc_auc"]
    window_size: int = 30
    min_samples: int = 100
    performance_window_type: str = "rolling"
    reference_window_type: str = "fixed"


class StorageConfig(BaseModel):
    """Configuration for data storage."""

    storage_type: str = "local"
    local_dir: str = "./model_monitor_data"
    s3_bucket: Optional[str] = None
    gcs_bucket: Optional[str] = None
    azure_container: Optional[str] = None
    retention_days: int = 90


class Config(BaseModel):
    """Main configuration class for model monitoring."""

    name: str = "default"
    version: str = "0.1.0"
    data_drift: DataDriftConfig = DataDriftConfig()
    model_drift: ModelDriftConfig = ModelDriftConfig()
    alerting: AlertConfig = AlertConfig()
    visualization: VisualizationConfig = VisualizationConfig()
    storage: StorageConfig = StorageConfig()

    @classmethod
    def from_yaml(cls, yaml_file: Union[str, Path]) -> "Config":
        """Load configuration from a YAML file."""
        with open(yaml_file, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)

    def to_yaml(self, yaml_file: Union[str, Path]) -> None:
        """Save configuration to a YAML file."""
        with open(yaml_file, 'w') as f:
            yaml.dump(self.dict(), f)

    @classmethod
    def default(cls) -> "Config":
        """Return the default configuration."""
        return cls()

    def update(self, config_dict: Dict[str, Any]) -> "Config":
        """Update configuration with values from a dictionary."""
        # Create a copy of the current config as a dictionary
        current_dict = self.dict()

        # Recursively update the dictionary
        def update_dict(d, u):
            for k, v in u.items():
                if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                    d[k] = update_dict(d[k], v)
                else:
                    d[k] = v
            return d

        updated_dict = update_dict(current_dict, config_dict)
        return Config(**updated_dict)