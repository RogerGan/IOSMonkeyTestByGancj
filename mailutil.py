# -*- coding:UTF-8 -*-

__author__ = 'roger'

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

import smtplib
import time
import os

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def sendemailto(toadd, filepaths, body):
    from_addr = 'ucwebautotest@163.com'
    password = 'ucwebautotest123'
    smtp_server = 'smtp.163.com'
    to_addr = toadd
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'monkey稳定性测试报告 <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    t = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
    msg['Subject'] = Header(u'测试结果:测试成功url个数:{0},测试失败url个数:{1},详情见内,测试时间:{2}'.format(body[0], body[1], t), 'utf-8').encode()
    msg.attach(MIMEText('详情见附件', 'plain', 'utf-8'))
    for filepath in filepaths:
        print filepath
        with open(filepath, 'rb') as f:
            mime = MIMEBase('image', 'png', filename=os.path.basename(filepath))
            mime.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()