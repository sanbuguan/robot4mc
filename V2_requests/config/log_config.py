#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("..")
import logging
from toollib import  *


#日志的打印配置
meican_logfile='log'+os.sep+toollib.datenow()+'-ordermeican.log'
# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
logging.basicConfig(level=logging.INFO, \
                format='%(asctime)s [file:%(filename)-10s][line:%(lineno)-5d] %(levelname)s %(message)s', \
                datefmt='%a, %d %b %Y %H:%M:%S', \
                filename=meican_logfile, \
                filemode='a+')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s : [file:%(filename)-10s] [line:%(lineno)-5d] %(levelname)-8s %(message)s')
console.setFormatter(formatter)

logging.getLogger('').addHandler(console)