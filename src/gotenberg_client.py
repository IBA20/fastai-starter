import httpx
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest
from httpx import Limits

from src.settings import settings
from src.storage import logger


async def get_screenshot(raw_html: str) -> bytes | None:
    try:
        async with httpx.AsyncClient(
            base_url=settings.gotenberg.base_url.encoded_string(),
            timeout=settings.gotenberg.timeout,
            limits=Limits(max_connections=settings.gotenberg.max_connections),
        ) as client:
            screenshot_bytes = await ScreenshotHTMLRequest(
                index_html=raw_html,
                width=settings.gotenberg.screenshot_width,
                format=settings.gotenberg.screenshot_format,
                wait_delay=settings.gotenberg.wait_delay,
            ).asend(client)
        return screenshot_bytes
    except GotenbergServerError as exc:
        logger.error('Failed to save screenshot: %s', exc)
