import discord
import os
from keep_alive import keep_alive
from discord.ext import commands

client = commands.Bot(command_prefix=':', self_bot=True, help_command=None)

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online)

keep_alive()
client.run(os.getenv("TOKEN"), bot=False)
