# coding=utf-8
import sched
import time


class ScheduleService(object):
    def __init__(self, weather_service):
        self.weather_service = weather_service
        self.schedule = sched.scheduler(time.time(), time.sleep)

    def refresh_cache(self):
        self.weather_service.refresh()
        msg = self.weather_service.get_publish_message()
        

