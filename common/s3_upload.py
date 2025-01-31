"""S3 upload operations"""
"""AWS S3 utilities for file upload/download"""
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from pathlib import Path
import os
from common.logger import log

class S3Manager:
    """Manager for S3 operations"""

    def __init__(self, bucket_name, region='us-east-1'):
        # Validate bucket name
        if not bucket_name or not bucket_name.strip():
            raise ValueError("Bucket name cannot be empty")
        """
        Initialize S3 manager

        Args:
            bucket_name: S3 bucket name
            region: AWS region
        """
        self.bucket_name = bucket_name
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)

    def upload_file(self, local_path, s3_key):
        """
        Upload file to S3

        Args:
            local_path: Local file path
            s3_key: S3 object key

        Returns:
            bool: True if successful
        """
        try:
            self.s3_client.upload_file(local_path, self.bucket_name, s3_key)
            log.info(f"Uploaded {local_path} to s3://{self.bucket_name}/{s3_key}")
            return True
        except FileNotFoundError:
            log.error(f"File not found: {local_path}")
            return False
        except NoCredentialsError:
            log.error("AWS credentials not found")
            return False
        except ClientError as e:
            log.error(f"S3 upload error: {e}")
            return False

    def download_file(self, s3_key, local_path):
        """
        Download file from S3

        Args:
            s3_key: S3 object key
            local_path: Local file path to save

        Returns:
            bool: True if successful
        """
        try:
            # Ensu
# Added retry logic with exponential backoff
