from fastapi_users.authentication import  AuthenticationBackend, CookieTransport
from fastapi_users.authentication import JWTStrategy
from settings import settings


cookie_transport = CookieTransport(cookie_max_age=3600)

SECRET_KEY = settings.SECRET_KEY

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)