# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 14:05:13 2018
@author: zhangsuowei
"""

from iFinDPy import *
import csv
import pandas as pd
import numpy as np
#设置显示行数
pd.set_option('display.max_columns', 10000, 'display.max_rows', 10000)
#取消科学计算法

thsLogin = iFinDPy.THS_iFinDLogin('账号','密码')

if not (thsLogin == 0 or thsLogin == -201):
    print("登录失败")
else:
	thsData=THS_DataPool('index','2019-04-02;885700.TI','date:Y,thscode:Y,security_name:Y,weight:Y')
	ths_codes=','.join(thsData['tables'][0]['table']['THSCODE'])
	roe_data=THS_RealtimeQuotes(ths_codes','mainNetInflow;latest;changeRatio') 
	result=THS_Trans2DataFrame(roe_data)
	result.to_csv('roe.csv',encoding='gbk')
	print("file saved")