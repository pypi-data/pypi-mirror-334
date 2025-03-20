"""
Data loading utilities for model monitoring.
"""

import pandas as pd
import numpy as np
import os
import json
import logging
from typing import Dict, List, Union, Optional, Any
from pathlib import Path
import tempfile

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Class for loading data from various sources.

    This class provides methods for loading data from files, databases,
    and cloud storage.
    """

    def __init__(self):
        """Initialize the data loader."""
        self.supported_extensions = {
            '.csv': self._load_csv,
            '.parquet': self._load_parquet,
            '.json': self._load_json,
            '.jsonl': self._load_jsonl,
            '.xlsx': self._load_excel,
            '.xls': self._load_excel,
            '.feather': self._load_feather,
            '.pickle': self._load_pickle,
            '.pkl': self._load_pickle
        }

        logger.info("Initialized DataLoader")

    def load(self, path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from a file path.

        Args:
            path: Path to the data file

        Returns:
            Loaded data as a pandas DataFrame
        """
        path = Path(path)

        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Get file extension
        extension = path.suffix.lower()

        # Check if extension is supported
        if extension not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {extension}")

        # Load data using the appropriate function
        loader_func = self.supported_extensions[extension]

        try:
            data = loader_func(path)
            logger.info(f"Loaded data from {path}: {len(data)} rows, {len(data.columns)} columns")
            return data
        except Exception as e:
            logger.error(f"Error loading data from {path}: {e}")
            raise

    def load_from_db(self,
                     query: str,
                     connection_string: str,
                     **kwargs) -> pd.DataFrame:
        """
        Load data from a database.

        Args:
            query: SQL query string
            connection_string: Database connection string
            **kwargs: Additional arguments for pandas.read_sql

        Returns:
            Loaded data as a pandas DataFrame
        """
        try:
            import sqlalchemy

            # Create database engine
            engine = sqlalchemy.create_engine(connection_string)

            # Execute query
            data = pd.read_sql(query, engine, **kwargs)
            logger.info(f"Loaded data from database: {len(data)} rows, {len(data.columns)} columns")

            return data

        except ImportError:
            logger.error("sqlalchemy not installed, required for database connections")
            raise
        except Exception as e:
            logger.error(f"Error loading data from database: {e}")
            raise

    def load_from_s3(self,
                     bucket: str,
                     key: str,
                     **kwargs) -> pd.DataFrame:
        """
        Load data from Amazon S3.

        Args:
            bucket: S3 bucket name
            key: S3 object key
            **kwargs: Additional arguments

        Returns:
            Loaded data as a pandas DataFrame
        """
        try:
            import boto3

            # Create S3 client
            s3 = boto3.client('s3')

            # Get file extension
            extension = os.path.splitext(key)[1].lower()

            if extension not in self.supported_extensions:
                raise ValueError(f"Unsupported file type: {extension}")

            # Download file to temporary location
            with tempfile.NamedTemporaryFile(suffix=extension) as temp_file:
                s3.download_file(bucket, key, temp_file.name)

                # Load data using the appropriate function
                loader_func = self.supported_extensions[extension]
                data = loader_func(temp_file.name)

            logger.info(f"Loaded data from S3 {bucket}/{key}: {len(data)} rows, {len(data.columns)} columns")
            return data

        except ImportError:
            logger.error("boto3 not installed, required for S3 connections")
            raise
        except Exception as e:
            logger.error(f"Error loading data from S3: {e}")
            raise

    def load_from_gcs(self,
                      bucket: str,
                      blob_name: str,
                      **kwargs) -> pd.DataFrame:
        """
        Load data from Google Cloud Storage.

        Args:
            bucket: GCS bucket name
            blob_name: GCS blob name
            **kwargs: Additional arguments

        Returns:
            Loaded data as a pandas DataFrame
        """
        try:
            from google.cloud import storage

            # Create GCS client
            client = storage.Client()

            # Get file extension
            extension = os.path.splitext(blob_name)[1].lower()

            if extension not in self.supported_extensions:
                raise ValueError(f"Unsupported file type: {extension}")

            # Download file to temporary location
            bucket = client.bucket(bucket)
            blob = bucket.blob(blob_name)

            with tempfile.NamedTemporaryFile(suffix=extension) as temp_file:
                blob.download_to_filename(temp_file.name)

                # Load data using the appropriate function
                loader_func = self.supported_extensions[extension]
                data = loader_func(temp_file.name)

            logger.info(f"Loaded data from GCS {bucket}/{blob_name}: {len(data)} rows, {len(data.columns)} columns")
            return data

        except ImportError:
            logger.error("google-cloud-storage not installed, required for GCS connections")
            raise
        except Exception as e:
            logger.error(f"Error loading data from GCS: {e}")
            raise

    def load_from_azure(self,
                        container: str,
                        blob_name: str,
                        connection_string: str,
                        **kwargs) -> pd.DataFrame:
        """
        Load data from Azure Blob Storage.

        Args:
            container: Azure container name
            blob_name: Azure blob name
            connection_string: Azure storage connection string
            **kwargs: Additional arguments

        Returns:
            Loaded data as a pandas DataFrame
        """
        try:
            from azure.storage.blob import BlobServiceClient

            # Create Azure client
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)

            # Get file extension
            extension = os.path.splitext(blob_name)[1].lower()

            if extension not in self.supported_extensions:
                raise ValueError(f"Unsupported file type: {extension}")

            # Download file to temporary location
            container_client = blob_service_client.get_container_client(container)
            blob_client = container_client.get_blob_client(blob_name)

            with tempfile.NamedTemporaryFile(suffix=extension) as temp_file:
                with open(temp_file.name, "wb") as file:
                    download_stream = blob_client.download_blob()
                    file.write(download_stream.readall())

                # Load data using the appropriate function
                loader_func = self.supported_extensions[extension]
                data = loader_func(temp_file.name)

            logger.info(
                f"Loaded data from Azure {container}/{blob_name}: {len(data)} rows, {len(data.columns)} columns")
            return data

        except ImportError:
            logger.error("azure-storage-blob not installed, required for Azure connections")
            raise
        except Exception as e:
            logger.error(f"Error loading data from Azure: {e}")
            raise

    def _load_csv(self, path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from a CSV file.

        Args:
            path: Path to the CSV file

        Returns:
            Loaded data as a pandas DataFrame
        """
        try:
            # First try with default settings
            return pd.read_csv(path)
        except:
            # If that fails, try with more flexible settings
            return pd.read_csv(
                path,
                sep=None,  # Detect separator
                engine='python',
                on_bad_lines='warn'
            )

    def _load_parquet(self, path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from a Parquet file.

        Args:
            path: Path to the Parquet file

        Returns:
            Loaded data as a pandas DataFrame
        """
        return pd.read_parquet(path)

    def _load_json(self, path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from a JSON file.

        Args:
            path: Path to the JSON file

        Returns:
            Loaded data as a pandas DataFrame
        """
        return pd.read_json(path)

    def _load_jsonl(self, path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from a JSONL file.

        Args:
            path: Path to the JSONL file

        Returns:
            Loaded data as a pandas DataFrame
        """
        return pd.read_json(path, lines=True)

    def _load_excel(self, path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from an Excel file.

        Args:
            path: Path to the Excel file

        Returns:
            Loaded data as a pandas DataFrame
        """
        return pd.read_excel(path)

    def _load_feather(self, path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from a Feather file.

        Args:
            path: Path to the Feather file

        Returns:
            Loaded data as a pandas DataFrame
        """
        return pd.read_feather(path)

    def _load_pickle(self, path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from a Pickle file.

        Args:
            path: Path to the Pickle file

        Returns:
            Loaded data as a pandas DataFrame
        """
        return pd.read_pickle(path)