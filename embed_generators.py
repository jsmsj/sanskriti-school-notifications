from websitefuncs import *
import discord
import datetime
import itertools
import urllib.parse
from dotenv import  load_dotenv
import os
load_dotenv()

def make_timestamp(date:str):
    date += " 12:00:00"
    tz = datetime.timezone(datetime.timedelta(hours=5.5))
    dtobj = datetime.datetime.strptime(date,"%d/%m/%Y %H:%M:%S").replace(tzinfo=tz)
    return round(dtobj.timestamp())


async def generate_navigation_embeds_list(author:discord.Member):
    resp = await get_nav_content()
    list_of_embeds = []
    master = discord.Embed(title="Index",color=discord.Colour.green())
    master.set_thumbnail(url=author.display_avatar)
    master.set_footer(text=f"Command invoked by {author.display_name}")
    master_desc = "```yaml\nThe serial number tells the position of the corrosponding section.\nUse the buttons to navigate.\n```\n__1.__ **Index of pages availabe**\n"
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

async def generate_x_embed_list(x,author:discord.Member):
    possible_x = {
        'news':"Circulars and Updates",
        'CBSEdoe':"CBSE & DoE Circulars",
        'achievements':'Achievements & Activities',
        'sports':'Sports Corner'
    }
    res = await get_updates_content()
    resp = res[x]
    list_of_embeds = []
    temp = itertools.islice(resp['items'],0,15)
    for val in temp:
        em = discord.Embed(title=f"{possible_x[x]} ({val['date']})",color=discord.Color.green(),timestamp=datetime.datetime.now())
        em.set_footer(text=f"Command invoked by {author.display_name}")
        desc = f"*<t:{make_timestamp(val['date'])}:R>*\n\n"
        text = remove_tags(val["message"].replace("<br>","\n"))
        if val['type'] == "text":
            desc += text
        elif val['type'] == "link":
            lnk = val['href']
            if lnk.startswith("http"):
                nlnk = lnk
            else:
                nlnk = get_href(urllib.parse.quote(val['href']))
            desc += f"[{text}]({nlnk})"
        em.description = desc
        list_of_embeds.append(em)
    master = discord.Embed(title=possible_x[x],description=f"Use the buttons to navigate through the most recent 15 circulars. To view the rest kindly visit the [school website]({base})",color=discord.Color.green())
    master.set_thumbnail(url=author.display_avatar)
    master.set_footer(text=f"Command invoked by {author.display_name}")
    list_of_embeds.insert(0,master)
    return list_of_embeds

async def generate_notification_embed(notif_data):
    possible_x = {
        'news':"Circulars and Updates",
        'CBSEdoe':"CBSE & DoE Circulars",
        'achievements':'Achievements & Activities',
        'sports':'Sports Corner'
    }
    emb = discord.Embed(title=f"{possible_x[notif_data[0]]} ({notif_data[1]['date']})",color=discord.Color.green(),timestamp=datetime.datetime.now())
    desc = f"*<t:{make_timestamp(notif_data[1]['date'])}:R>*\n\n"
    text = remove_tags(notif_data[1]["message"].replace("<br>","\n"))
    if notif_data[1]['type'] == "text":
        desc += text
    elif notif_data[1]['type'] == "link":
        lnk = notif_data[1]['href']
        if lnk.startswith("http"):
            nlnk = lnk
        else:
            nlnk = get_href(urllib.parse.quote(notif_data[1]['href']))
        desc += f"[{text}]({nlnk})"
    emb.description = desc
    return emb

