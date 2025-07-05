from __future__ import annotations

from datetime import datetime, time, date
import re

__all__ = ["DATE_FMT", "parse_date", "parse_time"]

DATE_FMT = "%d.%m.%Y"           # единый формат ввода для юзера
_TIME_RE = re.compile(r"^(\d{1,2}):(\d{2})$")   # 24-hour hh:mm


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
