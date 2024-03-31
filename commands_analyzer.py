import asyncio

import get_data
import discord
from discord.ext import commands

import random, os
import yt_dlp

import get_data

class Analyzer_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.list_of_the_unclear_answers = get_data.get_list_of_the_unclear_answers()
        self.answer_vc_error = get_data.VS_error()
        self.commands_object = ['']
        self.dir = os.path.abspath(os.curdir)
        self.ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
                          }],
        }

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
                
            ctx.voice_client.play(discord.FFmpegPCMAudio(song_info["url"], executable=f"{self.dir}\\data\\ffmpeg\\bin\\ffmpeg.exe"))

        except Exception as error:
            print(error)
            await ctx.send('я этого не знаю!')

    @commands.command(name='хватит')
    async def end_song(self, ctx):
        if self.voice_client.is_playing():
            self.voice_client.stop()
            await ctx.send('Ладно, так и быть')
        else:
            await ctx.send('Это не я. Отстань!')
            
    @commands.command(name='тест')
    async def mycustomstatus(self, ctx):
        for s in ctx.author.activities:
            if isinstance(s, discord.CustomActivity):
                await ctx.send(s)

