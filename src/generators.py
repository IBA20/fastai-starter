import logging

import anyio
from gotenberg_api import GotenbergServerError
from html_page_generator import AsyncDeepseekClient, AsyncPageGenerator, AsyncUnsplashClient

from src.gotenberg_client import get_screenshot
from src.settings import settings
from src.storage import upload_file_to_s3

logger = logging.getLogger(__name__)


async def page_generator(request, site_id, user_prompt: str):
    try:
        async with (
            AsyncUnsplashClient.setup(
                settings.unsplash.api_key,
                timeout=settings.unsplash.connection_timeout,
            ),
            AsyncDeepseekClient.setup(
                settings.deepseek.api_key.get_secret_value(),
                settings.deepseek.base_url.encoded_string(),
                settings.deepseek.model,
                timeout=settings.deepseek.connection_timeout,
            ),
        ):
            generator = AsyncPageGenerator(debug_mode=settings.debug)
            with anyio.CancelScope(shield=True):
                async for chunk in generator(user_prompt):
                    yield chunk

                await upload_file_to_s3(
                    request.app.state.client,
                    generator.html_page.html_code,
                    f'data/index_{site_id}.html',
                )
                logger.info('HTML успешно сохранён!')
                screenshot_bytes = await get_screenshot(generator.html_page.html_code)
                if not screenshot_bytes:
                    return
                await upload_file_to_s3(
                    request.app.state.client,
                    screenshot_bytes,
                    f'data/screenshot_{site_id}.png',
                    mime_type='image/png',
                )
                logger.info('Скриншот успешно сохранён!')
    except GotenbergServerError as exc:
        logger.error('Failed to save screenshot: %s', exc)
