import asyncio

import get_data
import discord
from discord.ext import commands

import random, os
import yt_dlp

import get_data, events, get_weather

class Analyzer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.list_of_the_unclear_answers = get_data.get_list_of_the_unclear_answers()
        self.answer_vc_error = get_data.VS_error()
        self.commands_object = ['']
        self.city = 'Москва'
        self.dir = os.path.abspath(os.curdir)
        self.ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
                          }],
        }
        self.guilds = None
        print("inited")


    @commands.command(name='измени')
    async def change(self, ctx,  *, message:str):
        key_word = message.split(' на ')[0]
        value = message.split(' на ')[1]

        if key_word.lower() == 'город':
            self.city = value
            await ctx.send(f'Установлен город {value}')
        else:
            await ctx.send(f'Как мне это исрользовать?'
                           f'вызывай /-помоги, чтобы узнать, что можно поменять!')


    @commands.command(name='напиши')
    async def write(self, ctx, line, count):
        try:
            for _ in range(int(count)):
                await ctx.send(line)
        except:
            await ctx.send(random.choice(self.list_of_the_unclear_answers))


    @commands.command(name='зайди')
    async def join(self, ctx):
        try:
            if ctx.author.voice is None:
                await ctx.send(random.choice(self.answer_vc_error))
                return
            channel = ctx.author.voice.channel
            self.voice_client = await channel.connect()
        except Exception as error:
            print(error)
            await ctx.send(random.choice(self.list_of_the_unclear_answers))


    @commands.command(aliases=['уходи', 'кыш'])
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
        except:
            await ctx.send('меня уже выгнали!')


    @commands.command(name='запусти')
    async def play_song(self, ctx, url):
        try:
##          audio_source = discord.FFmpegPCMAudio(f'{self.dir}\\data\\music\\{name}.mp3', executable=f"{self.dir}\\data\\ffmpeg\\bin\\ffmpeg.exe")
##          self.voice_client.play(audio_source)
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                song_info = ydl.extract_info(url, download=False)
                
            if self.voice_client.is_playing():
                self.voice_client.stop()
                
            self.voice_client.play(discord.FFmpegPCMAudio(song_info["url"], executable=f"{self.dir}\\data\\ffmpeg\\bin\\ffmpeg.exe"))

        except Exception as error:
            print(error)
            await ctx.send('я этого не знаю!')


    @commands.command(name='хватит')
    async def end_song(self, ctx):
        try:
            if self.voice_client.is_playing():
                self.voice_client.stop()
                await ctx.send('Ладно, так и быть')
            else:
                await ctx.send('Это не я. Отстань!')
        except Exception as error:
            print(error)


    @commands.command(name='погода')
    async def weather(self, ctx, *, message:str):
        if 'сегодня' in message.lower():
            await ctx.send(get_weather.current(self.city))
        elif 'завтра' in message.lower():
            try:
                await ctx.send(get_weather.forecast(self.city, 2).split('--------------------------\n')[1])
            except Exception as error:
                print(error)
        elif 'недел' in message.lower():
            await ctx.send(get_weather.forecast(self.city, 5))
        else:
            await ctx.send(random.choice(self.list_of_the_unclear_answers))

    @commands.command(name='найди', description="Ищет пользователя по имени")
    async def get_user(self, ctx, user_name: str):
        print("is this true?")
        channel = commands.Bot.get_all_members(self.bot)
        found = False
        for i in channel:
            if user_name in i.name:
                await ctx.send(f"Пользователь {i.name}, идентификатор {i.id}")
                found = True
                break
        if not found:
            await ctx.send(f"Ничего не нашел :sob:")

    @commands.command(name='пользователи', description="Печатает всех пользователей на сервере")
    async def get_users(self, ctx):
        print("is this true?")
        channel = commands.Bot.get_all_members(self.bot)
        if not channel:
            await ctx.send(f"Ничего не нашел :sob:")
            return
        for i in channel:
            await ctx.send(f"Пользователь {i.name}, идентификатор {i.id}")

    @commands.command(name='напиши-секрет', description="пока что ничего не находит смх")
    async def secret_dm(self, ctx, user_id, *message):
        """пока что ничего не находит смх"""
        try:
            user_id = int(user_id)
        except Exception:
            channel = commands.Bot.get_all_members(self.bot)
            found = False
            for i in channel:
                if user_id in i.name:
                    user_id = i.id
                    found = True
                    break
            if not found:
                await ctx.send(f"Ничего не нашел :sob: \nНе смог отправить сообщение")
                await ctx.message.delete()
        user = commands.Bot.get_user(self.bot, user_id)
        dm = await user.create_dm()
        dm.recipient = user
        await dm.send(f"Аноним: {' '.join(message)}")
        await ctx.message.delete()
        await ctx.send(f"Сообщение '{' '.join(message)}' отправлено адресату {user.name}!")


