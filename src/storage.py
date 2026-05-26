import logging
from typing import Literal

import aioboto3
from aiobotocore.client import AioBaseClient
from aiobotocore.config import AioConfig
from aiobotocore.session import ClientCreatorContext

from src.settings import settings

logger = logging.getLogger(__name__)


async def create_s3_client() -> ClientCreatorContext:
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
        endpoint_url=settings.storage.endpoint_url.encoded_string(),
        config=config,
    )


async def upload_file_to_s3(
    client: AioBaseClient,
    file_content: str | bytes,
    s3_key: str,
    mime_type: str = 'text/html',
    content_disposition: Literal['attachment', 'inline'] = 'inline',
) -> None:
    upload_params = {
        'Bucket': settings.storage.bucket_name,
        'Key': s3_key,
        'Body': file_content,
        'ContentType': mime_type,
        'ContentDisposition': content_disposition,
    }

    await client.put_object(**upload_params)
