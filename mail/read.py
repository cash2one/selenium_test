# -*- coding: utf-8 -*-

import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import re

global baidu_ssp_url

def getbaidu_ssp_url():
    global baidu_ssp_url
    return baidu_ssp_url

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg, indent=0):
    global baidu_ssp_url
    print 'call print_info----'
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
            url = re.findall('href="(.*?)">',content,re.S)
            print 'get url :'
            print url[0]
            baidu_ssp_url= url[0]
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

def loginmail():
    # email = raw_input('Email: ')
    # password = raw_input('Password: ')
    # pop3_server = raw_input('POP3 server: ')
    email = 'oblqelqyqm'
    password = 'zovqjw8t'
    pop3_server = 'pop3.sohu.com'
    server = poplib.POP3(pop3_server)
    #server.set_debuglevel(1)
    print(server.getwelcome())
    # 认证:
    server.user(email)
    server.pass_(password)
    print('Messages: %s. Size: %s' % server.stat())
    resp, mails, octets = server.list()
    # 获取最新一封邮件, 注意索引号从1开始:
    resp, lines, octets = server.retr(1)
    # 解析邮件:
    msg = Parser().parsestr('\r\n'.join(lines))
    # 打印邮件内容:
    print_info(msg)
    # 慎重:将直接从服务器删除邮件:
    # server.dele(len(mails))
    # 关闭连接:
    server.quit()

if __name__ == '__main__':
    loginmail()
    url = getbaidu_ssp_url()
    print url