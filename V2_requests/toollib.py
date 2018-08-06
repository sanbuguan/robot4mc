#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import datetime
import configparser
import base64


class toollib:

    @classmethod
    def is_json(cls,check_json):
        try:
            json_object = json.loads(check_json)
        except ValueError as e:
            return False
        return True

    @classmethod
    def date_now(cls):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))
        #return '2018-07-27'

    @classmethod
    def datenow(cls):
        return time.strftime('%Y%m%d',time.localtime(time.time()))

    @classmethod
    def time_now(cls):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    @classmethod
    def timenow(cls):
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    @classmethod
    def weekno(cls,date):
        return date.weekday()+1

    @classmethod
    def str2datetime(cls,datetimestr):
        return datetime.datetime.strptime(datetimestr, "%Y-%m-%d %H:%M:%S")


    @classmethod
    # 读取配置项的函数
    def getconfig(cls,filename, section,configitem):
        cf = configparser.ConfigParser()
        cf.read(filename, encoding='utf-8')
        return cf.get(section, configitem)

    @classmethod
    def getuserinfo(self,name):
        filename='config'+os.sep+'user_config.ini'
        return {'name':self.getconfig(filename,name,'name'), \
                'mail': self.getconfig(filename, name, 'mail'), \
                'passwd':self.getconfig(filename,name,'passwd'),\
                'cookie':str(base64.b64decode(self.getconfig(filename,name,'cookie')))}





if __name__ == '__main__':
    print(toollib.datenow())
    print(toollib.date_now())
    print(toollib.timenow())
    print(toollib.time_now())

    print(toollib.weekno(toollib.str2datetime(toollib.time_now())))
