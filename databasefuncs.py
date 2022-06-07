import motor.motor_asyncio
import os
from dotenv import  load_dotenv
load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('DBURL'))
db = client['ss_notifications_bot_db']
collection = db['updates_json']

async def insert_x(x,text):
    doc = {"type":x,"content":text}
    result = await collection.insert_one(doc)
    return

async def find_x(x):
    doc = await collection.find_one({"type":x})
    return doc

async def update_x(x,text):
    result = await collection.update_one({"type":x},{"$set":{"type":x,"content":text}})
    return

async def delete_x(x):
    result = await collection.delete_one({"type":x})
    return