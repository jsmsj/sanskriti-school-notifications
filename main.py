from dotenv import load_dotenv
from itertools import cycle
from discord.ext import commands,tasks
import discord
import os
import embed_generators as emg
from discord.ext import pages
from databasefuncs import *
from websitefuncs import *
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=os.environ.get("PREFIX"),intents=intents, case_insensitive=True,help_command=None)

ls_activities = cycle(["sanskritischool.edu.in",f"{os.environ.get('PREFIX')}help"])

@tasks.loop(seconds=60)
async def status_swap():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=next(ls_activities)))

@bot.event
async def on_ready():
    check_new_notifs.start()
    status_swap.start()
    print("Bot is ready!")

@bot.event
async def on_guild_join(guild:discord.Guild):
    # overwrites = {
    #     guild.default_role:discord.PermissionOverwrite(send_messages=False)
    # }
    channel = await guild.create_text_channel(name="sanskriti-school-notifications",reason=f"Channel Created by Sanskriti School Notifications Bot, to post the new circulars and updates present on the website {base}. Do not change the name of the channel, else the bot will create a new channel to post to.",position=0) #overwrites=overwrites,


@bot.command()
async def site(ctx):
    ems = await emg.generate_navigation_embeds_list(ctx.author)
    paginator = pages.Paginator(pages=ems)
    await paginator.send(ctx)

@bot.command(aliases=['news','updates'])
async def circulars(ctx):
    ems = await emg.generate_x_embed_list('news',ctx.author)
    paginator = pages.Paginator(pages=ems)
    await paginator.send(ctx)

@bot.command()
async def cbse(ctx):
    ems = await emg.generate_x_embed_list('CBSEdoe',ctx.author)
    paginator = pages.Paginator(pages=ems)
    await paginator.send(ctx)

@bot.command()
async def achievements(ctx):
    ems = await emg.generate_x_embed_list("achievements",ctx.author)
    paginator = pages.Paginator(pages=ems)
    await paginator.send(ctx)

@bot.command()
async def sports(ctx):
    ems = await emg.generate_x_embed_list("sports",ctx.author)
    paginator = pages.Paginator(pages=ems)
    await paginator.send(ctx)

@bot.command()
async def source(ctx):
    await ctx.send("https://github.com/jsmsj/sanskriti-school-notifications")

@bot.command()
async def info(ctx):
    emb = discord.Embed(title="About Me",color=discord.Color.green())
    emb.description = "This bot was created with the purpose of sending the announcements made on the website directly to discord, for better accessibility.\nThe announcements are sent to the set discord channel. Along with that, the bot also has features to retrieve the last 15 announcements made in all avaialble categories."
    emb.add_field(name="Help command",value=f"`{os.environ.get('PREFIX')}help`")
    emb.add_field(name="Source Code",value="[Github](https://github.com/jsmsj/sanskriti-school-notifications)")
    emb.add_field(name="Creater",value="<@!713276935064649792>")
    emb.set_footer(text="This bot is not affiliated with, endorsed or sponsored by Sanskriti School.")
    await ctx.send(embed=emb)

@bot.group(invoke_without_command = True)
async def help(ctx):
    await ctx.send(embed=emg.generate_help(ctx.author))

@help.command()
async def site(ctx):
    await ctx.send(embed=emg.generate_help(ctx.author,'site'))

@help.command()
async def circulars(ctx):
    await ctx.send(embed=emg.generate_help(ctx.author,'circulars'))

@help.command()
async def cbse(ctx):
    await ctx.send(embed=emg.generate_help(ctx.author,'cbse'))

@help.command()
async def achievements(ctx):
    await ctx.send(embed=emg.generate_help(ctx.author,'achievements'))

@help.command()
async def sports(ctx):
    await ctx.send(embed=emg.generate_help(ctx.author,'sports'))

@help.command()
async def source(ctx):
    await ctx.send(embed=emg.generate_help(ctx.author,'source'))

@help.command()
async def info(ctx):
    await ctx.send(embed=emg.generate_help(ctx.author,'info'))

@tasks.loop(minutes=1)
async def check_new_notifs():
    res = await get_updates_content()
    categories = []
    most_recent_item = []
    for key,value in res.items():
        categories.append(key)
        most_recent_item.append(value['items'][0])
    most_recent = zip(categories,most_recent_item)
    for i in most_recent:
        last_kn_x = await find_x(i[0])
        if not last_kn_x:
            await insert_x(i[0],"alive")
        else:
            cntnt = i[1]['message'] + i[1]['date']
            if not cntnt == last_kn_x['content']:
                emb = await emg.generate_notification_embed(i)
                for guild in bot.guilds:
                    sent = False
                    for channel in guild.channels:
                        if channel.name == "sanskriti-school-notifications":
                            await channel.send(embed=emb)
                            sent = True
                    if not sent:
                        # overwrites = {
                        #         guild.default_role:discord.PermissionOverwrite(send_messages=False)
                        #     }
                        ch = await guild.create_text_channel(name="sanskriti-school-notifications",reason=f"Channel Created by Sanskriti School Notifications Bot, to post the new circulars and updates present on the website {base}. Do not change the name of the channel, else the bot will create a new channel to post to.",position=0) #,overwrites=overwrites
                        await ch.send(embed=emb)
                        sent = True
                await update_x(i[0],cntnt)
                
if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # i.e. its not being imported from another python file run this
    bot.run(os.environ.get("TOKEN"))