from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient
from httpx import Limits

from src.routers.frontend import router as frontend_router
from src.settings import settings
from src.storage import create_s3_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    _httpx_client = httpx.AsyncClient(
        base_url=settings.gotenberg.base_url.encoded_string(),
        timeout=settings.gotenberg.timeout,
        limits=Limits(max_connections=settings.gotenberg.max_connections),
    )
    _unsplash_client = AsyncUnsplashClient.setup(
        settings.unsplash.api_key.get_secret_value(),
        timeout=settings.unsplash.connection_timeout,
    )
    _deepseek_client = AsyncDeepseekClient.setup(
        settings.deepseek.api_key.get_secret_value(),
        settings.deepseek.base_url.encoded_string(),
        settings.deepseek.model,
        timeout=settings.deepseek.connection_timeout,
    )
    _s3_client = await create_s3_client()
    async with (
        _s3_client as s3_client,
        _httpx_client as httpx_client,
        _deepseek_client,
        _unsplash_client,
    ):
        app.state.s3_client = s3_client
        app.state.httpx_client = httpx_client
        yield


app = FastAPI(
    title='FastAI',
    description='AI website generator',
    debug=settings.debug,
    root_path='/frontend-api',
    lifespan=lifespan,
)

app.include_router(router=frontend_router)
app.mount('/', StaticFiles(directory='frontend/', html=True), name='site')
