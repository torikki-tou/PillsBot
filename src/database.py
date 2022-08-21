import os
from enum import Enum
from functools import wraps
from typing import Callable, List, Optional, AsyncIterable

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from aiogram.types import User

from src.utils import notify_today

DB_NAME = 'pillsbot'
PILLS_LIMIT_BY_USER = 50
TIMES_LIMIT_BY_PILL = 3600  # max unique times for pill
MAX_NOTIFICATIONS = 7


class Collections(str, Enum):
    USERS = 'users'
    PILLS = 'pills'
    TIMES = 'times'


def _with_mongo_collection(collection_name: Collections) -> Callable:
    def with_mongodb_connection(func) -> Callable:
        client = AsyncIOMotorClient(os.environ.get('MONGO_CONNECTION_STRING'))
        collection = client[DB_NAME][collection_name]

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(collection, *args, **kwargs)
        return wrapper
    return with_mongodb_connection


@_with_mongo_collection(collection_name=Collections.USERS)
async def insert_new_user(collection, user: User) -> None:
    if not await collection.count_documents({'id': user.id}, limit=1):
        await collection.insert_one(dict(user))


@_with_mongo_collection(collection_name=Collections.PILLS)
async def insert_new_pill(collection, user_id: int, pill_title: str) -> ObjectId:

    pill_to_insert = {
        'user_id': user_id,
        'title': pill_title,
        'paused': False,
    }

    return (await collection.insert_one(pill_to_insert)).inserted_id


@_with_mongo_collection(collection_name=Collections.PILLS)
async def allowed_to_add_more_pills(collection, user_id: int) -> bool:
    return await collection.count_documents({'user_id': user_id}) < PILLS_LIMIT_BY_USER


@_with_mongo_collection(collection_name=Collections.PILLS)
async def get_pill_by_id(collection, pill_id: str) -> dict:
    return await collection.find_one({'_id': ObjectId(pill_id)})


@_with_mongo_collection(collection_name=Collections.PILLS)
async def get_pills_of_user(collection, user_id: int) -> List[dict]:
    return await collection.find({'user_id': user_id}).to_list(length=PILLS_LIMIT_BY_USER)


@_with_mongo_collection(collection_name=Collections.PILLS)
async def delete_pill(collection, pill_id: ObjectId | str) -> None:
    await collection.delete_one({'_id': ObjectId(pill_id)})


@_with_mongo_collection(collection_name=Collections.PILLS)
async def update_pill_title(collection, pill_id: str, new_title: str) -> None:
    await collection.update_one(
        {'_id': ObjectId(pill_id)},
        {'$set': {'title': new_title}}
    )


@_with_mongo_collection(collection_name=Collections.TIMES)
async def insert_times(collection, pill_id: ObjectId, times: List[str]) -> None:
    await collection.insert_many(
        {
            'pill_id': ObjectId(pill_id),
            'time': time,
            'notifications': MAX_NOTIFICATIONS if notify_today(time) else 0
        } for time in times
    )


@_with_mongo_collection(collection_name=Collections.TIMES)
async def get_times_of_pill(collection, pill_id: ObjectId | str) -> List[dict]:
    return await collection.find({'pill_id': ObjectId(pill_id)}).to_list(length=TIMES_LIMIT_BY_PILL)


@_with_mongo_collection(collection_name=Collections.TIMES)
async def delete_times(collection, pill_id: ObjectId | str, time: Optional[str] = None) -> None:
    filter_ = {'pill_id': ObjectId(pill_id)}
    if time:
        filter_['time'] = time
    await collection.delete_many(filter_)


@_with_mongo_collection(collection_name=Collections.PILLS)
async def set_notification_status(collection, pill_id: str, status: bool) -> None:
    await collection.update_one(
        {'_id': ObjectId(pill_id)},
        {'$set': {'paused': status}}
    )


@_with_mongo_collection(collection_name=Collections.TIMES)
async def get_times_to_notify(collection, now_time: str) -> AsyncIterable:
    return collection.find(
        {
            'time': {'$lt': now_time},
            'notifications': {'$gt': 0}
        }
    )


@_with_mongo_collection(collection_name=Collections.TIMES)
async def update_notification_count(collection, time_id: ObjectId | str, count: int):
    await collection.update_one(
        {'_id': ObjectId(time_id)},
        {'$set': {'notifications': count}}
    )


@_with_mongo_collection(collection_name=Collections.TIMES)
async def reset_notification_count(collection):
    await collection.update_many(
        {},
        {'$set': {'notifications': MAX_NOTIFICATIONS}}
    )
