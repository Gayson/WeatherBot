#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
from datetime import datetime
class WeatherBot(WXBot):
	push_flag = False				   #定时推送的标志，避免重复推送
	schedule_enable = True                             #定时任务使能
	set_time        = {"hour":11, "minute":51}         #定时推送时间，默认六点四十
	admin_list      = [{"Name":"顺达"}] 		   #管理员列表
	target_contact  = [{"Name":"顺达"}]	           #需要推送的联系人
	target_group    = [{"Name":"爆炸开发"}]	           #需要推送的群

	#响应接收到的消息
	def handle_msg_all(self,msg):
		command = msg["content"]["data"]
		uid = msg["user"]["id"]
		print msg["msg_type_id"] 
		if msg["msg_type_id"]  == 4 and msg["content"]["type"] == 0:            #来自联系人的文本消息
			for admin in self.admin_list:						#管理员消息
				if uid  == self.get_user_id(admin["Name"]): 
					self.handle_admin_msg(msg)
			self.handle_common_msg(msg)                   		         	#普通消息
		elif msg["msg_type_id"] == 3 and msg["content"]["type"] == 0:           #来自微信群的文本消息
			self.handle_group_msg(msg)
			
					
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
		
		
	#群发天气信息
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
	
	#获取初始配置信息
	def load_conf(self):
		try:
			conf_file = open("conf.json")
			conf = json.loads(conf_file.read())
			self.schedule_enable = conf["schedule_enable"]
			self.set_time        = conf["set_time"]
			self.admin_list      = conf["admin_list"]
			self.target_contact  = conf["target_contact"]
			self.target_group    = conf["target_group"]
			conf_file.close()
		except:							   #设置为默认值
			self.conf_fichedule_enable = True                  #定时任务使能
			set_time = {"hour":6, "minute":40}                 #定时推送时间，默认六点四十
			admin_list = [{"Name":"顺达"}]                     #管理员列表
			target_contact = [{"Name":"顺达"}]                 #需要推送的联系人
			target_group = [{"Name":"爆炸开发"}]               #需要推送的群
	
	#更新配置信息
	def set_conf(self):
		conf_file = open("conf.json", "w")
		conf = {}
		conf["schedule_enable"] = self.schedule_enable
		conf["set_time"]        = self.set_time
		conf["admin_list"]      = self.admin_list
		conf["target_contact"]  = self.target_contact
		conf["target_group"]    = self.target_group
		conf_file.write(json.dumps(conf))
		conf_file.close()
	
	#重写init函数
	def init(self):
		self.load_conf()                     #加载天气机器人配置
		url = self.base_uri + '/webwxinit?r=%i&lang=en_US&pass_ticket=%s' % (int(time.time()), self.pass_ticket)
        	params = {
           		 'BaseRequest': self.base_request
        	}
		r = self.session.post(url, data=json.dumps(params))
 		r.encoding = 'utf-8'
 		dic = json.loads(r.text)
 		self.sync_key = dic['SyncKey']
 		self.my_account = dic['User']
 		self.sync_key_str = '|'.join([str(keyVal['Key']) + '_' + str(keyVal['Val'])
				for keyVal in self.sync_key['List']]) 
		return dic['BaseResponse']['Ret'] == 0     
	
	#---------------------------------------------------------
	#                         用户响应
	#---------------------------------------------------------
	#----------------------1.管理员用户响应-------------------      
	def handle_admin_msg(self, msg):		     		#--------管理员命令---------
        	command = msg["content"]["data"]
                uid = msg["user"]["id"]
		if command == u"查看状态":                              #1-"查看状态"   
                	self.show_status(uid)
                elif command[:4] == u"设定时间":                        #2-"设定时间H:M"
                       	self.set_target_time(command[4:], uid)
                elif command ==  u"开启定时群发":                       #3-"开启定时群发"
                    	self.open_schedule(uid)
                elif command == u"关闭定时群发":                        #4-"关闭定时群发"
                       	self.close_schedule(uid)
                elif command == u"查看管理员列表":                      #5-"查看当前管理员列表"
                        self.check_admin_list(uid)
               	elif command == u"管理员":                              #6-"显示管理员命令列表"         
                        self.check_admin_command_list(uid)
                                                                        
	#----------------------2.通用命令响应--------------------
	def handle_common_msg(self, msg):				#---------通用命令-----------
	        command = msg["content"]["data"]
                uid = msg["user"]["id"]
		if command == u"天气":                                  #1-"天气"
                	self.push_weather_to_one(uid)
                elif command == u"天王盖地虎，宝塔镇河妖":              #2-管理员特权口令
                        self.upgrade_to_admin(uid)              
      
	#----------------------3.群消息响应----------------------
	
	#--------------------------------------------------------
	#			命令实现
	#--------------------------------------------------------
	#----------------------管理员命令------------------------
	#1.发送当前机器人状态----"查看状态"
	def show_status(self, uid):
		if self.schedule_enable:
			self.send_msg_by_uid("定时群发： 开启", uid)
		else:
			self.send_msg_by_uid("定时群发:  关闭", uid)
		reply = "当前设定时间：%i点%i分" % (self.set_time["hour"],self.set_time["minute"])
		self.send_msg_by_uid(reply, uid)
	
	#2.修改设定时间----"设定时间H：M"
	def set_target_time(self, time, uid):
		try:
			index = time.find(":")
                        hour = int(time[:index])
                        minute = int(time[index+1:])
                       	if 0<=hour and hour<=23 and 0<=minute and minute<=59:
                        	self.set_time["hour"] = hour
                        	self.set_time["minute"] = minute
                                self.set_conf()
                              	reply = "时间设定成功！当前设定时间为%i点%i分" % (hour, minute)
                        else:
                                reply = "时间参数错误"
                        self.send_msg_by_uid(reply, uid)
               	except:
                        self.send_msg_by_uid("设定时间失败", uid)
	
	#3.开启定时群发----"开启定时群发"
	def open_schedule(self, uid):
		self.schedule_enable = True
		self.show_status(uid)
                self.set_conf()
	
	#4.关闭定时群发----"关闭定时群发"
	def close_schedule(self, uid):
		self.schedule_enable = False
		self.show_status(uid)
		self.set_conf()
	
	#5.查看管理员列表----"查看管理员列表"
	def check_admin_list(self, uid):
                num_of_admin = len(self.admin_list)
                reply = u"当前共有%i名管理员:\n" % (num_of_admin)
                for admin in self.admin_list:
                	reply += admin["Name"]+"\n"
               	self.send_msg_by_uid(reply[:-1], uid)  	
		
	#6.显示管理员命令列表----"管理员"
	def check_admin_command_list(self, uid):
		reply = "管理员命令：\n"
                reply += "1.查看状态\n"
                reply += "2.设定时间H:M\n"
                reply += "3.开启定时群发\n"
                reply += "4.关闭定时群发\n"
                reply += "5.查看管理员列表"
                self.send_msg_by_uid(reply, uid)
	#-------------------------------------------------------------------------
	#-----------------------普通用户命令(通用功能)----------------------------
	#1.为特定目标推送天气信息----"天气"
        def push_weather_to_one(self, uid, city="default"):
                weather_img = "img/1.png"                  #推送的天气图片
                weather_txt = "测试"                       #推送的天气文本信息
                self.send_img_msg_by_uid(weather_img, uid)
                self.send_msg_by_uid(weather_txt, uid)
	
	#2.普通用户升级为管理员----"天王盖地虎，宝塔镇河妖"
	def upgrade_to_admin(self, uid): 
		admin_name = self.get_contact_prefer_name(self.get_contact_name(uid))
                self.admin_list.append({"Name": admin_name})                    #添加当前用户至管理员
                self.set_conf()
                self.send_msg_by_uid("管理员模式开启,回复\"管理员\"获得命令列表", uid)
	#------------------------------------------------------------------------	
	#---------------------------群消息响应-----------------------------------
	#1.响应@消息
	def handle_group_msg(self, msg):
		print msg["content"]
		if "detail" in msg["content"]:
			#获取机器人名字列表
			my_names = self.get_group_member_name(msg["user"]["id"], self.my_account["UserName"]) 
			if my_names is None:
				my_names = {}
			if "NickName" in self.my_account and self.my_account["NickName"]:
				my_names["nickname2"] = self.my_account["NickName"]
			if "RemarkName" in self.my_account and self.my_account["RemarkName"]:
				my_names["remark_name2"] = self.my_account["RemarkName"]
			
			#判断是否at自己
			is_at_me = False													
			for detail in msg["content"]["detail"]:
				print detail["value"]
				if detail["type"] == "at" or (detail["value"] != "" and detail["value"][0] == u"@"): 
				 #微信网页版@信息是str类型，@字符包含在"value"中
					print msg["content"]["detail"]
					for k in my_names:
						if my_names[k] and detail["value"].find(my_names[k]) != -1:
							is_at_me = True
							break
			#推送消息
			if is_at_me:
				self.push_weather_to_one(msg["user"]["id"])
			   
					
	
def main():
    bot = WeatherBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'tty'
    bot.run()

if __name__ == '__main__':
    main()

 
