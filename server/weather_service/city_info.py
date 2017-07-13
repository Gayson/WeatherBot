from server.enums import AirType


# hour between 8 to 20
class CityInfo(object):
    START_HOUR = 6
    END_HOUR = 22

    def __init__(self, city_name, city_id):
        self.city_name = city_name
        self.city_id = city_id

        self.hour_air_info = []
        self.hour_weather_info = []

        self.daily = {}

        self.total_info = {}

    def refresh_daily_air_index(self, air_info):
        self.daily['air'] = air_info

    def refresh_daily_weather(self, weather_info):
        self.daily['weather'] = weather_info

    def refresh_hour_air_index(self, air_index, hour):
        air_list = air_index
        if hour <= self.START_HOUR:
            self.hour_air_info = air_list[self.START_HOUR - hour:self.END_HOUR - hour]
        elif hour <= self.END_HOUR:
            self.hour_air_info = air_list[self.START_HOUR + 24 - hour:] + air_list[:self.END_HOUR - hour]
        else:
            self.hour_air_info = air_list[self.START_HOUR + 24 - hour:self.END_HOUR + 24 - hour]

    def refresh_hour_weather(self, _weather_info, hour):
        weather_list = _weather_info
        if hour <= self.START_HOUR:
            self.hour_weather_info = weather_list[self.START_HOUR - hour:self.END_HOUR - hour]
        elif hour <= self.END_HOUR:
            self.hour_weather_info = weather_list[self.START_HOUR + 24 - hour:] + weather_list[:self.END_HOUR - hour]
        else:
            self.hour_weather_info = weather_list[self.START_HOUR + 24 - hour:self.END_HOUR + 24 - hour]

    '''
    simple handle for data:
    1. calculate the average aqi
    2. reset low and high
    
    '''
    def refresh_total_info(self, time_status, hour):
        self.time_status = time_status

        weather = self.total_info['daily_weather'] = self.daily['weather']
        air_index = self.total_info['daily_air_index'] = self.daily['air']

        if 8 <= hour < 20:
            start = hour - self.START_HOUR

            low = 100
            high = -100
            aqi = 0

            for index in range(start, len(self.hour_air_info)):
                # temperature get
                temp = int(self.hour_weather_info[index]['temperature'])

                if temp < low:
                    low = temp
                elif temp > high:
                    high = temp

                aqi_temp = int(self.hour_air_info[index]['aqi'])
                aqi += aqi_temp

            aqi /= 1.0 * (self.END_HOUR - hour)

            air_index['aqi'] = aqi
            weather['low'] = low
            weather['high'] = high

        air_index['quality'] = int(AirType.get_air_type(air_index['aqi']))
