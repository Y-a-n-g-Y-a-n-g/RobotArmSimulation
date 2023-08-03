import random
import sys
from math import sqrt, atan, tan
import pygame.gfxdraw
import torch
from PyQt5.QtWidgets import QApplication

from matplotlib.path import Path
from common import *
from client import MainWindow

torch.set_printoptions(
    precision=2,  
    threshold=1000,
    edgeitems=3,
    linewidth=200,
    profile=None,
    sci_mode=False
)
portrandom = random.randint(10000, 50000)


def client():
    app = QApplication(sys.argv)
    w = MainWindow(port=portrandom)
    w.show()
    sys.exit(app.exec())


thread1 = threading.Thread(name='t1', target=client, args=())
thread1.start()
# 一些变量
color_RED = (255, 0, 0)
color_GREEN = (0, 255, 0)
color_BULE = (0, 0, 255)
color_Purple = (255, 0, 255)
color_Cyan = (0, 255, 255)
color_Yellow = (255, 255, 0)
color_Black = (0, 0, 0)
colors = [color_RED, color_GREEN, color_BULE]
# 关闭numpy的科学计数
np.set_printoptions(suppress=True)
# 机械臂关节连杆信息
angle = [-90, 40, -80, 80, -80, 80, -80, 80]
P = [(0, 0, 1), (60, 0, 1), (60, 0, 1), (60, 0, 1), (60, 0, 1), (60, 0, 1), (60, 0, 1), (60, 0, 1)]
Joints = []
# 墙壁

walls = []
all_Walls = pygame.sprite.Group()
# 初始化pygame
pygame.init()
# 定义变量
size = width, height = 900, 900
# 创建一个主窗口
screen = pygame.display.set_mode(size)
# 标题
pygame.display.set_caption("Robotic Arm Reinforcement Learning (RL) Control 2D-Test Environment V2022-10-6")
titleIcon = pygame.image.load('robot.png')
pygame.display.set_icon(titleIcon)
# PYGAME刷新率
clock = pygame.time.Clock()


def showconectsata():
    if recivemsg.conn:
        font = pygame.font.Font("C:/Windows/Fonts/STXINWEI.TTF", 20)
        text = font.render("Connected", True, (255, 0, 0), (255, 255, 0))
        screen.blit(text, (30, 25))
    else:
        font = pygame.font.Font("C:/Windows/Fonts/STXINWEI.TTF", 20)
        text = font.render("Disconnected", True, (255, 0, 0), (255, 255, 0))
        screen.blit(text, (20, 25))


polygon = []
reward = []
obstade = []
point = []


def checkdist(point):
    Mp = torch.Tensor(point)
    M1 = torch.unsqueeze(Mp, dim=1)
    M2 = torch.unsqueeze(Mp, dim=0)
    M4 = torch.sum((M1 - M2) ** 2, dim=-1) ** 0.5

    dist1 = M4[0, :]
    dist2 = M4[:, -1]

    return int(sum(dist1 < 120)) + int(sum(dist2 < 120)) - 2


for i in range(0, 6):
    p = (random.randint(550, 870), random.randint(150, 800))
    point.append(p)
    while checkdist(point) > 0:
        point.pop(-1)
        p = (random.randint(550, 870), random.randint(150, 800))
        point.append(p)
    reward.append(p)

    p = (random.randint(550, 870), random.randint(150, 800))
    point.append(p)
    while checkdist(point) > 0:
        point.pop(-1)
        p = (random.randint(550, 870), random.randint(150, 800))
        point.append(p)
    obstade.append(p)

    p = (random.randint(50, 350), random.randint(150, 800))
    point.append(p)
    while checkdist(point) > 0:
        point.pop(-1)
        p = (random.randint(50, 350), random.randint(150, 800))
        point.append(p)
    reward.append(p)

    p = (random.randint(50, 350), random.randint(150, 800))
    point.append(p)
    while checkdist(point) > 0:
        point.pop(-1)
        p = (random.randint(50, 350), random.randint(150, 800))
        point.append(p)
    obstade.append(p)
print(checkdist(point))


def return_P_xy(Pnum):
    A = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    for i in range(Pnum):
        A = np.dot(A, return_Tmatrix(angle[i], 100))
    return ((np.dot(A, np.array(P[0]))).tolist()[0] + 450, (np.dot(A, np.array(P[0]))).tolist()[1] + 800)


