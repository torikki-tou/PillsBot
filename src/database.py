import os
from enum import Enum
from functools import wraps
from typing import Callable, List, AsyncIterable

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from aiogram.types import User

from src.utils import notify_today

PILLS_LIMIT_BY_USER = 50
MAX_NOTIFICATIONS = 7


class Collections(str, Enum):
    USERS = 'users'
    PILLS = 'pills'


def _with_mongo_collection(collection_name: Collections) -> Callable:
    def with_mongodb_connection(func) -> Callable:
        client = AsyncIOMotorClient(os.environ.get('MONGO_CONNECTION_STRING'))
        collection = client.pillsbot[collection_name]

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(collection, *args, **kwargs)
        return wrapper
    return with_mongodb_connection


@_with_mongo_collection(collection_name=Collections.USERS)
async def insert_new_user(collection, user: User) -> None:
    await collection.insert_one(dict(user))


@_with_mongo_collection(collection_name=Collections.PILLS)
async def insert_new_pill(collection, user_id: int, pill_title: str, taking_times: List[str]) -> None:

    pill_to_insert = {
        'user_id': user_id,
        'title': pill_title,
        'taking_times': [
            {
                'time': time, 'notifications_left': MAX_NOTIFICATIONS if notify_today(time) else 0
            } for time in taking_times
        ],
        'paused': False,
    }

    await collection.insert_one(pill_to_insert)


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
async def delete_pill(collection, pill_id: str) -> None:
    await collection.delete_one({'_id': ObjectId(pill_id)})


@_with_mongo_collection(collection_name=Collections.PILLS)
async def update_pill_title(collection, pill_id: str, new_title: str) -> None:
    await collection.update_one(
        {'_id': ObjectId(pill_id)},
        {'$set': {'title': new_title}}
    )


@_with_mongo_collection(collection_name=Collections.PILLS)
async def add_time_to_pill(collection, pill_id: str, new_time: str) -> None:
    await collection.update_one(
        {'_id': ObjectId(pill_id)},
        {'$push': {'taking_times': {
            'time': new_time,
            'notifications_left': MAX_NOTIFICATIONS if notify_today(new_time) else 0}
        }}
    )


@_with_mongo_collection(collection_name=Collections.PILLS)
async def delete_pill_time(collection, pill_id: str, time_to_delete: str) -> None:
    await collection.update_one(
        {'_id': ObjectId(pill_id)},
        {'$pull': {'taking_times': {'time': time_to_delete}}}
    )


@_with_mongo_collection(collection_name=Collections.PILLS)
async def set_notification_status(collection, pill_id: str, status: bool) -> None:
    await collection.update_one(
        {'_id': ObjectId(pill_id)},
        {'$set': {'paused': status}}
    )


@_with_mongo_collection(collection_name=Collections.PILLS)
async def get_pills_need_to_take(collection, now: str) -> AsyncIterable:
    return collection.find({'$and': [
        {'taking_times': {'$elemMatch': {'time': {'$gt': now}, 'notifications_left': {'$gt': 0}}}},
        {'paused': False}
    ]})
