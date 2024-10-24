from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi_users.authentication import JWTStrategy
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates
from users.router import fastapi_users, current_user
from fastapi import Depends
from users.models import User
from logger import logger
from users.utils import get_token, get_user_from_token, get_users_emails
from db import get_async_session


templates = Jinja2Templates(directory="templates")


router = APIRouter(
    prefix="/pages",
    tags=["pages"]
)

@router.get("/", response_class=HTMLResponse)
async def read_root(
        request: Request,
        token=Depends(get_token),
        session: AsyncSession = Depends(get_async_session)
                    ):
    response = {"request": request}
    if token:
        user = await get_user_from_token(token, session)
        response["user"] = user.email

    return templates.TemplateResponse("index.html", response)


@router.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/chat/", response_class=HTMLResponse)
async def chat(
        request: Request,
        current_user: User = Depends(fastapi_users.current_user()),
        session: AsyncSession = Depends(get_async_session)
):

    users = await get_users_emails(session)
    users.remove(current_user.email)
    return templates.TemplateResponse(
        "chat.html", {
            "request": request,
            "user": current_user.email,
            "users": users
        })


@router.get("/register/", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})