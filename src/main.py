from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers.frontend import router as frontend_router
from src.settings import settings

app = FastAPI(title='FastAI', description='AI website generator', debug=settings.debug)

app.include_router(router=frontend_router)
app.mount('/', StaticFiles(directory='frontend/', html=True), name='site')
