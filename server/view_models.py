# coding=utf-8
from server.enums import LifeIndex, ReplyTemplate
import time


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
            'warning': self.get_alarm_brief(alarm_info),
            'date': weather_info['date']
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
            'details': [],
        }

        total_count = 0
        for i in range(0, len(LifeIndex.life_list)):
            for exclude_index in LifeIndex.exclude_list[i]:
                if total_count == 3:
                    break

                cur_life = life_info[LifeIndex.life_list[i]]

                brief = cur_life['brief']
                if exclude_index != cur_life['brief']:
                    total_count += 1
                    self.result['livingIndex'].append(LifeIndex.life_name_list[i])
                    self.result['livingAdvice'].append(LifeIndex.suggestion_list[i])
                    self.result['livingValue'].append(brief)
                    self.result['details'].append(cur_life['details'])


class ReplyMessage(object):
    def __init__(self, city_name, hour=-1, days=0):
        self.result = None
        self.location = city_name

        if hour == -1 or days != 0:
            self.hour = -1
            self.template = ReplyTemplate.temp_1
        else:
            self.hour = hour
            self.template = ReplyTemplate.temp_hour

        if days == 0:
            self.day = '今日'
        elif days == 1:
            self.day = '明日'
        elif days == 2:
            self.day = '后天'
        else:
            today = time.strftime('%d', time.localtime(time.time()))
            self.day = '%d日' % (int(today) + days)

    def set_data(self, weather_info, air_index, life_info):
        if self.hour != -1:
            self.result = self.template % (self.location,
                                           self.day,
                                           '%d点' % self.hour,
                                           int(weather_info['temperature']),
                                           int(weather_info['humidity']),
                                           weather_info['text'],
                                           int(air_index['aqi']),
                                           weather_info['wind_direction'],
                                           float(weather_info['wind_speed']))
        else:
            life_msg = LifeMessage(life_info)
            self.result = self.template % (self.day,
                                           self.location,
                                           int(weather_info['high']),
                                           int(weather_info['low']),
                                           weather_info['text_day'],
                                           int(air_index['aqi']),
                                           life_msg.result['details'][0],
                                           life_msg.result['details'][1],
                                           life_msg.result['details'][2])


class AlarmMessage(object):
    def __init__(self, alarms):
        self.result = '[今日预警]\n'

        for alarm in alarms:
            self.result += ('--%s%s%s--\n' % (alarm['type'], alarm['level'], '预警'))
            self.result += alarm['description'] + '\n'
