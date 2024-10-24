from pydantic import BaseModel
from users.schemas import UserRead


class MessageModel(BaseModel):
    id: int
    message: str
    from_user: UserRead

    class Config:
        from_attributes = True


class PrivateMessageModel(BaseModel):
    id: int
    message: str
    to_user: UserRead
    from_user: UserRead

    class Config:
        from_attributes = True