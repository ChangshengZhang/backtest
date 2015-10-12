# -*- coding: utf-8 -*-
# File Name: main.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

import data.LoadUserData as LoadUserData
import data.LoadData as LoadData
import output.WriteToFile as WriteToFile
import os 
import sys
from datetime import *

class CreepyDataFromWindClass():
	def __init__(self):
		self.data_type_list = ["daily","60min","30min","15min","5min"]
		file_path = "input/user_stock_name_list.xlsx"
		self.user_stock_name_list = LoadUserData.load_user_stock_name_list(file_path)
		print self.user_stock_name_list
		self.creepy_data_from_wind_to_local()

	def path_is_exist(self,stock_code):
		
		data_base_path = sys.path[0] +"\\"+"data"+"\\"+"data_base"
		stock_fold_path = data_base_path+"\\"+stock_code
		if os.path.exists(stock_fold_path) == False:
			print stock_fold_path
			os.mkdir(str(stock_fold_path))
			print "fold created "
			for data_type in self.data_type_list:
				os.mkdir(stock_fold_path+"\\"+data_type)
	
	#空文件返回20010101，否则返回最近一天日期
	def get_latest_date_in_fold(self,data_path):
		data_day_list = os.listdir(data_path)
		max_day = 0
		if len(data_day_list)==0:
			return "20000101"
		for data_day in data_day_list:
			temp_str = data_day.split(".")[0]
			
			if float(temp_str)>max_day:
				max_day = float(temp_str)
		return str(int(max_day))

	def get_day_sperate_index(self,stock_min_data):
		date_min_index = [0]
		for jj in range(1,len(stock_min_data[0])):
			if stock_min_data[0][jj][0][0:10]!=stock_min_data[0][jj-1][0][0:10]:
				date_min_index.append(jj)
		date_min_index.append(len(stock_min_data[0])+1)
		return date_min_index

	def creepy_data_from_wind_to_local(self):
		
		for ii in range(len(self.user_stock_name_list)):
			self.path_is_exist(self.user_stock_name_list[ii])
			data_base_path = sys.path[0] +"\\"+ "data"+"\\"+"data_base"
			stock_fold_path = data_base_path+"\\"+self.user_stock_name_list[ii]

			for data_type in self.data_type_list :
				
				data_path = stock_fold_path+"\\"+data_type
				latest_date = self.get_latest_date_in_fold(data_path)
				print latest_date
				temp_stock_name = []
				temp_stock_name.append(self.user_stock_name_list[ii])

				delta_day = (datetime.now()-datetime(int(latest_date[0:4]),int(latest_date[4:6]),int(latest_date[6:8]))).days
				print  latest_date, delta_day,self.user_stock_name_list[ii]

				pos = self.user_stock_name_list[ii].split(".")[1]
				print pos
				if data_type =="daily":

					stock_daily_data = LoadData.get_daily_stock_data(temp_stock_name,latest_date)
					for jj in range(len(stock_daily_data[0])):

						output_data_path = data_path+"\\"+stock_daily_data[0][jj][0]+".txt"
						WriteToFile.write_to_file(output_data_path,stock_daily_data[0][jj])

				if pos !="SZ" and pos !="SH" :
					break

				if float(delta_day)>3*365:
					delta_day = 1095
				if data_type == "60min":
					print "aaa"
	
					stock_60_min_data = LoadData.get_intraday_stock_data(temp_stock_name,bar_size=60,delta_days=delta_day)
					date_60_min_index = self.get_day_sperate_index(stock_60_min_data)
					print stock_60_min_data
					print date_60_min_index

					for jj in range(len(date_60_min_index)-1):
						file_path = data_path+"\\"+stock_60_min_data[0][date_60_min_index[jj]][0][0:8]+".txt"
						WriteToFile.write_list_to_file(file_path,stock_60_min_data[0][date_60_min_index[jj]:date_60_min_index[jj+1]])


				elif data_type == "30min":
					stock_30_min_data = LoadData.get_intraday_stock_data(temp_stock_name,bar_size=30,delta_days=delta_day)
					date_30_min_index = self.get_day_sperate_index(stock_30_min_data)

					for jj in range(len(date_30_min_index)-1):
						file_path = data_path +"\\"+stock_30_min_data[0][date_30_min_index[jj]][0][0:8]+".txt"
						WriteToFile.write_list_to_file(file_path,stock_30_min_data[0][date_30_min_index[jj]:date_30_min_index[jj+1]])
				elif data_type == "15min":
					stock_15_min_data = LoadData.get_intraday_stock_data(temp_stock_name,bar_size=15,delta_days=delta_day)
					date_15_min_index = self.get_day_sperate_index(stock_15_min_data)

					for jj in range(len(date_15_min_index)-1):
						file_path = data_path +"\\"+stock_15_min_data[0][date_15_min_index[jj]][0][0:8]+".txt"
						WriteToFile.write_list_to_file(file_path,stock_15_min_data[0][date_15_min_index[jj]:date_15_min_index[jj+1]])

				elif data_type == "5min":
					stock_5_min_data = LoadData.get_intraday_stock_data(temp_stock_name,bar_size=5,delta_days=delta_day)
					date_5_min_index = self.get_day_sperate_index(stock_5_min_data)

					for jj in range(len(date_5_min_index)-1):
						file_path = data_path +"\\"+stock_5_min_data[0][date_5_min_index[jj]][0][0:8]+".txt"
						
						WriteToFile.write_list_to_file(file_path,stock_5_min_data[0][date_5_min_index[jj]:date_5_min_index[jj+1]])



if __name__ == '__main__':
	a = CreepyDataFromWindClass()
	
