# -*- coding: utf-8 -*-
# File Name:  LoadData.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

from WindPy import *
from datetime import *
import os
import sys

def get_suspend_stock_name():
	if w.isconnected() == False:
		w.start()

	susp_stock_name = []

	res = w.wset("TradeSuspend",startdate=datetime.today(),enddate=datetime.today(),field="wind_code")
	if res.ErrorCode != 0:
		print(str(stock_name)+' wset Error \nError['+str(res.ErrorCode)+'][load stockcode list fail]\n')
		sys.exit()
		
	for ii in range(len(res.Data[0])):
		susp_stock_name.append(res.Data[0][ii])

	return susp_stock_name

#get all stock name which exclude suspended stock
def get_all_stock_name():

	if w.isconnected() == False:
		w.start()

	susp_stock_name = get_suspend_stock_name()
	stock_name = []
	# get all stock name
	res = w.wset("SectorConstituent",u"date=;sector=全部A股")
	if res.ErrorCode != 0:
		print(str(stock_name)+' wset Error \n Error['+str(res.ErrorCode)+'][load stockcode list fail]\n')
		sys.exit()

	for ii in range(len(res.Data[1])):
		if res.Data[1][ii] in susp_stock_name:
			continue
		else:
			stock_name.append(res.Data[1][ii])

	return stock_name


def get_daily_stock_data(stock_name_list,begin_date = "20000101"):
	if w.isconnected() == False:
		w.start()
	#3-dim: stock_name, time,indicator(time,open,high,low,close,volume,amt)
	daily_stock_data= []

	for stock_name in stock_name_list:
		
		temp_data_per_stock = []
		res = w.wsd(stock_name,"open,high,low,close,volume,amt", begin_date, "","PriceAdj=F",showblank=0)
		if res.ErrorCode != 0:
			print(str(stock_name)+' wsd Error \n Error['+str(res.ErrorCode)+'][load stockcode list fail]\n')
			sys.exit()

		for ii in range(len(res.Data[0])):
			temp_data_per_day = []
			if float(res.Data[0][ii])==0.0 or float(res.Data[1][ii])==0.0 or float(res.Data[2][ii])==0.0 or float(res.Data[3][ii])==0.0:
				continue
			temp_date = str(res.Times[ii])[0:10]
			temp_date_1 = temp_date.split("-")
			date_temp = ""
			for item in temp_date_1:
				date_temp = date_temp + item
			temp_data_per_day.append(date_temp)
			for jj in range(len(res.Fields)):
				temp_data_per_day.append(float(res.Data[jj][ii]))

			temp_data_per_stock.append(temp_data_per_day)
		daily_stock_data.append(temp_data_per_stock)

	return daily_stock_data
	
#3-dim: stock_name, time,indicator(time,open,high,low,close,volume,amt)
def get_intraday_stock_data(stock_name_list,bar_size = 60,delta_days = 365*3):
	if w.isconnected() == False:
		w.start()

	intraday_stock_data = []
	for stock_name in stock_name_list:
		temp_data_per_stock = []
		res = w.wsi(stock_name,"open,high,low,close,volume,amt",datetime.today()-timedelta(days=delta_days),datetime.today(),BarSize=bar_size,showblank=0)
		if res.ErrorCode != 0:
			print(str(stock_name)+' wsi Error \n Error['+str(res.ErrorCode)+'][load stockcode list fail]\n')
			sys.exit()

		for ii in range(len(res.Data[0])):
			temp_data_per_day = []
			if float(res.Data[0][ii])==0.0 or float(res.Data[1][ii])==0.0 or float(res.Data[2][ii])==0.0 or float(res.Data[3][ii])==0.0:
				continue
			temp_date = str(res.Times[ii])[0:19]
			temp_date_1 = temp_date.split("-")
			temp_date = ""
			for item in temp_date_1:
				temp_date = temp_date + item 
			temp_data_per_day.append(temp_date)
			for jj in range(len(res.Fields)):
				temp_data_per_day.append(float(res.Data[jj][ii]))

			temp_data_per_stock.append(temp_data_per_day)
		intraday_stock_data.append(temp_data_per_stock)

	return intraday_stock_data

#获取实时价格
def get_realtime_price(stock_name_list):
	realtime_price_list = []
	if w.isconnected() == False:
		w.start()

	for stock_name in stock_name_list:
		res = w.wsq(stock_name,"rt_last")
		#res=w.wst(stock_name,"open", datetime.today()-timedelta(minutes=1), datetime.now())
		if res.ErrorCode != 0:
			print(str(stock_name)+' wst Error \n Error['+str(res.ErrorCode)+'][load stockcode list fail]\n')
			print "wst"
			sys.exit()

		realtime_price_list.append(float(res.Data[0][-1]))

	return realtime_price_list

#得到实时的量价
def get_realtime_price_and_volume(stock_name_list):
	realtime_price_list = []
	realtime_volume_list = []
	if w.isconnected() == False:
		w.start()

	delta_minutes = 1
	lambda_volume = 1+(240.0/((float(datetime.today().hour) - 13)*60+float(datetime.today().minute)+120)-1)*1.05
	if float(datetime.today().hour) >=15:
		delta_minutes = (float(datetime.today().hour)-15+1)*60
		lambda_volume = 1

	for stock_name in stock_name_list:

		res_0 = w.wsq(stock_name,"rt_last")
		res=w.wst(stock_name,"open,volume", datetime.today()-timedelta(minutes=delta_minutes), datetime.now())
		
		if res.ErrorCode != 0:
			print(str(stock_name)+' wst Error \n Error['+str(res.ErrorCode)+'][load stockcode list fail]\n')
			print "wst"
			sys.exit()

		realtime_price_list.append(float(res_0.Data[0][-1]))
		realtime_volume_list.append(float(res.Data[1][-1])*lambda_volume)

	return realtime_price_list,realtime_volume_list

