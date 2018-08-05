#!/usr/sbin/env python
# -*- coding:utf-8 -*-

import time

from flask import Flask,url_for,request
app = Flask(__name__)

@app.route('/log')
def log():
    with open('ordermeican.log', 'r') as logfile:
        content=''
        for line in logfile:
        	content=content+'</br>'+line
    return content



@app.route('/')
def result():
    with open('ordermeican.log', 'r') as logfile:
        content=time.strftime(' %Y-%m-%d %H:%M:%S ',time.localtime(time.time()))+'<br>'
        for line in logfile:
        	if line.find('result') >=0:
        		content=content+'</br>'+line.split('#result#')[1]+'</br>'
    return content


if __name__ == '__main__':
    # with app.test_request_context():
    #     pass
    app.run(host='0.0.0.0',port=48080)