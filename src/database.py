import os
from functools import wraps
from typing import Callable, List, AsyncIterable

import aiogram.types
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


def _with_mongo_collection(collection_name: str) -> Callable:
    def with_mongodb_connection(func) -> Callable:
        client = AsyncIOMotorClient(os.environ.get('MONGO_CONNECTION_STRING'))
        collection = client.pillsbot[collection_name]

        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(collection, *args, **kwargs)
        return wrapper
    return with_mongodb_connection


@_with_mongo_collection(collection_name='users')
async def insert_new_user(collection, user: aiogram.types.User):

    await collection.insert_one(dict(user))


@_with_mongo_collection(collection_name='pills')
async def insert_new_pill(collection, user_id: int, pill_title: str, times_to_take: List[str]) -> None:

    pill_to_insert = {
        'user_id': user_id,
        'title': pill_title,
        'times_to_take': times_to_take,
        'paused': False,
    }

    await collection.insert_one(pill_to_insert)


@_with_mongo_collection(collection_name='pills')
async def get_pill_by_id(collection, pill_id: str) -> dict:
    return await collection.find_one({'_id': ObjectId(pill_id)})


@_with_mongo_collection(collection_name='pills')
async def get_all_pills_of_user(collection, user_id: int) -> AsyncIterable:

    return collection.find({'user_id': user_id})


@_with_mongo_collection(collection_name='pills')
async def delete_pill(collection, pill_id: str) -> None:

    return collection.delete_one({'_id': ObjectId(pill_id)})


@_with_mongo_collection(collection_name='pills')
async def update_pill_title(collection, pill_id: str, new_title: str) -> None:

    return collection.update_one(
        {'_id': ObjectId(pill_id)},
        {'$set': {'title': new_title}}
    )
