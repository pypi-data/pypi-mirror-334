"""
Visualization tools for data and model drift.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from typing import Dict, List, Union, Optional, Tuple, Any
import logging
from pathlib import Path
import json
import datetime

logger = logging.getLogger(__name__)


class DriftVisualizer:
    """
    Class for visualizing data and model drift.

    This class provides methods for creating visualizations of drift detection
    results and model performance metrics.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the drift visualizer.

        Args:
            config: Configuration for visualizations
        """
        self.config = config or {}

        # Set matplotlib style
        self.plot_style = self.config.get("plot_style", "seaborn")
        self.color_palette = self.config.get("color_palette", "viridis")
        self.default_width = self.config.get("default_width", 10)
        self.default_height = self.config.get("default_height", 6)
        self.interactive = self.config.get("interactive", True)
        self.export_format = self.config.get("export_format", "html")

        plt.style.use(self.plot_style)
        sns.set_palette(self.color_palette)

        logger.info("Initialized DriftVisualizer")

    def plot_numerical_distribution(
            self,
            baseline_data: np.ndarray,
            current_data: np.ndarray,
            feature_name: str,
            drift_score: Optional[float] = None,
            drift_detected: Optional[bool] = None
    ) -> go.Figure:
        """
        Plot the distribution of a numerical feature.

        Args:
            baseline_data: Baseline data for the feature
            current_data: Current data for the feature
            feature_name: Name of the feature
            drift_score: Drift score (optional)
            drift_detected: Whether drift was detected (optional)

        Returns:
            Plotly figure
        """
        # Create figure
        fig = go.Figure()

        # Add baseline histogram
        fig.add_trace(go.Histogram(
            x=baseline_data,
            histnorm='probability density',
            name='Baseline',
            opacity=0.7,
            marker_color='blue'
        ))

        # Add current histogram
        fig.add_trace(go.Histogram(
            x=current_data,
            histnorm='probability density',
            name='Current',
            opacity=0.7,
            marker_color='red'
        ))

        # Create title with drift information if provided
        title = f"Distribution of {feature_name}"
        if drift_score is not None:
            title += f" (Drift Score: {drift_score:.3f})"
        if drift_detected is not None:
            title += f" - {'Drift Detected' if drift_detected else 'No Drift'}"

        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title=feature_name,
            yaxis_title="Density",
            barmode='overlay',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Add KDE curves if we have enough data
        if len(baseline_data) > 10 and len(current_data) > 10:
            # Calculate KDE for baseline data
            try:
                baseline_kde = sns.kdeplot(baseline_data).get_lines()[0].get_data()
                fig.add_trace(go.Scatter(
                    x=baseline_kde[0],
                    y=baseline_kde[1],
                    mode='lines',
                    name='Baseline KDE',
                    line=dict(color='blue', width=2)
                ))
            except Exception as e:
                logger.warning(f"Error calculating baseline KDE for {feature_name}: {e}")

            # Calculate KDE for current data
            try:
                current_kde = sns.kdeplot(current_data).get_lines()[0].get_data()
                fig.add_trace(go.Scatter(
                    x=current_kde[0],
                    y=current_kde[1],
                    mode='lines',
                    name='Current KDE',
                    line=dict(color='red', width=2)
                ))
            except Exception as e:
                logger.warning(f"Error calculating current KDE for {feature_name}: {e}")

            # Clear the matplotlib figure
            plt.clf()

        return fig

    def plot_categorical_distribution(
            self,
            baseline_data: np.ndarray,
            current_data: np.ndarray,
            feature_name: str,
            drift_score: Optional[float] = None,
            drift_detected: Optional[bool] = None,
            top_n: int = 10
    ) -> go.Figure:
        """
        Plot the distribution of a categorical feature.

        Args:
            baseline_data: Baseline data for the feature
            current_data: Current data for the feature
            feature_name: Name of the feature
            drift_score: Drift score (optional)
            drift_detected: Whether drift was detected (optional)
            top_n: Number of top categories to display

        Returns:
            Plotly figure
        """
        # Count category frequencies
        baseline_counts = pd.Series(baseline_data).value_counts(normalize=True)
        current_counts = pd.Series(current_data).value_counts(normalize=True)

        # Get all categories
        all_categories = set(baseline_counts.index).union(set(current_counts.index))

        # Limit to top N categories if there are too many
        if len(all_categories) > top_n:
            # Combine top categories from both distributions
            top_baseline = set(baseline_counts.nlargest(top_n // 2).index)
            top_current = set(current_counts.nlargest(top_n // 2).index)
            top_categories = list(top_baseline.union(top_current))

            # Ensure we don't exceed top_n
            if len(top_categories) > top_n:
                top_categories = top_categories[:top_n]

            # Create "Other" category for remaining
            baseline_other = 1 - sum(baseline_counts.get(cat, 0) for cat in top_categories)
            current_other = 1 - sum(current_counts.get(cat, 0) for cat in top_categories)

            # Include "Other" if significant
            if baseline_other > 0.01 or current_other > 0.01:
                top_categories.append("Other")
                baseline_counts["Other"] = baseline_other
                current_counts["Other"] = current_other

            categories = top_categories
        else:
            categories = list(all_categories)

        # Create figure
        fig = go.Figure()

        # Add bar for baseline data
        fig.add_trace(go.Bar(
            x=categories,
            y=[baseline_counts.get(cat, 0) for cat in categories],
            name='Baseline',
            marker_color='blue',
            opacity=0.7
        ))

        # Add bar for current data
        fig.add_trace(go.Bar(
            x=categories,
            y=[current_counts.get(cat, 0) for cat in categories],
            name='Current',
            marker_color='red',
            opacity=0.7
        ))

        # Create title with drift information if provided
        title = f"Distribution of {feature_name}"
        if drift_score is not None:
            title += f" (Drift Score: {drift_score:.3f})"
        if drift_detected is not None:
            title += f" - {'Drift Detected' if drift_detected else 'No Drift'}"

        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title=feature_name,
            yaxis_title="Frequency",
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig

    def plot_drift_scores(
            self,
            drift_results: Dict[str, Any],
            top_n: int = 10
    ) -> go.Figure:
        """
        Plot drift scores for all features.

        Args:
            drift_results: Results from data drift detection
            top_n: Number of top drifting features to highlight

        Returns:
            Plotly figure
        """
        # Extract drift scores
        drift_scores = drift_results.get("drift_scores", {})

        if not drift_scores:
            # Create an empty figure with a message
            fig = go.Figure()
            fig.add_annotation(
                text="No drift scores available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=20)
            )
            return fig

        # Sort features by drift score
        sorted_features = sorted(drift_scores.items(), key=lambda x: x[1], reverse=True)

        # Extract feature names and scores
        feature_names = [f[0] for f in sorted_features]
        scores = [f[1] for f in sorted_features]

        # Create drift threshold line
        threshold = 0.1  # Example threshold

        # Determine colors based on drift detection
        drift_detected = drift_results.get("drift_detected", {})
        colors = ['red' if drift_detected.get(feat, False) else 'blue'
                  for feat in feature_names]

        # Create figure
        fig = go.Figure()

        # Add bar chart
        fig.add_trace(go.Bar(
            x=feature_names,
            y=scores,
            marker_color=colors,
            name='Drift Score'
        ))

        # Add threshold line
        fig.add_shape(
            type="line",
            x0=-0.5,
            x1=len(feature_names) - 0.5,
            y0=threshold,
            y1=threshold,
            line=dict(
                color="red",
                width=2,
                dash="dash",
            )
        )

        # Add annotation for threshold
        fig.add_annotation(
            x=len(feature_names) - 1,
            y=threshold,
            text="Threshold",
            showarrow=False,
            yshift=10,
            font=dict(color="red")
        )

        # Update layout
        fig.update_layout(
            title="Feature Drift Scores",
            xaxis_title="Feature",
            yaxis_title="Drift Score",
            xaxis_tickangle=-45,
            yaxis=dict(range=[0, max(scores) * 1.1])
        )

        return fig

    def plot_performance_metrics(
            self,
            model_drift_results: Dict[str, Any],
            history: Optional[List[Dict[str, Any]]] = None
    ) -> go.Figure:
        """
        Plot model performance metrics.

        Args:
            model_drift_results: Results from model drift detection
            history: Historical performance data (optional)

        Returns:
            Plotly figure
        """
        # Check if we have model drift results
        if not model_drift_results:
            # Create an empty figure with a message
            fig = go.Figure()
            fig.add_annotation(
                text="No model performance data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=20)
            )
            return fig

        # Extract performance metrics
        baseline_perf = model_drift_results.get("baseline_performance", {})
        current_perf = model_drift_results.get("current_performance", {})

        if not baseline_perf or not current_perf:
            # Create an empty figure with a message
            fig = go.Figure()
            fig.add_annotation(
                text="Incomplete performance data",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=20)
            )
            return fig

        # Get common metrics
        metrics = [m for m in baseline_perf.keys() if m in current_perf and m != "confusion_matrix"]

        if history and len(history) > 1:
            # Create a time series plot
            fig = make_subplots(rows=len(metrics), cols=1,
                                subplot_titles=[m.upper() for m in metrics],
                                shared_xaxes=True,
                                vertical_spacing=0.05)

            # Extract timestamps and values
            timestamps = []
            metric_values = {metric: [] for metric in metrics}

            for entry in history:
                if "timestamp" in entry and "metrics" in entry:
                    timestamps.append(entry["timestamp"])
                    for metric in metrics:
                        if metric in entry["metrics"]:
                            metric_values[metric].append(entry["metrics"][metric])
                        else:
                            metric_values[metric].append(None)

            # Add traces for each metric
            for i, metric in enumerate(metrics):
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=metric_values[metric],
                        mode='lines+markers',
                        name=metric.upper(),
                        line=dict(width=2)
                    ),
                    row=i + 1, col=1
                )

                # Add baseline reference line
                if metric in baseline_perf:
                    fig.add_shape(
                        type="line",
                        x0=timestamps[0],
                        x1=timestamps[-1],
                        y0=baseline_perf[metric],
                        y1=baseline_perf[metric],
                        line=dict(color="green", width=1, dash="dash"),
                        row=i + 1, col=1
                    )

                    fig.add_annotation(
                        x=timestamps[0],
                        y=baseline_perf[metric],
                        text="Baseline",
                        showarrow=False,
                        xshift=-40,
                        font=dict(color="green", size=10),
                        row=i + 1, col=1
                    )

            # Update layout
            fig.update_layout(
                title="Model Performance Metrics Over Time",
                height=250 * len(metrics),
                showlegend=False,
                margin=dict(t=50, b=20, l=50, r=20)
            )
        else:
            # Create a comparison bar chart
            fig = go.Figure()

            # Add baseline metrics
            fig.add_trace(go.Bar(
                x=metrics,
                y=[baseline_perf.get(m, 0) for m in metrics],
                name='Baseline',
                marker_color='green'
            ))

            # Add current metrics
            fig.add_trace(go.Bar(
                x=metrics,
                y=[current_perf.get(m, 0) for m in metrics],
                name='Current',
                marker_color='blue'
            ))

            # Update layout
            fig.update_layout(
                title="Model Performance Metrics",
                xaxis_title="Metric",
                yaxis_title="Value",
                barmode='group',
                yaxis=dict(range=[0, 1.1]),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

        return fig

    def plot_confusion_matrix(
            self,
            baseline_cm: np.ndarray,
            current_cm: np.ndarray
    ) -> Tuple[go.Figure, go.Figure]:
        """
        Plot confusion matrices for baseline and current data.

        Args:
            baseline_cm: Baseline confusion matrix
            current_cm: Current confusion matrix

        Returns:
            Tuple of (baseline_figure, current_figure)
        """
        # Create baseline confusion matrix figure
        baseline_fig = px.imshow(
            baseline_cm,
            labels=dict(x="Predicted", y="Actual", color="Count"),
            x=['Class ' + str(i) for i in range(len(baseline_cm))],
            y=['Class ' + str(i) for i in range(len(baseline_cm))],
            title="Baseline Confusion Matrix",
            color_continuous_scale="Blues"
        )

        # Add text annotations
        for i in range(len(baseline_cm)):
            for j in range(len(baseline_cm)):
                baseline_fig.add_annotation(
                    x=j, y=i,
                    text=str(baseline_cm[i, j]),
                    showarrow=False,
                    font=dict(color="white" if baseline_cm[i, j] > np.max(baseline_cm) / 2 else "black")
                )

        # Create current confusion matrix figure
        current_fig = px.imshow(
            current_cm,
            labels=dict(x="Predicted", y="Actual", color="Count"),
            x=['Class ' + str(i) for i in range(len(current_cm))],
            y=['Class ' + str(i) for i in range(len(current_cm))],
            title="Current Confusion Matrix",
            color_continuous_scale="Reds"
        )

        # Add text annotations
        for i in range(len(current_cm)):
            for j in range(len(current_cm)):
                current_fig.add_annotation(
                    x=j, y=i,
                    text=str(current_cm[i, j]),
                    showarrow=False,
                    font=dict(color="white" if current_cm[i, j] > np.max(current_cm) / 2 else "black")
                )

        return baseline_fig, current_fig

    def plot_prediction_distribution(
            self,
            prediction_distribution: Dict[str, Any]
    ) -> go.Figure:
        """
        Plot the distribution of model predictions.

        Args:
            prediction_distribution: Prediction distribution analysis results

        Returns:
            Plotly figure
        """
        # Check if we have prediction distribution data
        if not prediction_distribution:
            # Create an empty figure with a message
            fig = go.Figure()
            fig.add_annotation(
                text="No prediction distribution data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=20)
            )
            return fig

        # Check if we have label distribution
        if "label_distribution" in prediction_distribution:
            label_dist = prediction_distribution["label_distribution"]

            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=list(label_dist.keys()),
                values=list(label_dist.values()),
                hole=.3,
                textinfo='label+percent'
            )])

            # Update layout
            fig.update_layout(
                title="Prediction Class Distribution",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.1,
                    xanchor="center",
                    x=0.5
                )
            )

            return fig
        elif "probability_distribution" in prediction_distribution:
            # For probability distributions
            prob_dist = prediction_distribution["probability_distribution"]

            if isinstance(prob_dist, dict) and len(prob_dist) > 0:
                # Create subplots for each class
                fig = make_subplots(
                    rows=len(prob_dist), cols=1,
                    subplot_titles=[f"Class {cls}" for cls in prob_dist.keys()],
                    vertical_spacing=0.05
                )

                for i, (cls, dist) in enumerate(prob_dist.items()):
                    if "bin_edges" in dist and "counts" in dist:
                        # Get bin centers
                        bin_edges = dist["bin_edges"]
                        bin_centers = [(bin_edges[j] + bin_edges[j + 1]) / 2 for j in range(len(bin_edges) - 1)]

                        # Add histogram
                        fig.add_trace(
                            go.Bar(
                                x=bin_centers,
                                y=dist["counts"],
                                name=cls
                            ),
                            row=i + 1, col=1
                        )

                # Update layout
                fig.update_layout(
                    title="Prediction Probability Distributions",
                    height=300 * len(prob_dist),
                    showlegend=False
                )

                return fig

        # Fallback to empty figure
        fig = go.Figure()
        fig.add_annotation(
            text="No usable prediction distribution data",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20)
        )
        return fig

    def create_drift_dashboard(
            self,
            drift_results: Dict[str, Any],
            baseline_data: pd.DataFrame,
            current_data: Optional[pd.DataFrame] = None,
            monitoring_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a comprehensive dashboard of drift visualizations.

        Args:
            drift_results: Results from drift detection
            baseline_data: Baseline data
            current_data: Current data (optional)
            monitoring_history: Historical monitoring data (optional)

        Returns:
            Dictionary of Plotly figures
        """
        figures = {}

        # Overview figure - drift scores for all features
        figures["drift_scores"] = self.plot_drift_scores(drift_results)

        # Feature distribution figures
        if "feature_drift" in drift_results and "comparison" in drift_results and current_data is not None:
            # Find drifting features
            drifting_features = [
                feature for feature, is_drift in drift_results.get("drift_detected", {}).items()
                if is_drift and feature in current_data.columns
            ]

            # Find features with highest drift scores
            drift_scores = drift_results.get("drift_scores", {})
            top_features = sorted(
                drift_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            top_feature_names = [f[0] for f in top_features]

            # Combine drifting and top features
            features_to_plot = list(set(drifting_features + top_feature_names))

            # Create distribution plots
            feature_figures = {}

            for feature in features_to_plot:
                if feature not in baseline_data.columns or feature not in current_data.columns:
                    continue

                baseline_values = baseline_data[feature].values
                current_values = current_data[feature].values

                drift_score = drift_scores.get(feature, None)
                drift_detected = drift_results.get("drift_detected", {}).get(feature, None)

                # Determine if feature is categorical or numerical
                is_categorical = (
                        feature in drift_results.get("categorical_features", []) or
                        baseline_data[feature].dtype == 'object' or
                        baseline_data[feature].dtype == 'category' or
                        len(np.unique(baseline_values)) < 10
                )

                if is_categorical:
                    fig = self.plot_categorical_distribution(
                        baseline_values,
                        current_values,
                        feature,
                        drift_score=drift_score,
                        drift_detected=drift_detected
                    )
                else:
                    fig = self.plot_numerical_distribution(
                        baseline_values,
                        current_values,
                        feature,
                        drift_score=drift_score,
                        drift_detected=drift_detected
                    )

                feature_figures[feature] = fig

            figures["feature_distributions"] = feature_figures

        # Model performance figures
        if "model_drift" in drift_results:
            model_drift = drift_results["model_drift"]

            # Performance metrics
            figures["performance_metrics"] = self.plot_performance_metrics(
                model_drift,
                history=monitoring_history
            )

            # Confusion matrix
            if ("baseline_performance" in model_drift and
                    "current_performance" in model_drift and
                    "confusion_matrix" in model_drift["baseline_performance"] and
                    "confusion_matrix" in model_drift["current_performance"]):
                baseline_cm = np.array(model_drift["baseline_performance"]["confusion_matrix"])
                current_cm = np.array(model_drift["current_performance"]["confusion_matrix"])

                baseline_cm_fig, current_cm_fig = self.plot_confusion_matrix(baseline_cm, current_cm)
                figures["confusion_matrices"] = {
                    "baseline": baseline_cm_fig,
                    "current": current_cm_fig
                }

            # Prediction distribution
            if "prediction_distribution" in model_drift:
                figures["prediction_distribution"] = self.plot_prediction_distribution(
                    model_drift["prediction_distribution"]
                )

        return figures

    def export_report(
            self,
            figures: Dict[str, Any],
            drift_results: Dict[str, Any],
            baseline_metadata: Dict[str, Any],
            model_metadata: Dict[str, Any],
            output_path: Union[str, Path]
    ) -> str:
        """
        Export a drift detection report.

        Args:
            figures: Dictionary of Plotly figures
            drift_results: Results from drift detection
            baseline_metadata: Metadata about the baseline data
            model_metadata: Metadata about the model
            output_path: Path to save the report

        Returns:
            Path to the saved report
        """
        output_path = str(output_path)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Create HTML report
        if output_path.endswith('.html'):
            import plotly.io as pio

            # Start HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Model Monitor - Drift Report</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                    .section {{ margin-bottom: 30px; }}
                    .subsection {{ margin-bottom: 20px; }}
                    .plot-container {{ margin-bottom: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                    .drift-detected {{ color: red; font-weight: bold; }}
                    .no-drift {{ color: green; }}
                    .summary-box {{ padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                    .summary-box.drift {{ background-color: #ffebee; border: 1px solid #ef9a9a; }}
                    .summary-box.no-drift {{ background-color: #e8f5e9; border: 1px solid #a5d6a7; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Model Monitoring Report</h1>
                    <p>Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            """

            # Summary section
            data_drift_detected = drift_results.get("any_drift_detected", False)
            model_drift_detected = drift_results.get("model_drift", {}).get("performance_drift_detected", False)
            overall_drift = data_drift_detected or model_drift_detected

            drift_class = "drift" if overall_drift else "no-drift"
            summary_text = "Drift Detected" if overall_drift else "No Significant Drift Detected"

            html_content += f"""
                <div class="section">
                    <h2>Summary</h2>
                    <div class="summary-box {drift_class}">
                        <h3>{summary_text}</h3>
                        <ul>
                            <li>Data Drift: <span class="{'drift-detected' if data_drift_detected else 'no-drift'}">{data_drift_detected}</span></li>
                            <li>Model Performance Drift: <span class="{'drift-detected' if model_drift_detected else 'no-drift'}">{model_drift_detected}</span></li>
                            <li>Overall Drift Score: {drift_results.get("overall_drift_score", 0):.4f}</li>
                        </ul>
                    </div>
                </div>
            """

            # Metadata section
            html_content += f"""
                <div class="section">
                    <h2>Metadata</h2>
                    <div class="subsection">
                        <h3>Baseline Data</h3>
                        <table>
                            <tr><th>Property</th><th>Value</th></tr>
                            <tr><td>Timestamp</td><td>{baseline_metadata.get('timestamp', 'N/A')}</td></tr>
                            <tr><td>Number of Samples</td><td>{baseline_metadata.get('n_samples', 'N/A')}</td></tr>
                            <tr><td>Number of Features</td><td>{baseline_metadata.get('n_features', 'N/A')}</td></tr>
                        </table>
                    </div>
            """

            if model_metadata:
                html_content += f"""
                    <div class="subsection">
                        <h3>Model</h3>
                        <table>
                            <tr><th>Property</th><th>Value</th></tr>
                            <tr><td>Name</td><td>{model_metadata.get('name', 'N/A')}</td></tr>
                            <tr><td>Version</td><td>{model_metadata.get('version', 'N/A')}</td></tr>
                            <tr><td>Timestamp</td><td>{model_metadata.get('timestamp', 'N/A')}</td></tr>
                        </table>
                    </div>
                """

            html_content += """
                </div>
            """

            # Overall drift scores plot
            if "drift_scores" in figures:
                fig_html = pio.to_html(figures["drift_scores"], include_plotlyjs=False)
                html_content += f"""
                    <div class="section">
                        <h2>Feature Drift Scores</h2>
                        <div class="plot-container">
                            {fig_html}
                        </div>
                    </div>
                """

            # Feature distribution plots
            if "feature_distributions" in figures:
                html_content += f"""
                    <div class="section">
                        <h2>Feature Distributions</h2>
                """

                for feature, fig in figures["feature_distributions"].items():
                    fig_html = pio.to_html(fig, include_plotlyjs=False)
                    html_content += f"""
                        <div class="subsection">
                            <div class="plot-container">
                                {fig_html}
                            </div>
                        </div>
                    """

                html_content += """
                    </div>
                """

            # Model performance section
            if "performance_metrics" in figures:
                html_content += f"""
                    <div class="section">
                        <h2>Model Performance</h2>
                        <div class="plot-container">
                            {pio.to_html(figures["performance_metrics"], include_plotlyjs=False)}
                        </div>
                    </div>
                """

            # Confusion matrices
            if "confusion_matrices" in figures:
                html_content += f"""
                    <div class="section">
                        <h2>Confusion Matrices</h2>
                        <div class="subsection">
                            <div class="plot-container">
                                {pio.to_html(figures["confusion_matrices"]["baseline"], include_plotlyjs=False)}
                            </div>
                            <div class="plot-container">
                                {pio.to_html(figures["confusion_matrices"]["current"], include_plotlyjs=False)}
                            </div>
                        </div>
                    </div>
                """

            # Prediction distribution
            if "prediction_distribution" in figures:
                html_content += f"""
                    <div class="section">
                        <h2>Prediction Distribution</h2>
                        <div class="plot-container">
                            {pio.to_html(figures["prediction_distribution"], include_plotlyjs=False)}
                        </div>
                    </div>
                """

            # Close HTML
            html_content += """
            </body>
            </html>
            """

            # Write to file
            with open(output_path, 'w') as f:
                f.write(html_content)

            return output_path

        # JSON report
        elif output_path.endswith('.json'):
            # Convert figures to JSON
            figures_json = {}

            for key, fig in figures.items():
                if isinstance(fig, dict):
                    figures_json[key] = {k: fig[k].to_json() for k in fig}
                else:
                    figures_json[key] = fig.to_json()

            # Create report data
            report_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "drift_results": drift_results,
                "baseline_metadata": baseline_metadata,
                "model_metadata": model_metadata,
                "figures": figures_json
            }

            # Write to file
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2)

            return output_path

        else:
            raise ValueError(f"Unsupported report format: {output_path}")