import aiohttp
import asyncio
import requests
import time

nav_url = "http://www.sanskritischool.edu.in/assets/json/navigation.json"
updates_url = "http://www.sanskritischool.edu.in/assets/json/updates.json"
base = "http://www.sanskritischool.edu.in"

async def get_nav_content():
    async with aiohttp.ClientSession() as session:
        resp = await session.get(nav_url,ssl=False)
        return await resp.json()

async def get_updates_content():
    async with aiohttp.ClientSession() as session:
        resp = await session.get(updates_url,ssl=False)
        return await resp.json()

def get_href(path):
    if path.startswith("/"):
        return base + path
    elif path =="":
        return base
    else:
        return path