# coding=utf-8
from enums import LifeIndex


class PicMessage(object):
    def __init__(self, city_info, life_info, alarm_info):
        weather_info = city_info.total_info['daily_weather']
        air_index = city_info.total_info['daily_air_index']
        cur_life_info = life_info['results'][0]['suggestion']

        self.result = {
            'minTemp': weather_info['low'],
            'maxTemp': weather_info['high'],
            'location': city_info.city_name,
            'weather': weather_info['code_day'],
            'wind': weather_info['wind_direction'],
            'livingIndex': [],
            'livingValue': [],
            'livingAdvice': [],
            'aqi': air_index['aqi'],
            'quality': air_index['quality'],
            'warning': self.get_alarm_brief(alarm_info)
        }

        total_count = 0
        for i in range(0, len(LifeIndex.life_list)):
            for exclude_index in LifeIndex.exclude_list[i]:
                if total_count == 3:
                    break

                brief = cur_life_info[LifeIndex.life_list[i]]['brief']
                if exclude_index != cur_life_info[LifeIndex.life_list[i]]['brief']:
                    total_count += 1
                    self.result['livingIndex'].append(LifeIndex.life_name_list[i])
                    self.result['livingAdvice'].append(LifeIndex.suggestion_list[i])
                    self.result['livingValue'].append(brief)

    @staticmethod
    def get_alarm_brief(alarm_info):
        inner_a_info = alarm_info['results'][0]['alarms']
        if len(inner_a_info) == 1:
            return inner_a_info[0]['type'] + inner_a_info[0]['level'] + '预警'
        return '无预警'




class ImpMessage(object):
    pass


class ReplyMessage(object):
    pass


class alarmMessage(object):
    pass
