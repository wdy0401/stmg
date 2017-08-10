# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 10:12:39 2017

@author: admin
"""
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib 

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  

mailto_list=["chensiqi100@163.com"] 
mail_host="smtp.163.com"  #设置服务器
mail_user=""    #用户名
mail_pass=""    #口令 
mail_postfix="163.com"  #发件箱的后缀

def png(fn,fns):
    with open(fn, 'rb') as f:
        mime = MIMEBase('image', 'png', filename=fns)
        mime.add_header('Content-Disposition', 'attachment', filename=fns)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        return mime
def send_mail(to_list,sub,content):  
    msg = MIMEMultipart()
    
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    msg['Subject'] = 'daily report'
    msg['From'] = 'me'  
    msg['To'] = ";".join(to_list) 
    
    msg.attach(png('../fig/part.png',"part.png"))
    
    server = smtplib.SMTP()  
    server.connect(mail_host)  
    server.login(mail_user,mail_pass)  
    server.sendmail(me, to_list, msg.as_string())  
    server.close()  

send_mail(mailto_list,"hello","hello world！")
