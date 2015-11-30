# -*- coding: utf-8 -*-
# File Name: AbsoluteMomentumClass.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

import strategy.AbsoluteMomentum as AbsoluteMomentum
import data.LoadUserData as LoadUserData
import data.LoadData as LoadData
import output.SendEmail as SendEmail

class AbsoluteMomentumClass():
	"""docstring for AbsoluteMomentumClass"""
	def __init__(self):
		file_path = "input/user_data.xlsx"
		self.user_stock_code_list,self.user_stock_name_list,user_stock_buy_point_list,user_stock_sell_point_list = LoadUserData.load_user_data(file_path)

		self.daily_stock_data_all = LoadData.get_daily_stock_data(self.user_stock_code_list,"20150101")
		#存放收盘价
		self.daily_stock_data = []

		for ii in range(len(self.daily_stock_data_all)):
			temp = []
			for jj in range(len(self.daily_stock_data_all[ii])):
				temp.append(self.daily_stock_data_all[ii][jj][4])
			self.daily_stock_data.append(temp)
		#print self.daily_stock_data[0][-1],self.daily_stock_data[1][-1]
		self.reminder_info= []
		self.run()



	def run(self):
		
		action_index_list,action_type_list = AbsoluteMomentum.AbsoluteMomentum(self.daily_stock_data)

		for ii in range(len(self.daily_stock_data)):
			#print len(self.daily_stock_data[ii]),float(action_index_list[ii][-1]),len(action_index_list[ii])
			if len(self.daily_stock_data[ii])-1 == float(action_index_list[ii][-1]) :
				if action_type_list[ii][-1] =="l":
					msg = str(self.user_stock_code_list[ii])+" should buy."
					self.reminder_info.append(msg)
				else:
					msg = str(self.user_stock_code_list[ii])+" should sell/short."
					self.reminder_info.append(msg)

		print self.reminder_info

		msg = ""
		for item in self.reminder_info:
			msg = msg +item +"\n"

		b = SendEmail.Send_Email("Absolute Momentum Reminder",msg)



if __name__ == '__main__':
	a = AbsoluteMomentumClass()
		