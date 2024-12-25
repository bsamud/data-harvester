"""S3 download operations"""
re directory exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            log.info(f"Downloaded s3://{self.bucket_name}/{s3_key} to {local_path}")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                log.error(f"S3 object not found: {s3_key}")
            else:
                log.error(f"S3 download error: {e}")
            return False

    def list_objects(self, prefix=''):
        """
        List objects in S3 bucket with prefix

        Args:
            prefix: S3 key prefix

        Returns:
            list: List of object keys
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )

            if 'Contents' not in response:
                return []

            return [obj['Key'] for obj in response['Contents']]
        except ClientError as e:
            log.error(f"S3 list error: {e}")
            return []

    def file_exists(self, s3_key):
        """
        Check if file exists in S3

        Args:
            s3_key: S3 object key

        Returns:
            bool: True if exists
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError:
            return False

def get_s3_manager(bucket_name=None, region='us-east-1'):
    """Get S3 manager instance"""
    from common.app_config import get_config

    if bucket_name is None:
        config = get_config()
        bucket_name = config.get('S3', 'bucket_name')

    return S3Manager(bucket_name, region)
