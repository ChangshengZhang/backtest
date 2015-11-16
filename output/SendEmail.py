# -*- coding: utf-8 -*-
# File Name: SendEmail.py
# Author: Changsheng Zhang
# mail: zhangcsxx@gmail.com
# Created Time: Tue Jul  7 10:09:08 2015

#########################################################################
import os
import smtplib  
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Send_Email():
	"""docstring for Send_Email"""
	def __init__(self,mail_sub,mail_content):
		self.mail_content = mail_content
		self.mailto_list=["changsheng.zhang@nedugroup.com","zhangcsxx@163.com"] 
		self.mail_host="smtp.nedugroup.com"  #设置服务器
		self.mail_user="changsheng.zhang@nedugroup.com"	#用户名
		self.mail_pass="Leed1234"   #口令 
		self.mail_postfix="nedugroup.com"  #发件箱的后缀
		self.isSend = self.send_text_mail(self.mailto_list,mail_sub,mail_content)


	def send_text_mail(self,to_list,sub,content):  
		me="Changsheng Zhang"+"<"+self.mail_user+"@"+self.mail_postfix+">"  
		msg = MIMEText(content,_subtype='html',_charset='utf-8')  
		msg['Subject'] = sub
		msg['From'] = me 
		msg['To'] = ";".join(to_list)  
		try: 
			server = smtplib.SMTP()  
			server.connect(self.mail_host)  
			server.login(self.mail_user,self.mail_pass)  
			server.sendmail(me, to_list, msg.as_string())  
			server.close()  
			return True
		except Exception, e:
			print str(e)
			return False

if __name__ == '__main__':  
	
	a = Send_Email("system test","send mail module test.")
	print a.isSend