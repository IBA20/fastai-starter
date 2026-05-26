from aiobotocore.client import AioBaseClient

from src.gotenberg_client import get_screenshot
from src.storage import logger, upload_file_to_s3


async def save_screenshot(s3_client: AioBaseClient, raw_html: str, s3_key: str) -> None:
    screenshot_bytes = await get_screenshot(raw_html)
    if not screenshot_bytes:
        return
    await upload_file_to_s3(
        s3_client,
        screenshot_bytes,
        s3_key,
        mime_type='image/png',
    )
    logger.info('Скриншот успешно сохранён!')
