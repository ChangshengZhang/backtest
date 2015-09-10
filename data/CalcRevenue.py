# -*- coding: utf-8 -*-
# File Name: CalcRevenue .py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

# stock_close_data_list is a 2-dim list, which only contains closed price
# action_index is a -2-dim list
# action_type 's value is "l", "s", "e"(empty)
def calc_revenue(stock_close_data_list,action_index,action_type,trade_cost=0.0015):

	revenue_list = []
	for ii in range(len(stock_close_data_list)):
		revenue_per_stock = []
		index_kk = 0
		pos_status = 0

		temp = 1

		for jj in range(len(stock_close_data_list[ii])):

			if pos_status ==0:
				revenue_per_stock.append(temp)
			elif pos_status ==1:
				temp = float(stock_close_data_list[ii][jj])/float(stock_close_data_list[ii][jj-1])*temp
				revenue_per_stock.append(temp)
			else:
				temp = (2-float(stock_close_data_list[ii][jj])/float(stock_close_data_list[ii][jj-1]))*temp
					revenue_per_stock.append(temp)

			if index_kk <len(action_index[ii]) and jj == action_index[ii][index_kk]:
				if action_type[ii][index_kk] =="l":
					pos_status =1
					temp = temp*(1-trade_cost)
				elif: action_type[ii][index_kk] =="s":
					pos_status = -1 
					temp = temp *(1-trade_cost)
				elif: action_type[ii][index_kk] == "e":
					pos_status = 0 
					temp = temp*(1-trade_cost)
				else:
					pos_status = 0 
			index_kk = index_kk + 1 
		revenue_list.append(revenue_per_stock)
	return revenue_list
	



