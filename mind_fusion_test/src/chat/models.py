from sqlalchemy import Column, Integer, String, ForeignKey

from db import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(String)
    from_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    from_user = relationship("users.models.User")
