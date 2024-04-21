import requests, os, datetime


dir = os.path.abspath(os.curdir)


def get_current_day_info():
    with open(dir + '\\data\\links\\calendar.txt', 'r', encoding="utf-8") as file:
        url = file.read().replace('XXXX', str(datetime.date.today().year))
        
    reqest = requests.get(url)
    days_data = reqest.json()
    date = datetime.date.today().strftime("%d.%m.%Y")
    for day in days_data['days']:
        if str(day['date']) == date:
            current_day = day
            break
        
    day_id = int(current_day['type_id'])
    type_day = current_day['type_text']
    note = current_day['note'] if day_id == 3 else None
    week_day = current_day['week_day']

    week_day = f' ({week_day.upper()}) '

    return type_day, note, week_day
