# -*- coding: utf-8 -*-
# File Name: AbsoluteMomentum .py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

# short_flag = True : long/short else : long away
def AbsoluteMomentum(stock_data_list,compare_day=4,short_flag = True):

	action_index_list = []
	action_type_list = []
	revenue_list = []

	for ii in range(len(stock_data_list)):

		action_index_list_per_stock = []
		action_type_list_per_stock = []
		revenue_list_per_stock = []
		
		# 0, empty 1,long -1 short
		pos_flag = 0
		for jj in range(compare_day,len(stock_data_list[ii])):

			if float(stock_data_list[ii][jj]) >= float(stock_data_list[ii][jj-compare_day]):
				
				if pos_flag !=1:
					action_index_list_per_stock.append(jj)
					action_type_list_per_stock.append("l")
					pos_flag = 1 
			else:
				if short_flag == True:
					if pos_flag != -1 :
						action_index_list_per_stock.append(jj)
						action_type_list_per_stock.append("s")
						pos_flag = -1 
				else:
					if pos_flag != 0 :
						action_index_list_per_stock.append(jj)
						action_type_list_per_stock.append("e")
						pos_flag = 0
		action_index_list.append(action_index_list_per_stock)
		action_type_list.append(action_type_list_per_stock)

	return action_index_list,action_type_list

