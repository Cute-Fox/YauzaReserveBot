from datetime import datetime, date, time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Date, Time, String, TIMESTAMP, ForeignKey
from .base import Base

class TableRequest(Base):
    __tablename__ = "table_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    reserve_date: Mapped[date] = mapped_column(Date, nullable=False)
    reserve_time: Mapped[time] = mapped_column(Time, nullable=False)
    guests: Mapped[int] = mapped_column(Integer, nullable=False)
    phone: Mapped[str] = mapped_column(String(25), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False
    )
