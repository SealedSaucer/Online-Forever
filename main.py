import discord, os, keep_alive, asyncio, datetime, requests
from discord.ext import tasks, commands
from keep_alive import keep_alive

client = commands.Bot(
  command_prefix=':',
  self_bot=True
)

async def on_ready():
    client.remove_command('help')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("TESTING"))

keep_alive()
client.run(os.getenv("TOKEN"), bot=False)
