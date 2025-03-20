"""
Command-line interface for model monitoring.
"""

import argparse
import sys
import os
import logging
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional

from model_monitor import Monitor, Config
from model_monitor.utils import DataLoader


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(
        level=log_level,
        format=log_format
    )


def create_parser():
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description='Model Monitor - A tool for monitoring ML models in production',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new monitoring configuration')
    init_parser.add_argument('--output', '-o', type=str, default='model_monitor_config.yaml',
                             help='Output file for the configuration')
    init_parser.add_argument('--name', '-n', type=str, default='default',
                             help='Name for the monitoring configuration')

    # Set baseline command
    baseline_parser = subparsers.add_parser('set-baseline', help='Set baseline data for drift detection')
    baseline_parser.add_argument('--data', '-d', type=str, required=True,
                                 help='Path to baseline data file')
    baseline_parser.add_argument('--config', '-c', type=str, default='model_monitor_config.yaml',
                                 help='Path to configuration file')
    baseline_parser.add_argument('--target', '-t', type=str,
                                 help='Name of target column')
    baseline_parser.add_argument('--output', '-o', type=str, default='.',
                                 help='Output directory for baseline artifacts')
    baseline_parser.add_argument('--categorical', type=str, nargs='+',
                                 help='List of categorical features')
    baseline_parser.add_argument('--numerical', type=str, nargs='+',
                                 help='List of numerical features')

    # Detect drift command
    detect_parser = subparsers.add_parser('detect-drift', help='Detect drift in new data')
    detect_parser.add_argument('--data', '-d', type=str, required=True,
                               help='Path to current data file')
    detect_parser.add_argument('--baseline', '-b', type=str, required=True,
                               help='Path to baseline directory')
    detect_parser.add_argument('--target-actual', '-t', type=str,
                               help='Path to file with actual target values')
    detect_parser.add_argument('--output', '-o', type=str, default='drift_report.html',
                               help='Output path for drift report')
    detect_parser.add_argument('--all-metrics', '-a', action='store_true',
                               help='Compute all drift metrics (slower)')

    # Generate report command
    report_parser = subparsers.add_parser('generate-report', help='Generate drift report')
    report_parser.add_argument('--results', '-r', type=str, required=True,
                               help='Path to drift detection results file')
    report_parser.add_argument('--baseline', '-b', type=str, required=True,
                               help='Path to baseline directory')
    report_parser.add_argument('--output', '-o', type=str, default='drift_report.html',
                               help='Output path for drift report')
    report_parser.add_argument('--include-history', action='store_true',
                               help='Include historical drift data in the report')

    # Common arguments
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')

    return parser


def command_init(args):
    """Run the init command."""
    # Create default configuration
    config = Config.default()
    config.name = args.name

    # Save configuration
    config.to_yaml(args.output)
    print(f"Configuration saved to: {args.output}")


def command_set_baseline(args):
    """Run the set-baseline command."""
    # Load configuration
    config = Config.from_yaml(args.config)

    # Create monitor
    monitor = Monitor(config)

    # Load data
    data_loader = DataLoader()
    data = data_loader.load(args.data)

    # Set baseline
    monitor.set_baseline(
        data,
        target=args.target,
        categorical_features=args.categorical,
        numerical_features=args.numerical
    )

    # Save monitor
    output_path = args.output
    monitor.save(output_path)

    print(f"Baseline set and saved to: {output_path}")


def command_detect_drift(args):
    """Run the detect-drift command."""
    # Load monitor
    try:
        monitor = Monitor.load(args.baseline)
    except Exception as e:
        print(f"Error loading monitor: {e}")
        return

    # Load data
    data_loader = DataLoader()
    data = data_loader.load(args.data)

    # Load target data if provided
    target_actual = None
    if args.target_actual:
        try:
            target_df = data_loader.load(args.target_actual)
            target_col = monitor.target

            if target_col in target_df.columns:
                target_actual = target_df[target_col]
            else:
                # Assume the first column is the target
                target_actual = target_df.iloc[:, 0]
        except Exception as e:
            print(f"Error loading target values: {e}")

    # Detect drift
    results = monitor.detect_drift(
        data,
        target_actual=target_actual,
        compute_all=args.all_metrics
    )

    # Generate report
    report_path = monitor.generate_report(args.output, results)

    # Print summary
    data_drift = any(results.get("data_drift", {}).get("drift_detected", {}).values())
    model_drift = results.get("model_drift", {}).get("performance_drift_detected", False)

    print("\nDrift Detection Results:")
    print(f"Data Drift: {'Detected' if data_drift else 'Not Detected'}")
    print(f"Model Drift: {'Detected' if model_drift else 'Not Detected'}")
    print(f"Report generated at: {report_path}")


def command_generate_report(args):
    """Run the generate-report command."""
    # Load monitor
    try:
        monitor = Monitor.load(args.baseline)
    except Exception as e:
        print(f"Error loading monitor: {e}")
        return

    # Load drift results
    try:
        with open(args.results, 'r') as f:
            results = json.load(f)
    except Exception as e:
        print(f"Error loading drift results: {e}")
        return

    # Generate report
    report_path = monitor.generate_report(
        args.output,
        results,
        include_history=args.include_history
    )

    print(f"Report generated at: {report_path}")


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Set up logging
    setup_logging(args.verbose)

    # Run command
    if args.command == 'init':
        command_init(args)
    elif args.command == 'set-baseline':
        command_set_baseline(args)
    elif args.command == 'detect-drift':
        command_detect_drift(args)
    elif args.command == 'generate-report':
        command_generate_report(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()