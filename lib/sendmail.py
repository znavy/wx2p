#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import email
import smtplib
import logging

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class SendMail:
    def __init__(self, smtp, port, username, passwd):
        self.smtp = smtp
        self.port = port
        self.username = username
        self.passwd = passwd


    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


    def _send(self, _from, to, subject, content):
        try:
            server = smtplib.SMTP_SSL(self.smtp, port = self.port)
            resp = server.login(self.username,self.passwd)
            
            logging.info(json.dumps(resp))
            
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['From'] = self._format_addr('WX2P <%s>' % _from)
            msg['To'] = to
            msg['Subject'] = Header('Alert from wx2p...', 'utf-8').encode()
            
            resp = server.sendmail(_from, [to], msg.as_string())
            server.quit()
            if len(resp) == 0:
                return True
            else:
                return False
        except Exception, e:
            logging.error(str(e))
            return False
