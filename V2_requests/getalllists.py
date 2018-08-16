#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from io import BytesIO
import pickle
import traceback
import random
import time

import requests
#from PIL import Image

from url_def import *
from config.log_config import *
from  toollib import *

class getalllists:

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38'}

    def __init__(self,userinfo):
        self.userinfo=userinfo
        self.cookie_path='cookie'+os.sep
        self.pickle_cookie_file = self.cookie_path + self.userinfo['name'] + '.cpkg'
        self.query_session = requests.Session()
        self.query_session.headers=self.headers
        self.restrant=list()
        self.id={}
        self.dinnerlist={}
        self.dinnerlistfile='dinnerlist.json'
        self.tab_location=2


    #用于登录的接口，先使用直接登录，再使用pinckle进行登录，最后使用文件cookie进行登录
    def login(self):

        #直接使用登录接口
        data={'username':self.userinfo['mail'],'loginType':'username','password':self.userinfo['passwd'],'remember':'true','openId':'','redirectUrl':''}
        self.query_session.post(url_config.url_login,data)
        time.sleep(0.5)

        tab_url=url_config.tab_url%(toollib.date_now(),toollib.date_now())
        logging.info(tab_url)
        left_tab_content=self.query_session.get(tab_url).text
        time.sleep(0.5)
        #left_tab_content=''
        logging.info('%s direct login is %s'%(self.userinfo['name'],toollib.is_json(left_tab_content)))


        if ( not toollib.is_json(left_tab_content)):
            ###表示没有登录成功,先尝试进行pinckle登录，在进行文件加载cookie
            self.pickle_cookie_file=self.cookie_path+self.userinfo['name']+'.cpkg'
            if os.path.exists(self.pickle_cookie_file):
                logging.info('exist cookie file  ,login use cookie file')
                pickle_cookie = pickle.load(open(self.pickle_cookie_file, 'rb'))
                self.query_session.cookies.clear()
                self.query_session.cookies=pickle_cookie
            else:
                logging.info(self.userinfo['name']+' not exist cookie file ,login use cookie file')

        else:
            pickle.dump(self.query_session.cookies, open(self.pickle_cookie_file, 'wb'))
            return True

        left_tab_content = self.query_session.get(tab_url).text
        time.sleep(0.5)

        #left_tab_content = ''
        if (not toollib.is_json(left_tab_content)):
            logging.info(self.userinfo['name']+' use cookie file login fail , will use config file cookie')
            self.query_session.cookies.clear()
            cookies = {}
            #尝试使用配置文件cookie进行登录
            for line in self.userinfo['cookie'].split(';'):
                name, value = line.strip().split('=', 1)
                self.query_session.cookies.set(name,value)
        else:
            logging.info(self.userinfo['name']+' use cookie file login OK ')
            pickle.dump(self.query_session.cookies, open(self.pickle_cookie_file, 'wb'))
            return True

        left_tab_content = self.query_session.get(tab_url).text
        time.sleep(0.5)

        if (not toollib.is_json(left_tab_content)):
            logging.info(self.userinfo['name'] + ' use config cookie file ,login fail will die ')
            logging.error(self.userinfo['name']+' login fail........[<>]')
            return False
        else:
            logging.info(self.userinfo['name']+' use config cookie file login OK ')
            pickle.dump(self.query_session.cookies, open(self.pickle_cookie_file, 'wb'))
            return True
        #显示图片
        # a=self.query_session.get("https://www.cnblogs.com/skins/summerGarden/images/header.jpg", stream=True).content
        # im = Image.open(BytesIO(a))
        # im.show()

    #得到订餐的左树ID，后面需要使用
    def get_left_id(self):
        tab_url = url_config.tab_url % (toollib.date_now(), toollib.date_now())
        logging.info(self.query_session.cookies.items())
        left_tab_content=self.query_session.get(tab_url).text
        time.sleep(0.5)
        logging.info('left tab url -> %s'%(tab_url))
        #logging.info(left_tab_content)
        tab_json=json.loads(left_tab_content)

        #logging.info(tab_json)
        for i in range(0,len(tab_json['dateList'][0]['calendarItemList'])):
            if tab_json['dateList'][0]['calendarItemList'][i]['title'] == '分期乐（深圳）晚餐':
                self.tab_location=i
        logging.info('%s left tab id is %s'%(self.userinfo['name'],self.tab_location))

        self.id['open_id']=((tab_json['dateList'][0]['calendarItemList'][self.tab_location]['openingTime']['uniqueId']))
        self.id['user_id']=((tab_json['dateList'][0]['calendarItemList'][self.tab_location]['userTab']['uniqueId']))
        self.id['user_corp_id']=((tab_json['dateList'][0]['calendarItemList'][self.tab_location]['userTab']['corp']['uniqueId']))
        self.id['user_corp_add_id']=((tab_json['dateList'][0]['calendarItemList'][self.tab_location]['userTab']['corp']['addressList'][0]['uniqueId']))
        logging.info(self.id)

    #得到可以点餐的餐厅列表
    def get_restrant_list(self):
        restrants_url=url_config.restrants_url%(self.id['user_id'],toollib.date_now())
        logging.info(restrants_url)
        restrants_content=self.query_session.get(restrants_url).text
        time.sleep(0.5)
        restrants_content = json.loads(restrants_content)
        logging.info(restrants_content['restaurantList'])

        for i in range(0,len(restrants_content['restaurantList'])):
            self.restrant.append({'name':restrants_content['restaurantList'][i]['name'],\
                                  'id':restrants_content['restaurantList'][i]['uniqueId']})
        logging.info(self.restrant)

    #得到对应餐厅的餐品list
    def get_dinner_list(self):
        for restrant_item in self.restrant:
            dinner_url=url_config.dinner_url%(restrant_item['id'],self.id['user_id'],toollib.date_now())
            dinner_content=self.query_session.get(dinner_url).text
            time.sleep(0.5)
            dinner_content=json.loads(dinner_content)
            for dish_item in dinner_content['dishList']:
                if (dish_item['originalPriceInCent'] != 0 ):
                    dinner_name,ignore=dish_item['name'].strip().split('(', 1)
                    self.dinnerlist[dinner_name]={'dinner_name':dinner_name,\
                        'dinner_id':dish_item['id'],'restrant_id':restrant_item['id'],\
                        'restrant_name':restrant_item['name']}

        logging.info('%s ---> %s'%(toollib.date_now(),len(self.dinnerlist)))
        for item in self.dinnerlist:
            logging.info(self.dinnerlist[item])
        json.dump(self.dinnerlist,open(self.dinnerlistfile, 'w'))


    #查询对应的订餐信息
    def check_dinner_info(self,order_date):
        try:
            query_url=url_config.query_url%(order_date,order_date)
            logging.info(query_url)
            query_content=self.query_session.get(query_url).text
            query_content=json.loads(query_content)
            logging.info(self.tab_location)
            order_query_id=query_content['dateList'][0]['calendarItemList'][self.tab_location]['corpOrderUser']['uniqueId']

            order_data={'uniqueId':order_query_id,'type':'CORP_ORDER','progressMarkdownSupport':'true'}
            order_info=self.query_session.post(url_config.order_info_url,order_data).text
            time.sleep(0.5)
            order_info=json.loads(order_info)

            logging.info('%s in %s dinner ---> %s '%(self.userinfo['name'],order_date,order_info['restaurantItemList'][0]['dishItemList'][0]['dish']['name']))
            order_dinner_info=order_info['restaurantItemList'][0]['dishItemList'][0]['dish']['name']
            return order_dinner_info
        except Exception as e:
            logging.error('%s %s query dinner fail'%(order_date,self.userinfo['name']))
            logging.error(e)
            #logging.error(traceback.print_exc())
            return ''


    #根据ID进行点餐的接口
    def order_dinner(self,dinnerid,date):
        order_dinner_url=url_config.order_dinner_url%(self.id['user_corp_add_id'],dinnerid,self.id['user_id'],date,self.id['user_corp_add_id'])
        logging.info(order_dinner_url)

        order_result=self.query_session.post(order_dinner_url).text
        time.sleep(0.5)
        order_result=json.loads(order_result)
        logging.info(order_result)
        # order_result={"message":"","order":{"uniqueId":"e6ec0a946cae"},"status":"SUCCESSFUL"}
        # order_result={'error': 'CORP_NOT_IN_OPENING_TIME', 'error_description': '您的企业目前不在订餐时段，请在订餐时段再次尝试'}
        # order_result ={"error": "CORP_MEMBER_ORDER_EXISTS","error_description": "您已经创建过订单，需要先取消才能再次创建"}

        if ('status' in order_result):
            return {'ret':0,'msg':'OK'}
        elif('error' in order_result):
            if order_result['error']=='CORP_NOT_IN_OPENING_TIME':
                return {'ret':1,'msg':'TIME ERROR'}
            elif order_result['error']=='CORP_MEMBER_ORDER_EXISTS':
                return {'ret': 2, 'msg': 'ALREADY'}
            else:
                return {'ret': 99, 'msg': 'unknow error'}
        else:
             return {'ret':999,'msg':'unknow status'}


    @classmethod
    def dinner_name2id(cls,dinner_name):
        dinnerlistfile = 'dinnerlist.json'
        if os.path.exists(dinnerlistfile):
            dinnerlist=json.load(open(dinnerlistfile, 'rb'))


        # 增加一个真正随机的逻辑
        if dinner_name == '0':
            random_id = random.randint(0, len(dinnerlist) - 1)
            dinner_name = list(dinnerlist.keys())[random_id]
            logging.info('fully random dinner is %s' %(dinner_name))

        #菜品不在里面，可能是下架了，就随机点一个
        if (not (dinner_name in dinnerlist)):
            logging.error('%s is not exist, will remove'%(dinner_name))
            
            random_id = random.randint(0, len(dinnerlist) - 1)
            dinner_name = list(dinnerlist.keys())[random_id]
            logging.info('fully random dinner is %s' %(dinner_name))


        return dinnerlist[dinner_name]['dinner_id']


    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 下面是整合接口

    #拼合函数进行生成列表
    def generate_dinnerlist(self):
        try:
            self.login()
            self.get_left_id()
            self.get_restrant_list()
            self.get_dinner_list()
        except Exception as e:
            logging.error('%s generate dinner list fail '%(self.userinfo['name']))
            logging.error(e)
            logging.error(traceback.print_exc())

    def order_dinner_by_name(self,dinnername):
        try:
            self.login()
            self.get_left_id()
            dinner_id=self.dinner_name2id(dinnername)
            ret=self.order_dinner(dinner_id,toollib.date_now())
            logging.info(('%s %s -> %s')%(self.userinfo['name'],toollib.date_now(),ret))
            return ret
        except Exception as e:
            logging.error(('%s %s order fail .....') % ( self.userinfo['name'], toollib.date_now()))
            logging.error(e)
            logging.error(traceback.print_exc())

if __name__ == '__main__':

    if (len(sys.argv) != 3):
        print('usage : cmd username dinnername')
        exit()
    # 单个人点餐
    username=sys.argv[1]
    dinnername=sys.argv[2]
    userinfo=toollib.getuserinfo(username)
    logging.info(userinfo)
    meican_session=getalllists(userinfo)
    meican_session.generate_dinnerlist()
    ret=meican_session.order_dinner_by_name(dinnername)
    logging.info(ret)
    ret=meican_session.check_dinner_info(toollib.date_now())
    logging.info('%s -> %s -> %s'%(toollib.date_now(),meican_session.userinfo['name'],ret))













