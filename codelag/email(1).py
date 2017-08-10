# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 13:48:59 2017

@author: ccc
"""

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  
import smtplib

from_addr="wdy0401@qq.com"
to_addr="wdy0401@163.com"
password='xxxxxxxxx'#这里填写qq邮箱的授权码
smtp_server='smtp.qq.com'


def png(fn,fns):
    with open(fn, 'rb') as f:
        mime = MIMEBase('image', 'png', filename=fns)
        mime.add_header('Content-Disposition', 'attachment', filename=fns)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        return mime

msg = MIMEMultipart()
msg['Subject'] = Header('Code from zrhx', 'utf-8').encode()
msg['From'] = from_addr
msg['To'] = to_addr
msg.attach(MIMEText('png file', 'plain', 'utf-8'))
msg.attach(png('../fig/sum.png',"sum.png"))
msg.attach(png('../fig/part.png',"part.png"))
server = smtplib.SMTP_SSL(smtp_server, 465)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())  

