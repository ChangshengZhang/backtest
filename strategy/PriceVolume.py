# -*- coding: utf-8 -*-
# File Name: pricevolume.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################
import scipy.stats as stats

def calc_ma(per_stock_data_list,jj,range_day):
	s = 0.0
	for ii in range(range_day): 
		s = s+per_stock_data_list[jj+ii-range_day+1]
	s = s/range_day
	return s


# data_list is 2-dim list
def PriceVolume(stock_data_list,range_day=1,regression_day = 5):
	slope_list = []

	for ii in range(len(stock_data_list)):
		
		ma_per_stock_data_list = []
		for jj in range(range_day-1,len(stock_data_list[ii])):
			ma_per_stock_data_list.append(calc_ma(stock_data_list[ii],jj,range_day))
		
		slope_per_stock_list = []
		for jj in range(regression_day-1,len(ma_per_stock_data_list)):
			temp = []
			for ii in range(regression_day):
				temp.append(ii+1)
			slope, intercept, r_value, p_value, std_err = stats.linregress(temp,ma_per_stock_data_list[jj-regression_day+1:jj+1])
			if slope>0:
				slope_per_stock_list.append(1)
			else:
				slope_per_stock_list.append(-1)

		slope_list.append(slope_per_stock_list)
	return slope_list






