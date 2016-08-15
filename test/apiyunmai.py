#-*-coding:utf8-*-
from selenium import webdriver
import time
import os
import sys
import re
import shutil
import os.path
import hashlib
import requests
import md5

reload(sys)
sys.setdefaultencoding('utf-8')
'''
<action>idcard.scan</action>
<client>username</client>
<system>系统描述：包括硬件型号和操作系统型号等</system><!--不能为空-->
<password>password</password><!--必须MD5加密-->
<key>随机数UUID</key><!--不能为空，也永远不能重复，长度没有限制-->
<time>当前时间</time><!--long型13位数字，时间误差不能超过2天-->
<verify>MD5(action+client+key+time+password)</verify>
<file>二进制文件，文件最大5M</file><!--要进行识别的文件-->
<ext>文件扩展名</ext><!--只能为下面的之一：jpg/jpeg/bmp/tif/tiff-->
<header>是否输出头像图片</header><!—1:是；0：否；不填默认为否-->

上传包说明：
1）verify为32位大写的MD5值
2）<!-- -->内包含的是注释，所以上传包时，不要传注释
'''
l=[]
# <action>idcard.scan</action>
action='idcard.scan'
l.append('<action>'+action+'</action>')

# <client>username</client>
username='he1chenglong'
l.append('<client>'+username+'</client>')

# <system>系统描述：包括硬件型号和操作系统型号等</system><!--不能为空-->
system='PC'
l.append('<system>'+system+'</system>')

# <password>password</password><!--必须MD5加密-->
pwd = '1qazsw2'
md5pwd = hashlib.md5()
# md5pwd = md5.new()
md5pwd.update(pwd)
passmd5 = md5pwd.hexdigest()

l.append('<password>'+passmd5+'</password>')

# <key>随机数UUID</key><!--不能为空，也永远不能重复，长度没有限制-->
uuid =''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(4)))
l.append('<key>'+uuid+'</key>')

# <time>当前时间</time><!--long型13位数字，时间误差不能超过2天-->
current_milli_time = lambda: int(round(time.time() * 1000))
cur=current_milli_time()
curtime =str(cur)

l.append('<time>'+curtime+'</time>')

# <verify>MD5(action+client+key+time+password)</verify>
allstr=action+username+uuid+curtime+passmd5
md5all = hashlib.md5()
md5all.update(allstr)
md5allstr = md5all.hexdigest()

l.append('<verify>'+md5allstr.upper()+')</verify>')

# <file>二进制文件，文件最大5M</file><!--要进行识别的文件-->
filename=u'D:\\python\\sfz\\(1)王燕斌\\2.jpg'
l.append('<file>'+filename+'</file>')

# <ext>文件扩展名</ext><!--只能为下面的之一：jpg/jpeg/bmp/tif/tiff-->
l.append('<ext>jpg/ext>')

xmlstr=''.join(l)

print xmlstr

url='http://www.yunmaiocr.com/SrvXMLAPI'
result=requests.post(url,xmlstr)

print result.text