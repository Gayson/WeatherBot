# coding=utf-8
from server.enums import LifeIndex


class PicMessage(object):
    def __init__(self, city_info, life_info, alarm_info):
        weather_info = city_info.total_info['daily_weather']
        air_index = city_info.total_info['daily_air_index']

        self.result = {
            'minTemp': weather_info['low'],
            'maxTemp': weather_info['high'],
            'location': city_info.city_name,
            'weather': weather_info['code_day'],
            'wind': weather_info['wind_direction'],
            'aqi': air_index['aqi'],
            'quality': str(air_index['quality']),
            'warning': self.get_alarm_brief(alarm_info)
        }

        life_message = LifeMessage(life_info)
        self.result = dict(self.result, **life_message.result)

    @staticmethod
    def get_alarm_brief(alarm_info):
        alarms = alarm_info
        if len(alarms) >= 1:
            return alarms[0]['type'] + alarms[0]['level'] + '预警'
        return '无预警'


class LifeMessage(object):

    def __init__(self, life_info):
        self.result = {
            'livingIndex': [],
            'livingAdvice': [],
            'livingValue': [],
        }

        total_count = 0
        for i in range(0, len(LifeIndex.life_list)):
            for exclude_index in LifeIndex.exclude_list[i]:
                if total_count == 3:
                    break

                brief = life_info[LifeIndex.life_list[i]]['brief']
                if exclude_index != life_info[LifeIndex.life_list[i]]['brief']:
                    total_count += 1
                    self.result['livingIndex'].append(LifeIndex.life_name_list[i])
                    self.result['livingAdvice'].append(LifeIndex.suggestion_list[i])
                    self.result['livingValue'].append(brief)


class ReplyMessage(object):
    def __init__(self):
        self.results = None

    def set_data(self, weather_info, air_index, life_info):
        self.results = ''


class AlarmMessage(object):
    def __init__(self, alarms):
        self.results = '[今日预警]\n'

        for alarm in alarms:
            self.results += ('--%s%s%s--\n' % (alarm['type'], alarm['level'], '预警'))
            self.results += alarm['description'] + '\n\n'



