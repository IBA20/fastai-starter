import logging
from typing import Literal

import aioboto3
import httpx
from aiobotocore.client import AioBaseClient
from aiobotocore.config import AioConfig
from aiobotocore.session import ClientCreatorContext
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from httpx import Limits

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
        endpoint_url=settings.storage.endpoint_url,
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


async def save_screenshot(s3_client: AioBaseClient, raw_html: str, s3_key: str) -> None:
    try:
        async with httpx.AsyncClient(
            base_url=settings.gotenberg.base_url,
            timeout=settings.gotenberg.timeout,
            limits=Limits(max_connections=settings.gotenberg.max_connections),
        ) as client:
            screenshot_bytes = await ScreenshotHTMLRequest(
                index_html=raw_html,
                width=settings.gotenberg.screenshot_width,
                format=settings.gotenberg.screenshot_format,
                wait_delay=settings.gotenberg.wait_delay,
            ).asend(client)

        await upload_file_to_s3(
            s3_client,
            screenshot_bytes,
            s3_key,
            mime_type='image/png',
        )
        logger.info('Скриншот успешно сохранён!')
    except GotenbergServerError as exc:
        logger.error('Failed to save screenshot: %s', exc)
