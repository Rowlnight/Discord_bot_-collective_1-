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

def get_data_for_help():
    return ([
            f'Меню помощи:\n'
            f'---Внимание это команды настройки бота. Настоятельно рекомендуется прочитать и настроить перед использованием:\n'
            f'--------------------------\n'
            f'/-пиши\n'
            f'    Команда установки необходимая для установки основного канала бота\n'
            f'    Необходимо для проведения случайных событий.\n'
            f'    Принимает аргументы:\n'
            f'        [сюда, здесь, тут] - для задания канала в котором написано сообщение.\n'
            f'        Пример: "/-пиши сюда"\n'
            f'--------------------------\n\n'
            f'/-измени\n'
            f'    Команда установки необходимая для изменения некоторых переменных.\n'
            f'    Принимает аргументы:\n'
            f'        город - изменение города, для определения погоды и праздников\n'
            f'        Пример: "/-измени город на Иваново"\n'
            f'        --------------------------\n'
            f'        утро  - для изменения времени утреннего приветствия\n'
            f'        Пример: "/-измени утро на 10:00"\n\n'
            f'--------------------------\n'
            f'---Остальные команды:\n'
            f'--------------------------\n\n'
            f'/-заспамь\n'
            f'    Команда говорит сама за себя.\n'
            f'    Пишет в чат одно и тоже сообщение несколько раз.\n'
            f'    Пример: "/-заспамь какое-то сообщение 5"\n'
            f'--------------------------\n\n'
            f'/-[найди, поищи, покажи, напиши]\n'
            f'    Команда поиска.\n'
            f'    Принимает аргументы:\n'
            f'        [цитату, факт] - для поиска рандомной цитаты\n'
            f'            Пример: "/-найди цитату"\n'
            f'        --------------------------\n'
            f'        [игру, игрушку, тайтл] - для поиска игры\n'
            f'            Пример: "/-найди игру rdr2" - найдёт игру rdr2\n'
            f'            Пример: "/-найди игру" - найдёт абсолютно рандомную игру с сайта rawg.io (придётся немного подождать)\n'
            f'        --------------------------\n'
            f'        [пользователя, юзера, придурка] - для поиска информации о пользователе\n'
            f'            Пример: "/-найди пользователя имя пользователя"\n'
            f'        --------------------------\n'
            f'        [пользователей, юзеров, придурков] - для поиска информации о всех пользователях\n'
            f'            Пример: "/-найди пользователей"\n'
            f'        --------------------------\n'
            f'        [видео, видос, видосик] - для поиска видео на ютубе\n'
            f'            Пример: "/-найди видео название видео"\n'
            f'--------------------------\n\n',
            f'/-зайди\n'
            f'    призывает бота в голосовой канал автора сообщения\n'
            f'    Пример: "/-зайди" - нужно находится в голосовом канале\n'
            f'--------------------------\n\n'
            f'/-[уходи, кыш]\n'
            f'    Выгоняет бота из голосового канала\n'
            f'    Пример: "/-уходи"\n'
            f'--------------------------\n\n'
            f'/-запусти\n'
            f'    находясь в голосовом канале бот запускает музыку\n'
            f'    сперва бота нужно позвать командой "/-зайди"\n'
            f'    Пример: "/-запусти ссылка на ютуб видео" - запускает звук с точного видео по ссылке\n'
            f'    Пример: "/-запусти название песни" - запускает звук с первого видео по запросу на ютуб\n'
            f'--------------------------\n\n'
            f'/-хватит\n'
            f'    бот прикращает играть музыку\n'
            f'    Пример: "/-хватит"\n'
            f'--------------------------\n\n'
            f'/-погода\n'
            f'    Бот показывает погоду с сайта openweathermap.org\n'
            f'    Принимает аргументы:\n'
            f'        сегодня - показывает погоду на сегодня\n'
            f'            Пример: "/-погода на сегодня"\n'
            f'        --------------------------\n'
            f'        завтра - показывает погоду на завтра\n'
            f'            Пример: "/-погода на завтра"\n'
            f'        --------------------------\n'
            f'        неделю - показывает погоду на неделю\n'
            f'            Пример: "/-погода на неделю"\n'
            f'--------------------------\n\n'
            f'/-напиши-секрет\n'
            f'    анонимно пишет в личку пользователя сообщение\n'
            f'        Пример: "/-напиши-секрет id поользователя сообщение" - отправит сообщение по id пользователя\n'
            f'        Пример: "/-напиши-секрет имя пользователя сообщение" - отправит сообщение по имени пользователя\n'
            f'--------------------------\n\n'
            f'/-аватарка\n'
            f'    Получи аватарку пользователя!\n'
            f'        Пример: "/-аватарка id ользователя" - получит аватарку по id пользователя\n'
            f'        Пример: "/-аватарка имя пользователя" - получит аватарку по имени пользователя\n'
            ])

    
