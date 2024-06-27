"""
Small endpoint to check the server is alive
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping():
    """Route answering pong to any request"""
    return {"result": "pong"}
