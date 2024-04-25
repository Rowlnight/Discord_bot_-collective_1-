import requests, pprint, datetime, os

dir = os.path.abspath(os.curdir)

def degToCompass(num):
    val = int((num/22.5)+.5)
    arr = ["Север", "Северо-северо-восток", "Северо-восток", "Восток-северо-восток", "Восток",
           "Восточно-юго-восток", "Юго-восток", "Юго-юго-восток", "Юг","Юго-юго-запад", "Юго-запад",
           "Западно-юго-запад", "Запад", "Западно-северо-запад", "Северо-запад", "Северо-северо-запад"]
    return arr[(val % 16)]

def forecast(city, count):
    with open(dir + '\\data\\links\\weather.txt', 'r', encoding="utf-8") as file:
        url = file.read().split('\n')[1].replace('XXXX', city)
    reqest = requests.get(url)

    if reqest.status_code == 404:
        return 'Город указан не верно! Его можно изменить командой: /-измени'
    else:
        weather_data = reqest.json()['list']
        days = [weather_data[0], weather_data[7], weather_data[15], weather_data[23], weather_data[31]]
        result = ''
        for day in days[:count]:
            result = result + get_and_print_weather(day, city, day['dt_txt'].split()[0]) + '\n--------------------------\n'
            
        return result

def current(city):
    with open(dir + '\\data\\links\\weather.txt', 'r', encoding="utf-8") as file:
        url = file.read().split('\n')[0].replace('XXXX', city)
    reqest = requests.get(url)

    if reqest.status_code == 404:
        return 'Город указан не верно! Его можно изменить командой: #!place'
    else:
        weather_data = reqest.json()
        return get_and_print_weather(weather_data, city, str(datetime.datetime.now()).split()[0])

def get_and_print_weather(weather_data, city, date):    
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    wind_speed = weather_data['wind']['speed']
    wind_direction = degToCompass(weather_data['wind']['deg'])
    humidity = weather_data['main']['humidity']
    pressure = str(round(int(weather_data['main']['pressure']) * 0.75024, 0)).split('.')[0]
   
    return (f'Погода в городе {city} на {date}\n'
            f'Температура: {temperature} °C, ощущается как {temperature_feels} °C\n'
            f'Скорость ветра: {wind_speed} (м/с), Направление: {wind_direction}\n'
            f'Влажность: {humidity} (г/м³)\n'
            f'Давление: {pressure} (мм ртутного столба)')


