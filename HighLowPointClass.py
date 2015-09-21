# -*- coding: utf-8 -*-
# File Name: main.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

import os
import sys
import strategy.HighLowPoint as HighLowPoint
import data.LoadUserData as LoadUserData
import data.LoadData as LoadData
import time
import output.SendEmail as SendEmail

class HighLowPointClass():
	"""docstring for HighLowPointClass"""
	def __init__(self):
		file_path = "input/user_data.xlsx"
		self.stock_code_list,self.stock_name_list,self.stock_buy_price_list,self.stock_sell_price_list =LoadUserData.load_user_data(file_path)
		self.stock_daily_data_list = LoadData.get_daily_stock_data(self.stock_code_list) 


		self.high_point_index_list,self.high_point_list,self.low_point_index_list,self.low_point_list = HighLowPoint.get_high_low_points_list(self.stock_daily_data_list)
		self.realtime_price_list = LoadData.get_realtime_price(self.stock_code_list)
		
		self.reminder_info = []
		self.stock_price_reminder()

	def stock_price_reminder(self):
		
		for ii in range(len(self.stock_code_list)):

			if float(self.realtime_price_list[ii]) >=float(self.stock_sell_price_list[ii]):
				#sell
				reminder_info = str(self.stock_code_list[ii])+" should be sold, whose target sell price is "+str(self.stock_sell_price_list[ii])+", now price is "+str(self.realtime_price_list[ii])
				self.reminder_info.append(reminder_info)
			elif float(self.realtime_price_list[ii])<=float(self.stock_buy_price_list[ii]):
				
				reminder_info = str(self.stock_code_list[ii])+" should be bought, whose target buy price is "+str(self.stock_buy_price_list[ii])+ ", now price is "+str(self.realtime_price_list[ii])
				self.reminder_info.append(reminder_info)
	
	def get_high_low_points(self):

		bar_size = [5,30,60]
		column_num = [5,7,9]
		for ii in range(len(bar_size)):
			stock_intraday_data = LoadData.get_intraday_stock_data(self.stock_code_list,bar_size=bar_size[ii],delta_days = 365)
			high_point_index_list,high_point_list,low_point_index_list,low_point_list = HighLowPoint.get_high_low_points_list(stock_intraday_data)
			self.write_data_to_file(column_num[ii],high_point_list[-1],low_point_list[-1])

	def write_data_to_file(self,column_num,high_point,low_point):
		file_name = "input/user_data.xlsx"
		wb = load_workbook(file_name)
		sheet_names = wb.get_sheet_names()
		ws = wb.get_sheet_by_name(sheet_names[0])

		for ii in range(1,len(ws.rows)):
			ws.cell(row=ii+1,column = column_num).value = str(high_point)
			ws.cell(row=ii+1,column = column_num +1).value = str(low_point)

		wb.save(file_name)
		


if __name__ == '__main__':
	
	for ii in range(5):
		a = HighLowPointClass()
		
		if len(a.reminder_info)!=0:
			mail_content = ""
			for jj in range(len(a.reminder_info)):
				mail_content = mail_content + "\n" +a.reminder_info[jj]+"\n"
			print mail_content
			b = SendEmail.Send_Email("stock price remidner",mail_content)
			print b.isSend

		time.sleep(300)
	