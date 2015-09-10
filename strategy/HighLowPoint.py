# -*- coding: utf-8 -*-
# File Name: low and high point .py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################




def get_rise_rate_flag(new_point,old_point,threshold = 0.1):
	
	if (float(new_point)-float(old_point))/float(old_point) > threshold:
		return True
	else:
		return False

def get_fall_rate_flag(new_point,old_point,threshold = 0.1):
	if (float(new_point)-float(old_point))/float(old_point) < -1.0* threshold:
		return True
	else:
		return False


def get_high_low_points_list(stock_data_list):

	stock_date_index = 0
	stock_open_index = 1
	stock_high_index = 2
	stock_low_index = 3
	stock_close_index = 4
	stock_volume_index = 5
	stock_amt_index = 6

	compare_day = 13
	threshold = 0.1

	low_points_index_list = []
	low_points_list = [] 
	high_points_index_list = []
	high_points_list = []

	for ii in range(len(stock_data_list)):

		low_points_list_per_stock =[]
		low_points_index_list_per_stock = []
		high_points_list_per_stock = []
		high_points_index_list_per_stock = []

		temp_high_index = 0
		temp_low_index = 0 
		temp_high_point = stock_data_list[ii][0][stock_high_index]
		temp_low_point = stock_data_list[ii][0][stock_low_index]

		rise_fall_flag =1 

		for kk in range(len(stock_data_list[ii])):

			if stock_data_list[ii][kk][stock_high_index] >=temp_high_point:
				temp_high_index = kk 
				temp_high_point = stock_data_list[ii][temp_high_index][stock_high_index]
			if stock_data_list[ii][kk][stock_low_index] <= temp_low_point:
				temp_low_index = kk 
				temp_low_point = stock_data_list[ii][temp_low_index][stock_low_index]

			if rise_fall_flag ==1:
				if temp_low_index - temp_high_index < 0:
					temp_low_index = temp_high_index 
					temp_low_point = stock_data_list[ii][temp_low_index][stock_low_index]
			elif rise_fall_flag == -1:
				if temp_high_index - temp_low_index <0:
					temp_high_index = temp_low_index
					temp_high_point = stock_data_list[ii][temp_high_index][stock_high_index]

			if rise_fall_flag ==1 and (get_fall_rate_flag(stock_data_list[ii][kk][stock_low_index],temp_high_point,threshold) or temp_low_index - temp_high_index > compare_day):
				high_points_index_list_per_stock.append(temp_high_index)
				high_points_list_per_stock.append(stock_data_list[ii][temp_high_index][stock_high_index])
				temp_low_index = kk 
				temp_low_point = stock_data_list[ii][temp_low_index][stock_low_index]
				rise_fall_flag = rise_fall_flag*-1

			elif rise_fall_flag ==-1 and (get_rise_rate_flag(stock_data_list[ii][kk][stock_high_index],temp_low_point,threshold)or temp_high_index  -temp_low_index > compare_day):
				low_points_index_list_per_stock.append(temp_low_index)
				low_points_list_per_stock.append(stock_data_list[ii][temp_low_index][stock_low_index])
				temp_high_index = kk 
				temp_low_point = stock_data_list[ii][temp_high_index][stock_high_index]
				rise_fall_flag = rise_fall_flag*-1

		low_points_index_list.append(low_points_index_list_per_stock)
		low_points_list.append(low_points_list_per_stock)
		high_points_index_list.append(high_points_index_list_per_stock)
		high_points_list.append(high_points_list_per_stock)

	return high_points_index_list,high_points_list,low_points_index_list,low_points_list

