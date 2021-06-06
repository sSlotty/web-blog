from fastapi import APIRouter

from api.api_v1.endpoints import item, authentication, article

api_router = APIRouter()
api_router.include_router(item.router, prefix="/items", tags=["items"])
api_router.include_router(authentication.router, prefix="/authentication", tags=["authentication"])
api_router.include_router(article.router, prefix="/articles", tags=['articles'])
