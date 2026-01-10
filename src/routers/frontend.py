import asyncio
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import anyio
from fastapi import APIRouter, Path
from fastapi.responses import PlainTextResponse, StreamingResponse
from html_page_generator import AsyncDeepseekClient, AsyncPageGenerator, AsyncUnsplashClient

from src.models import (
    CreateSiteRequest,
    GeneratedSitesResponse,
    SiteResponse,
    SitesGenerationRequest,
    UserDetailsResponse,
)
from src.settings import settings
from src.storage import save_screenshot, upload_file_to_s3

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/frontend-api')


@router.get(
    '/users/me',
    summary='Получить учетные данные пользователя',
    response_description='json containing user data',
    tags=['Users'],
    response_model=UserDetailsResponse,
)
async def show_current_user() -> UserDetailsResponse:
    """
    Returns current user data\n
    **no params**
    """
    user_data = {
        'username': 'user123',
        'email': 'example@example.com',
        'isActive': True,
        'profileId': '1',
        'registeredAt': '2025-06-15T18:29:56+03:00',
        'updatedAt': '2025-06-15T18:29:56+03:00',
        'onemorefield': 'something',
    }
    user = UserDetailsResponse(**user_data)
    return user


@router.post(
    '/sites/create',
    summary='Создать сайт',
    tags=['Sites'],
    response_model=SiteResponse,
)
async def create_site(request: CreateSiteRequest):
    created_at = datetime.now(ZoneInfo('Europe/Moscow')).replace(microsecond=0)
    created_site = {
        'id': 1,
        'title': 'Site title',
        'prompt': request.prompt,
        'htmlCodeUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}/data/index.html',
        'htmlCodeDownloadUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}'
        f'/data/index.html?response-content-disposition=attachment',
        'screenshotUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}/data/screenshot.png',
        'createdAt': created_at,
        'updatedAt': created_at,
    }
    return SiteResponse(**created_site)


@router.post(
    '/sites/{site_id}/generate',
    summary='Сгенерировать HTML код сайта',
    tags=['Sites'],
    response_class=PlainTextResponse,
)
async def generate_site(
    site_id: int = Path(..., gt=0, title='ID сайта', description='Должен быть положительным'),
    request: SitesGenerationRequest | None = None,
):
    """
    Код сайта будет транслироваться стримом по мере генерации.
    """

    async def page_generator(user_prompt: str):
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

                await upload_file_to_s3(generator.html_page.html_code, 'data/index.html')
                logger.info('HTML успешно сохранён!')
                asyncio.create_task(save_screenshot(generator.html_page.html_code))

    return StreamingResponse(
        content=page_generator(request.prompt),
        media_type='text/plain',
    )


@router.get(
    '/sites/my',
    summary='Получить список сгенерированных сайтов текущего пользователя',
    tags=['Sites'],
    response_model=GeneratedSitesResponse,
)
async def get_sites():
    created_sites = {
        'sites': [
            {
                'id': 1,
                'title': 'Фан клуб Домино',
                'prompt': 'Сайт любителей играть в домино',
                'htmlCodeUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}/data/index.html',
                'htmlCodeDownloadUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}'
                f'/data/index.html?response-content-disposition=attachment',
                'screenshotUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}/data/screenshot.png',
                'createdAt': '2025-06-15T18:29:56+00:00',
                'updatedAt': '2025-06-15T18:29:56+00:00',
            },
        ],
    }
    return GeneratedSitesResponse(**created_sites)


@router.get(
    '/sites/{site_id}',
    summary='Получить сайт',
    tags=['Sites'],
    response_model=SiteResponse,
)
async def get_site(
    site_id: int = Path(..., gt=0, title='ID сайта', description='Должен быть положительным'),
):
    created_site = {
        'id': site_id,
        'title': 'Фан клуб Домино',
        'prompt': 'Сайт любителей играть в домино',
        'htmlCodeUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}/data/index.html',
        'htmlCodeDownloadUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}/data'
        f'/index.html?response-content-disposition=attachment',
        'screenshotUrl': f'{settings.storage.endpoint_url}{settings.storage.bucket_name}/data/screenshot.png',
        'createdAt': '2025-06-15T18:29:56+00:00',
        'updatedAt': '2025-06-15T18:29:56+00:00',
    }
    return SiteResponse(**created_site)


@router.get('/settings')
def get_settings():
    return settings.model_dump()
