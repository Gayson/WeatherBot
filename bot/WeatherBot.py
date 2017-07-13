#!/usr/bin/env python
# coding: utf-8
#

import sys

sys.path.append("..")
from wxbot import *
from datetime import datetime

from server.weather_service.weather_service import WeatherService
from server.schedule_service.schedule_service import ScheduleService
from image_service.interface import ImageService
from server import utils

#---------百姓天气小助手----------#
#------------功能介绍-------------#
#1.定时群发天气信息               #
#2.管理员通过聊天窗口进行快捷管理 #
#3.响应普通用户和群内的天气请求   #
#---------------------------------#
#      2017.7.13 by 林顺达        #
#      linshunda@baixing.com      #
#---------------------------------#
class WeatherBot(WXBot):
    push_flag = False                    # 定时推送的标志，避免重复推送
    schedule_enable = True               # 定时任务使能
    set_time = {}                                # 定时推送时间
    admin_list = []                      # 管理员列表
    target_contact = []                  # 需要推送的联系人
    target_group = []            # 需要推送的群
    admin_password = ""                  # 管理员口令

    image_exist = False

    # 响应接收到的消息
    def handle_msg_all(self, msg):
        command = msg["content"]["data"]
        uid = msg["user"]["id"]
        print msg["msg_type_id"]
        if msg["msg_type_id"] == 4 and msg["content"]["type"] == 0:  # 来自联系人的文本消息
            for admin in self.admin_list:  # 管理员消息
                if uid == self.get_user_id(admin["Name"]):
                    self.handle_admin_msg(msg)
            self.handle_common_msg(msg)  # 普通消息
        elif msg["msg_type_id"] == 3 and msg["content"]["type"] == 0:  # 来自微信群的文本消息
            self.handle_group_msg(msg)

    # 定时任务
    def schedule(self):
        if self.schedule_enable:
            now = datetime.now()
            print now
            if now.hour == self.set_time["hour"] and now.minute == self.set_time["minute"]:
                if (not self.push_flag) and self.image_exist:
                    print "Target Time!"
                    self.push_msg_to_target_contact(utils.get_image_path(), True)
                    self.push_msg_to_target_contact(u"今日定时天气预报已推送～")
                    self.push_msg_to_target_group(utils.get_image_path(), True)
                    self.push_msg_to_target_group(u"今日定时天气预报已推送～")
                    #self.push_weather_information()
                    self.push_flag = True
                else:
                    self.push_flag = False

    # 获取初始配置信息
    def load_conf(self):
        try:
            conf_file = open("conf.json")
            conf = json.loads(conf_file.read())
            self.schedule_enable = conf["schedule_enable"]
            self.set_time = conf["set_time"]
            self.admin_list = conf["admin_list"]
            self.target_contact = conf["target_contact"]
            self.target_group = conf["target_group"]
            self.admin_password = conf["admin_password"]
            conf_file.close()
        except:  # 设置为默认值
            self.conf_fichedule_enable = True                            # 定时任务使能
            self.set_time = {"hour": 6, "minute": 40}            # 定时推送时间，默认六点四十
            self.admin_list = [{"Name": "顺达"}]                         # 管理员列表
            self.target_contact = [{"Name": "顺达"}]             # 需要推送的联系人
            self.target_group = [{"Name": "爆炸开发"}]           # 需要推送的群
            self.admin_password = u"天王盖地虎宝塔镇河妖"        # 默认管理员口令

    # 更新配置信息
    def set_conf(self):
        conf_file = open("conf.json", "w")
        conf = {}
        conf["schedule_enable"] = self.schedule_enable
        conf["set_time"] = self.set_time
        conf["admin_list"] = self.admin_list
        conf["target_contact"] = self.target_contact
        conf["target_group"] = self.target_group
        conf["admin_password"] = self.admin_password
        conf_file.write(json.dumps(conf))
        conf_file.close()

    # 重写init函数
    def init(self):
        self.load_conf()  # 加载天气机器人配置
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

    # 判断某用户是否在推送列表中
    def is_target(self, name):
        for contact in self.target_contact:
            if contact["Name"] == name:
                return True;
        for group in self.target_group:
            if group["Name"] == name:
                return True;
        return False

    # ---------------------------------------------------------
    #                         用户响应
    # ---------------------------------------------------------
    # ----------------------1.管理员用户响应-------------------
    def handle_admin_msg(self, msg):                                                                         # --------管理员命令---------
        command = msg["content"]["data"]
        uid = msg["user"]["id"]
        if command == u"查看状态":                                                                               # 1-"查看状态"
            self.show_status(uid)
        elif len(command) > 4 and command[:4] == u"设定时间":                                                    # 2-"设定时间H:M"
            self.set_target_time(command[4:], uid)
        elif command == u"开启定时群发":                                                                         # 3-"开启定时群发"
            self.open_schedule(uid)
        elif command == u"关闭定时群发":                                                                         # 4-"关闭定时群发"
            self.close_schedule(uid)
        elif command == u"查看管理员列表":                                                                       # 5-"查看当前管理员列表"
            self.check_admin_list(uid)
        elif command == u"查看联系人列表":                                                                       # 6-"查看联系人列表"
            self.check_contact_list(uid)
        elif command == u"查看推送列表":                                                                         # 7-"查看推送列表"
            self.check_push_list(uid)
        elif len(command) > 4 and command[:4] == u"添加推送":                                                    # 8-"添加推送NickName"
            self.add_push_by_name(command[4:], uid)
        elif len(command) > 4 and command[:4] == u"取消推送":                                                    # 9-"取消推送NickName"
            self.cancel_push_by_name(command[4:], uid)
        elif command == u"立即推送":                                                                             # 10-"立即推送"
            self.push_weather_information()
        elif command == u"更新联系人列表":                                                                       # 11-"更新联系人列表"
            self.get_contact()
            self.send_msg_by_uid("更新成功", uid)
        elif command == u"管理员":                                                                               # 11-"显示管理员命令列表"
            self.check_admin_command_list(uid)

    # ----------------------2.通用命令响应--------------------
    def handle_common_msg(self, msg):                                                                        # ---------通用命令-----------
        command = msg["content"]["data"]
        uid = msg["user"]["id"]
        if command.find(u"天气") != -1:                                                                                           # 1-"天气"
            self.handle_weather_query(command, uid)
        elif command == self.admin_password:                                                         # 2-管理员特权口令
            self.upgrade_to_admin(uid)
        elif command == u"帮助":
            self.check_help_info(uid)

    # ----------------------3.群消息响应----------------------
    # 1.响应@消息
    def handle_group_msg(self, msg):
        print msg["content"]
        if "detail" in msg["content"]:
            # 获取机器人名字列表
            my_names = self.get_group_member_name(msg["user"]["id"], self.my_account["UserName"])
            if my_names is None:
                my_names = {}
            if "NickName" in self.my_account and self.my_account["NickName"]:
                my_names["nickname2"] = self.my_account["NickName"]
            if "RemarkName" in self.my_account and self.my_account["RemarkName"]:
                my_names["remark_name2"] = self.my_account["RemarkName"]

            # 判断是否at自己
            is_at_me = False
            in_phone = False    #移动端和电脑端微信@后返回的msg不同
            print msg["content"]["detail"]
            
            detail = msg["content"]["detail"]
            if detail[0]["type"] == "at":             #移动端@          
                for k in my_names:
                    if my_names[k] and detail[0]["value"] == my_names[k]:
                        is_at_me = True
                        content = detail[1]["value"]
                        break
            elif (detail[0]["type"] == "str" and detail[0]["value"][0] == u"@"):
                for k in my_names:
                    if my_names[k] and detail[0]["value"].find(my_names[k]) != -1:
                        is_at_me = True
                        content = detail[0]["value"]
                        content = content.replace("@", "")
                        content = content.replace(my_names[k], "")
                        break

            # 推送消息
            if is_at_me and content.find(u"天气") != -1:
                content = content.replace(" ", "")
                self.handle_weather_query(content, msg["user"]["id"])

    # --------------------------------------------------------
    #                       命令实现
    # --------------------------------------------------------
    # ----------------------管理员命令------------------------
    # 1.发送当前机器人状态----"查看状态"
    def show_status(self, uid):
        if self.schedule_enable:
            self.send_msg_by_uid("定时群发： 开启", uid)
        else:
            self.send_msg_by_uid("定时群发:  关闭", uid)
        reply = "当前设定时间：%i点%i分" % (self.set_time["hour"], self.set_time["minute"])
        self.send_msg_by_uid(reply, uid)

    # 2.修改设定时间----"设定时间H：M"
    def set_target_time(self, time, uid):
        try:
            index = time.find(":")
            hour = int(time[:index])
            minute = int(time[index + 1:])
            if 0 <= hour and hour <= 23 and 0 <= minute and minute <= 59:
                self.set_time["hour"] = hour
                self.set_time["minute"] = minute
                self.set_conf()
                reply = "时间设定成功！当前设定时间为%i点%i分" % (hour, minute)
            else:
                reply = "时间参数错误"
            self.send_msg_by_uid(reply, uid)
        except:
            self.send_msg_by_uid("设定时间失败", uid)

    # 3.开启定时群发----"开启定时群发"
    def open_schedule(self, uid):
        self.schedule_enable = True
        self.show_status(uid)
        self.set_conf()

    # 4.关闭定时群发----"关闭定时群发"
    def close_schedule(self, uid):
        self.schedule_enable = False
        self.show_status(uid)
        self.set_conf()

    # 5.查看管理员列表----"查看管理员列表"
    def check_admin_list(self, uid):
        num_of_admin = len(self.admin_list)
        index = 1
        reply = u"当前共有%i名管理员:\n" % (num_of_admin)
        for admin in self.admin_list:
            reply += str(index) + "." + admin["Name"] + "\n"
            index += 1
        self.send_msg_by_uid(reply[:-1], uid)

    # 6.查看联系人列表----"查看联系人列表"
    def check_contact_list(self, uid):
        # 联系人
        index = 1
        num_of_contact = len(self.contact_list)
        reply = u"%i名联系人：\n" % (num_of_contact)
        for contact in self.contact_list:
            reply += "C" + str(index) + "." + contact["NickName"] + "\n"
            index += 1

        # 微信群
        index = 1
        num_of_group = len(self.group_list)
        reply += u"%i个微信群：\n" % (num_of_group)
        for group in self.group_list:
            reply += "G" + str(index) + "." + group["NickName"] + "\n"
            index += 1
        self.send_msg_by_uid(reply[:-1], uid)

    # 7.查看推送列表----"查看推送列表"
    def check_push_list(self, uid):
        index = 1
        num_of_contact = len(self.target_contact)
        reply = u"%i名推送用户: \n" % (num_of_contact)
        for contact in self.target_contact:
            reply += "C" + str(index) + "." + contact["Name"] + "\n"
            index += 1

        index = 1
        num_of_group = len(self.target_group)
        reply += u"%i个推送的微信群：\n" % (num_of_group)
        for group in self.target_group:
            reply += "G" + str(index) + "." + group["Name"] + "\n"
            index += 1
        self.send_msg_by_uid(reply[:-1], uid)

    # 8.添加推送----"添加推送：NickName"
    def add_push_by_name(self, name, uid):
        success_flag = False
        if name != "" and name[0] == "C":
            id_code = 0
            index = 1
            try:
                while True:
                    id_code = id_code * 10 + int(name[index])
                    index += 1
            except:
                print id_code
            if id_code != 0 and id_code <= len(self.contact_list):
                NickName = self.contact_list[id_code-1]["NickName"]
                print NickName
                if self.is_target(NickName):
                    reply = "该用户已在推送列表"
                    success_flag = True
                else:
                    self.target_contact.append({"Name": NickName})
                    self.set_conf()
                    reply = NickName + "添加成功"
                    success_flag = True
            else:
                print "编号错误"
        elif name != "" and name[0] == "G":
            id_code = 0
            index = 1
            try:
                while True:
                    id_code = id_code * 10 + int(name[index])
                    index += 1
            except:
                print id_code
            if id_code != 0 and id_code <= len(self.group_list):
                NickName = self.group_list[id_code-1]["NickName"]
                print NickName
                if self.is_target(NickName):
                    reply = "该用户已在推送列表"
                    success_flag = True
                else:
                    self.target_group.append({"Name": NickName})
                    self.set_conf()
                    reply = NickName + "添加成功"
                    success_flag = True
            else:
                print "编号错误"
        
        if not success_flag:
            if self.is_target(name):
                reply = "该用户已在推送列表"
            else:
                target_id = self.get_user_id(name)
                if target_id == "" or target_id == "":
                    reply = "用户不存在"
                elif self.is_contact(target_id):
                    self.target_contact.append({"Name": name})
                    self.set_conf()
                    reply = "需推送的联系人添加成功"
                elif self.is_group(target_id):
                    self.target_group.append({"Name": name})
                    self.set_conf()
                    reply = "需推送的微信群添加成功"
                else:
                    reply = "用户类型错误"
        self.send_msg_by_uid(reply, uid)

    # 9.删除推送----"取消推送：NickName"
    def cancel_push_by_name(self, name, uid):
        success_flag = False
        if name != "" and name[0] == "C":
            id_code = 0
            index = 1
            try:
                while True:
                    id_code = id_code * 10 + int(name[index])
                    index += 1
            except:
                print id_code
            if id_code != 0 and id_code <= len(self.target_contact):
                del self.target_contact[id_code-1]
                self.set_conf()
                self.send_msg_by_uid("取消推送联系人成功", uid)
                return True
        elif name != "" and name[0] == "G":
            id_code = 0
            index = 1
            try:
                while True:
                    id_code = id_code * 10 + int(name[index])
                    index += 1
            except:
                print id_code
            if id_code != 0 and id_code <= len(self.target_group):
                del self.target_group[id_code-1]
                self.set_conf()
                self.send_msg_by_uid("取消推送微信群成功", uid)
                return True

        for index in range(len(self.target_contact)):
            if self.target_contact[index]["Name"] == name:
                del self.target_contact[index]
                self.set_conf()
                self.send_msg_by_uid("取消推送联系人成功", uid)
                return True
        for index in range(len(self.target_group)):
            if self.target_group[index]["Name"] == name:
                del self.target_group[index]
                self.set_conf()
                self.send_msg_by_uid("取消推送微信群成功", uid)
                return True
        self.send_msg_by_uid("未找到联系人", uid)

    # 10.群发天气信息----"立即推送"
    def push_weather_information(self):
        print '接受推送请求'
        if self.image_exist:
            weather_img = utils.get_image_path()       #获取天气图片
        else:
            weather_img = 'img/1.png'

        print '获取图片路径'
        self.push_msg_to_target_contact(weather_img, True)
        self.push_msg_to_target_group(weather_img, True)

        print '推送图片'
        has_txt = True  # 存在第二条文本消息
        weather_txt = "天气已推送"
        if has_txt:
            self.push_msg_to_target_contact(weather_txt)
            self.push_msg_to_target_group(weather_txt)

        print '推送第二条消息'
    
    # 11.更新联系人列表

    # 12.显示管理员命令列表----"管理员"
    def check_admin_command_list(self, uid):
        reply = "管理员命令：\n"
        reply += "1.查看状态\n"
        reply += "2.设定时间H:M\n"
        reply += "3.开启定时群发\n"
        reply += "4.关闭定时群发\n"
        reply += "5.查看管理员列表\n"
        reply += "6.查看联系人列表\n"
        reply += "7.查看推送列表\n"
        reply += "8.添加推送:NickName\n"
        reply += "9.取消推送:NickName\n"
        reply += "10.立即推送\n"
        reply += "11.更新联系人列表"
        self.send_msg_by_uid(reply, uid)

    # -------------------------------------------------------------------------
    # -----------------------普通用户命令(通用功能)----------------------------
    # 1.为特定目标推送天气信息----"天气"
    def push_weather_to_one(self, uid, city=u"上海", day=0):
        print city + "<><><>" + str(day)
        msg = self.weather_service.get_city_message(city, -1, day)
        print msg
        #msg = city + "<><><>" + str(day)
        self.send_msg_by_uid(msg, uid)

    # 2.普通用户升级为管理员（输入管理员口令）
    def upgrade_to_admin(self, uid):
        admin_name = self.get_contact_prefer_name(self.get_contact_name(uid))
        for admin in self.admin_list:
            if admin_name == admin["Name"]:
                self.send_msg_by_uid("你当前已是管理员，回复\"管理员\"获得命令列表", uid)
                return None
        self.admin_list.append({"Name": admin_name})  # 添加当前用户至管理员
        self.set_conf()
        self.send_msg_by_uid("管理员模式开启,回复\"管理员\"获得命令列表", uid)

    # 3. 帮助信息----"帮助"
    def check_help_info(self, uid):
        reply = "[帮助]\n"
        reply += "回复\"天气\"获得天气信息\n"
        reply += "回复特殊口令获得管理员特权\n"
        reply += "Support by 爆炸开发小组"
        self.send_msg_by_uid(reply, uid)

    # ----------------------------响应天气请求---------------------------------
    #处理天气请求,默认回复今天上海天气
    def handle_weather_query(self, msg, uid):
        try:
            days = [u"今天", u"明天", u"后天", u"大后天"]
            key_words = [u"号", u"日"]
            day_code = 0
            for key_word in key_words:                         #判断是否有日期请求
                index = msg.find(key_words)
                if index != -1:
                    day_code = int(msg[index-1])
                    try:
                        day_code += int(msg[index-2])
                    except:
                        psss

            now = datetime.now()
            if now.month in [1,3,5,7,8,10,12]:                   #确定当前月天数
                a_month = 31
            

            msg = msg.replace(u"天气", "")                                   #删除消息中的"天气"
            for index in range(3, 0, -1):
                if msg.find(days[index]) != -1:
                    day_code = index
                    msg = msg.replace(days[index], "")                   #删除消息中的时间
            
            city = u"上海"
            if msg != "":
                 city = msg

            self.push_weather_to_one(uid, city, day_code)
        except:
            self.send_msg_by_uid("获取天气信息失败", uid)

    # ---------------------------通用群发函数----------------------------------
    # 群发消息给推送列表里的联系人
    def push_msg_to_target_contact(self, msg, isImg=False):
        for contact in self.target_contact:
            uid = self.get_user_id(contact["Name"])
            if uid is not None:
                if isImg:
                    self.send_img_msg_by_uid(msg, uid)
                else:
                    self.send_msg_by_uid(msg, uid)
            else:
                if self.DEBUG:
                    print "[ERROR] NOT FIND CONTACT %s." % (contact["Name"])

    # 群发消息给推送列表里的微信群
    def push_msg_to_target_group(self, msg, isImg=False):
        for group in self.target_group:
            uid = self.get_user_id(group["Name"])
            if uid is not None:
                if isImg:
                    self.send_img_msg_by_uid(msg, uid)
                else:
                    self.send_msg_by_uid(msg, uid)
            else:
                if self.DEBUG:
                    print "[ERROR] NOT FIND GROUP %s." % (group["Name"])

    def set_weather_service(self, weather_service):
        self.weather_service = weather_service

    def set_image_exist(self):
        self.image_exist = True


def main():
    # 启动天气服务
    weather_service = WeatherService()
    weather_service.refresh()

    # 启动机器人
    bot = WeatherBot()
    bot.set_weather_service(weather_service)

    # 启动图片渲染服务
    #image_service = ImageService()
    #image_service.generate_image(weather_service.get_publish_message(),
    #                             utils.get_image_path(),
    #                             bot.set_image_exist)

    # 启动定时服务
    #schedule_service = ScheduleService(weather_service, bot, image_service)
    #schedule_service.start_service()

    bot.DEBUG = True
    bot.conf['qr'] = 'tty'
    bot.run()

if __name__ == '__main__':
    main()
