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
import datetime
import output.SendEmail as SendEmail

class HighLowPointClass():
	"""docstring for HighLowPointClass"""
	def __init__(self):
		file_path = "input/user_data.xlsx"

		stock_code_list,stock_name_list,stock_buy_price_list,stock_sell_price_list = LoadUserData.load_user_data(file_path)
		stock_daily_data_list = LoadData.get_daily_stock_data(stock_code_list)

		self.buy_signal_flag = 0
		self.sell_signal_flag = 0

		self.run(stock_code_list,stock_buy_price_list,stock_sell_price_list)



	def run(stock_code_list,stock_buy_price_list,stock_sell_price_list):

		for ii in range(60):
			self.buy_signal_flag = 0
			self.sell_signal_flag = 0

			self.get_high_low_points(stock_code_list)
			self.stock_price_reminder(stock_code_list,stock_buy_price_list,stock_sell_price_list)
			print "the "+ str(ii) + " th is done."
			time.sleep(600)



	def stock_price_reminder(self,stock_code_list,stock_buy_price_list,stock_sell_price_list):
		
		realtime_price_list = LoadData.get_realtime_price(stock_code_list)
		reminder_info = []

		for ii in range(len(stock_code_list)):

			if float(realtime_price_list[ii]) >=float(stock_sell_price_list[ii]):
				#sell
				temp_reminder_info = str(stock_code_list[ii])+" should be sold, whose target sell price is "+str(stock_sell_price_list[ii])+", now price is "+str(realtime_price_list[ii])
				reminder_info.append(temp_reminder_info)
			elif float(realtime_price_list[ii])<=float(stock_buy_price_list[ii]):
				
				temp_reminder_info = str(stock_code_list[ii])+" should be bought, whose target buy price is "+str(stock_buy_price_list[ii])+ ", now price is "+str(realtime_price_list[ii])
				reminder_info.append(temp_reminder_info)

		if len(reminder_info)!= 0:
			mail_content = ""
			for jj in range(len(reminder_info)):
				mail_content = mail_content + "\n" + reminder_info[jj]+"\n"
			print mail_content 
			b = SendEmail.Send_Email("Stock price reminder from H&L Model",mail_content)


	def get_high_low_points(self,stock_code_list):
		msg = ""
		bar_size = [5,30,60]
		column_num = [5,7,9]
		for ii in range(len(bar_size)):
			stock_intraday_data = LoadData.get_intraday_stock_data(stock_code_list,bar_size=bar_size[ii],delta_days = 365)
			high_point_index_list,high_point_list,low_point_index_list,low_point_list = HighLowPoint.get_high_low_points_list(stock_intraday_data)
			msg = msg + str(bar_size[ii]) + " min level:\n" 
			for jj in range(len(stock_code_list)):

				self.write_data_to_file(column_num[ii],high_point_list[jj][-1],low_point_list[jj][-1])

				msg = msg + str(stock_code_list[jj])+ self.judge_trend_inverse(high_point_list[jj],low_point_list[jj])

				msg = msg + "\n\n"
		a = SendEmail.Send_Email("Trend inverse reminder from H&L Model",msg)


	
	def judge_trend_inverse(self,high_point_list,low_point_list):

		msg = ""
		if len(high_point_list)>=3 and self.buy_signal_flag == 0:
			if high_point_list[-1]>= high_point_list[-2] and high_point_list[-2]<=high_point_list[-3]:
				self.buy_signal_flag =1
				msg = msg + "\nA new high point has break through the previous high point. Falling trend ends.\n"
		else:
			if high_point_list[-1]<= high_point_list[-2] or high_point_list[-2]>=high_point_list[-3]:
				self.buy_signal_flag =0

		if len(low_point_list>=3) and self.sell_signal_flag ==0:
			if low_point_list[-1]<=low_point_list[-2] and low_point_list[-2] >= low_point_list[-3]:
				self.sell_signal_flag = 1
				msg = msg + "\nA new low point has break through the previous low point. Up trend ends.\n"
		else:
			if low_point_list[-1]>=low_point_list[-2] or low_point_list[-2] <= low_point_list[-3]:
				self.sell_signal_flag = 0

		return msg 

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
	
	a = HighLowPointClass()