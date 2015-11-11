# -*- coding: utf-8 -*-
# File Name: pricevolume.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

import strategy.PriceVolume as PriceVolume
import data.LoadData as LoadData
import output.PlotChart as PlotChart
import matplotlib.pyplot as plt

class PriceVolumeClass():
	"""docstring for PriceVolumeClass"""
	def __init__(self):
		bench_mark_list = ["000016.SH","000300.SH","399006.SZ"]
		self.bench_mark_name_list = [u"上证50",u"沪深300",u"创业板指"]
		stock_data_list = LoadData.get_daily_stock_data(bench_mark_list,"20110101")
		self.price_index = 4
		self.volume_index = 5 

		self.trade_cost = 1-0.001
		self.range_day = [2,5,7,10]
		self.regression_day = [2,5,7,10]
		self.offset = offset = self.range_day + self.regression_day -2
		short_flag = 1
		
		self.price_list = []
		self.volume_list = []

		for ii in range(len(bench_mark_list)):
			self.price_list.append(zip(*stock_data_list[ii])[self.price_index])
			self.volume_list.append(zip(*stock_data_list[ii])[self.volume_index])



		self.slope_price_list = PriceVolume.PriceVolume(self.price_list,self.range_day,self.regression_day)
		self.slope_volume_list = PriceVolume.PriceVolume(self.volume_list,self.range_day,self.regression_day)

		action_index_list,action_type_list,revenue_list = self.run_strategy(short_flag)
		self.plot(revenue_list,self.price_list,bench_mark_list,action_index_list,action_type_list,short_flag)

		print "done\n"
		

	def plot(self,revenue_list,price_list,bench_mark_list,action_index_list,action_type_list,short_flag=1):
		color =["b","y","c","k"]

		for ii in range(len(revenue_list)):
			plt.figure(ii)
			temp_long_action_index = []
			temp_short_action_index = []
			for jj in range(len(action_index_list[ii])):
				if action_type_list[ii][jj] == "b":
					temp_long_action_index.append([action_index_list[ii][jj],price_list[ii][action_index_list[ii][jj]+self.offset]/price_list[ii][self.offset]])
				else:
					temp_short_action_index.append([action_index_list[ii][jj],price_list[ii][action_index_list[ii][jj]+self.offset]/price_list[ii][self.offset]])
			volume_index = []
			volume_num = []
			max_volumn = 2.0*max(self.volume_list[ii])
			for kk in range(len(self.volume_list[ii])-self.offset):
				volume_index.append(kk)
				volume_num.append(self.volume_list[ii][kk+self.offset]/max_volumn)
			
			plt.plot(revenue_list[ii],color = color[ii%len(color)],linewidth = 2.5,label = self.bench_mark_name_list[ii]+u"的策略收益")
			plt.plot(self.norm_list(price_list[ii][self.offset:]),color = color[ii%len(color)],label =self.bench_mark_name_list[ii]+u"的走势")
			plt.scatter(list(zip(*temp_long_action_index)[0]),list(zip(*temp_long_action_index)[1]),c="r",s=30,marker="s")
			plt.scatter(list(zip(*temp_short_action_index)[0]),list(zip(*temp_short_action_index)[1]),c="g",s=30,marker="v")
			plt.bar(volume_index,volume_num)
			temp_a = max(revenue_list[ii])
			temp_b = max(self.norm_list(price_list[ii][self.offset:]))


			plt.legend(loc="upper left")
			plt.xlim(0,len(revenue_list[0])+30)
			plt.ylim(0,max(temp_a,temp_b)+0.3)
			if short_flag ==1:
				plt.title("long/short")
			else:
				plt.title("long/hold")
			plt.xlabel("Time /day")
			plt.ylabel("Stock Revenue")
			plt.grid(True)
		plt.show()

	def norm_list(self,list_a):
		new_list =[]
		for ii in range(len(list_a)):
			new_list.append(list_a[ii]/list_a[0])
		return new_list
	#short_flag =1表示能short
	def run_strategy(self,short_flag=1):
		action_index_list = []
		action_type_list =[] 
		revenue_list = []
		offset = self.range_day + self.regression_day -2

		for ii in range(len(self.slope_price_list)):
			pos_flag = 0
			temp_action_index_list = []
			temp_action_type_list = []
			temp_revenue_list = []
			
			for jj in range(len(self.slope_price_list[ii])):
				if self.slope_price_list[ii][jj] ==1 and self.slope_volume_list[ii][jj]== 1:
					if pos_flag ==0:
						if len(temp_action_index_list)==0:
							temp_revenue_list.append(1.0*self.trade_cost)
						else:
							temp_revenue_list.append(temp_revenue_list[-1]*self.trade_cost)

						
						temp_action_type_list.append("b")
						temp_action_index_list.append(jj)
						pos_flag =1
					else:
						temp_revenue_list.append(temp_revenue_list[-1]*float(self.price_list[ii][jj+offset])/float(self.price_list[ii][jj+offset-1]))

				else:
					if pos_flag ==1:
						temp_revenue_list.append(temp_revenue_list[-1]*float(self.price_list[ii][jj+offset])/float(self.price_list[ii][jj+offset-1])*self.trade_cost)

						temp_action_index_list.append(jj)
						temp_action_type_list.append("s")
						pos_flag = 0
					else:
						if len(temp_action_index_list)==0:
							temp_revenue_list.append(1.0)
						else:
							if short_flag ==0:
								temp_revenue_list.append(temp_revenue_list[-1])
							else:
								temp_revenue_list.append(temp_revenue_list[-1]*(2-float(self.price_list[ii][jj+offset]/float(self.price_list[ii][jj+offset-1])))*self.trade_cost)
			revenue_list.append(temp_revenue_list)
			action_index_list.append(temp_action_index_list)
			action_type_list.append(temp_action_type_list)
		return action_index_list,action_type_list,revenue_list


if __name__ == '__main__':
	a = PriceVolumeClass()




