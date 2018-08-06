#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import traceback
from collections import Counter
from config.log_config import *
#from meican_action import *
from meican_action import *
from  toollib import *
from getalllists import *

plan_path='plan'+os.sep

#需要用一个用户进行登陆，拉取最新的菜单
user_login='XXXXX'


if __name__ == '__main__':
    order_user_list=[]
    if len(sys.argv) > 1:
        # 使用固定参数的调试模式
        for item in sys.argv[1:]:
            order_user_list.append(item)
    else:
        # 使用自动扫描目录
        for item in os.listdir(plan_path):
            if os.path.splitext(item)[-1] == '.conf':
                order_user_list.append(os.path.splitext(item)[0])
    logging.info(order_user_list)

    #生成对应的列表
    logging.info('Try to generate the dinner list json...')
    try:
        userinfo = toollib.getuserinfo(user_login)
        logging.info(userinfo)
        meican_session = getalllists(userinfo)
        meican_session.generate_dinnerlist()

    except Exception as e:
        logging.error('oh generate dinner list fail ')
        logging.error(e)
        logging.error(traceback.print_exc())
        exit()

    #正式进行点餐
    allret = {}
    for item in order_user_list:
        try:
            plan_action=meican_plan_action(item)
            ret=plan_action.do()

            for item in ret:
                allret[ret[item]['name']] = {
                    'name':ret[item]['name'],'dinner_name':ret[item]['dinner_name'],'result':ret[item]['result']
                }
                logging.info('%s -> %s -> %s -> %s'%(toollib.date_now(),ret[item]['name'],ret[item]['dinner_name'],ret[item]['result']))

        except Exception as e:
            logging.error('%s.conf diner fail '%(item))
            logging.error(e)
            logging.error(traceback.print_exc())

    for item in allret:
        logging.info('<**> %s -> %s -> %s -> %s' % (toollib.date_now(), allret[item]['name'], allret[item]['dinner_name'], allret[item]['result']))
