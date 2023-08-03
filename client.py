# -*- coding: utf-8 -*-
"""
@Time ： 2022/9/24 21:26
@Auth ： YY
@File ：client.py
@IDE ：PyCharm
@state:
@Function：用于向多关节机器人手动发送关节命令信息
"""
import socket
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi

step = 1


class RunThread(QThread):
    job = pyqtSignal(str)  # 定义更新进度条的信号

    def __init__(self):
        super().__init__()

    def run(self):
        for j in range(10):
            for i in range(0, 7):
                self.job.emit(f"[{i},{i+1}]")
                time.sleep(0.15)
        for j in range(10):
            for i in range(0, 7):
                self.job.emit(f"[{i},{-i-1}]")
                time.sleep(0.15)
        for j in range(10):
            for i in range(0, 7):
                self.job.emit(f"[{i},{-i}]")
                time.sleep(0.15)
        for j in range(10):
            for i in range(0, 7):
                self.job.emit(f"[{i},{i}]")
                time.sleep(0.15)


class MainWindow(QWidget):
    def __init__(self,port=6666,parent=None):
        super(MainWindow, self).__init__(parent)

        loadUi('clientgui.ui', self)
        self.port.setText(str(port))
        self.btn_conect.clicked.connect(self.f_btn_conect)
        self.pushButton.clicked.connect(lambda: self.sendmsg(f"[0,-{step}]"))
        self.pushButton_2.clicked.connect(lambda: self.sendmsg(f"[0,{step}]"))
        self.pushButton_3.clicked.connect(lambda: self.sendmsg(f"[1,-{step}]"))
        self.pushButton_4.clicked.connect(lambda: self.sendmsg(f"[1,{step}]"))
        self.pushButton_5.clicked.connect(lambda: self.sendmsg(f"[2,-{step}]"))
        self.pushButton_6.clicked.connect(lambda: self.sendmsg(f"[2,{step}]"))
        self.pushButton_7.clicked.connect(lambda: self.sendmsg(f"[3,-{step}]"))
        self.pushButton_8.clicked.connect(lambda: self.sendmsg(f"[3,{step}]"))
        self.pushButton_9.clicked.connect(lambda: self.sendmsg(f"[4,-{step}]"))
        self.pushButton_10.clicked.connect(lambda: self.sendmsg(f"[4,{step}]"))
        self.pushButton_11.clicked.connect(lambda: self.sendmsg(f"[5,-{step}]"))
        self.pushButton_12.clicked.connect(lambda: self.sendmsg(f"[5,{step}]"))
        self.pushButton_13.clicked.connect(lambda: self.sendmsg(f"[6,-{step}]"))
        self.pushButton_14.clicked.connect(lambda: self.sendmsg(f"[6,{step}]"))
        self.pushButton_15.clicked.connect(lambda: self.sendmsg(f"[7,-{step}]"))
        self.pushButton_16.clicked.connect(lambda: self.sendmsg(f"[7,{step}]"))
        self.btn_addanobstade.clicked.connect(lambda: self.sendmsg("['add','obstade'"))
        self.btn_removeallobstade.clicked.connect(lambda: self.sendmsg("['remove','obstade'"))
        self.btn_addareward.clicked.connect(lambda: self.sendmsg("['add','reward'"))
        self.btn_removeallreward.clicked.connect(lambda: self.sendmsg("['remove','reward'"))
        self.btn_randommove.clicked.connect(self.f_btn_randommove)
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def f_btn_randommove(self):
        self.thread = RunThread()
        self.thread.job.connect(self.sendmsg)  # 关联
        self.thread.start()

    def f_btn_conect(self):
        try:
            self.tcp_client.connect((self.ip.text(), int(self.port.text())))
            self.addlog(f'{time.strftime("%H:%M:%S", time.localtime())} #sever conect successful')
            self.btn_conect.setEnabled(False)
        except:
            self.addlog(f'{time.strftime("%H:%M:%S", time.localtime())} #sever conect failed')
            self.btn_conect.setEnabled(True)

    def sendmsg(self, msg):
        try:
            self.tcp_client.send(msg.encode())
            self.addlog(f'{time.strftime("%H:%M:%S", time.localtime())}-->msg:{msg}')
        except:
            self.addlog(f'{time.strftime("%H:%M:%S", time.localtime())}-->msg send faild')
            self.btn_conect.setEnabled(True)

    def addlog(self, logs):
        self.txt_log.append(logs)