def return_TwoBisectorPoints(point1, point2, point3, lenth=10):
    # 两个端点的中心点
    x4 = (point1[0] + point3[0]) / 2
    y4 = (point1[1] + point3[1]) / 2
    # 如果中心点与中间点纵坐标一样
    if abs(y4 - point2[1]) < 0.001:
        y1 = y2 = point2[1]
        x1 = point2[0] - lenth
        x2 = point2[0] + lenth
    # 如果中心点与中间点横坐标一样
    elif abs(x4 - point2[0]) < 0.001:
        x1 = x2 = point2[0]
        y1 = point2[1] - lenth
        y2 = point2[1] + lenth
    # 如果第一连杆第二连杆斜率一样
    elif (point2[1] - point1[1]) * (point3[0] - point2[0]) == (point3[1] - point2[1]) * (point2[0] - point1[0]):
        kse = (point3[1] - point1[1]) / (point3[0] - point1[0])
        k3 = -1 / kse
        x1 = point2[0] - sqrt(lenth ** 2.0 / (k3 ** 2 + 1))
        y1 = k3 * (x1 - point2[0]) + point2[1]
        x2 = point2[0] + sqrt(lenth ** 2.0 / (k3 ** 2 + 1))
        y2 = k3 * (x2 - point2[0]) + point2[1]
    # 正常情况
    else:
        k3 = (point2[1] - y4) / (point2[0] - x4)
        x1 = point2[0] - sqrt(lenth ** 2.0 / (k3 ** 2 + 1))
        x2 = point2[0] + sqrt(lenth ** 2.0 / (k3 ** 2 + 1))
        y1 = k3 * (x1 - point2[0]) + point2[1]
        y2 = k3 * (x2 - point2[0]) + point2[1]

    pygame.draw.line(screen, color_GREEN, (x1, y1), (x2, y2), 1)
    return (x1, y1), (x2, y2)


def return_TwoendPoints(points, pointe, lenth=10):
    if points[0] == pointe[0]:
        x1 = pointe[0] - lenth
        x2 = pointe[0] + lenth
        y1 = y2 = pointe[1]
    else:
        kse = (pointe[1] - points[1]) / (pointe[0] - points[0])
        if kse != 0:
            k3 = -1 / kse
            x1 = pointe[0] - sqrt(lenth ** 2.0 / (k3 ** 2 + 1))
            y1 = k3 * (x1 - pointe[0]) + pointe[1]
            x2 = pointe[0] + sqrt(lenth ** 2.0 / (k3 ** 2 + 1))
            y2 = k3 * (x2 - pointe[0]) + pointe[1]
        else:
            x1 = x2 = pointe[0]
            y1 = pointe[1] - lenth
            y2 = pointe[1] + lenth
    pygame.draw.line(screen, color_GREEN, (x1, y1), (x2, y2), 1)
    return (x1, y1), (x2, y2)


def show_allLinks():
    for i in range(0, len(angle)):
        pygame.draw.line(screen, color_RED, return_P_xy(i), return_P_xy(i + 1), 5)


def create_allwall():
    # 左墙壁
    wall = Wall((0, 0), (20, 900))
    all_Walls.add(wall)
    walls.append(wall)
    # 右墙壁
    wall = Wall((880, 0), (50, 900))
    all_Walls.add(wall)
    walls.append(wall)
    # 上墙壁
    wall = Wall((20, 0), (880, 80))
    all_Walls.add(wall)
    walls.append(wall)

    # 下墙壁
    wall = Wall((20, 850), (880, 50))
    all_Walls.add(wall)
    walls.append(wall)
    # 机械臂工作台
    wall = Wall((350, 800), (200, 50))
    all_Walls.add(wall)
    walls.append(wall)


def showall_Walls():
    for wall in walls:
        screen.blit(wall.image, wall.rect)
    info = pygame.image.load("img.png").convert_alpha()
    screen.blit(info, (150, 10))


