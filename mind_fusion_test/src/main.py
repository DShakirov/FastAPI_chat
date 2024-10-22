from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users.router import fastapi_users
from users.auth import auth_backend
from users.schemas import UserCreate, UserRead
from pages.router import router as pages_router
from chat.router import router as chat_router
from fastapi_cache import caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from settings import settings


app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)


app.include_router(fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)


app.include_router(pages_router)
app.include_router(chat_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend(f'redis://{settings.REDIS_HOST}')
    caches.set(CACHE_KEY, rc)


