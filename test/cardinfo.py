#-*-coding:utf8-*-
from selenium import webdriver
import time
import os
import sys
import re
import shutil
import os.path

reload(sys)
sys.setdefaultencoding('utf-8')

# 图像文件所在目录
initfilesdir='D:\\python\\sfz'

# 存储所有结果的文件
allresultfile = 'D:\\python\\info.txt'

fball=file(allresultfile,'a')

browser = webdriver.Firefox()
driver = browser.get("http://ocr.ccyunmai.com/idcard/")

filelist=os.listdir(initfilesdir)

i=0
for pathname in filelist:
    print '-----------------------------------------------------------------'
    i=i+1
    # 定位 要操作的文件目录
    filedir ="D:\\python\\sfz\\"+pathname
    print 'filedir: '+filedir


    #-----------------------------------------------------------------
    # 身份证信息识别
    # 图像 文件名
    filename = filedir+"\\2.jpg"
    print 'filename: '+filename

    # 将 正面信息 拷贝一份
    picfile='D:\\python\\tmp\\'+str(i) +'.jpg'
    #os.system ("copy %s %s" % (filename, picfile))
    shutil.copy(filename,picfile)
    # 选择 身份证
    browser.find_element_by_xpath("//*[@id='uploadForm']/h3/input[1]").click()
    time.sleep(1)
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

    #-------------------------------------------------------
    #  银行卡 信息识别
    # 银行卡图像 文件名
    bankfilename = filedir+"\\4.jpg"
    print 'bankfilename: '+bankfilename

    # 将 正面信息 拷贝一份
    picfile='D:\\python\\tmp.jpg'
    os.system ("copy %s %s" % (bankfilename, picfile))
    # 选择 银行卡
    browser.find_element_by_xpath("//*[@id='uploadForm']/h3/input[6]").click()
    # 提交 图像
    browser.find_element_by_xpath("//*[@id='uploadForm']/p[2]/input").send_keys(picfile)

    time.sleep(2)

    #  开始识别
    browser.find_element_by_xpath("//*[@id='start']").click()

    # 读取识别结果
    bankresult=browser.find_element_by_xpath("html/body/div[1]/div/div[3]/div/div[1]/fieldset")

    print bankresult.text

    #-------------------------------------------------------
    #  保存文件
    resultfile = filedir+'\\'+pathname+'.txt'
    print 'resultfile name is: '+resultfile
    fb=file(resultfile,'a')
    fb.write(name)
    fb.write('\n')
    fb.write(cardno)
    fb.write('\n')
    fb.write(sex)
    fb.write('\n')
    fb.write(folk)
    fb.write('\n')
    fb.write(birthday)
    fb.write('\n')
    fb.write(address)
    fb.write('\n')
    fb.write(bankresult.text)
    fb.write('\n')
    fb.close()

    # 保存到 统一的文件中
    fball.write('--------------')
    fball.write(name)
    fball.write('\n')
    fball.write(cardno)
    fball.write('\n')
    fball.write(sex)
    fball.write('\n')
    fball.write(folk)
    fball.write('\n')
    fball.write(birthday)
    fball.write('\n')
    fball.write(address)
    fball.write('\n')
    fball.write(bankresult.text)
    fball.write('\n')
    fball.write('--------------')
    fball.write('\n')


fball.close()