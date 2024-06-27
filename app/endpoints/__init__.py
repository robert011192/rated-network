"""
List of routers
"""
from fastapi import APIRouter

from app.endpoints import ping, stats

root_router = APIRouter()

root_router.include_router(ping.router, tags=["ping"])
root_router.include_router(stats.router, tags=["stats"])
