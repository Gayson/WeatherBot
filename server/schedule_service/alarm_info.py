# coding=utf-8
from server.enums import AlarmStatus


class PublishedAlarm(object):

    def __init__(self, alarm):

        self.title = alarm['title']
        self.pub_date = alarm['pub_date']
        self.status = AlarmStatus.ACTIVE

    # from java
    def equal(self, alarm):
        if self.title == alarm['title'] and self.pub_date == alarm['pub_date']:
            self.status = AlarmStatus.ACTIVE
            return True
        return False

    def set_active(self):
        self.status = AlarmStatus.ACTIVE

    def set_inactive(self):
        self.status = AlarmStatus.INACTIVE

    def is_active(self):
        return self.status == AlarmStatus.ACTIVE