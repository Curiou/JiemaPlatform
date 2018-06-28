# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import requests
import re
import os
import random
import time
import json
import hashlib


class JiemaPlatform(object):
    def __init__(self, user, pwd, docks):
        self.user = user
        self.pwd = pwd
        self.docks = docks
        self.logIn()
        self.telnum = ["17", "18", "15", "13"]

    def get_md5(self, strs):
        m = hashlib.md5()
        m.update(strs)
        return m.hexdigest()

    def logIn(self):
        # 登陆获key
        log_in = "http://sms.60ma.net/loginuser?cmd=login&encode=utf-8"
        data = {
            "username": self.user,
            "password": self.get_md5(self.pwd),
            "dtype": "json",
        }
        ron = requests.get(log_in, params=data)
        ron = json.loads(ron.text)["Return"]
        self.uid = ron["UserID"]
        self.key = ron["UserKey"]

    def select(self):
        # 查询信息
        select = "http://sms.60ma.net/queryinfo?cmd=query&encode=utf-8&api=yes"
        data = {
            "userid": self.uid,
            "userkey": self.key,
            "dtype": "json",
        }
        ron = requests.get(select, params=data)
        return json.loads(ron.text)["Return"]

    def getPhone(self):
        # 获得号码
        phone = "http://sms.60ma.net/newsmssrv?cmd=gettelnum&encode=utf-8"
        data = {
            "userid": self.uid,
            "userkey": self.key,
            "docks": self.docks,
            "telnumsection": "18",
            "dtype": "json",
        }
        data["telnumsection"] = random.choice(self.telnum)
        ron = requests.get(phone, params=data)
        return json.loads(ron.text)["Return"]

    def getNote(self, phone):
        # 获取短信
        note = "http://sms.60ma.net/newsmssrv?cmd=getsms&encode=utf-8"
        data = {
            "userid": self.uid,
            "userkey": self.key,
            "dockcode": self.docks,
            "telnum": phone,
            "dtype": "json",
        }
        ron = requests.get(note, params=data)
        return json.loads(ron.text)["Return"]

    def liberatePhone(self, phone):
        # 释放号码
        note = "http://sms.60ma.net/newsmssrv?cmd=freetelnum&encode=utf-8"
        data = {
            "userid": self.uid,
            "userkey": self.key,
            "docks": self.docks,
            "telnum": phone,
            "dtype": "json",
        }
        ron = requests.get(note, params=data)
        print json.loads(ron.text)["Return"]

    def liberateAllPhone(self):
        # 释放所有号码
        note = "http://sms.60ma.net/newsmssrv?cmd=freetelnumall&encode=utf-8"
        data = {
            "userid": self.uid,
            "userkey": self.key,
            "dtype": "json",
        }
        ron = requests.get(note, params=data)
        print json.loads(ron.text)["Return"]

    def blackPhone(self, phone):
        # 拉黑号码
        note = "http://sms.60ma.net/newsmssrv?cmd=addblacktelnum&encode=utf-8"
        data = {
            "userid": self.uid,
            "userkey": self.key,
            "docks": self.docks,
            "telnum": phone,
            "dtype": "json",
        }
        ron = requests.get(note, params=data)
        print json.loads(ron.text)["Return"]


if __name__ == '__main__':
    jingzhunjiema = JiemaPlatform(user="用户名", pwd="密码", docks="对接码")
    phone = jingzhunjiema.getPhone()["Telnum"]
    print(phone)
