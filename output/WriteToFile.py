# -*- coding: utf-8 -*-
# File Name:  LoadData.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################

def write_to_file(file_path,file_content):

	f = open(file_path,"w")
	line = ""
	for content in file_content:
		line = line + content +"  "
	line = line+"\n"
	f.write(line)

	f.close

def write_list_to_file(file_path,file_content):
	f = open(file_path,"w")

	for ii in range(len(file_content)):
		line = ""
		for content in file_content[ii]:
			line = line + content +"  "
		line = line +"\n"
		f.write(line)
	f.close()