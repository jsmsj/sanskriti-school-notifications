from websitefuncs import *
import discord
import datetime


async def generate_navigation_embeds_list(author:discord.Member):
    resp = await get_nav_content()
    list_of_embeds = []
    master = discord.Embed(title="Index",color=discord.Colour.green())
    master.set_thumbnail(url=author.display_avatar)
    master.set_footer(text=f"Command invoked by {author.display_name}")
    master_desc = "```yaml\nThe serial number tells the position of the corrosponding section.\n```\n__1.__ **Index of pages availabe**\n"
    t_lst = []
    for key,value in resp.items():
        em = discord.Embed(title=key,color=discord.Color.green(),timestamp=datetime.datetime.now())
        em.set_footer(text=f"Command invoked by {author.display_name}")
        desc = ""
        if type(value) == list:
            for index,item in enumerate(value):
                desc+=f"__{index+1}.__ **[{item['name']}]({get_href(item['href'])})**\n"
        elif type(value) == str:
            desc+=get_href(value) + "\n"
        em.description = desc
        list_of_embeds.append(em)
        t_lst.append(key)
    for idx,k in enumerate(t_lst):
        master_desc+= f"__{idx+2}.__ **{k}**\n"
    master.description = master_desc
    list_of_embeds.insert(0,master)
    return list_of_embeds