from pydantic import BaseModel
from users.schemas import UserRead


class MessageModel(BaseModel):
    id: int
    message: str
    from_user: UserRead

    class Config:
        from_attributes = True