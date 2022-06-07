from dotenv import load_dotenv
from discord.ext import commands
import discord
import os
import embed_generators as emg
from discord.ext import pages

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=os.environ.get("PREFIX"),intents=intents, case_insensitive=True) #TODO help_command=None,

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="sanskritischool.edu.in")) #TODO add a list of activities somewhere
    print("Bot is ready!")

@bot.command()
async def site(ctx):
    ems = await emg.generate_navigation_embeds_list(ctx.author)
    paginator = pages.Paginator(pages=ems)
    await paginator.send(ctx)

@bot.command()
async def circulars(ctx):
    await ctx.send("hi")

@bot.command()
async def cbse(ctx):
    await ctx.send("hi")

@bot.command()
async def achivements(ctx):
    await ctx.send("hi")

@bot.command()
async def sports(ctx):
    await ctx.send("hi")

if __name__ == '__main__':
    # When running this file, if it is the 'main' file
    # i.e. its not being imported from another python file run this
    bot.run(os.environ.get("TOKEN"))