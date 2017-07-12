# coding=utf-8
from __future__ import unicode_literals

import json
import sys
import traceback
import urllib

import requests

from city_info import CityInfo
from server import utils
from server.enums import TimeStatus
from server.enums import WeatherType
from server.view_models import PicMessage

reload(sys)
sys.setdefaultencoding('utf-8')


class WeatherService(object):
    city_list = {}

    def __init__(self):
        self.total_info = {}
        self.life_index = {}
        try:
            for city_name, city_id in self.get_distinct_id(utils.LOCATION):
                city = CityInfo(city_name=city_name, city_id=city_id)
                self.city_list[city_name] = city

                # self.refresh()

        except Exception, e:
            print traceback.print_exc()

    def refresh(self):
        hour = TimeStatus.get_hour()
        for city in self.city_list.values():
            city.refresh_daily_weather(utils.fetch_api(city.city_id, utils.WEATHER_DAILY_API, 1))
            city.refresh_hour_weather(utils.fetch_api(city.city_id, utils.WEATHER_HOURLY_API, 1), hour)
            city.refresh_daily_air_index(utils.fetch_api(city.city_id, utils.AIR_DAILY_API, 1))
            city.refresh_hour_air_index(utils.fetch_api(city.city_id, utils.AIR_HOURLY_API, 1), hour)

            city.refresh_total_info(TimeStatus.get_status(), hour)

    '''
    depends on XuHui and ShangHai info
    '''

    def refresh_total_info(self):
        sh_info = self.get_city(utils.LOCATION)
        sh_code_type = WeatherType.get_weather_type(sh_info.total_info['daily_weather']['code_day'])
        count = 0
        for city_info in self.city_list.values():
            code = city_info.total_info['daily_weather']['code_day']
            code_type = WeatherType.get_weather_type(code)

            # distinct weather equal to shanghai weather
            if code_type == sh_code_type:
                count += 1

        # if half of distinct in shanghai have the same weather type to shanghai
        if count >= len(self.city_list):
            self.total_info = sh_info
            cur_city = utils.LOCATION
        else:
            self.total_info = self.get_city(utils.IMP_LOCATION)
            cur_city = utils.IMP_LOCATION

        self.life_index = utils.fetch_api(cur_city, utils.LIFE_API)

    @staticmethod
    def get_distinct_id(city_name):
        params = urllib.urlencode({
            'key': utils.API_KEY,
            'q': city_name
        })

        response = requests.get(utils.CITY_API, params=params).text
        try:
            json_res = json.loads(response, 'utf-8')
            for city_res in json_res['results']:
                yield city_res['name'], city_res['id']
        except Exception, e:
            print traceback.print_exc()

    def get_city(self, city_name, hour=-1):
        if city_name in self.city_list.keys():
            return self.city_list[city_name]
        else:
            return utils.fetch_api(city_name, utils.WEATHER_NOW_API, 1)

    def get_publish_message(self):
        self.refresh_total_info()

        ci = self.total_info
        li = self.life_index
        ai = utils.fetch_api(utils.LOCATION, utils.ALARM_API)
        pic_message = PicMessage(ci, li, ai)

        pic_message_json = json.dumps(pic_message.__dict__, ensure_ascii=False)
        return pic_message_json

