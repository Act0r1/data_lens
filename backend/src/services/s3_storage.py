import logging
from functools import lru_cache

import boto3
from botocore.config import Config

from src.config import settings

logger = logging.getLogger(__name__)


@lru_cache
def _get_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint or None,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
        config=Config(signature_version="s3v4"),
    )


async def upload_to_s3(key: str, data: bytes, content_type: str = "application/octet-stream"):
    client = _get_client()
    client.put_object(Bucket=settings.s3_bucket, Key=key, Body=data, ContentType=content_type)
    logger.info("Uploaded to S3: %s", key)


async def download_from_s3(key: str) -> bytes:
    client = _get_client()
    response = client.get_object(Bucket=settings.s3_bucket, Key=key)
    return response["Body"].read()
