import asyncio
import motor.motor_asyncio
import json
import pymongo


async def do_insert_and_index():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://fynd_admin:fynd123@localhost:27017/admin")
    db = client.admin
    data = json.load(open("imdb.json", "r"))
    await db.movies.insert_many(data)
    await db.movies.create_index([('name', pymongo.TEXT)], name='search_index')

asyncio.run(do_insert_and_index())
