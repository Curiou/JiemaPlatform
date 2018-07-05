# !/usr/bin/python
# -*- encoding: utf-8 -*-
"""
    author: conglin du
    license: (C) Copyright 2018-2020, Shanghai hot nest network technology co. LTD.
    contact: gduxiansheng@gmail.com or 2544284522@qq.com
    file: JiemaPlatform_51ym.py
    time: 2018/6/28 13:43
"""
import re
import time

import requests
requests.packages.urllib3.disable_warnings()
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import random
import json
import hashlib


class JiemaPlatform(object):
    def __init__(self, username, password, number):
        self.username = username
        self.password = password
        self.number = number
        self.num = 1
        self.logIn()
        self.telnum = ["175", "187", "153", "135"]
        

    def logIn(self):
        # 登陆获key
        log_in = "http://api.fxhyd.cn/UserInterface.aspx?action=login&username=%s&password=%s"%(self.username,self.password)
        ron = requests.get(log_in)
        token = re.findall(u"success\|(.*)", ron.text)
        if token:
            self.token = token[0]
        elif self.num < 3:
            self.num += 1
            self.logIn()
        else:
            print("Account or password error")

    def select(self):
        # 查询信息
        select = "http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token=%s&format=1"%self.token
        ron = requests.get(select)
        return ron.text

    def getPhone(self):
        # 获得号码
        phone = "http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=%s&itemid=%s&excludeno=%s&release=1"%(self.token, self.number, random.choice(self.telnum))
        ron = requests.get(phone)
        phone_number = re.findall(u"success\|(.*)", ron.text)
        if phone_number:
            return phone_number[0]
        else:
            print("token not None")

    def getNote(self, phone):
        # 获取短信
        note = "http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=%s&itemid=%s&mobile=%s"%(self.token, self.number, phone)
        ron = requests.get(note)
        notesend = re.findall(u"success\|(.*)", ron.content)
        if notesend:
            return notesend[0]
        else:
            print("No SMS or network timeout received")

    def liberatePhone(self, phone):
        # 释放号码
        note = "http://api.fxhyd.cn/UserInterface.aspx?action=release&token=%s&itemid=%s&mobile=%s"%(self.token, self.number, phone)
        ron = requests.get(note)
        print (ron.text)

    def blackPhone(self, phone):
        # 拉黑号码
        note = "http://api.fxhyd.cn/UserInterface.aspx?action=addignore&token=%s&itemid=%s&mobile=%s"%(self.token, self.number, phone)
        ron = requests.get(note)
        print (ron.text)


if __name__ == '__main__':
    jiema = JiemaPlatform(username="用户名", password="密码", number="项目编号")
    phone = jiema.getPhone()
    print(phone)
