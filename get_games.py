import requests, pprint, os, random

dir = os.path.abspath(os.curdir)


def get_tags(game_data):
    all_tag_list = []
    for tag in game_data['tags']:
        if tag['language'] == 'rus':
            all_tag_list.append(tag['name'])
    return ' , '.join(all_tag_list)

def get_platforms(game_data):
    platforms = []
    for platform in game_data['platforms']:
        platforms.append(platform['platform']['name'])
    return ' , '.join(platforms)

def get_game(name, tag=None):
    if name is not None:
        with open(dir + '\\data\\links\\games.txt', 'r', encoding="utf-8") as file:
            url = file.read().split('\n')[0].replace('XXXX', name)

        reqest = requests.get(url)
        game_data = reqest.json()['results'][0]
        
    else:
        game_data = get_random_game(tag)
    
    full_name = game_data['name']
    tag_list = get_tags(game_data)
    platforms = get_platforms(game_data)
    released = game_data['released']
    image = game_data['background_image']
    metacritic_ball = game_data['metacritic']

    return full_name, image, released, tag_list, platforms, metacritic_ball


def get_random_game(tag):
    with open(dir + '\\data\\links\\games.txt', 'r', encoding="utf-8") as file:
        file_data = file.read().split('\n')
        url_1 = file_data[1]
        if tag is None:
            url_2 = file_data[2]
        else:
            url_2 = file_data[2] + '&tags=' + tag

    count_reqest = requests.get(url_1)
    count = count_reqest.json()['count']

    random_page_number = str(random.randint(1, count))
    
    game_data_reqest = requests.get(url_2.replace('XXXX', random_page_number))
    game_data = game_data_reqest.json()['results'][0]

    return game_data


