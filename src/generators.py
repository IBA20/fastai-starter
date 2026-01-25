import asyncio
import logging

import anyio
from html_page_generator import AsyncDeepseekClient, AsyncPageGenerator, AsyncUnsplashClient

from src.settings import settings
from src.storage import save_screenshot, upload_file_to_s3

logger = logging.getLogger(__name__)


async def page_generator(request, site_id, user_prompt: str):
    async with (
        AsyncUnsplashClient.setup(
            settings.unsplash.api_key,
            timeout=settings.unsplash.connection_timeout,
        ),
        AsyncDeepseekClient.setup(
            settings.deepseek.api_key.get_secret_value(),
            settings.deepseek.base_url,
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
            asyncio.create_task(
                save_screenshot(
                    request.app.state.client,
                    generator.html_page.html_code,
                    f'data/screenshot_{site_id}.png',
                ),
            )
