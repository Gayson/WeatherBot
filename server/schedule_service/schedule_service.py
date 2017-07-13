# coding=utf-8
import sched
import time
import sys
from server.render.pic_render import PicRender
from server import utils
from alarm_info import PublishedAlarm
from server.view_models import AlarmMessage
import server.utils
import threading

reload(sys)
sys.setdefaultencoding('utf-8')


class ScheduleService(object):
    INTERVAL_WEATHER_REFRESH = 30
    INTERVAL_ALARM_REFRESH = 180

    pub_alarms = []

    def __init__(self, weather_service, bot, image_service):
        self.weather_service = weather_service
        self.bot = bot
        self.image_service = image_service

        self.schedule = sched.scheduler(time.time, time.sleep)
        self.schedule.enter(self.INTERVAL_WEATHER_REFRESH, 1, self.refresh_cache, self.refresh_over)
        self.schedule.enter(self.INTERVAL_ALARM_REFRESH, 0, self.fetch_alarm, (utils.LOCATION,))

    def refresh_cache(self):

        print 'refresh weather service'
        self.weather_service.refresh()
        msg = self.weather_service.get_publish_message()

        img_path = utils.IMAGE_PATH % (utils.LOCATION, time.strftime("%M-%d", time.localtime(time.time())))
        self.image_service.generate_image(msg, img_path, )
        self.schedule.enter(self.INTERVAL_WEATHER_REFRESH, 1, self.refresh_cache, ())

    @staticmethod
    def refresh_over():
        print 'refresh over'

    def fetch_alarm(self, location):

        print 'fetch alarm'
        alarms = utils.filter_fetch_api(location, utils.API_LIST['ALARM_API'])

        res_alarms = []

        if len(alarms) >= 1:  # has alarms
            for pub_alarm in self.pub_alarms:
                pub_alarm.set_inactive()

            for alarm in alarms:
                alarm_exist = False
                for pub_alarm in self.pub_alarms:
                    if pub_alarm.equal(alarm):
                        pub_alarm.set_active()
                        alarm_exist = True
                        break
                if not alarm_exist:
                    res_alarms.append(alarm)
                    self.pub_alarms.append(PublishedAlarm(alarm))

            self.pub_alarms = filter(lambda a: a.is_active(), self.pub_alarms)

        if len(res_alarms) > 0:
            message = AlarmMessage(res_alarms)
            self.bot.push_msg_to_target_contact(message.result, False)
            self.bot.push_msg_to_target_group(message.result, False)

        self.schedule.enter(self.INTERVAL_ALARM_REFRESH, 0, self.fetch_alarm, (location,))

    def start_service(self):
        sched_thread = threading.Thread(target=self.schedule.run, args=())
        sched_thread.setDaemon(True)
        sched_thread.start()
