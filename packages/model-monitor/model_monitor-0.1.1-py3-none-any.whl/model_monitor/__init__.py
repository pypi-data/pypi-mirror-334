"""
Model Monitor
============

A comprehensive library for automated model monitoring and drift detection.

This package provides tools to detect data drift, model performance degradation,
concept drift, and prediction distribution shifts in machine learning systems.
It includes visualization tools, alerting systems, and integrations with common
ML frameworks.

Main Components:
---------------
- Monitor: The main class for monitoring models and data
- DataDrift: Tools for detecting changes in feature distributions
- ModelDrift: Tools for monitoring model performance over time
- Visualization: Components for visualizing drift metrics
- Alerting: Systems for setting thresholds and sending notifications

Example:
--------
>>> from model_monitor import Monitor
>>> monitor = Monitor()
>>> monitor.set_baseline(baseline_data)
>>> results = monitor.detect_drift(new_data)
>>> monitor.generate_report("drift_report.html")
"""

__version__ = "0.1.1"
__author__ = "Biswanath Roul"

from model_monitor.monitor import Monitor
from model_monitor.data_drift import DataDrift
from model_monitor.model_drift import ModelDrift
from model_monitor.config import Config

__all__ = ["Monitor", "DataDrift", "ModelDrift", "Config"]