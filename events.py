import asyncio
import get_data
import discord
from discord.ext import commands

import random, os, time

import commands_analyzer

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dir = os.path.abspath(os.curdir)
        self.obscene_words = {}
        self.all_channel = []

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author == self.bot.user:
                return
            #print(message.author) #prints author of the message
            #await message.channel.send('Запрещаю!')
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
                    all_files_list = os.listdir(f'{self.dir}\\data\\music\\Sad_moments')
                    commands_analyzer.Analyzer.voice_client = await channel.connect()
                    
                    audio_source = discord.FFmpegPCMAudio(f'{self.dir}\\data\\music\\Sad_moments\\{random.choice(all_files_list)}',
                                                          executable=f"{self.dir}\\data\\ffmpeg\\bin\\ffmpeg.exe")
                    
                    commands_analyzer.Analyzer.voice_client.play(audio_source)
                    
                elif (count_of_members > 1 and str(self.bot.user.name) in members_names) or (count_of_members == 1 and str(self.bot.user.name) in members_names):
                    await commands_analyzer.Analyzer.voice_client.disconnect()
                    
        except Exception as error:
            print(error)


        
