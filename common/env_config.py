"""Environment variable configuration"""
import os
from dotenv import load_dotenv
from common.logger import log

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()

    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
    ]

    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        log.warning(f"Missing environment variables: {missing}")

    return {
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'aws_s3_bucket': os.getenv('AWS_S3_BUCKET', 'dataharvest-bucket'),
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
    }

def get_env(key, default=None):
    """Get environment variable"""
    return os.getenv(key, default)
