# coding=utf-8
import enum
import time


class TimeStatus(enum.Enum):
    MID_NIGHT = 0
    DAY = 1
    NIGHT = 2

    @staticmethod
    def get_status():
        hour_now = TimeStatus.get_hour()
        if hour_now <= 5:
            return TimeStatus.MID_NIGHT
        elif hour_now <= 20:
            return TimeStatus.DAY
        else:
            return TimeStatus.NIGHT

    @staticmethod
    def get_hour():
        return int(time.strftime('%H', time.localtime(time.time())))


class AirType(enum.Enum):
    GOOD = 0
    MODERATE = 1
    LIGHTLY_POLLUTED = 2
    MODERATELY_POLLUTED = 3
    HEAVILY_POLLUTED = 4
    SEVERELY_POLLUTED = 5

    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __int__(self):
        return self._value_

    @staticmethod
    def get_air_type(aqi):
        if aqi <= 50:
            return AirType.GOOD
        elif aqi <= 100:
            return AirType.MODERATE
        elif aqi <= 150:
            return AirType.LIGHTLY_POLLUTED
        elif aqi <= 200:
            return AirType.MODERATELY_POLLUTED
        elif aqi <= 300:
            return AirType.HEAVILY_POLLUTED
        else:
            return AirType.SEVERELY_POLLUTED


class WeatherType(enum.Enum):
    SHINE = 'SHINE'
    CLOUDY = 'CLOUDY'
    RAIN = 'RAIN'
    ICE_RAIN = 'ICE_RAIN'
    SNOW = 'SNOW'
    SAND = 'SAND'
    FOGGY_HAZE = 'FOGGY_HAZE'
    WINDY = 'WINDY'
    COLD = 'COLD'
    HOT = 'HOT'
    UNKNOWN = 'UNKNOWN'

    @staticmethod
    def get_weather_type(code):
        if code <= 3:
            return WeatherType.SHINE
        if code <= 9:
            return WeatherType.CLOUDY
        if code <= 18:
            return WeatherType.RAIN
        if code <= 20:
            return WeatherType.ICE_RAIN
        if code <= 25:
            return WeatherType.SNOW
        if code <= 29:
            return WeatherType.SAND
        if code <= 31:
            return WeatherType.FOGGY_HAZE
        if code <= 36:
            return WeatherType.WINDY
        if code == 37:
            return WeatherType.COLD
        if code == 38:
            return WeatherType.HOT
        if code == 99:
            return WeatherType.UNKNOWN


class LifeIndex(object):

    life_list = ['umbrella',
                 'air_pollution',
                 'uv',
                 'chill',
                 'flu',
                 'traffic',
                 'mood',
                 'dressing',
                 'comfort',
                 'makeup',
                 ]

    life_name_list = [
        '雨伞',
        '污染扩散',
        '紫外线',
        '风寒',
        '感冒',
        '交通',
        '心情',
        '穿衣',
        '舒适度',
        '化妆',
    ]

    exclude_list = [
        ['不带伞'],
        [''],
        ['弱'],
        ['无'],
        ['少发'],
        ['良好'],
        [''],
        [''],
        ['舒适'],
        ['']
    ]

    suggestion_list = [
        '出门请带伞',
        '减少室外活动',
        '请做好防晒措施',
        '请做好防寒准备',
        '请做好防范',
        '请提前出门',
        '及时调整心情',
        '根据温度调整',
        '',
        '',
    ]


class AlarmStatus(enum.Enum):
    ACTIVE = 0,
    INACTIVE = 1


class ReplyTemplate(object):
    temp_1 = '%s%s工作时间最高气温%d度，最低气温%d度，%s，空气质量指数%d。\n%s%s%s'
    temp_hour = '%s%s%s气温%d度，湿度%d，%s，空气质量指数%d。%s风，风速%.1f公里每小时。'
