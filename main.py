import asyncio
import discord
from discord.ext import commands, tasks
import discord.utils
import sys

import logging
import random, os, yt_dlp, time, datetime

import get_data, get_weather, current_day_info
import get_youtube_video

dir = os.path.abspath(os.curdir)

TOKEN = sys.argv[1]

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/-', intents=intents)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dir = os.path.abspath(os.curdir)
        self.obscene_words = {}
        self.all_channel = []

        self.list_of_the_unclear_answers = get_data.get_list_of_the_unclear_answers()
        self.answer_vc_error = get_data.VS_error()
        self.commands_object = ['']
        
        self.dir = os.path.abspath(os.curdir)
        self.command_permission_on_vc = False

        self.city = 'Москва'
        self.morning_words_is_sent = False
        self.main_bot_channel = None
        self.morning_time = '9:00'

        self.game_event_time = '18:30'
        self.game_event_words_is_sent = False
        type_day, note, self.week_day = current_day_info.get_current_day_info()
        
        self.ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
                          }],
        }

        self.automatic_function.start()

    @tasks.loop(seconds=10)
    async def automatic_function(self):
        try:
            channel = self.main_bot_channel
            
            if channel is not None:
                if str(datetime.datetime.today().strftime('%H:%M')) == self.morning_time and not self.morning_words_is_sent:
                    self.morning_words_is_sent = True
                    type_day, note, week_day = current_day_info.get_current_day_info()
                    self.week_day = week_day
                    await channel.send(f'------------------------------------------------------------------------\n'
                                       f'{get_data.base_good_morning()}\n{get_weather.current(self.city)}'
                                       f'\n\n{get_data.for_quote_words()}\n{get_data.get_random_quote()}\n'
                                       f'------------------------------------------------------------------------')
                if self.morning_words_is_sent and str(datetime.datetime.today().strftime('%H:%M')) != self.morning_time:
                    self.morning_words_is_sent = False
                    
                if str(datetime.datetime.today().strftime('%H:%M')) == self.game_event_time and not self.game_event_words_is_sent and week_day == 'пт':
                    self.game_event_words_is_sent = True
                    game = get_data.get_game_for_event(None)
                    await channel.send(f'------------------------------------------------------------------------\n{game[0]}\n')
                    await channel.send(game[1])
                    await channel.send(game[2])
                    await channel.send(f'{game[3]}\n------------------------------------------------------------------------')
                if self.game_event_words_is_sent and str(datetime.datetime.today().strftime('%H:%M')) != self.morning_time:
                    self.game_event_words_is_sent = False

            
                        
        except Exception as error:
            self.main_bot_channel = None
            print(error)

            
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author == self.bot.user:
                return
            
            if '/-' in message.content and random.randint(1, 5) == 2 and self.main_bot_channel is None:
                await message.channel.send(get_data.get_warning(1))
                
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        try:
            VoiceChannel_id = after.channel.id
        except Exception as error:
            VoiceChannel_id = before.channel.id
            
        channel = self.bot.get_channel(VoiceChannel_id)
        name = member.name
        
        members_names = []
        members = channel.members
        count_of_members = len(members)
        for member in members:
            members_names.append(member.name)

        try:
            if before.channel is not None:
                old_channel = self.bot.get_channel(before.channel.id)
                before_count_of_members = len(old_channel.members)
            else:
                before_count_of_members = 0

            if after.channel is not None:
                new_channel = self.bot.get_channel(after.channel.id)
                after_count_of_members = len(new_channel.members)
            else:
                after_count_of_members = 0

        except Exception as error:
            print(error)
            
            
        print(count_of_members, before_count_of_members)

        try:
            print(name, self.bot.user.name)
            if str(name) != str(self.bot.user.name) and after_count_of_members != before_count_of_members:
                if count_of_members == 1 and str(self.bot.user.name) not in members_names:
                    await asyncio.sleep(5)
                    if len(self.bot.get_channel(VoiceChannel_id).members) == 1:
                        all_files_list = os.listdir(f'{self.dir}\\data\\music\\Sad_moments')
                        self.voice_client = await channel.connect()

                        audio_source = discord.FFmpegPCMAudio(f'{self.dir}\\data\\music\\Sad_moments\\{random.choice(all_files_list)}',
                                                              executable=f"{self.dir}\\data\\ffmpeg\\bin\\ffmpeg.exe")

                        self.voice_client.play(audio_source)

                elif ((count_of_members > 1 and str(self.bot.user.name) in members_names and self.command_permission_on_vc is False)
                      or (count_of_members == 1 and str(self.bot.user.name) in members_names)):
                    
                    await self.voice_client.disconnect()
                    
        except Exception as error:
            print(error)

