from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from users.router import fastapi_users
from fastapi import Depends
from users.models import User
from users.schemas import UserRead


templates = Jinja2Templates(directory="templates")


router = APIRouter(
    prefix="/pages",
    tags=["pages"]
)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/chat/", response_class=HTMLResponse)
async def chat(request: Request, current_user: User = Depends(fastapi_users.current_user())):
    return templates.TemplateResponse(
        "chat.html", {
            "request": request,
            "user": current_user.email,
        })


@router.get("/register/", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})