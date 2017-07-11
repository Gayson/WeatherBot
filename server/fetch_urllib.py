#coding=utf-8
from __future__ import unicode_literals
import ssl
import urllib
import requests
import sys
import json
import utils

reload(sys)
sys.setdefaultencoding('utf-8')

gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


def fetchAPI(location, api, days = 0):
    params = getParams(location, days)
    response = requests.get(api, params=params).text.decode('UTF-8')
    return response

def getParams(location, days):
    if days == 0:
        params = urllib.urlencode({
            'key': utils.API_KEY,
            'location': location,
            'language': utils.LANGUAGE,
            'unit': utils.UNIT
            })
        return params
    else:
        params = urllib.urlencode({
            'key': utils.API_KEY,
            'location': location,
            'language': utils.LANGUAGE,
            'unit': utils.UNIT,
            'days': days
            })
        return params

if __name__ == '__main__':
    result = fetchAPI(utils.XUHUI_ID, utils.WEATHER_DAILY_API, days = 1)
    weather = json.loads(result)
    print str(weather).decode('unicode-escape').encode('utf-8')
