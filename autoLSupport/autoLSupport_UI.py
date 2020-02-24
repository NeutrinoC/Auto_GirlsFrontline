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
from tkinter import *


IMAGE_PATH = 'initial_IMG/'#读取截图的路径
L_SUPPORT_IMAGE_BOX = [0.02,0.30,0.18,0.37]#后勤完成界面判断区域
DESKTOP_IMAGE_BOX = [0.10,0.20,0.22,0.40]#模拟器桌面判断区域                    
L_SUPPORT_STEP1_CLICK_BOX = [0.50,0.50,0.60,0.60]#确认后勤完成
L_SUPPORT_STEP2_CLICK_BOX = [0.53,0.62,0.62,0.67]#再次派出
START_GAME_STEP1_CLICK_BOX = [0.14,0.23,0.18,0.28]#点击图标启动
START_GAME_STEP2_CLICK_BOX = [0.50,0.70,0.50,0.70]#点击一次
START_GAME_STEP3_CLICK_BOX = [0.50,0.75,0.50,0.75]#点击开始

SWITCH = True

def wait(minTime,maxTime):
    waitTime = minTime + (maxTime - minTime) * random.random()
    time.sleep(waitTime)


def getWindowData():
    windowName = "少女前线 - MuMu模拟器"
    windowNameDesktop = "MuMu模拟器"
    hwnd = win32gui.FindWindow(None,windowName)#根据窗口名称找到窗口句柄
    hwnd_desktop = win32gui.FindWindow(None,windowNameDesktop)
    if hwnd == 0 and hwnd_desktop == 0:
        exit(0)
    elif hwnd != 0:
        left,top,right,bottom = win32gui.GetWindowRect(hwnd)#获取窗口的位置数据
    elif hwnd_desktop != 0:
        left,top,right,bottom = win32gui.GetWindowRect(hwnd_desktop)#获取窗口的位置数据
    width  = right - left
    height = bottom - top
    return [left,top,right,bottom,width,height]
        
def getImage(box):  
    windowData = getWindowData()
    imgLeft   = int(windowData[0] + windowData[4] * box[0])
    imgTop    = int(windowData[1] + windowData[5] * box[1])
    imgRight  = int(windowData[0] + windowData[4] * box[2])
    imgBottom = int(windowData[1] + windowData[5] * box[3])
    img = ImageGrab.grab((imgLeft,imgTop,imgRight,imgBottom))
    return img
    
def mouseClick(box,minTime,maxTime):
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

def imageCompare(img1,img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(gray_img1, gray_img2, full=True)
    return score > 0.95

def showWindow():
    windowName = "少女前线 - MuMu模拟器"
    windowNameDesktop = "MuMu模拟器"
    hwnd = win32gui.FindWindow(None,windowName)#根据窗口名称找到窗口句柄
    hwnd_desktop = win32gui.FindWindow(None,windowNameDesktop)
    if hwnd == 0 and hwnd_desktop == 0:
        exit(0)
    elif hwnd != 0:
        win32gui.ShowWindow(hwnd,win32con.SW_SHOW)
    elif hwnd_desktop != 0:
        win32gui.ShowWindow(hwnd_desktop,win32con.SW_SHOW)
    time.sleep(3)

def hideWindow():
    windowName = "少女前线 - MuMu模拟器"
    windowNameDesktop = "MuMu模拟器"
    hwnd = win32gui.FindWindow(None,windowName)#根据窗口名称找到窗口句柄
    hwnd_desktop = win32gui.FindWindow(None,windowNameDesktop)
    if hwnd == 0 and hwnd_desktop == 0:
        exit(0)
    elif hwnd != 0:
        win32gui.ShowWindow(hwnd,win32con.SW_HIDE)
    elif hwnd_desktop != 0:
        win32gui.ShowWindow(hwnd_desktop,win32con.SW_HIDE)
    time.sleep(3)

def isLSupport():
    initImage = cv2.imread(IMAGE_PATH+"L_support.png")
    capImage  = getImage(L_SUPPORT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

def isDesktop():
    initImage = cv2.imread(IMAGE_PATH+"desktop.png")
    capImage  = getImage(DESKTOP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

def takeLSupport():
    mouseClick(L_SUPPORT_STEP1_CLICK_BOX,2,3)
    mouseClick(L_SUPPORT_STEP2_CLICK_BOX,4,5)

def startGame():
    mouseClick(START_GAME_STEP1_CLICK_BOX,30,30)
    mouseClick(START_GAME_STEP2_CLICK_BOX,30,30)
    mouseClick(START_GAME_STEP3_CLICK_BOX,30,30)

class autoLS_UI:
    def __init__(self):
        self.initWindow()
        self.initButton()
        self.initLabel()
        self.root.mainloop()
            
    def initWindow(self):
        self.root = Tk()
        self.root.title("UI")
        self.root.geometry("160x100+10+10")
    
    def initButton(self):
        self.endButton = Button(self.root,text = "关闭自动后勤",command = self.endLS())
        self.endButton.grid(padx = 40, pady = 2)
        
    def endLS(self):
        SWITCH = False
        
    def initLabel(self):
        self.textVar = StringVar()
        self.textVar.set('0')
        self.label1 = Label(self.root,text = "收派委托数：")
        self.label1.grid(padx = 0,pady = 4)
        self.label2 = Label(self.root,textvariable = self.textVar)
        self.label2.grid(padx = 40,pady = 4)
    

if __name__ == '__main__': 
    UI = autoLS_UI()
    L_SupportCount = 0
    while SWITCH:
        showWindow()
        if isLSupport():
            takeLSupport()
            L_SupportCount += 1
            UI.textVar.set(str(L_SupportCount))
            continue
        elif isDesktop():
            startGame()
            continue
        hideWindow()
        for i in range(600):
            if SWITCH:
                wait(0.5,1)
            else:
                showWindow() 
        

