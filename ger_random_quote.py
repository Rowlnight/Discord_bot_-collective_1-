import requests, pprint, datetime

url = f'https://production-calendar.ru/get-period/40dd218baee4eee3eabb1d58dcef1382/ru/2024/json'


def get_quote():
    reqest = requests.get(url)
    quote_data = reqest.json()

    date = datetime.date.today().strftime("%d.%m.%Y")

    for day in quote_data['days']:
        print(day)
   
   # return quote_data[]

get_quote()
