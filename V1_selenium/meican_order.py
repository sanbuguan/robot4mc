#!/usr/sbin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import sys
import pickle
import configparser
import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


#url变量
login_url='https://meican.com/login'
order_list='https://meican.com/orders/list'
order_index='https://meican.com/index'
meican_prefix='https://meican.com'

#文件路径
config_path='config'+os.sep
cookie_path='cookie'+os.sep

#对应的网页按钮的配置
meican_html_username_text_id='email'
meican_html_passwd_text_id='password'
meican_html_login_btn_id='signin'



#日志的打印配置
meican_logfile='ordermeican.log'
# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
logging.basicConfig(level=logging.INFO, \
                format='%(asctime)s [line:%(lineno)-5d] %(levelname)s %(message)s', \
                datefmt='%a, %d %b %Y %H:%M:%S', \
                filename=meican_logfile, \
                filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s : [line:%(lineno)-5d] %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)



#读取配置项的函数
def getconfig(filename,configitem):
    cf = configparser.ConfigParser()
    cf.read(filename,encoding='utf-8')
    return cf.get("config", configitem)


#负责订餐的类
class order_meican:

    opener=None
    person=None
    configfile=None


    def __init__(self,person):

        self.person=person
        self.configfile=config_path+self.person+'.conf'

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-proxy-server')
        chrome_options.binary_location = (getconfig(self.configfile,'chrome'))
        #chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

        self.opener = webdriver.Chrome(chrome_options=chrome_options)
        self.opener.set_window_size(1440, 900)

    def __del__(self):
        try:
            self.opener.close()
            self.opener.quit()
        except Exception:
            pass


    def meican_login(self):
        logging.info('login for %s'%(self.person))
        pickle_cookie_file=cookie_path+self.person+'.cpkg'
        if os.path.exists(pickle_cookie_file):
            logging.info('exist cookie ,login use cookie file')
            pickle_cookie = pickle.load(open(pickle_cookie_file, 'rb'))
            self.opener.get(login_url)

            self.opener.delete_all_cookies()
            for cookie_item in pickle_cookie:
                self.opener.add_cookie({'name': cookie_item['name'], 'value': cookie_item['value']})
            self.opener.refresh()

        self.opener.get(order_list)
        time.sleep(0.5)
        cur_url=self.opener.current_url
        logging.info('get order_list url : %s ,except %s'%(cur_url,order_list))

        if ( cur_url != order_list):
            logging.info('use cookie file login fail, use passwd login')

            meican_username=getconfig(self.configfile,'username')
            meican_passwd=getconfig(self.configfile,'password')

            html_username=self.opener.find_element_by_id('email')
            html_username.clear()
            html_username.send_keys(meican_username)

            html_passwd=self.opener.find_element_by_id('password')
            html_passwd.clear()
            html_passwd.click()
            time.sleep(1)
            html_passwd.send_keys(meican_passwd)
            time.sleep(0.5)
            self.opener.find_element_by_id('signin').click()

        self.opener.get(order_list)
        time.sleep(0.5)
        cur_url = self.opener.current_url
        if (cur_url != order_list):
            logging.error('use cookie and passwd for login both file')
            raise
        else:
            logging.info('login OK @_@')
            pickle.dump(self.opener.get_cookies(),open(pickle_cookie_file, 'wb'))


    def order_dinner(self):

        #点击第一部分
        self.opener.get(order_index)
        count=0
        while len(self.opener.find_elements_by_partial_link_text('晚餐')) <= 0:
            time.sleep(0.5)
            logging.info('order index,waiting for page load complete')
            count=count+1
            if count > 30:
                logging.error('find step1 left date error')
                raise
        self.opener.find_elements_by_partial_link_text('晚餐')[0].click()
        time.sleep(2)

        config_item = 'day%d' % (datetime.datetime.now().weekday() + 1)
        dinner_array=getconfig(self.configfile,config_item).split('-')

        #获取配置信息
        dinner_room=dinner_array[0]
        dinner_type=dinner_array[1]
        dinner_name=dinner_array[2]


        #第二步，点击店名
        count = 0
        while len(self.opener.find_elements_by_partial_link_text(dinner_room)) <= 0:
            time.sleep(0.5)
            logging.info('order dinner_room,waiting for page load complete')
            logging.info(self.opener.find_elements_by_partial_link_text(dinner_room))
            count = count + 1
            if count > 30:
                logging.error('find step2 dinner_room error')
                raise
        self.opener.find_elements_by_partial_link_text(dinner_room)[0].click()
        time.sleep(2)

        # # 第三步，点击类型
        count = 0
        css_selector="li"
        while len(self.opener.find_elements_by_css_selector(css_selector)) <= 0:
            time.sleep(0.5)
            logging.info('order dinner_type,selenium waiting for page load complete')
            count = count + 1
            if count > 30:
                logging.error('selenium waiting for find step3 dinner_type error')
                raise

        css_selector_target=-1
        css_selector_list=self.opener.find_elements_by_css_selector(css_selector)
        for i in range(0,len(css_selector_list)):
            if css_selector_list[i].get_attribute('innerHTML').strip() == dinner_type:
                css_selector_target=i
                print(css_selector_target)
                break
        if css_selector_target == -1:
            logging.error('selenium can not for find step3 dinner_type error')
            raise

        print(css_selector_target)

        #注入jquery 3.2.1
        with open('jquery.min.js', 'r') as jquery_js:
            jquery = jquery_js.read()  # read the jquery from a file
            self.opener.execute_script(jquery)  # active the jquery lib

        if self.opener.execute_script('return $.fn.jquery') != '3.2.1':
            logging.error('Inject jquery 3.2.1. fail')
            raise

        self.opener.execute_script("$('li')[%d].click()"%(css_selector_target))
        time.sleep(2)




        # 第四步，点击菜品
        count = 0
        css_selector = "li"
        while len(self.opener.find_elements_by_css_selector(css_selector)) <= 0:
            time.sleep(0.5)
            logging.info('order dinner_name,selenium waiting for page load complete')
            count = count + 1
            if count > 30:
                logging.error('selenium waiting for find step4 dinner_name error')
                raise

        css_selector_target = -1
        css_selector_list = self.opener.find_elements_by_css_selector(css_selector)
        for i in range(0, len(css_selector_list)):
            if css_selector_list[i].get_attribute('innerText').strip().find(dinner_name) == 0:
                css_selector_target = i
                print(css_selector_target)
                break
        if css_selector_target == -1:
            logging.error('selenium can not for find step4 dinner_name error')
            raise

        print(css_selector_target)

        #qqq = self.opener.execute_script('return $.fn.jquery')
        self.opener.execute_script("$('li')[%d].click()" % (css_selector_target))
        time.sleep(2)


        #第五步
        meican_orderBtn_Click='$(\':contains("下单")\')[$(\':contains("下单")\').length-1].click()'

        time.sleep(1)
        #第一次click
        self.opener.execute_script(meican_orderBtn_Click)
        time.sleep(2)
        # 第二次click
        self.opener.execute_script(meican_orderBtn_Click)

        # 
        # for i in range(0,10):
        #     time.sleep(0.5)
        #     # 第二次click
        #     self.opener.execute_script(meican_orderBtn_Click)
        #
        if (not self.order_dinner_check()):
            logging.error('finally check dinner order fail')
            raise


    def order_dinner_check(self):
        self.opener.get(order_list)
        time.sleep(0.5)


        count = 0
        while len(self.opener.find_elements_by_css_selector("option")) <= 0:
            time.sleep(0.5)
            logging.info('check dinner,waiting for page load complete')
            count = count + 1
            if count > 30:
                logging.error('check dinner option  error')
                return False

        dinner_check_url=''
        option_list=self.opener.find_elements_by_css_selector("option")
        for item in option_list:

            if item.get_attribute('innerHTML').strip().find('晚餐') >=0:
                dinner_check_url=item.get_attribute('value').strip()

        if dinner_check_url=='':
            logging.error('get check url value fail')
            return False

        self.opener.get(meican_prefix+dinner_check_url)
        time.sleep(1)

        count = 0
        while len(self.opener.find_elements_by_css_selector("a")) <= 0:
            time.sleep(0.5)
            logging.info('check dinner item ,waiting for page load complete')
            count = count + 1
            if count > 30:
                logging.error('check dinner item  error')
                return False

        #获取今天的日期
        today=datetime.datetime.now().strftime('%Y-%m-%d')

        check_item=self.opener.find_elements_by_css_selector("a")
        for item in check_item:
            if item.get_attribute('innerHTML').strip().find(today) >=0 :
                return True
        return False


