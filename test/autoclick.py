#-*-coding:utf8-*-
from pywinauto import application

import time
name = 'C:\\Users\\GAOPAN\\Desktop\\sfz\\IDCard.exe'
app=application.Application()
# app.start(name)
# app.connect(path=name)
# app.connect(process = 2341)
app.connect(handle=0x80E60)

#
dlg = app.Window_(title_re = u'身份证识别')

dlg.print_control_identifiers()
openpic=u'打开图片'
dlg[openpic].Click()


#
dlgopen =app.Window_(title_re = u'打开')
#dlgopen.print_control_identifiers()
filename=u'D:\\python\\2.jpg'
print filename
dlgopen.TypeKeys(filename)
openfile=u'打开(&O)'
dlgopen[openfile].Click()
# time.sleep(5)
# cancle=u'取消'
# dlgopen[cancle].Click()

recog=u'识别'
dlg[recog].Click()

print app.window_(handle=0x110C4E).WindowText()
