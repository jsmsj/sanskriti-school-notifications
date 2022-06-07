import aiohttp
from bs4 import BeautifulSoup


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

def remove_tags(html):
  
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
  
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)