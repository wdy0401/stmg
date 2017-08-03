# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 10:12:39 2017

@author: admin
"""
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  

import smtplib

from_addr="wdy0401@163.com"
to_addr="wdy0401@163.com"
password=input('Password')
smtp_server = 'smtp.163.com'


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
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()


msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
msg.attach(png('../fig/sum.png',"sum.png"))
msg.attach(png('../fig/part.png',"part.png"))

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())  