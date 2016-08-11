#encoding:utf-8
#! /usr/bin/env python
#coding=gbk
from selenium import webdriver

browser =webdriver.Firefox()

browser.get("http://www.baidu.com")

# 点击登录
browser.find_element_by_xpath(".//*[@id='u1']/a[7]").click()

# 登录框
div=browser.find_element_by_class_name("pass-login-pop-content")
#输入用户名
div.find_element_by_name("userName").send_keys("he1chenglong")
#输出密码
div.find_element_by_name("password").send_keys("1qazxsw2")

# 点击登录
browser.find_element_by_xpath(".//*[@id='TANGRAM__PSP_8__submit']").click()
