#!/usr/sbin/env python
# -*- coding:utf-8 -*-

import time
import toollib
import os

from flask import Flask,url_for,request
app = Flask(__name__)

@app.route('/')
def result():
    with open('result.log', 'r',encoding='utf-8') as logfile:
        content = time.strftime(' %Y-%m-%d %H:%M:%S ', time.localtime(time.time())) + '<br>'
        i=1
        for line in logfile:
            content="%s </br> %02d -> %s"%(content,i,line)
            i=i+1
    return content



@app.route('/log')
def log():

    logfile = 'log' + os.sep + toollib.toollib.datenow() + '-ordermeican.log'

    if not os.path.exists(logfile):
        content = time.strftime(' %Y-%m-%d %H:%M:%S ', time.localtime(time.time())) + '<br>'
        content =content + '点餐任务未执行，请执行任务'
        return content
    else:
        with open(logfile, 'r') as logfile:
            content=time.strftime(' %Y-%m-%d %H:%M:%S ',time.localtime(time.time()))+'<br>'
            for line in logfile:
                content = content + '</br>' + line
        return content


if __name__ == '__main__':
    # with app.test_request_context():
    #     pass
    app.run(host='0.0.0.0',port=48080)
