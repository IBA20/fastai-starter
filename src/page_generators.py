import logging
from collections.abc import AsyncGenerator

import anyio
from aiobotocore.client import AioBaseClient
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from html_page_generator import AsyncPageGenerator
from httpx import AsyncClient

from src.settings import settings
from src.storage import upload_file_to_s3

logger = logging.getLogger(__name__)


async def generate_page(
    s3_client: AioBaseClient,
    httpx_client: AsyncClient,
    site_id: int,
    user_prompt: str,
) -> AsyncGenerator:
    try:
        generator = AsyncPageGenerator(debug_mode=settings.debug)
        with anyio.CancelScope(shield=True):
            async for chunk in generator(user_prompt):
                yield chunk

            await upload_file_to_s3(
                s3_client,
                generator.html_page.html_code,
                f'data/index_{site_id}.html',
            )
            logger.info('HTML успешно сохранён!')
            screenshot_bytes = await ScreenshotHTMLRequest(
                index_html=generator.html_page.html_code,
                width=settings.gotenberg.screenshot_width,
                format=settings.gotenberg.screenshot_format,
                wait_delay=settings.gotenberg.wait_delay,
            ).asend(httpx_client)
            if not screenshot_bytes:
                return
            await upload_file_to_s3(
                s3_client,
                screenshot_bytes,
                f'data/screenshot_{site_id}.png',
                mime_type='image/png',
            )
            logger.info('Скриншот успешно сохранён!')
    except GotenbergServerError as exc:
        logger.error('Failed to save screenshot: %s', exc)
