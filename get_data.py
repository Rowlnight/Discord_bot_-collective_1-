import os, requests, datetime, random
import current_day_info, get_games, get_youtube_video
import discord.ext.commands

dir = os.path.abspath(os.curdir)


def get_list(way):
    with open(dir + way, 'r', encoding="utf-8") as file:
        result = file.read().split('\n')
    return result

def VS_error():
    return get_list('\\data\\text\\answers\\VC_error.txt')

def get_list_of_the_unclear_answers():
    return get_list('\\data\\text\\answers\\unclear.txt')

def get_random_soon_words():
    return random.choice(get_list('\\data\\text\\answers\\Please_wait.txt'))

def get_random_quote():
    with open(dir + '\\data\\links\\random_quote.txt', 'r', encoding="utf-8") as file:
        url = file.read()

    reqest = requests.get(url)
    
    if reqest.status_code == 404:
        return 'сайта больше нет!'
    else:
        quote_data = reqest.json()
        Author = quote_data['Author']
        Quote = quote_data['Quote']
        
        return (f'Как говорил {Author}:\n'
                f'{Quote}')
  
def base_good_morning():
    type_day, note, week_day = current_day_info.get_current_day_info()
    
    hello_words = get_list('\\data\\text\\morning\\hello_words.txt')
    info_words = get_list('\\data\\text\\morning\\about_day.txt')
    fest_words = f'Поздравляю всех с праздником: {note}' if note is not None else 'Государственных праздников сегодня нет'
    weather_words = get_list('\\data\\text\\morning\\weather_words.txt')
        
    return (f'{random.choice(hello_words)}\n\n'
            f'{random.choice(info_words)} {week_day}, {type_day}\n'
            f'{fest_words}.\n\n'
            f'{random.choice(weather_words)}')

def get_game_command(name):
    if name is None:
        head = random.choice(get_list('\\data\\text\\answers\\Random_game_search.txt'))
    else:
        head = random.choice(get_list('\\data\\text\\answers\\Game_search.txt'))
        
    full_name, image, released, tag_list, platforms, metacritic_ball = get_games.get_game(name)
    video = get_youtube_video.get_game_thriller(full_name)
    return [f'{head}\n\n'
            f'Название: {full_name}',
            f'Обложка: {image}',
            f'Видео: {video}',
            f'Дата выхода: {released}\n\n'
            f'Жанры: {tag_list}\n\n'
            f'Платформы: {platforms}\n'
            f'Балл на метакритике: {metacritic_ball}\n']

def get_game_for_event(name):
    head = random.choice(get_list('\\data\\text\\weekend_event\\random_online game_(weekend_event).txt'))
    full_name, image, released, tag_list, platforms, metacritic_ball = get_games.get_game(name, 'multiplayer')
    video = get_youtube_video.get_game_thriller(full_name)
    return [f'{head}\n\n'
            f'Название: {full_name}',
            f'Обложка: {image}',
            f'Видео: {video}',
            f'Дата выхода: {released}\n\n'
            f'Жанры: {tag_list}\n\n'
            f'Платформы: {platforms}\n'
            f'Балл на метакритике: {metacritic_ball}\n']

def for_quote_words():
    words = random.choice(get_list('\\data\\text\\morning\\for_quote_words.txt'))
    return words

def get_warning(id):
    if id == 1:
        return (f'Напоминаю, что мне нужно сказать куда я могу писать!\n'
                f'Это нужно для проведения различных событий, например утреннего приветствия.\n'
                f'Сделать это можно написав "/-пиши сюда" в нужный канал!\n')
    else:
        return f'Что-то не так, но не могу понять что.'

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

    
