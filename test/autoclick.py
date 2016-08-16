#-*-coding:utf8-*-
from pywinauto import application
import time
import os
import sys
import re
import shutil
import os.path

# 要先打开软件 ，读取这两个句柄
# 整个窗口的句柄
apphandle=0xA0E60
# 要读取的文本框的句柄
texthandle=0x1F1060

# name = 'C:\\Users\\GAOPAN\\Desktop\\sfz\\IDCard.exe'
app=application.Application()

# 首先打开 身份证识别软件
app.connect(handle=apphandle)

# 获取 窗口 句柄
dlg = app.Window_(title_re = u'身份证识别')

# 图像文件所在目录
initfilesdir='D:\\python\\sfz'
#查看当前目录
filelist=os.listdir(initfilesdir)
count=0
for pathname in filelist:
    print '-----------------------------------------------------------------次数： '+str(count)
    count=count+1
    if count<10:
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
        print 'filename: '+filename

        # 将 正面信息 拷贝一份
        picfile='D:\\python\\tmp.jpg'
        try:
            shutil.copy(filename,picfile)
        except:
            continue

        # 开始 操作  软件
        # 点击打开图片 按钮
        openpic=u'打开图片'
        dlg[openpic].Click()
        time.sleep(2)

        # 获取弹出的对话框
        dlgopen =app.Window_(title_re = u'打开')
        # 输入图片路径
        dlgopen.TypeKeys(picfile)
        # 点击打开
        openfile=u'打开(&O)'
        dlgopen[openfile].Click()
        time.sleep(2)

        # 点击识别按钮
        recog=u'识别'
        dlg[recog].Click()
        time.sleep(2)

        # 读取结果
        idtext=app.window_(handle=texthandle).WindowText()
        print idtext

        if idtext:
            #---------------------------------保存文件----------------------
            #  保存文件
            resultfile = filedir+'\\'+pathname+'.txt'
            print 'resultfile name is: '+resultfile
            fb=file(resultfile,'a')
            fb.write(idtext.encode('UTF-8'))
            fb.close()
