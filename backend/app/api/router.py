from fastapi import APIRouter
from app.api import health, users, auth, catalog
from app.api import voice
from app.api import matching

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["Health Check"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["Smart Cataloging"])
api_router.include_router(voice.router)
api_router.include_router(matching.router)