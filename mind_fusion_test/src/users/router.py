from fastapi_users import FastAPIUsers

from .manager import get_user_manager
from .models import User
from .auth import auth_backend



fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

