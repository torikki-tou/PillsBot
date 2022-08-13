import os
from datetime import datetime, timedelta, timezone
from typing import List

TZ = timezone(timedelta(hours=int(os.environ.get('TZ'))))


def get_string_from_time(time_list: List[str]) -> str:
    if len(time_list) <= 2:
        return ' и '.join(time_list)
    else:
        return f'{", ".join(time_list[:-1])} и {time_list[-1]}'


def notify_today(time):
    return datetime.strptime(time, '%H:%M').time() > datetime.now(tz=TZ).time()
