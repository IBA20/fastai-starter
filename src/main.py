from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers.frontend import router as frontend_router

app = FastAPI(title='FastAI', description='AI website generator')

app.include_router(router=frontend_router)
app.mount('/', StaticFiles(directory='frontend/', html=True), name='site')
