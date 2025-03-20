# Model Monitor

![PyPI](https://img.shields.io/pypi/v/model-monitor)
![Python](https://img.shields.io/pypi/pyversions/model-monitor)
![License](https://img.shields.io/pypi/l/model-monitor)
![Build Status](https://img.shields.io/github/workflow/status/biswanathroul/model-monitor/Python%20package)

A comprehensive Python library for automated model monitoring and drift detection in machine learning systems.

## Features

- **Data Drift Detection**: Identify shifts in feature distributions using statistical tests and distance metrics
- **Model Performance Monitoring**: Track key metrics over time and detect degradation
- **Prediction Drift Analysis**: Monitor changes in model output distributions
- **Customizable Alerting**: Set thresholds and receive notifications when drift is detected
- **Visualization Tools**: Generate comprehensive reports and visualizations of drift metrics
- **Integration Flexibility**: Works with various ML frameworks and data sources
- **Scalable Architecture**: Efficiently handle large datasets and high-throughput models

## Installation

```bash
pip install model-monitor
```

## Quick Start

```python
from model_monitor import Monitor
import pandas as pd

# Initialize monitor with baseline data
baseline_data = pd.read_csv("baseline_data.csv")
production_data = pd.read_csv("production_data.csv") 

monitor = Monitor()
monitor.set_baseline(baseline_data)

# Run drift detection
results = monitor.detect_drift(production_data)

# Generate report
monitor.generate_report("drift_report.html")

# Set up automated monitoring
monitor.schedule(
    data_source="s3://bucket/path/to/data/",
    frequency="daily",
    alert_threshold=0.05,
    notification_email="alerts@example.com"
)
```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

- **Biswanath Roul** - [GitHub](https://github.com/biswanathroul/model-monitor)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.