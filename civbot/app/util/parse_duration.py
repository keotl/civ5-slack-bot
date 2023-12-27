import re
from datetime import datetime, timedelta
from typing import Optional


def parse_duration(text: Optional[str], now: datetime) -> datetime:
    if text is None:
        return datetime.max
    matches = _pattern.match(text)
    if not matches:
        return datetime.max

    weeks = int(matches.group(2) or "0")
    days = int(matches.group(4) or "0")
    hours = int(matches.group(6) or "0")
    minutes = int(matches.group(8) or "0")

    return now + timedelta(days=days + 7 * weeks, hours=hours, minutes=minutes)


_pattern = re.compile(r"((\d+)w)?((\d+)d)?((\d+)h)?((\d+)m)?")
