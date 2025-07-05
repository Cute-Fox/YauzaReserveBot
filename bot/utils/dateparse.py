from __future__ import annotations

from datetime import datetime, time, date
from zoneinfo import ZoneInfo
import os, re

__all__ = ["DATE_FMT", "parse_date", "parse_time"]

DATE_FMT = "%d.%m.%Y"           # единый формат ввода для юзера
_TIME_RE = re.compile(r"^(\d{1,2}):(\d{2})$")   # 24-hour hh:mm
LOCAL_TZ = ZoneInfo(os.getenv("BOT_TZ", "Europe/Moscow"))

def parse_date(raw: str) -> date:
    return datetime.strptime(raw.strip(), DATE_FMT).date()


def parse_time(raw: str) -> time:
    m = _TIME_RE.fullmatch(raw.strip())
    if not m:
        raise ValueError("Неверный формат времени")
    hh, mm = map(int, m.groups())
    if not (0 <= hh < 24 and 0 <= mm < 60):
        raise ValueError("Неверное время")
    return time(hour=hh, minute=mm)

class PastDateError(ValueError):
    pass

class PastDateTimeError(ValueError):
    pass

def ensure_future_date(d: date) -> date:
    if d < datetime.now(LOCAL_TZ).date():
        raise PastDateError("Дата в прошлом")
    return d

def ensure_future_datetime(d: date, t: time) -> None:
    event = datetime.combine(d, t, LOCAL_TZ)
    if event <= datetime.now(LOCAL_TZ):
        raise PastDateTimeError("Время уже прошло")