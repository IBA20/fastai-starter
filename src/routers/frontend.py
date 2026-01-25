import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Path, Request
from fastapi.responses import PlainTextResponse, StreamingResponse

from src.generators import page_generator
from src.models import (
    DEFAULT_SITE_EXAMPLE,
    CreateSiteRequest,
    GeneratedSitesResponse,
    SiteResponse,
    SitesGenerationRequest,
    UserDetailsResponse,
)
from src.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter()


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
async def create_site(request_payload: CreateSiteRequest):
    created_at = datetime.now(ZoneInfo('Europe/Moscow')).replace(microsecond=0)
    created_site = {
        'id': 1,
        'title': 'Site title',
        'prompt': request_payload.prompt,
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
    request: Request,
    site_id: int = Path(..., gt=0, title='ID сайта', description='Должен быть положительным'),
    request_payload: SitesGenerationRequest | None = None,
):
    """
    Код сайта будет транслироваться стримом по мере генерации.
    """

    return StreamingResponse(
        content=page_generator(request, site_id, request_payload.prompt),
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
        'sites': [DEFAULT_SITE_EXAMPLE],
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
    return SiteResponse(**DEFAULT_SITE_EXAMPLE)
