# coding=utf-8
import requests
import urllib
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

LOCATION = u'上海'  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
IMP_LOCATION = u'徐家汇'

API_LIST = {
    'CITY_API': 'https://api.seniverse.com/v3/location/search.json',

    'LIFE_API': 'https://api.seniverse.com/v3/life/suggestion.json',
    'ALARM_API': 'https://api.seniverse.com/v3/weather/alarm.json',

    'WEATHER_DAILY_API': 'https://api.seniverse.com/v3/weather/daily.json',
    'WEATHER_NOW_API': 'https://api.seniverse.com/v3/weather/now.json',
    'WEATHER_HOURLY_API': 'https://api.seniverse.com/v3/weather/hourly.json',

    'AIR_NOW_API': 'https://api.seniverse.com/v3/air/now.json',
    'AIR_DAILY_API': 'https://api.seniverse.com/v3/air/daily.json',
    'AIR_HOURLY_API': 'https://api.seniverse.com/v3/air/hourly.json',
}

LANGUAGE = 'zh-Hans'  # 查询结果的返回语言
UNIT = 'c'

API_KEY = 'cmm7uo5ftsziioro'
UID = 'UEE3F1CD43'


def fetch_api(location, api, days=0):
    params = get_params(location, days)
    response = requests.get(api, params=params).text
    json_res = json.loads(response, 'utf-8')
    return json_res


def get_params(location, days):
    if days == 0:
        params = urllib.urlencode({
            'key': API_KEY,
            'location': location,
            'language': LANGUAGE,
            'unit': UNIT
        })
        return params
    else:
        params = urllib.urlencode({
            'key': API_KEY,
            'location': location,
            'language': LANGUAGE,
            'unit': UNIT,
            'days': days
        })
        return params


def filter_fetch_api(location, api, days=0):
    json_res = fetch_api(location, api, days)
    json_res = json_res['results'][0]

    if days == 0:
        day_index = 0
    else:
        day_index = days - 1

    if api == API_LIST['LIFE_API']:
        return json_res['suggestion']

    if api == API_LIST['ALARM_API']:
        return json_res['alarms']

    if api == API_LIST['WEATHER_DAILY_API']:
        return json_res['daily'][day_index]

    if api == API_LIST['WEATHER_NOW_API']:
        return json_res['now']

    if api == API_LIST['WEATHER_HOURLY_API']:
        return json_res['hourly']

    if api == API_LIST['AIR_DAILY_API']:
        return json_res['daily'][day_index]

    if api == API_LIST['AIR_HOURLY_API']:
        return json_res['hourly']

    if api == API_LIST['AIR_NOW_API']:
        return json_res['now']


# def test_fetch_api(location='shanghai'):
#     for api in API_LIST.keys():
#         json_res = fetch_api(location, API_LIST[api], 1)
#         res_str = str(json_res).decode('unicode-escape').encode('utf-8')
#         with open(('./res/ %s.json' % api), 'w') as f:
#             f.write(res_str)


def test_days_api(location='shanghai', days=3):
    json_res = filter_fetch_api(location, API_LIST['AIR_DAILY_API'], days=days)
    res_str = str(json_res).decode('unicode-escape').encode('utf-8')
    # res_str = res_str.replace('\'', '"')
    # res_str = res_str.replace('u', '')
    with open('./res/ WEATHER_DAYS_API.json', 'w') as f:
        f.write(res_str)

if __name__ == '__main__':
    test_days_api()
