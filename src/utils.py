from typing import List


async def get_string_from_time(time_list: List[str]) -> str:
    if len(time_list) <= 2:
        return ' и '.join(time_list)
    else:
        return f'{", ".join(time_list[:-1])} и {time_list[-1]}'
