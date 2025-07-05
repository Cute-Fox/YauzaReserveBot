from __future__ import annotations

from datetime import datetime, date, time

from sqlalchemy import Date, Time, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class BanquetRequest(Base):
    __tablename__ = "banquet_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    banquet_date: Mapped[date]  = mapped_column(Date, nullable=False)
    banquet_time: Mapped[time]  = mapped_column(Time, nullable=False)
    guests:       Mapped[int]   = mapped_column(Integer, nullable=False)
    event_type:   Mapped[str]   = mapped_column(String(100), nullable=False)
    phone:        Mapped[str]   = mapped_column(String(25), nullable=False)

    created_at:   Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False
    )
