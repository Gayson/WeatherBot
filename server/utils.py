# coding=utf-8
import requests
import urllib
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

LOCATION = u'上海'  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
IMP_LOCATION = u'徐家汇'

CITY_API = 'https://api.seniverse.com/v3/location/search.json'
LIFE_API = 'https://api.seniverse.com/v3/life/suggestion.json'  # API URL，可替换为其他 URL
ALARM_API = 'https://api.seniverse.com/v3/weather/alarm.json'

WEATHER_DAILY_API = 'https://api.seniverse.com/v3/weather/daily.json'
WEATHER_NOW_API = 'https://api.seniverse.com/v3/weather/now.json'
WEATHER_HOURLY_API = 'https://api.seniverse.com/v3/weather/hourly.json'

AIR_NOW_API = 'https://api.seniverse.com/v3/air/now.json'
AIR_DAILY_API = 'https://api.seniverse.com/v3/air/now.json'
AIR_HOURLY_API = 'https://api.seniverse.com/v3/air/hourly.json'

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
