"""
Notification system for model monitoring alerts.
"""

import os
import logging
import datetime
import json
from typing import Dict, List, Union, Optional, Any
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback

from model_monitor.alerting.thresholds import ThresholdManager

logger = logging.getLogger(__name__)


class AlertManager:
    """
    Manager for sending alerts when drift or performance issues are detected.

    This class provides methods for sending notifications through various
    channels like email, Slack, etc.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the alert manager.

        Args:
            config: Configuration for alerting
        """
        self.config = config or {}

        # Alerting settings
        self.enabled = self.config.get("enabled", True)
        self.drift_threshold = self.config.get("drift_threshold", 0.05)
        self.performance_threshold = self.config.get("performance_threshold", 0.1)

        # Notification channels
        self.notification_channels = self.config.get("notification_channels", ["email"])

        # Channel-specific settings
        self.email_recipients = self.config.get("email_recipients", [])
        self.slack_webhook = self.config.get("slack_webhook", None)

        # Notification frequency
        self.notification_frequency = self.config.get("notification_frequency", "immediate")

        # Initialize threshold manager
        self.threshold_manager = ThresholdManager(config)

        # Create alert history directory
        self.alert_dir = os.path.join(os.getcwd(), "model_monitor_alerts")
        os.makedirs(self.alert_dir, exist_ok=True)

        logger.info("Initialized AlertManager")

    def send_data_drift_alert(self,
                              drift_score: float,
                              drift_details: Dict[str, Any],
                              timestamp: Optional[str] = None) -> bool:
        """
        Send an alert for data drift detection.

        Args:
            drift_score: Overall drift score
            drift_details: Details about the drift
            timestamp: Alert timestamp (if None, current time is used)

        Returns:
            True if alert was sent successfully, False otherwise
        """
        if not self.enabled:
            logger.info("Alerting is disabled, skipping data drift alert")
            return False

        # Set timestamp if not provided
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
        elif isinstance(timestamp, datetime.datetime):
            timestamp = timestamp.isoformat()

        # Check if alert should be sent based on threshold
        if drift_score <= self.drift_threshold:
            logger.info(f"Drift score {drift_score} below threshold {self.drift_threshold}, no alert sent")
            return False

        # Format alert message
        alert_data = {
            "type": "data_drift",
            "timestamp": timestamp,
            "severity": "high" if drift_score > 2 * self.drift_threshold else "medium",
            "drift_score": drift_score,
            "details": drift_details
        }

        # Generate alert message
        subject = f"[MODEL ALERT] Data Drift Detected (Score: {drift_score:.4f})"

        # Find top drifting features
        drift_scores = drift_details.get("drift_scores", {})
        top_features = sorted(
            drift_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        message = f"""
Data drift detected with score: {drift_score:.4f}

Top drifting features:
"""

        for feature, score in top_features:
            message += f"- {feature}: {score:.4f}\n"

        message += f"\nTimestamp: {timestamp}"

        # Save alert to history
        self._save_alert(alert_data)

        # Send notifications
        success = False

        if "email" in self.notification_channels and self.email_recipients:
            email_success = self._send_email_alert(subject, message)
            success = success or email_success

        if "slack" in self.notification_channels and self.slack_webhook:
            slack_success = self._send_slack_alert(subject, message)
            success = success or slack_success

        return success

    def send_model_drift_alert(self,
                               performance_degradation: float,
                               performance_details: Dict[str, Any],
                               timestamp: Optional[str] = None) -> bool:
        """
        Send an alert for model performance drift detection.

        Args:
            performance_degradation: Performance degradation measurement
            performance_details: Details about the performance drift
            timestamp: Alert timestamp (if None, current time is used)

        Returns:
            True if alert was sent successfully, False otherwise
        """
        if not self.enabled:
            logger.info("Alerting is disabled, skipping model drift alert")
            return False

        # Set timestamp if not provided
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
        elif isinstance(timestamp, datetime.datetime):
            timestamp = timestamp.isoformat()

        # Check if alert should be sent based on threshold
        if performance_degradation <= self.performance_threshold:
            logger.info(
                f"Performance degradation {performance_degradation} below threshold {self.performance_threshold}, no alert sent")
            return False

        # Format alert message
        alert_data = {
            "type": "model_drift",
            "timestamp": timestamp,
            "severity": "high" if performance_degradation > 2 * self.performance_threshold else "medium",
            "performance_degradation": performance_degradation,
            "details": performance_details
        }

        # Generate alert message
        subject = f"[MODEL ALERT] Model Performance Degradation (Score: {performance_degradation:.4f})"

        # Get performance differences
        differences = performance_details.get("differences", {})

        message = f"""
Model performance degradation detected: {performance_degradation:.4f}

Performance changes:
"""

        for metric, diff in differences.items():
            if isinstance(diff, dict) and "baseline" in diff and "current" in diff:
                baseline = diff["baseline"]
                current = diff["current"]
                absolute_diff = diff.get("absolute_diff", current - baseline)

                message += f"- {metric}: {baseline:.4f} → {current:.4f} (change: {absolute_diff:.4f})\n"

        message += f"\nTimestamp: {timestamp}"

        # Save alert to history
        self._save_alert(alert_data)

        # Send notifications
        success = False

        if "email" in self.notification_channels and self.email_recipients:
            email_success = self._send_email_alert(subject, message)
            success = success or email_success

        if "slack" in self.notification_channels and self.slack_webhook:
            slack_success = self._send_slack_alert(subject, message)
            success = success or slack_success

        return success

    def _save_alert(self, alert_data: Dict[str, Any]) -> str:
        """
        Save alert data to history.

        Args:
            alert_data: Alert data

        Returns:
            Path to saved alert file
        """
        # Create filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        alert_type = alert_data.get("type", "alert")
        filename = f"{timestamp}_{alert_type}.json"

        # Save to file
        filepath = os.path.join(self.alert_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(alert_data, f, indent=2)

        logger.info(f"Alert saved to {filepath}")

        return filepath

    def _send_email_alert(self, subject: str, message: str) -> bool:
        """
        Send an email alert.

        Args:
            subject: Email subject
            message: Email body

        Returns:
            True if email was sent successfully, False otherwise
        """
        # Check if email configuration is available
        if not self.email_recipients:
            logger.warning("No email recipients configured")
            return False

        # Environment variables for email configuration
        smtp_server = os.environ.get("MONITOR_SMTP_SERVER")
        smtp_port = int(os.environ.get("MONITOR_SMTP_PORT", 587))
        smtp_username = os.environ.get("MONITOR_SMTP_USERNAME")
        smtp_password = os.environ.get("MONITOR_SMTP_PASSWORD")
        sender_email = os.environ.get("MONITOR_SENDER_EMAIL")

        if not all([smtp_server, smtp_username, smtp_password, sender_email]):
            logger.warning("Incomplete email configuration, check environment variables")
            return False

        try:
            # Create email message
            email_message = MIMEMultipart()
            email_message["From"] = sender_email
            email_message["To"] = ", ".join(self.email_recipients)
            email_message["Subject"] = subject

            # Add message body
            email_message.attach(MIMEText(message, "plain"))

            # Connect to SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(email_message)

            logger.info(f"Email alert sent to {len(self.email_recipients)} recipients")
            return True

        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            logger.debug(traceback.format_exc())
            return False

    def _send_slack_alert(self, subject: str, message: str) -> bool:
        """
        Send a Slack alert.

        Args:
            subject: Alert subject
            message: Alert message

        Returns:
            True if alert was sent successfully, False otherwise
        """
        # Check if Slack webhook is configured
        if not self.slack_webhook:
            logger.warning("No Slack webhook configured")
            return False

        try:
            import requests

            # Format message for Slack
            slack_message = {
                "text": subject,
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": subject
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": message.replace("\n", "\n\n")
                        }
                    }
                ]
            }

            # Send message
            response = requests.post(
                self.slack_webhook,
                json=slack_message,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                logger.info("Slack alert sent successfully")
                return True
            else:
                logger.warning(f"Failed to send Slack alert: {response.status_code} {response.text}")
                return False

        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            logger.debug(traceback.format_exc())
            return False

    def get_alert_history(self,
                          alert_type: Optional[str] = None,
                          limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get alert history.

        Args:
            alert_type: Type of alerts to retrieve (if None, all alerts are returned)
            limit: Maximum number of alerts to return

        Returns:
            List of alert data dictionaries
        """
        alerts = []

        # Get all alert files
        alert_files = sorted(
            [f for f in os.listdir(self.alert_dir) if f.endswith(".json")],
            reverse=True
        )

        # Load alert data
        for filename in alert_files[:limit]:
            filepath = os.path.join(self.alert_dir, filename)

            try:
                with open(filepath, 'r') as f:
                    alert_data = json.load(f)

                if alert_type is None or alert_data.get("type") == alert_type:
                    alerts.append(alert_data)
            except Exception as e:
                logger.warning(f"Failed to load alert from {filepath}: {e}")

        return alerts