def show_alljoint():
    Joints = []
    for i in range(0, len(angle)):
        Joints.append(return_P_xy(i))
        pygame.draw.circle(screen, color_Purple, return_P_xy(i), 8, width=0)
    pygame.draw.circle(screen, color_Yellow, return_P_xy(len(angle)), 8, width=0)

    safeareapoint1 = []
    safeareapoint2 = []
    p1, p2 = return_TwoendPoints(return_P_xy(1), return_P_xy(0), 30)
    safeareapoint1.append(p2)
    safeareapoint2.append(p1)
    for i in range(0, len(angle) - 1):
        p1, p2 = return_TwoBisectorPoints(return_P_xy(i), return_P_xy(i + 1), return_P_xy(i + 2), 30)
        x1, x2, x3, x4 = p1, p2, safeareapoint1[-1], safeareapoint2[-1]
        a = (x2[0] - x1[0], x2[1] - x1[1])
        b = (x3[0] - x2[0], x3[1] - x2[1])
        c = (x4[0] - x3[0], x4[1] - x3[1])
        d = (x1[0] - x4[0], x1[1] - x4[1])
        if (np.cross(a, b) > 0 and np.cross(b, c) > 0 and np.cross(c, d) > 0) or (
                np.cross(a, b) < 0 and np.cross(b, c) < 0 and np.cross(c, d) < 0):
            safeareapoint1.append(p2)
            safeareapoint2.append(p1)
        else:
            safeareapoint1.append(p1)
            safeareapoint2.append(p2)

    p1, p2 = return_TwoendPoints(return_P_xy(len(angle) - 1), return_P_xy(len(angle)), 30)
    x1, x2, x3, x4 = p1, p2, safeareapoint1[-1], safeareapoint2[-1]
    a = (x2[0] - x1[0], x2[1] - x1[1])
    b = (x3[0] - x2[0], x3[1] - x2[1])
    c = (x4[0] - x3[0], x4[1] - x3[1])
    d = (x1[0] - x4[0], x1[1] - x4[1])
    if (np.cross(a, b) > 0 and np.cross(b, c) > 0 and np.cross(c, d) > 0) or (
            np.cross(a, b) < 0 and np.cross(b, c) < 0 and np.cross(c, d) < 0):
        safeareapoint1.append(p2)
        safeareapoint2.append(p1)
    else:
        safeareapoint1.append(p1)
        safeareapoint2.append(p2)

    global polygon
    polygon = []
    polygon = safeareapoint1.copy()
    polygon = polygon + safeareapoint2[::-1]

    for i in range(len(polygon) - 1):
        pygame.draw.line(screen, color_BULE, polygon[i], polygon[i + 1], 1)
    pygame.draw.line(screen, color_BULE, polygon[0], polygon[len(polygon) - 1], 1)


def show_allrewards():
    for i in reward:
        pygame.draw.circle(screen, color_Cyan, i, 8, width=0)


def show_allobstade():
    for i in obstade:
        pygame.draw.circle(screen, color_Black, i, 8, width=0)


create_allwall()
recivemsg = Recivemsg(port=portrandom)
done = False
pointflag = 0
linecrossflag = True
while not done:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            recivemsg.closeconn()
            done = True
        if event.type == USEREVENT:
            try:
                angle[event.Joint] += event.angle
            except:
                pass

    # 填充背景
    screen.fill((200, 200, 200))

    if pointflag > 0:
        screen.fill((249, 131, 131))
    if linecrossflag == False:
        screen.fill((249, 50, 50))

    # 更新显示界面
    showall_Walls()
    show_allLinks()
    show_alljoint()
    show_allrewards()
    show_allobstade()
    showconectsata()

    font = pygame.font.Font("C:/Windows/Fonts/STXINWEI.TTF", 20)
    text = font.render("Normal", True, (255, 0, 0), (0, 255, 0))
    screen.blit(text, (760, 25))
    if pointflag > 0:
        font = pygame.font.Font("C:/Windows/Fonts/STXINWEI.TTF", 20)
        text = font.render("Hit an obstacle", True, (255, 0, 0), (0, 255, 0))
        screen.blit(text, (760, 25))
    if linecrossflag == False:
        font = pygame.font.Font("C:/Windows/Fonts/STXINWEI.TTF", 20)
        text = font.render("Self-collision", True, (255, 0, 0), (0, 255, 0))
        screen.blit(text, (760, 25))

    # print(polygon)
    # print(point)
    # print(polygon)
    ppath = Path(polygon)

    pointflag = sum(ppath.contains_points(point))
    del ppath

    linecrossflag = True
    for idx in range(len(polygon) - 4):
        for i in range(idx + 2, len(polygon) - 1):
            linecrossflag = linecrossflag * (
                not return_twolinecrosssate(polygon[idx], polygon[idx + 1], polygon[i], polygon[i + 1]))

    pygame.display.flip()

pygame.quit()
