# aws_setup.py
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from loguru import logger

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

if not all([AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME]):
    raise ValueError("Missing AWS environment variables.")

try:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
except (NoCredentialsError, PartialCredentialsError) as e:
    logger.error(f"Credentials error: {e}")
    raise

def upload_file_to_s3(file_path, bucket_name, s3_file_name):
    try:
        s3_client.upload_file(file_path, bucket_name, s3_file_name)
        logger.info(f"File {file_path} uploaded to S3 bucket {bucket_name} as {s3_file_name}")
        return f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"
    except (FileNotFoundError, NoCredentialsError, ClientError) as e:
        logger.error(f"Error uploading file: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
