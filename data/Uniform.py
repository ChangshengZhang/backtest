# -*- coding: utf-8 -*-
# File Name: Uniform .py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

def uniform(data_list,base_index):
	if len(data_list)==0:
		return []
	new_data_list = []
	base = data_list[base_index]
	for data in data_list:
		new_data_list.append(1.0*data_list[ii]/base)

	return new_data_list
	

