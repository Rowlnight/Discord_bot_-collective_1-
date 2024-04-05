import asyncio
import discord
from discord.ext import commands
import discord.utils

import logging
import random

import get_data, commands_analyzer, events


TOKEN = input('Введите токен бота: ')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/-', intents=intents)

async def main():
    await bot.add_cog(commands_analyzer.Analyzer(bot))
    await bot.add_cog(events.Events(bot))
    await bot.start(TOKEN)


asyncio.run(main())
