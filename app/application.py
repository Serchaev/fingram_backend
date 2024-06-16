from fastapi import FastAPI

from app.api.routers.auth import router as auth_router
from app.api.routers.events import router as events_router
from app.api.routers.news import router as news_router
from app.api.routers.partners import router as partners_router

app = FastAPI()

app.include_router(partners_router)
app.include_router(news_router)
app.include_router(events_router)
app.include_router(auth_router)
