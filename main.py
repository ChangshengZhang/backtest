# -*- coding: utf-8 -*-
# File Name: main.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

import os
import sys
import strategy.test as test
import data.LoadData as LoadData
if __name__ == '__main__':
	
	b = LoadData.get_daily_stock_data(["600000.SH"])
	print b[0][0]

