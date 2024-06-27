"""
Root of the API.

Whenever a new endpoint is added its router should be included here
"""
from fastapi import FastAPI
from app.core.config import settings
from app.endpoints import root_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(root_router)
