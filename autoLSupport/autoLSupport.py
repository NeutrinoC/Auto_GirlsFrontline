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
from skimage.metrics import structural_similarity

#=============================================#
#                                             #
#                 定义所需常量                 #
#                                             #
#=============================================#


#=================截图比对区域=================#
IMAGE_PATH = 'initial_IMG/'#读取截图的路径
MAIN_MENU_IMAGE_BOX = [0.62,0.52,0.76,0.60]#主界面判断区域                      
L_SUPPORT_IMAGE_BOX = [0.02,0.30,0.18,0.37]#后勤完成界面判断区域         
DESKTOP_IMAGE_BOX = [0.10,0.20,0.22,0.40]#模拟器桌面判断区域         

#=================点击拖动区域=================#
#收后勤支援
L_SUPPORT_STEP1_CLICK_BOX = [0.50,0.50,0.60,0.60]#确认后勤完成
L_SUPPORT_STEP2_CLICK_BOX = [0.53,0.62,0.62,0.67]#再次派出

#启动游戏
START_GAME_STEP1_CLICK_BOX = [0.14,0.23,0.18,0.28]#点击图标启动
START_GAME_STEP2_CLICK_BOX = [0.50,0.70,0.50,0.70]#点击开始
START_GAME_STEP3_CLICK_BOX = [0.50,0.75,0.50,0.75]#点击登录
 
#关闭游戏
CLOSE_GAME_CLICK_BOX = [0.52,0.03,0.53,0.04]
#=============================================#
#                                             #
#                 基本功能函数                 #
#                                             #
#=============================================#

#启动界面，传统艺能
def preface():    
    print(">>>这是一个自动收派后勤的程序，每5~6分钟检测一次\n")
    for x in range(5,-1,-1):
        mystr =">>> 将在"+str(x)+"s 后启动"
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


#比较两图片吻合度，结构相似性比较法
def imageCompare(img1,img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
    return score > 0.95


#显示窗口
def showWindow():
    windowName = "少女前线 - MuMu模拟器"
    windowNameDesktop = "MuMu模拟器"
    hwnd = win32gui.FindWindow(None,windowName)#根据窗口名称找到窗口句柄
    hwnd_desktop = win32gui.FindWindow(None,windowNameDesktop)
    if hwnd == 0 and hwnd_desktop == 0:
        print("未找到窗口界面,程序自动退出！")
        exit(0)
    elif hwnd != 0:
        win32gui.ShowWindow(hwnd,win32con.SW_SHOW)
    elif hwnd_desktop != 0:
        win32gui.ShowWindow(hwnd_desktop,win32con.SW_SHOW)
    time.sleep(3)


#隐藏窗口
def hideWindow():
    windowName = "少女前线 - MuMu模拟器"
    windowNameDesktop = "MuMu模拟器"
    hwnd = win32gui.FindWindow(None,windowName)#根据窗口名称找到窗口句柄
    hwnd_desktop = win32gui.FindWindow(None,windowNameDesktop)
    if hwnd == 0 and hwnd_desktop == 0:
        print("未找到窗口界面,程序自动退出！")
        exit(0)
    elif hwnd != 0:
        win32gui.ShowWindow(hwnd,win32con.SW_HIDE)
    elif hwnd_desktop != 0:
        win32gui.ShowWindow(hwnd_desktop,win32con.SW_HIDE)
    time.sleep(3)

#=============================================#
#                                             #
#                 高级功能函数                 #
#                                             #
#=============================================#

#判断是否是委托完成界面
def isMainMenu():
    initImage = cv2.imread(IMAGE_PATH+"main_menu.png")
    capImage  = getImage(MAIN_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
    
#判断是否是委托完成界面
def isLSupport():
    initImage = cv2.imread(IMAGE_PATH+"L_support.png")
    capImage  = getImage(L_SUPPORT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是模拟器桌面
def isDesktop():
    initImage = cv2.imread(IMAGE_PATH+"desktop.png")
    capImage  = getImage(DESKTOP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#收后勤支援
def takeLSupport():
    mouseClick(L_SUPPORT_STEP1_CLICK_BOX,2,3)
    mouseClick(L_SUPPORT_STEP2_CLICK_BOX,6,8)

#启动游戏
def startGame():
    mouseClick(START_GAME_STEP1_CLICK_BOX,30,30)
    mouseClick(START_GAME_STEP2_CLICK_BOX,30,30)
    mouseClick(START_GAME_STEP3_CLICK_BOX,30,30)

#关闭游戏
def closeGame():
    mouseClick(CLOSE_GAME_CLICK_BOX,5,5)

#=============================================#
#                                             #
#                 本程序主函数                 #
#                                             #
#=============================================#

if __name__ == "__main__": 
    preface()
    L_SupportCount = 0
    failCount = 0
    while True:
        showWindow()
        if isMainMenu():
            print(">>> ",datetime.datetime.now()," 主菜单")
            failCount = 0
        elif isLSupport():
            print(">>> ",datetime.datetime.now()," 委托完成")
            failCount = 0
            takeLSupport()
            L_SupportCount += 1
            print(">>> ",datetime.datetime.now()," 收派后勤数：",L_SupportCount)
            continue
        elif isDesktop():
            print(">>> ",datetime.datetime.now()," 模拟器桌面")
            failCount = 0
            startGame()
            continue
        else:#有的时候卡了或者是怎么样了，直接关了重启
            print(">>> ",datetime.datetime.now()," 当前状态未知")
            failCount += 1
            if failCount == 3:
                closeGame()
            else:
                time.sleep(10)
            continue
        hideWindow()#隐藏窗口，这样你就可以同时做其他事了
        wait(300,360)
                
            
            
