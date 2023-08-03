# -*- coding: utf-8 -*-
"""
@Time ： 2022/9/25 12:47
@Auth ： YY
@File ：common.py
@IDE ：PyCharm
@state:
@Function：存放一些与主程序逻辑影响不大的程序
"""
import socket
import threading
from math import sin, cos, pi
import numpy as np
import pygame
from pygame import USEREVENT
def return_twolinecrosssate(p1,p2,p3,p4):
    x1,y1=p1
    x2,y2=p2
    x3,y3=p3
    x4,y4=p4
    if max(x1, x2) < min(x3, x4) or max(y1, y2) < min(y3, y4) or min(x1, x2) > max(x3, x4) or min(y1, y2) > max(y3, y4):
        return False
    # 使用跨立试验进行相交判断
    if ((x3 - x1) * (y3 - y4) - (y3 - y1) * (x3 - x4)) * (
            (x3 - x2) * (y3 - y4) - (y3 - y2) * (x3 - x4)) <= 0 and (
            (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) * (
            (x1 - x4) * (y1 - y2) - (y1 - y4) * (x1 - x2)) <= 0:
        return True
    else:
        return False
def angle_180topi(angle):
    return angle * pi / 180
def mycos(angle):
    return cos(angle_180topi(angle))
def mysin(angle):
    return sin(angle_180topi(angle))
def return_Rmatrix(angle):
    return np.array([[mycos(angle), -mysin(angle)], [mysin(angle), mycos(angle)]])
def return_Tmatrix(angle, l):
    return np.array(
        [[mycos(angle), -mysin(angle), l * mycos(angle)], [mysin(angle), mycos(angle), l * mysin(angle)], [0, 0, 1]])
class Wall(pygame.sprite.Sprite):
    def __init__(self, topleftlocation, size):
        # 调父类来初始化子类
        pygame.sprite.Sprite.__init__(self)
        # 加载图片
        self.image = pygame.Surface(size)
        self.image.fill((0, 0, 0))
        # 获取图片rect区域
        self.rect = self.image.get_rect()
        # 设置位置
        self.rect.topleft = topleftlocation
class Recivemsg():
    def __init__(self,port=6666):
        self.conn=None
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(("localhost", port))
        thread1 = threading.Thread(name='t1', target=self.recivemsg, args=())
        thread1.start()
    def recivemsg(self):
        while True:
            try:
                self.s.listen(10)
                self.conn, self.addr = self.s.accept()
                try:
                    while self.conn:
                        request = self.conn.recv(1024)
                        if request == b"":
                            self.conn.close()
                            self.conn=None
                        msg = eval(request.decode())
                        pygame.event.post(pygame.event.Event(USEREVENT, {"Joint": msg[0], "angle": msg[1]}))
                except:
                    self.conn.close()
            except:
                pass
    def closeconn(self):
        if self.conn:
            self.conn.close()