##############################################################################################################################################################################################
    
    @commands.command(name='пиши')
    async def change_text_channel(self, ctx, place):
        if place in ['сюда', 'здесь', 'тут']:
            self.main_bot_channel = ctx
            await ctx.send(f'Всё, что не касается ответов буду стараться писать сюда.')
        else:
            await ctx.send(random.choice(self.list_of_the_unclear_answers))
        
    @commands.command(name='измени')
    async def change(self, ctx,  *, message:str):
        key_word = message.split(' на ')[0]
        value = message.split(' на ')[1]

        if key_word.lower() == 'город':
            self.city = value
            await ctx.send(f'Установлен город {value}')
            
        elif key_word.lower() == 'утро':
            try:
                if len(value.split(':')[0]) == len((value.split(':')[1])) == 2:
                    int(value.split(':')[0]) + int((value.split(':')[1]))
                    self.morning_time = value
                    await ctx.send(f'Теперь утреннее приветствие будет начинаться в {value}')
                else:
                    await ctx.send('Неверный формат времени, вызывай "/-помоги", чтобы узнать верный!')
            except Exception as error:
                await ctx.send('Неверный формат времени, вызывай "/-помоги", чтобы узнать верный!')
            
        else:
            await ctx.send(f'Как мне это исрользовать?'
                           f'вызывай "/-помоги", чтобы узнать, что можно поменять!')

    @commands.command(name='заспамь')
    async def spam(self, ctx, *, message:str):
        count = int(message.split()[-1])
        line = ' '.join(message.split()[:-1])
        for _ in range(int(count)):
            await ctx.send(line)
            await asyncio.sleep(1)

    @commands.command(aliases=['найди', 'поищи', 'тоищи', 'напиши']) 
    async def write(self, ctx, *, message:str):
        try:
            if message in ['цитату', 'факт']:
                await ctx.send(f'------------------------------------------------------------------------\n'
                               f'{get_data.get_random_quote()}\n'
                               f'------------------------------------------------------------------------')
                
            elif message.split()[0] in ['игру', 'игрушку', 'тайтл']:
                if len(message.split()) == 1:
                    game_name = None
                else:
                    game_name = ' '.join(message.split()[1:])
                game = get_data.get_game_command(game_name)
                await ctx.send(f'------------------------------------------------------------------------\n{game[0]}\n')
                await ctx.send(game[1])
                await ctx.send(game[2])
                await ctx.send(f'{game[3]}\n------------------------------------------------------------------------')

            elif message.split()[0] in ['пользователя', 'юзера', 'придурка']:
                channel = commands.Bot.get_all_members(self.bot)
                found = False
                for i in channel:
                    if message.split()[1] in i.name:
                        await ctx.send(f"Пользователь {i.name}, идентификатор {i.id}")
                        found = True
                        break
                if not found:
                    await ctx.send(f"Ничего не нашел :sob:")

            elif message.split()[0] in ['пользователей', 'юзеров', 'придурков']:
                channel = commands.Bot.get_all_members(self.bot)
                if not channel:
                    await ctx.send(f"Ничего не нашел :sob:")
                    return
                for i in channel:
                    await ctx.send(f"Пользователь {i.name}, идентификатор {i.id}")

            elif message.split()[0] in ['видео', 'видос', 'видосик']:
                await ctx.send(get_youtube_video.get_video(" ".join(message.split()[1:])))
                
           
        except Exception as error:
            print(error)
            await ctx.send(random.choice(self.list_of_the_unclear_answers))

    @commands.command(name='зайди')
    async def join(self, ctx):
        try:
            if ctx.author.voice is None:
                await ctx.send(random.choice(self.answer_vc_error))
                return
            channel = ctx.author.voice.channel
            self.voice_client = await channel.connect()
            self.command_permission_on_vc = True
        except Exception as error:
            print(error)
            await ctx.send(random.choice(self.list_of_the_unclear_answers))

    @commands.command(aliases=['уходи', 'кыш'])
    async def leave(self, ctx):
        try:
            self.command_permission_on_vc = False
            await ctx.voice_client.disconnect()
        except:
            await ctx.send('меня уже выгнали!')

    @commands.command(name='запусти')
    async def play_song(self, ctx, *url):
        try:
            if not url[0].startswith("https://"):
                url = get_youtube_video.get_video(" ".join(url))

            if self.voice_client.is_playing():
                self.voice_client.stop()

            await ctx.send(get_data.get_random_soon_words())

            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                song_info = ydl.extract_info(url[0], download=False)

            self.voice_client.play(
                discord.FFmpegPCMAudio(song_info["url"], executable=f"{self.dir}\\data\\ffmpeg\\bin\\ffmpeg.exe"))

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
            await ctx.send(random.choice(self.list_of_the_unclear_answers))
            
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

    @commands.command(name='напиши-секрет', description="Анонимно пишет в личку пользователя сообщение")
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
        await ctx.send(f"Сообщение ({' '.join(message)}) отправлено адресату {user.name}!")

    @commands.command(name='аватарка', description="Получи аватарку пользователя!")
    async def get_avatar(self, ctx, user):
        user = get_data.find_user(self.bot, user)
        if user:
            await ctx.send(f"Вот: {user.display_avatar.url}")
        else:
            await ctx.send(f"Нет такого пользователя! Бесишь!")



async def main():
    await bot.add_cog(Events(bot))
    await bot.start(TOKEN)


asyncio.run(main())
