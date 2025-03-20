import boto3
import os
from src.config import GlobalConfig

def upload_bytes_to_s3(file_bytes: bytes, bucket: str, object_name: str, config: GlobalConfig = None) -> str:
    """
    Upload bytes to S3 and return the URL.
    
    Args:
        file_bytes: Bytes to upload
        bucket: S3 bucket name
        object_name: Object name in S3
        config: Optional GlobalConfig object. If not provided, will use default config.
        
    Returns:
        str: URL of the uploaded file
    """
    if not config:
        config = GlobalConfig()
        
    if not config.aws or not config.aws.access_key_id or not config.aws.secret_access_key or not config.aws.region:
        raise ValueError("AWS credentials not configured")
        
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=config.aws.access_key_id,
            aws_secret_access_key=config.aws.secret_access_key,
            region_name=config.aws.region
        )
        
        s3_client.put_object(
            Bucket=bucket,
            Key=object_name,
            Body=file_bytes
        )
        
        url = f"https://{bucket}.s3.{config.aws.region}.amazonaws.com/{object_name}"
        return url
        
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None