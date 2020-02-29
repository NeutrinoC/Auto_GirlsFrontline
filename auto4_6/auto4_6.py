#
#=============================================#
#                                             #
#                 导入所需模块                 #
#                                             #
#=============================================#

import cv2
import time
import random
import datetime
import win32api
import win32gui
import win32con
import numpy as np
from PIL import ImageGrab
from skimage.measure import compare_ssim

#=============================================#
#                                             #
#                 定义所需常量                 #
#                                             #
#=============================================#


#=================截图比对区域=================#
IMAGE_PATH = 'initial_IMG/'#读取截图的路径        
MAP_IMAGE_BOX = [0.47,0.45,0.54,0.56]#地图判断区域         
COMBAT_IMAGE_BOX = [0.50,0.62,0.60,0.68]

#=================点击拖动区域=================#

#地图拖动区
MAP_DRAG_BOX = [0.70,0.40,0.71,0.41]

#队伍放置点
COMMAND_CLICK_BOX = [0.47,0.45,0.54,0.56]#指挥部
AIRPORT_CLICK_BOX = [0.55,0.34,0.61,0.41]#机场

#放置队伍
TEAM_SET_CLICK_BOX = [0.84,0.78,0.90,0.83]

#点击开始作战
START_COMBAT_CLICK_BOX = [0.82,0.78,0.95,0.85]

#前往各点
POINT_1_CLICK_BOX = [0.53,0.72,0.57,0.78]
POINT_2_CLICK_BOX = [0.36,0.58,0.43,0.67]
POINT_3_CLICK_BOX = [0.40,0.72,0.44,0.80]
POINT_4_CLICK_BOX = [0.15,0.60,0.20,0.65]

#确认事件
CONTINUE_CLICK_BOX = [0.45,0.45,0.55,0.55]

#重启作战
RESTART_STEP1_CLICK_BOX = [0.2,0.09,0.25,0.15]#点击终止作战
RESTART_STEP2_CLICK_BOX = [0.36,0.62,0.44,0.65]#点击重新作战

#撤退
PAUSE_CLICK_BOX = [0.49,0.08,0.51,0.12]
WITHDRAW_CLICK_BOX = [0.35,0.08,0.40,0.12]

 
#=============================================#
#                                             #
#                 基本功能函数                 #
#                                             #
#=============================================#

#启动界面，传统艺能
def preface():    
    for x in range(5,-1,-1):
        mystr =">>> "+str(x)+"s 后将开始操作，请切换至模拟器界面"
        print(mystr,end="")
        print("\b" * (len(mystr)*2),end = "",flush=True)
        time.sleep(1)
    print(">>> 开始操作,现在是",datetime.datetime.now(),"\n")


#等待若干时间,时间在min~max之间
def wait(minTime,maxTime):
    waitTime = minTime + (maxTime - minTime) * random.random()
    time.sleep(waitTime)


#获取模拟器窗口数据
def getWindowData():
    windowName = "少女前线 - MuMu模拟器"
    windowNameDesktop = "MuMu模拟器"
#    windowName = "Spyder (Python 3.7)"
    hwnd = win32gui.FindWindow(None,windowName)#根据窗口名称找到窗口句柄
    hwnd_desktop = win32gui.FindWindow(None,windowNameDesktop)
    if hwnd == 0 and hwnd_desktop == 0:
        print("未找到窗口界面,程序自动退出！")
        exit(0)
    elif hwnd != 0:
        left,top,right,bottom = win32gui.GetWindowRect(hwnd)#获取窗口的位置数据
    elif hwnd_desktop != 0:
        left,top,right,bottom = win32gui.GetWindowRect(hwnd_desktop)#获取窗口的位置数据
    width  = right - left
    height = bottom - top
    return [left,top,right,bottom,width,height]
        

#获取指定区域box的截图
def getImage(box):
    #windowData = [left,top,right,bottom,width,height]        
    windowData = getWindowData()
    imgLeft   = int(windowData[0] + windowData[4] * box[0])
    imgTop    = int(windowData[1] + windowData[5] * box[1])
    imgRight  = int(windowData[0] + windowData[4] * box[2])
    imgBottom = int(windowData[1] + windowData[5] * box[3])
    img = ImageGrab.grab((imgLeft,imgTop,imgRight,imgBottom))
    return img
    
    
