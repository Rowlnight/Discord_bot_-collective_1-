import asyncio
import discord
from discord.ext import commands
import discord.utils
import sys

import logging
import random

import get_data
from commands_analyzer import Analyzer
from events import Events

args = sys.argv

# kleiner token:
ANOTHER_TOKEN = args[1]
TOKEN = args[2]

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

async def main():
    await bot.add_cog(Analyzer(bot))
    await bot.add_cog(Events(bot))
    await bot.start(TOKEN)


asyncio.run(main())
