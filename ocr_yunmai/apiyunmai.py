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
import urllib2
import json

reload(sys)
sys.setdefaultencoding('utf-8')

# 跳过前面的文件夹
skipnum=213
# 图像文件所在目录
initfilesdir='D:\\python\\sfz'

# 存储所有结果的文件
allresultfile = 'D:\\python\\infoapi.txt'

'''
http://www.yunmaiocr.com/

协议 参考文档
[厦门云脉]二代证云识别接口【客户测试专用】.doc
[厦门云脉]银行卡云识别接口【客户测试专用】.doc

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

def getxml(action,image):
    l=[]
    # <action>idcard.scan</action>
    # 身份证识别
    # action='idcard.scan'

    # 银行卡识别
    # action = 'bankcard.scan'
    l.append('<action>'+action+'</action>')

    # <client>username</client>
    username='228cacc7-74ce-4b39-b008-fbd3a93f5da4'

    l.append('<client>'+username+'</client>')

    # <system>系统描述：包括硬件型号和操作系统型号等</system><!--不能为空-->
    system='PC'
    l.append('<system>'+system+'</system>')

    # <password>password</password><!--必须MD5加密-->
    pwd = 'WoZkPPOcnRGVgIJqpvHtbBrnEDVBrd'

    md5pwd = hashlib.md5()
    md5pwd.update(pwd)
    passmd5 = md5pwd.hexdigest()

    # print 'pass  md5 32bit :'
    # print passmd5

    l.append('<password>'+passmd5.upper()+'</password>')

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

    l.append('<verify>'+md5allstr.upper()+'</verify>')

    # <file>二进制文件，文件最大5M</file><!--要进行识别的文件-->
    # filename=u'D:\\python\\sfz\\(1)王燕斌\\4.jpg'
    # fb=open(filename,'rb')
    # imagebin=fb.read()
    l.append('<file>'+image+'</file>')

    # <ext>文件扩展名</ext><!--只能为下面的之一：jpg/jpeg/bmp/tif/tiff-->
    l.append('<ext>jpg</ext>')

    # <json>是否需要将结果转成json格式</json><!-- 当值为1时，返回的结果是json格式，如果不传该参数或为其它值，结果返回是xml格式 -->
    l.append('<json>1</json>')

    xmlstr=''.join(l)

    return  xmlstr

# print xmlstr

url='http://www.yunmaiocr.com/SrvXMLAPI'



# 使用 urllib2
# req = urllib2.Request(url=url,headers={'Content-Type':'text/xml'},data=xmlstr)
# response = urllib2.urlopen(req)
# res = response.read()
# print res


#查看当前目录
filelist=os.listdir(initfilesdir)
count=0
for pathname in filelist:
    print '-----------------------------------------------------------------次数： '+str(count)
    count=count+1
    if count<skipnum:
        continue

    # 定位 要操作的文件目录
    filedir ="D:\\python\\sfz\\"+pathname
    print 'filedir: '+filedir

    # 判断是否是 目录
    if os.path.isdir(filedir):
        #----------------------------------身份证信息识别-------------------------------
        # 身份证信息识别
        # 图像 文件名
        filename = filedir+"\\2.jpg"
        try:
            fb=open(filename,'rb')
            imagebin=fb.read()
        except:
            continue

        postxml=getxml('idcard.scan',imagebin)

        # 使用 Request
        result=requests.post(url,postxml)
        print result.text

        idjson =json.loads(result.text)

        try:
            status=idjson["status"]
        except:
            continue

        if status == "OK":
            print 'idjson status OK'
            #---------------------------------保存文件----------------------
            #  保存文件
            resultfile = filedir+'\\'+pathname+'.txt'
            print 'resultfile name is: '+resultfile
            fb=file(resultfile,'a')
            fb.write(result.text)
            fb.write('\n')
            fb.close()

            # 保存到 统一的文件中
            fball=file(allresultfile,'a')
            fball.write('------------------------')
            fball.write('\n')
            fball.write(result.text)
            fball.write('\n')
            fball.close()

        time.sleep(3)
        #----------------------------------银行卡信息识别-------------------------------
        # 银行卡信息识别
        # 图像 文件名
        filename = filedir+"\\4.jpg"
        try:
            fb=open(filename,'rb')
            imagebin=fb.read()
        except:
            continue

        postxml=getxml('bankcard.scan',imagebin)

        # 使用 Request
        bankresult=requests.post(url,postxml)
        print bankresult.text

        bankjson =json.loads(bankresult.text)

        try:
            status=idjson["status"]
        except:
            continue

        if status == "OK":
            print 'bankjson status OK'
            #---------------------------------保存文件----------------------
            #  保存文件
            resultfile = filedir+'\\'+pathname+'.txt'
            print 'resultfile name is: '+resultfile
            fb=file(resultfile,'a')
            fb.write(bankresult.text)
            fb.write('\n')
            fb.close()

            # 保存到 统一的文件中
            fball=file(allresultfile,'a')
            fball.write('\n')
            fball.write(bankresult.text)
            fball.write('\n')
            fball.close()

        time.sleep(3)