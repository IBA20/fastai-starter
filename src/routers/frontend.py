import logging

from fastapi import APIRouter, Path, Request
from fastapi.responses import PlainTextResponse, StreamingResponse

from src.models import (
    DEFAULT_SITE_EXAMPLE,
    CreateSiteRequest,
    GeneratedSitesResponse,
    SiteResponse,
    SitesGenerationRequest,
)
from src.page_generators import generate_page

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/sites', tags=['Sites'])


@router.post(
    '/create',
    summary='Создать сайт',
    response_model=SiteResponse,
)
async def create_site(request_payload: CreateSiteRequest):
    return SiteResponse(**DEFAULT_SITE_EXAMPLE)


@router.post(
    '/{site_id}/generate',
    summary='Сгенерировать HTML код сайта',
    response_class=PlainTextResponse,
)
async def generate_site(
    request: Request,
    request_payload: SitesGenerationRequest,
    site_id: int = Path(..., gt=0, title='ID сайта', description='Должен быть положительным'),
):
    """
    Код сайта будет транслироваться стримом по мере генерации.
    """

    return StreamingResponse(
        content=generate_page(
            request.app.state.s3_client,
            request.app.state.httpx_client,
            site_id,
            request_payload.prompt,
        ),
        media_type='text/plain',
    )


@router.get(
    '/my',
    summary='Получить список сгенерированных сайтов текущего пользователя',
    response_model=GeneratedSitesResponse,
)
async def get_sites():
    created_sites = {
        'sites': [DEFAULT_SITE_EXAMPLE],
    }
    return GeneratedSitesResponse(**created_sites)


@router.get(
    '/{site_id}',
    summary='Получить сайт',
    response_model=SiteResponse,
)
async def get_site(
    site_id: int = Path(..., gt=0, title='ID сайта', description='Должен быть положительным'),
):
    return SiteResponse(**DEFAULT_SITE_EXAMPLE)
