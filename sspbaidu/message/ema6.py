#-*-coding:utf8-*-
import requests
import time
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

file='setting.txt'

class ema6(object):
    def __init__(self):
        print u'messagebase __init__ ...'
        #从配置文件中读出项目的配置信息
        d=dict()
        # 打开配置文件

        fp = open(file, 'r')
        for line in fp:
            #print 'read: '+line
            l=line.split(':')
            #print l[0]
            if len(l) > 1:
                d[l[0]]=l[1]

        #打印 项目配置信息
        print 'ema6projectName:  '+ d['ema6projectName']
        print 'ema6projectId:  '+d['ema6projectId']
        print 'ema6username: '+ d['ema6username']
        print 'ema6password: ' + d['ema6password']
        #保存项目配置信息
        self.__pid = d['ema6projectId']
        self.__username = d['ema6username']
        self.__password = d['ema6password']
        self.__parameter= 'K5uq9pNtFkNqZL%2breS3Xsw%3d%3d'

        self.__username='he1chenglong'
        self.__password='1qazsw2'
        self.__pid='9329'

    def login(self):
        '''
        登录 获取保存 token
        :return:
        '''
        # http://api.ema6.com:20161/Api/userLogin?uName=用户名&pWord=密码&Developer=开发者参数
        cmd='http://api.ema6.com:20161/Api/userLogin?uName=%s&pWord=%s&Developer=%s'%(self.__username,self.__password,self.__parameter)
        # print cmd
        s=requests.get(cmd)
        print 'login  gettoken:'
        print s.text
        l=s.text.split("&")
        self.__token= l[0]

    def getPhoneNumber(self):
        '''
        获取 可以使用的手机号
        :return:  手机号
        '''
        # http://api.ema6.com:20161/Api/userGetPhone?ItemId=项目ID&token=登陆token&PhoneType=0
        cmd='http://api.ema6.com:20161/Api/userGetPhone?ItemId=%s&token=%s&PhoneType=0'%(self.__pid,self.__token)
        # print cmd
        pn=requests.get(cmd)
        print 'getPhoneNumber:'
        print pn.text
        li=pn.text.split(";")
        self.__pnum = li[0]
        return li[0]

    def readPhoneNum(self):
        return self.__pnum

    def releasePhoneNumber(self):
        '''
        释放手机号
        :return:
        '''
        #  http://api.ema6.com:20161/Api/userReleasePhone?token=登陆token&phoneList=phone-itemId;phone-itemId;
        cmd='http://api.ema6.com:20161/Api/userReleasePhone?token=%s&phoneList=%s;%s'%(self.__token,self.__pid,self.__pnum)
        #print cmd
        ret=requests.get(cmd)
        print 'releasePhoneNumber '+ ret.text

    def phoneBlacklist(self):
        '''
        把手机号 加入 黑名单
        :return:
        '''
        # http://api.ema6.com:20161/Api/userAddBlack?token=登陆token&phoneList=itemId-phone,phone,phone;itemId-phone,phone;
        cmd='http://api.ema6.com:20161/Api/userAddBlack?token=%s&phoneList=%s,%s'%(self.__token,self.__pid,self.__pnum)
        ret=requests.get(cmd)
        print 'phoneBlacklist '+ret.text

    def getVerifyCode(self):
        '''
        获取验证码
        :return:  验证码
        '''
        # http://api.ema6.com:20161/Api/userSingleGetMessage?token=登陆token&itemId=获取的项目ID&phone=获取的号码
        for i in range(0,50):
            cmd='http://api.ema6.com:20161/Api/userSingleGetMessage?token=%s&itemId=%s&phone=%s'%(self.__token,self.__pid,self.__pnum)
            vc=requests.get(cmd)
            print vc.text
            if vc.text[0:3] == 'MSG&':
                print 'try to find the number:'
                numlist=re.findall('(\d+)',vc.text,re.S)
                print 'getVerifyCode:'+numlist[0]
                return numlist[0]
            else:
                time.sleep(5)

        return '0000'


if __name__ =='__main__':
    file='..\\setting.txt'
    m=ema6()
    m.login()
    m.getPhoneNumber()
    m.getVerifyCode()
    m.releasePhoneNumber()
    m.phoneBlacklist()