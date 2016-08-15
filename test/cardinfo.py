#-*-coding:utf8-*-
from selenium import webdriver
import time
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

initfilesdir='D:\\python\\sfz'

browser = webdriver.Firefox()
driver = browser.get("http://ocr.ccyunmai.com/idcard/")
# 选择 身份证
browser.find_element_by_xpath("//*[@id='uploadForm']/h3/input[1]").click()
time.sleep(2)

# 选择 银行卡
#browser.find_element_by_xpath("//*[@id='uploadForm']/h3/input[6]").click()

# 无用的
# browser.find_element_by_xpath("//*[@id='uploadForm']/p[2]/input").send_keys(u"D:\\python\\sfz\\2.jpg")
# time.sleep(2)

filelist=os.listdir(initfilesdir)

for pathname in filelist:
    #pathname.decode('utf-8')
    filedir ="D:\\python\\sfz\\"+pathname
    # 图像 文件名
    filename = filedir+"\\2.jpg"
   # filename.encode('utf-8')
    print 'filename: '+filename

    picfile='D:\\python\\tmp.jpg'
    os.system ("copy %s %s" % (filename, picfile))
    # browser = webdriver.Firefox()

    # 提交 图像
    browser.find_element_by_xpath("//*[@id='uploadForm']/p[2]/input").send_keys(picfile)

    time.sleep(2)

    #  开始识别
    browser.find_element_by_xpath("//*[@id='start']").click()

    # 读取识别结果
    result=browser.find_element_by_xpath("html/body/div[1]/div/div[3]/div/div[1]/fieldset")

    print result.text
    # 解析识别结果
    name=re.findall('<name>(.*?)</name>',result.text,re.S)[0]
    cardno=re.findall('<cardno>(.*?)</cardno>',result.text,re.S)[0]
    sex=re.findall('<sex>(.*?)</sex>',result.text,re.S)[0]
    folk=re.findall('<folk>(.*?)</folk>',result.text,re.S)[0]
    birthday=re.findall('<birthday>(.*?)</birthday>',result.text,re.S)[0]
    address=re.findall('<address>(.*?)</address>',result.text,re.S)[0]

    #  保存文件
    resultfile = filedir+pathname+'.txt'
    print resultfile
    fb=file(resultfile,'w')
    fb.write(name)
    fb.write(cardno)
    fb.write(sex)
    fb.write(folk)
    fb.write(birthday)
    fb.write(address)
    fb.write(result.text)
    fb.close()