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
        'htmlCodeUrl': 'https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html',
        'htmlCodeDownloadUrl': 'https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html?response-content-disposition=attachment',
        'screenshotUrl': 'https://dvmn.org/tilda_assets/tild6435-3366-4037-b963-323530656465__devman_logo_heart_wi.svg',
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

                with open('frontend/media/index.html', 'w', encoding='utf8') as f:
                    f.write(generator.html_page.html_code)
                logger.debug('Файл успешно сохранён!')

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
                'htmlCodeUrl': 'https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html',
                'htmlCodeDownloadUrl': 'https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html?response-content-disposition=attachment',
                'screenshotUrl': 'http://dvmn.org/media/index.png',
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
        'htmlCodeUrl': 'https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html',
        'htmlCodeDownloadUrl': 'https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html?response-content-disposition=attachment',
        'screenshotUrl': 'http://dvmn.org/media/index.png',
        'createdAt': '2025-06-15T18:29:56+00:00',
        'updatedAt': '2025-06-15T18:29:56+00:00',
    }
    return SiteResponse(**created_site)


@router.get('/settings')
def get_settings():
    return {
        'db_host': settings.database.host,
        'db_port': settings.database.port,
        'db_user': settings.database.username,
        'db_password': settings.database.password,
    }