#点击box内随机一点
def mouseClick(box,minTime,maxTime):
    #box = [left,top,right,bottom]
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    clickX = (int)(windowData[0] + windowData[4] * box[0] + windowData[4] * width  * random.random())
    clickY = (int)(windowData[1] + windowData[5] * box[1] + windowData[5] * height * random.random())
    clickPos = (clickX,clickY)
    win32api.SetCursorPos(clickPos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    wait(minTime,maxTime)


#模拟鼠标拖动，box为起始区域,times为拖动次数,distance为单次拖动距离，frame_interval为鼠标拖动帧
#间隔,multi_interval为多次拖动时的中间间隔
#direct   drag_towards
#  0          up
#  1         down
#  2         left
#  3         right
def mouseDrag(box,direct,times,distance,frame_interval,multi_interval):
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    dragX = (int)(windowData[0] + windowData[4] * box[0] + windowData[4] * width  * random.random())
    dragY = (int)(windowData[1] + windowData[5] * box[1] + windowData[5] * height * random.random())
    dragPos = (dragX, dragY)
    if direct == 0:
        dx, dy =  0,-1
    elif direct == 1:
        dx, dy =  0, 1
    elif direct == 2:
        dx, dy = -1, 0
    elif direct == 3:
        dx, dy =  1, 0
    else:
        dx, dy =  0, 0
    for i in range(times):
        win32api.SetCursorPos(dragPos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        for i in range(distance):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,dx,dy,0,0)
            time.sleep(frame_interval)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        time.sleep(multi_interval)


#比较两图片吻合度，结构相似性比较法
def imageCompare(img1,img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(gray_img1, gray_img2, full=True)
    return score > 0.97


#=============================================#
#                                             #
#                 高级功能函数                 #
#                                             #
#=============================================#
     
#判断是否进入了地图
def isMap():
    initImage = cv2.imread(IMAGE_PATH+"map.png")
    capImage  = getImage(MAP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
 
#判断是否遇敌
def isCombat():
    initImage = cv2.imread(IMAGE_PATH+"combat.png")
    capImage  = getImage(COMBAT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
    
#放置队伍
def setTeam():
    print("ACTION: 放置队伍")
    mouseClick(COMMAND_CLICK_BOX,0.8,1)
    mouseClick(TEAM_SET_CLICK_BOX,2.3,2.5)
    mouseDrag(MAP_DRAG_BOX,1,5,325,0.001,0.3)
    mouseClick(AIRPORT_CLICK_BOX,0.8,1)
    mouseClick(TEAM_SET_CLICK_BOX,1.8,2)

#开始作战
def startCombat():
    print("ACTION: 开始作战")
    mouseClick(START_COMBAT_CLICK_BOX,3.3,3.5)

#
def action_1():
    print("ACTION: 前往1号点")
    mouseClick(AIRPORT_CLICK_BOX,0.5,0.7)
    mouseClick(POINT_1_CLICK_BOX,1.7,2)

#
def action_2():
    print("ACTION: 前往2号点")
    mouseDrag(MAP_DRAG_BOX,0,2,250,0.001,0.6)
    mouseClick(POINT_2_CLICK_BOX,1.7,2)

#
def action_3():
    print("ACTION: 前往3号点")
    mouseDrag(MAP_DRAG_BOX,0,1,260,0.001,0.6)
    mouseClick(POINT_3_CLICK_BOX,1.7,2)

#
def action_4():
    print("ACTION: 前往4号点")
    mouseClick(POINT_4_CLICK_BOX,1.7,2)

#
def confirmReward():
    mouseClick(CONTINUE_CLICK_BOX,0.8,1)

def withdraw():
    print("ACTION: 撤退")
    confirmReward()
    time.sleep(3.5)
    mouseClick(PAUSE_CLICK_BOX,0.7,0.8)
    mouseClick(WITHDRAW_CLICK_BOX,6,6)
    for i in range(10):
       mouseClick(PAUSE_CLICK_BOX,0.7,0.8) 

#重启作战
def restartCombat():
    print("ACTION: 重启作战")
    mouseClick(RESTART_STEP1_CLICK_BOX,0.6,0.8)
    mouseClick(RESTART_STEP2_CLICK_BOX,4,5)



#=============================================#
#                                             #
#                 本程序主函数                 #
#                                             #
#=============================================#

if __name__ == "__main__": 
    preface()
    startTime = datetime.datetime.now()

    while True:
        if isMap():
            print("STATE：地图")
            setTeam()
            startCombat()
            #=================
            action_1()
            if isCombat():
                print("STATE：遇敌")
                withdraw()
                restartCombat()
                continue
            else:
                confirmReward()
            #=================
            action_2()
            #=================
            action_3()
            if isCombat():
                print("STATE：遇敌")
                withdraw()
                restartCombat()
                continue
            else:
                confirmReward()
            #=================
            action_4()
            if isCombat():
                print("STATE：遇敌")
                withdraw()
                restartCombat()
                continue
            else:
                confirmReward()
            restartCombat()

            currentTime = datetime.datetime.now()
            runtime = currentTime - startTime
            print('> 已运行：',runtime)                



                
            
            
