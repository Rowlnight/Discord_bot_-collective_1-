import asyncio

import get_data
import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author == self.bot.user:
                return
            print(message.author) #prints author of the message
            await message.channel.send("Спокойной ночи тебе!")
        except Exception as error:
            print(error)
