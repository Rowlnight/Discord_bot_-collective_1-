from youtubesearchpython import VideosSearch
import pprint

def get_game_thriller(name):
    try:
        videosSearch = VideosSearch(f'{name} thriller', limit=2)
        if name.lower() in videosSearch.result()['result'][0]['title'].lower():
            return videosSearch.result()['result'][0]['link']
        else:
            return 'Видео в ютубе не обнаружено!'
    except Exception as error:
        return 'Что-то пошло не так!'

def get_video(name):
    try:
        videosSearch = VideosSearch(f'{name}', limit=2)
        print(videosSearch.result()['result'])
        return videosSearch.result()['result'][0]['link']
    except Exception as error:
        return 'Что-то пошло не так!'