def generate_help(author:discord.Member,cmd=None):
    if not cmd:
        emb = discord.Embed(title="Help is here",color=discord.Color.green(),timestamp=datetime.datetime.now())
        emb.set_author(name=author.display_name,icon_url=author.display_avatar)
        emb.set_footer(text="This bot is not affiliated with, endorsed or sponsored by Sanskriti School.")
        emb.set_thumbnail(url="https://i.imgur.com/Mh4PoJ5.png")
        emb.description = f"Run `{os.environ.get('PREFIX')}help <command_name>` for extended help on that particular command"
        emb.add_field(
            name="Navigate through the website",
            value=f"`{os.environ.get('PREFIX')}site`"
        )
        emb.add_field(
            name="Check recent circulars",
            value=f"`{os.environ.get('PREFIX')}circulars`"
        )
        emb.add_field(
            name="See CBSE announcements",
            value=f"`{os.environ.get('PREFIX')}cbse`"
        )
        emb.add_field(
            name="See recent achievements",
            value=f"`{os.environ.get('PREFIX')}achievements`"
        )
        emb.add_field(
            name="See details about sports",
            value=f"`{os.environ.get('PREFIX')}sports`"
        )
        emb.add_field(
            name="Check out the source code of the bot",
            value=f"`{os.environ.get('PREFIX')}source`"
        )
        emb.add_field(
            name="About me",
            value=f"`{os.environ.get('PREFIX')}info`"
        )
    elif cmd == "site":
        emb = discord.Embed(title="Site command",color=discord.Color.green(),timestamp=datetime.datetime.now())
        emb.set_footer(text=f"Command invoked by {author.display_name}")
        emb.description = "Use this command to navigate through the navigation bar present on sanskriti school website. i.e. Access the links present in this section via discord."
        emb.set_image(url="https://i.imgur.com/sDgDlH7.png")
        emb.add_field(name="Syntax",value=f"`{os.environ.get('PREFIX')}site`")
    elif cmd == "circulars":
        emb = discord.Embed(title="Circulars and Updates command",color=discord.Color.green(),timestamp=datetime.datetime.now())
        emb.set_footer(text=f"Command invoked by {author.display_name}")
        emb.description = "Use this command to see the last 15 circulars posted on the website."
        emb.set_image(url="https://i.imgur.com/c5oH2Zb.png")
        emb.add_field(name="Syntax",value=f"`{os.environ.get('PREFIX')}circulars`")
    elif cmd == "cbse":
        emb = discord.Embed(title="CBSE and DOE circulars command",color=discord.Color.green(),timestamp=datetime.datetime.now())
        emb.set_footer(text=f"Command invoked by {author.display_name}")
        emb.description = "Use this command to see the last 15 circulars issued by CBSE and/or DOE posted on the website."
        emb.set_image(url="https://i.imgur.com/cof5Kuj.png")
        emb.add_field(name="Syntax",value=f"`{os.environ.get('PREFIX')}cbse`")
    elif cmd == "achievements":
        emb = discord.Embed(title="Achievements command",color=discord.Color.green(),timestamp=datetime.datetime.now())
        emb.set_footer(text=f"Command invoked by {author.display_name}")
        emb.description = "Use this command to see the last 15 achivements by students, posted on the website."
        emb.set_image(url="https://i.imgur.com/mj0yyVg.png")
        emb.add_field(name="Syntax",value=f"`{os.environ.get('PREFIX')}achievements`")
    elif cmd == "sports":
        emb = discord.Embed(title="Sports command",color=discord.Color.green(),timestamp=datetime.datetime.now())
        emb.set_footer(text=f"Command invoked by {author.display_name}")
        emb.description = "Use this command to see the last 15 circulars on sports, posted on the website."
        emb.set_image(url="https://i.imgur.com/HZ2SR2n.png")
        emb.add_field(name="Syntax",value=f"`{os.environ.get('PREFIX')}sports`")
    elif cmd=="source":
        emb = discord.Embed(title="Source command",color=discord.Color.green(),timestamp=datetime.datetime.now())
        emb.set_footer(text=f"Command invoked by {author.display_name}")
        emb.description = "Use this command to see my source code."
        emb.add_field(name="Syntax",value=f"`{os.environ.get('PREFIX')}source`")
    elif cmd=="info":
        emb = discord.Embed(title="Info command",color=discord.Color.green(),timestamp=datetime.datetime.now())
        emb.set_footer(text=f"Command invoked by {author.display_name}")
        emb.description = "Use this command to know more about me."
        emb.add_field(name="Syntax",value=f"`{os.environ.get('PREFIX')}info`")
    else:
        emb=discord.Embed(title="Error: Command Not Found",color=discord.Color.green(),timestamp=datetime.datetime.now())
        emb.set_footer(text=f"Command invoked by {author.display_name}")

    return emb
