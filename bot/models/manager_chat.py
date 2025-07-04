from sqlalchemy.orm import Mapped, mapped_column
from bot.models.base import Base

class ManagerChat(Base):
    __tablename__ = "manager_chats"
    id:      Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(unique=True, index=True)
    title:   Mapped[str] = mapped_column(nullable=True)