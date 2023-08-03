# -*- coding: utf-8 -*-
"""
@Time ： 10/6/2022 10:45 PM
@Auth ： YY
@File ：StartGame.py
@IDE ：PyCharm
@state:
@Function：Game model parameter setting and startup
"""
import os
import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUi


class StartGameWindow(QWidget):
    def __init__(self,parent=None):
        super(StartGameWindow, self).__init__(parent)
        loadUi('StartGame.ui', self)
    def f_btn_startgame(self):
        os.system('python main.py')
app = QApplication(sys.argv)
startwindow = StartGameWindow()
startwindow.show()
sys.exit(app.exec())