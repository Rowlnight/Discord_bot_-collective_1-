import os

import discord.ext.commands

dir = os.path.abspath(os.curdir)


def VS_error():
    with open(dir + '\\data\\text\\answers\\VC_error.txt', 'r', encoding="utf-8") as file:
        result = file.read().split('\n')
    return result


def get_list_of_the_unclear_answers():
    with open(dir + '\\data\\text\\answers\\unclear.txt', 'r', encoding="utf-8") as file:
        result = file.read().split('\n')
    return result


def find_user(bot, user):
    try:
        user_id = int(user)
        return discord.ext.commands.Bot.get_user(bot, user_id)
    except Exception:
        found_users = list(filter(lambda x: user in x.name, discord.ext.commands.Bot.get_all_members(bot)))
        print(found_users)
        if found_users:
            return found_users[0]
        return
