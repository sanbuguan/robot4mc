#!/usr/bin/env python
# -*- coding: utf-8 -*-


from toollib import *
from getalllists import *
import traceback
import random



class meican_plan_action:


    def __init__(self,plan_file):
        self.plan_file='plan'+os.sep+plan_file+'.conf'
        self.do_list={}


    def generate_order_list(self):
        ignore_date = toollib.getconfig(self.plan_file, 'ignore', 'date').split(';')
        for date_item in ignore_date:
            if toollib.date_now() == date_item:
                logging.info('%s %s will igonre....'%(date_item,self.plan_file))
                self.do_list = {}
                return self.do_list

        userlist=toollib.getconfig(self.plan_file,'userlist','userlist').split(';')
        logging.info('%s userlist is %s'%(self.plan_file,userlist))

        for user in userlist:
            self.do_list[user]={'name':user,'dinner_name':'','dinner_id':'','ret':'','result':''}

        weekday='day'+str(toollib.weekno(datetime.datetime.today()))
        logging.info('today is %s'%(weekday))

        dinnerlist = toollib.getconfig(self.plan_file, weekday, 'dinnerlist').split(';')
        logging.info('%s userlist %s is %s' % (self.plan_file, weekday,dinnerlist))

        for user in userlist:
            random_dinner=dinnerlist.pop(random.randint(0,len(dinnerlist)-1))
            dinner_id=getalllists.dinner_name2id(random_dinner)
            self.do_list[user]['dinner_name']=random_dinner
            self.do_list[user]['dinner_id']=dinner_id

        return self.do_list


    #需要操作的聚合函数
    def do(self):

        self.generate_order_list()
        logging.info(self.do_list)
        try:
            for item in self.do_list:
                logging.info('%s will order dinner'%(item))

                meican_session=getalllists(toollib.getuserinfo(item))

                ret=meican_session.order_dinner_by_name(self.do_list[item]['dinner_name'])
                self.do_list[item]['ret']=ret
                self.do_list[item]['result']=meican_session.check_dinner_info(toollib.date_now())

            return self.do_list

        except Exception as e:
            logging.error(e)
            logging.error(traceback.print_exc())

if __name__ == '__main__':
    logging.info(random.randint(1,10))