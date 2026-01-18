from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers.frontend import router as frontend_router
from src.settings import settings
from src.storage import create_s3_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    _client = await create_s3_client()
    app.state.client = await _client.__aenter__()  # noqa: PLC2801
    yield
    await app.state.client.__aexit__(None, None, None)


app = FastAPI(
    title='FastAI',
    description='AI website generator',
    debug=settings.debug,
    root_path='/frontend-api',
    lifespan=lifespan,
)

app.include_router(router=frontend_router)
app.mount('/', StaticFiles(directory='frontend/', html=True), name='site')
