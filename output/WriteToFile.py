# -*- coding: utf-8 -*-
# File Name:  LoadData.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

def write_to_file(file_path,file_content):

	f = open(file_path,"w")
	f.write("date    	open 		   high    		 low  		    close 		     volume  	        amt")
	f.write("\n")
	line = ""
	for content in file_content:
		line = line + str(content) +"  "
	line = line+"\n"
	f.write(line)

	f.close

def write_list_to_file(file_path,file_content):
	f = open(file_path,"w")
	f.write("date    			open   		 high  		   low    		  close  		    volume       	  amt")
	f.write("\n")
	for ii in range(len(file_content)):
		line = ""
		for content in file_content[ii]:
			line = line + str(content) +"  "
		line = line +"\n"
		f.write(line)
	f.close()