import discord
import os
import keep_alive
from discord.ext import commands

client = commands.Bot(command_prefix=':', self_bot=True, help_command=None)


@client.event
async def on_ready():
    # Playing
    # await client.change_presence(activity=discord.Game(name="a game"))

    # Streaming
    # await bot.change_presence(activity=discord.Streaming(name="a Stream", url="http://your-url-here.com/"))

    # Listening
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

    # Watching
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The world burn"))


keep_alive.keep_alive()
client.run(os.getenv("TOKEN"), bot=False)
