#encoding:utf-8
#! /usr/bin/env python
#coding=gbk
import sys
import os
from ctypes import *

class yundama(object):
    def __init__(self):
        # 下载接口放目录 http://www.yundama.com/apidoc/YDM_SDK.html
        # 错误代码请查询 http://www.yundama.com/apidoc/YDM_ErrorCode.html
        # 所有函数请查询 http://www.yundama.com/apidoc

        print(u'>>>正在初始化...')

        self.YDMApi = windll.LoadLibrary('yundamaAPI')

        # 1. http://www.yundama.com/index/reg/developer 注册开发者账号
        # 2. http://www.yundama.com/developer/myapp 添加新软件
        # 3. 使用添加的软件ID和密钥进行开发，享受丰厚分成

        self.appId = 2600   # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
        self.appKey = 'e23b38d4e094d366fda38c15033a1b29'     # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！

        print(u'软件ＩＤ：%d\r\n软件密钥：%s' % (self.appId, self.appKey))

        # 注意这里是普通会员账号，不是开发者账号，注册地址 http://www.yundama.com/index/reg/user
        # 开发者可以联系客服领取免费调试题分

        # username = raw_input('用户账号：')
        # password = raw_input('用户密码：')
        #从配置文件中读出项目的配置信息
        d=dict()
        # 打开配置文件
        file='setting.txt'
        fp = open(file, 'r')
        for line in fp:
            #print 'read: '+line
            l=line.split(':')
            #print l[0]
            if len(l) > 1:
                d[l[0]]=l[1]

        self.username = d['damaUsername']
        self.password = d['damaPassword']

    def decode(self):
        ####################### 一键识别函数 YDM_EasyDecodeByPath #######################
        print(u'\r\n>>>正在一键识别...')

        # 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
        codetype = 1004

        # 分配30个字节存放识别结果
        result = c_char_p("                              ")

        # 识别超时时间 单位：秒
        timeout = 60

        # 验证码文件路径
        filename = 'getimage.jpg'

        # 一键识别函数，无需调用 YDM_SetAppInfo 和 YDM_Login，适合脚本调用
        captchaId = self.YDMApi.YDM_EasyDecodeByPath(self.username, self.password, self.appId, self.appKey, filename, codetype, timeout, result)

        print(u"一键识别：验证码ID：%d，识别结果：%s" % (captchaId, result))

        size = -1
        code = string_at(result, size)
        print(code.decode('utf-8'))

        print u'识别结果：'+code

        return code

    def decodeNormal(self):
        ########################## 普通识别函数 YDM_DecodeByPath #########################

        print(u'\r\n>>>正在登陆...')

        # 第一步：初始化云打码，只需调用一次即可
        self.YDMApi.YDM_SetAppInfo(self.appId, self.appKey)

        # 第二步：登陆云打码账号，只需调用一次即可
        uid = self.YDMApi.YDM_Login(self.username, self.password)

        if uid > 0:

            print(u'>>>正在获取余额...')

            # 查询账号余额，按需要调用
            balance = self.YDMApi.YDM_GetBalance(self.username, self.password)

            print(u'登陆成功，用户名：%s，剩余题分：%d' % (self.username, balance))

            print(u'\r\n>>>正在普通识别...')

            # 第三步：开始识别

            # 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
            codetype = 1004

            # 分配30个字节存放识别结果
            result = c_char_p("                              ")

            # 验证码文件路径
            filename = 'getimage.jpg'

            # 普通识别函数，需先调用 YDM_SetAppInfo 和 YDM_Login 初始化
            captchaId = self.YDMApi.YDM_DecodeByPath(filename, codetype, result)

            print(u"普通识别：验证码ID：%d，识别结果：%s" % (captchaId, result))

            size = -1
            code = string_at(result, size)
            print(code.decode('utf-8'))

            print u'识别结果：'+code

            return code

        else:
            print(u'登陆失败，错误代码：%d' % uid)

            return  'fail --'

        ################################################################################

        # print(u'\r\n>>>错误代码请查询 http://www.yundama.com/apidoc/YDM_ErrorCode.html')

        # raw_input('\r\n测试完成，按回车键结束...')

