# coding=utf-8
from __future__ import unicode_literals

import json
import sys
import traceback
import urllib

import requests

from city_info import CityInfo
from server import utils
from server.enums import TimeStatus, WeatherType
from server.view_models import PicMessage, ReplyMessage


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

            city_id = city.city_id
            city.refresh_daily_weather(utils.filter_fetch_api(city_id, utils.API_LIST['WEATHER_DAILY_API'], 1))
            city.refresh_hour_weather(utils.filter_fetch_api(city_id, utils.API_LIST['WEATHER_HOURLY_API'], 1), hour)
            city.refresh_daily_air_index(utils.filter_fetch_api(city_id, utils.API_LIST['AIR_DAILY_API'], 1))
            city.refresh_hour_air_index(utils.filter_fetch_api(city_id, utils.API_LIST['AIR_HOURLY_API'], 1), hour)
            city.refresh_total_info(TimeStatus.get_status(), hour)

    '''
    depends on XuHui and ShangHai info
    '''

    def refresh_total_info(self):
        sh_info = self.city_list[utils.LOCATION]
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
            self.total_info = self.city_list[utils.IMP_LOCATION]
            cur_city = utils.IMP_LOCATION

        self.life_index = utils.filter_fetch_api(cur_city, utils.API_LIST['LIFE_API'])

    @staticmethod
    def get_distinct_id(city_name):
        params = urllib.urlencode({
            'key': utils.API_KEY,
            'q': city_name
        })

        response = requests.get(utils.API_LIST['CITY_API'], params=params).text
        try:
            json_res = json.loads(response, 'utf-8')
            for city_res in json_res['results']:
                yield city_res['name'], city_res['id']
        except Exception, e:
            print traceback.print_exc()

    def get_publish_message(self):
        self.refresh_total_info()

        ci = self.total_info
        li = self.life_index
        ai = utils.filter_fetch_api(utils.LOCATION, utils.API_LIST['ALARM_API'])
        pic_message = PicMessage(ci, li, ai)

        pic_message_json = json.dumps(pic_message.__dict__, ensure_ascii=False)
        return pic_message_json

    def get_city_message(self, city_name, hour=-1, days=0):
        message = ReplyMessage(city_name, hour, days)
        if hour != -1 and hour < CityInfo.START_HOUR:
            message.results = '这个点你就起床啦？看凌晨四点的太阳吗？'
            return message
        elif hour > CityInfo.END_HOUR:
            message.results = '这个点你不在家吗？这么舒服的吗？'
            return message

        # 今日数据
        if days == 0:

            # 城市已缓存
            if city_name in self.city_list.keys():
                city = self.city_list[city_name]

                life_info = utils.filter_fetch_api(city.city_id, utils.API_LIST['LIFE_API'])
                if hour == -1:
                    message.set_data(city.total_info['daily_weather'], city.total_info['daily_air_index'],
                                     life_info)
                else:
                    message.set_data(city.hour_weather_info[hour - CityInfo.START_HOUR],
                                     city.hour_air_info[hour - CityInfo.START_HOUR],
                                     life_info)

        else:
            message.set_data(utils.filter_fetch_api(city_name, utils.API_LIST['WEATHER_DAILY_API'], days=days),
                             utils.filter_fetch_api(city_name, utils.API_LIST['AIR_DAILY_API'], days=days),
                             utils.filter_fetch_api(city_name, utils.API_LIST['LIFE_API'], days=days))
        return message.result

if __name__ == '__main__':
    service = WeatherService()
    # service.refresh()
    print service.get_city_message('徐家汇', hour=18, days=1)
