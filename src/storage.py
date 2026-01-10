from typing import Literal

import aioboto3
from aiobotocore.config import AioConfig

from src.settings import settings


async def create_s3_client():
    config = AioConfig(
        max_pool_connections=settings.storage.max_pool_connections,
        connect_timeout=settings.storage.connect_timeout,
        read_timeout=settings.storage.read_timeout,
    )
    session = aioboto3.Session(
        aws_access_key_id=settings.storage.access_key.get_secret_value(),
        aws_secret_access_key=settings.storage.secret_key.get_secret_value(),
    )
    return session.client(
        's3',
        endpoint_url=settings.storage.endpoint_url,
        config=config,
    )


async def upload_file_to_s3(
    file_content: str | bytes,
    s3_key: str,
    mime_type: str = 'text/html',
    content_disposition: Literal['attachment', 'inline'] = 'inline',
):
    upload_params = {
        'Bucket': settings.storage.bucket_name,
        'Key': s3_key,
        'Body': file_content,
        'ContentType': mime_type,
        'ContentDisposition': content_disposition,
    }

    s3_client = await create_s3_client()
    async with s3_client as client:
        await client.put_object(**upload_params)
