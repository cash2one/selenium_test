#encoding:utf-8
#! /usr/bin/env python
#coding=gbk
from selenium import webdriver
from PIL import Image
import pytesseract
from recognition.yundama import yundama
from   message.m51ym import m51ym
from   message.ema6 import ema6
from  mail.read import *
from selenium.webdriver.support.ui import WebDriverWait
import time
import re

def initMailDict():
    file='mail.txt'
    maildict=dict()
    fp=open(file,'r')
    for line in fp:
        line=line.strip('\n')

        tmplist=line.split('----')

        if len(tmplist) > 1:
            maildict[tmplist[0]]=tmplist[1]

    return maildict

def clickVerifyMail():
    loginmail()
    verifyurl = getbaidu_ssp_url()
    browser = webdriver.Firefox()
    driver = browser.get(verifyurl)


def sspLogin():
    print 'sspLogin 开始登录 ：'
    browser =webdriver.Firefox()

    driver=browser.get("http://ssp.baidu.com/home")
    #点击我是开发者
    print '点击我是开发者'
    browser.find_elements_by_class_name("login-entrence")[1].click()
    time.sleep(5)
    # 输入用户名
    browser.find_element_by_id("entered-login").send_keys("he8chenglong")
    # 输入密码
    browser.find_element_by_id("entered-password").send_keys("Hehenglong123")

    # 识别验证码
    authcode=verificode(browser,'captcha-image')
    browser.find_element_by_id("entered-imagecode").send_keys(authcode)

    # 开始登录
    browser.find_element_by_xpath('//*[@id="login"]/form/button').click()

def sspRegister(mailaddr,mailpwd):
    print 'sspRegister 开始注册 开始打开 Firefox浏览器 ：'
    browser =webdriver.Firefox()

    # 打开ssp 注册网页
    # driver=browser.get("http://ssp.baidu.com/static/register.html#/~productId=2")
    driver=browser.get("http://ssp.baidu.com/home")

    #点击我是开发者
    print '点击我是开发者'
    browser.find_elements_by_class_name("login-entrence")[1].click()
    time.sleep(5)
    # 点击 注册新用户
    image= browser.find_element_by_id("register-user").click()
    time.sleep(5)

    #等待页面加载
    print '等待页面加载'
    WebDriverWait(driver,50).until(lambda  drvier:browser.find_element_by_id("verify-image"))
    print '页面加载 完成 。。。'

    #  界面 填写
    # 识别验证码
    vcode=verificode(browser,'verify-image')
    # 验证码
    browser.find_element_by_id("image-verify-code").send_keys(vcode)

    # 用户名
    username=re.findall('(.*?)@',mailaddr,re.S)[0]+'abc'
    browser.find_element_by_id("username").send_keys(username)

    # 设置密码
    password='Aa1'+mailpwd
    browser.find_element_by_id("password").send_keys(password)

    #确认密码
    browser.find_element_by_id("confirm-password").send_keys(password)

    #电子邮件
    browser.find_element_by_id("email").send_keys(mailaddr)

    #  登陆验证码平台
    # mes=m51ym()
    mes=ema6()
    mes.login()
    # 获取 要注册 的手机号
    pnum=mes.getPhoneNumber()

    # 填写要注册的手机号  ，点击 获取验证码 按钮
    #手机号码
    browser.find_element_by_id("cellphone").send_keys(pnum)

    # 点击 获取短信验证码
    browser.find_element_by_id("fetch-verify-code").click()

    vcode=mes.getVerifyCode()

    #短信验证码
    browser.find_element_by_id("verify-code").send_keys(vcode)

    # 提交信息
    browser.find_element_by_id("submit").click()

    print u'等待 验证 email'
    time.sleep(10)
    print u'开始获取email中的验证链接 '
    loginmail(mailaddr,mailpwd, 'pop3.sohu.com')
    verifyurl = getbaidu_ssp_url()
    print u'点击验证链接'
    driver=browser.get(verifyurl)

def verificode(browser,imageid):
    # 保存 验证码 到本地
    image= browser.find_element_by_id(imageid)
    # 保存整个页面
    browser.get_screenshot_as_file('tu.jpg')
    # 通过坐标截图的方式 获取到验证码 图片
    im = Image.open('tu.jpg')
    box = (image.location['x'],image.location['y'],image.location['x']+image.size['width'],image.location['y']+image.size['height'])
    boxint =(int(box[0]),int(box[1]),int(box[2]),int(box[3]))
    img = im.crop(boxint)
    img.save("getimage.jpg")

    # 识别图片验证码
    #第一种方式 使用pytesseract
    vcode =pytesseract.image_to_string(img)
    print 'verficode is '+vcode

    # 第二种方式 ：调用 云打码接口 识别图片验证码
    dama=yundama()
    # 云打码接口 一键识别
    vcode=dama.decode()
    print 'yundama decode is '+vcode
    # 云打码接口 普通识别
    # vcode=dama.decodeNormal()
    # print 'yundama decodeNormal is '+vcode
    return vcode

if __name__ == '__main__':
    print '程序开始运行。。。'
    mdict=initMailDict()

    for mailaddr,mailpwd in mdict.items():
        print mailaddr,mailpwd
        sspRegister(mailaddr,mailpwd)
    # sspLogin()