if __name__ == '__main__':

    logging.info('version:1.0.1 - build 20171017-1030')
    order_user_list=[]
    fail_user_list=[]

    
    if len(sys.argv) > 1:
        #使用固定参数的调试模式
        for item in sys.argv[1:]:
            order_user_list.append(item)
    else:
        #使用自动扫描目录
        for item in os.listdir(config_path):
            if os.path.splitext(item)[-1] == '.conf':
                order_user_list.append(os.path.splitext(item)[0])

    for item in order_user_list:
        try:

            order_dinner=order_meican(item)
            order_dinner.meican_login()

            if (not order_dinner.order_dinner_check()) :
                order_dinner.order_dinner()
            else:
                logging.info('*' * 40)
                logging.info('### #result# [%s]:already order dinner' % item)
                logging.info('*' * 40)

        except Exception as e :
            logging.error(e,exc_info=True)
            logging.info('*' * 40)
            logging.error('### #result# [%s]:order dinner fail'%item)
            logging.info('*' * 40)
            fail_user_list.append(item)
        else:
            logging.info('*' * 40)
            logging.info('### #result# [%s]:order dinner OK' %item)
            logging.info('*' * 40)

    # for item in range(1, len(sys.argv)):
    #     try:
    #         order_dinner=order_meican(sys.argv[item])
    #         order_dinner.meican_login()
    #         order_dinner.order_dinner()
    #     except Exception as e :
    #         logging.error(e,exc_info=True)
    #         logging.error('#result# [%s]:点餐失败fail，不知道他有没有饭吃，不管他了'%sys.argv[item])
    #     else:
    #         logging.info('#result# [%s]:点餐成功OK' % sys.argv[item])
    logging.info('### #result# ************* try again ********')
    for item in fail_user_list:
        try:

            order_dinner=order_meican(item)
            order_dinner.meican_login()

            if (not order_dinner.order_dinner_check()) :
                order_dinner.order_dinner()
            else:
                logging.info('*' * 40)
                logging.info('### #result# [%s]:already order dinner' % item)
                logging.info('*' * 40)

        except Exception as e :
            logging.error(e,exc_info=True)
            logging.info('*' * 40)
            logging.error('### #result# [%s]:order dinner fail'%item)
            logging.info('*' * 40)
        else:
            logging.info('*' * 40)
            logging.info('### #result# [%s]:order dinner OK' %item)
            logging.info('*' * 40)

















