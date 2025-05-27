from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test_connection():
    client = AsyncIOMotorClient("MONGODB_URI")
    db = client["DATABASE_NAME"]
    try:
        collections = await db.list_collection_names()
        print("Collections:", collections)
    except Exception as e:
        print("Error:", e)

asyncio.run(test_connection())
