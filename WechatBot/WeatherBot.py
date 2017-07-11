#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
from datetime import datetime

class WeatherBot(WXBot):
	schedule_enable = True                   #定时任务使能
	push_flag = False			 #推送的标志，避免重复推送
	set_time = {"hour":11, "minute":51}       #定时推送时间，默认六点四十
	admin_list = [{"Name":"顺达"}] 			 #管理员列表
	target_contact = [{"Name":"顺达"}]			 #需要推送的联系人
	target_group = [{"Name":"爆炸开发"}]			 #需要推送的群

	#响应接收到的消息
	def handle_msg_all(self,msg):
		print msg['user']['id']
	
	#定时任务
	def schedule(self):
		if self.schedule_enable:
			now = datetime.now()
			print now
			if now.hour == self.set_time["hour"] and now.minute == self.set_time["minute"]:
				if self.push_flag == False:
					print "target time!"
					self.push_weather_information()
					self.push_flag = True
			else:
				self.push_flag = False
	
	#推送天气信息
	def push_weather_information(self):
		weather_img = "img/1.png"  	          #推送的天气图片
		weather_txt = "测试"			  #推送的天气文本信息
		#给联系人推送天气信息
		for contact in self.target_contact:     
			uid = self.get_user_id(contact["Name"])
			if uid is not None:
				self.send_img_msg_by_uid(weather_img, uid)
				self.send_msg_by_uid(weather_txt, uid)
			else:
				if self.DEBUG:
					print "[ERROR] NOT FIND CONTACT %s." % (contact["Name"])	
		#给群推送天气信息
		for group in self.target_group:
			uid = self.get_user_id(group["Name"])
			if uid is not None:
				self.send_img_msg_by_uid(weather_img, uid)
				self.send_msg_by_uid(weather_txt, uid)
			else:
				if self.DEBUG:
					print "[ERROR] NOT FIND GROUP %s." % (contact["Name"])

def main():
    bot = WeatherBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'
    bot.run()

if __name__ == '__main__':
    main()

 
