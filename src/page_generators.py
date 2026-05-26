import logging
from collections.abc import AsyncGenerator

import anyio
from aiobotocore.client import AioBaseClient
from gotenberg_api import GotenbergServerError
from html_page_generator import AsyncPageGenerator

from src.gotenberg_client import get_screenshot
from src.settings import settings
from src.storage import upload_file_to_s3

logger = logging.getLogger(__name__)


async def generate_page(
    s3_client: AioBaseClient,
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
            screenshot_bytes = await get_screenshot(generator.html_page.html_code)
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
