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
MAIN_MENU_IMAGE_BOX = [0.62,0.52,0.76,0.60]#主界面判断区域                        》
L_SUPPORT_IMAGE_BOX = [0.02,0.30,0.18,0.37]#后勤完成界面判断区域                 》
CHAPTER_MENU_IMAGE_BOX = [0.60,0.25,0.70,0.35]#章节菜单界面判断区域         》
EPISODE_MENU_IMAGE_BOX = [0.01,0.30,0.10,0.40]#小节菜单界面判断区域          》        
MAP_IMAGE_BOX = [0.47,0.45,0.54,0.54]#干涉仪II地图判断区域                             》     
PLAN_FINISH_IMAGE_BOX = [0.80,0.78,0.98,0.87]#计划完成判断区域                     》   
GOTO_POWERUP_IMAGE_BOX = [0.54,0.60,0.68,0.68]#提醒强化判断区域               》
NAVIGATE_IMAGE_BOX = [0.18,0.10,0.22,0.17]#导航条判断区域                             》
DESKTOP_IMAGE_BOX = [0.10,0.20,0.22,0.40]#模拟器桌面判断区域                        》 

#=================点击拖动区域=================#

#从主菜单点击活动
ACTIVITY_CLICK_BOX = [0.80,0.65,0.90,0.73]

#在章节选择界面选择第2章
CHAPTER_2_CLICK_BOX = [0.70,0.25,0.85,0.30]

#开始干涉仪II
EPISODE_CLICK_BOX = [0.72,0.71,0.80,0.73]#选择第2节
ENTER_COMBAT_CLICK_BOX = [0.88,0.54,0.94,0.60]#进入作战

#地图拖动区
MAP_DRAG_BOX = [0.70,0.60,0.70,0.60]

#队伍放置点
AIRPORT_1_CLICK_BOX = [0.25,0.30,0.30,0.38]#左机场
AIRPORT_2_CLICK_BOX = [0.88,0.62,0.94,0.70]#右机场

#放置队伍
TEAM_SET_CLICK_BOX = [0.84,0.78,0.90,0.83]

#点击开始作战
START_COMBAT_CLICK_BOX = [0.82,0.78,0.95,0.85]

#补给
#---------------------------------------------#选中打捞队
SUPPLY_STEP1_CLICK_BOX = [0.82,0.68,0.92,0.74]#点击补给
SUPPLY_STEP2_CLICK_BOX = [0.70,0.40,0.80,0.50]#取消选中

#计划模式
#------------------------------------------#选中打捞队
PLAN_MODE_CLICK_BOX = [0.05,0.73,0.10,0.76]#点击计划模式
PLAN_POINT_CLICK_BOX = [0.05,0.60,0.10,0.65]#点击计划点 
PLAN_START_CLICK_BOX = [0.88,0.80,0.98,0.85]#点击执行计划

#在终点点击结束回合
ACTION_END_CLICK_BOX = [0.88,0.80,0.96,0.86]

#点击打捞队
DESTINATION_CLICK_BOX = [0.47,0.45,0.53,0.55]

#撤退打捞队
WITHDRAW_STEP1_CLICK_BOX = [0.70,0.78,0.76,0.83]#点击撤退
WITHDRAW_STEP2_CLICK_BOX = [0.55,0.62,0.62,0.67]#确认撤退

#重启作战
RESTART_STEP1_CLICK_BOX = [0.2,0.09,0.25,0.15]#点击终止作战
RESTART_STEP2_CLICK_BOX = [0.36,0.62,0.44,0.65]#点击重新作战

#强化（拆解）
GOTO_POWERUP_CLICK_BOX = [0.56,0.61,0.66,0.67]#前往强化界面
CHOOSE_RETIRE_CLICK_BOX = [0.08,0.52,0.16,0.58]#选择回收拆解选项
CHOOSE_CHARACTER_CLICK_BOX = [0.25,0.26,0.3,0.33]#选择拆解人形
CHARACTER_1_CLICK_BOX = [0.09,0.3,0.17,0.36]#第一行第一只人形 
CHARACTER_2_CLICK_BOX = [0.21,0.3,0.29,0.36]#第一行第二只人形 
CHARACTER_3_CLICK_BOX = [0.33,0.3,0.41,0.36]#第一行第三只人形 
CHARACTER_4_CLICK_BOX = [0.45,0.3,0.53,0.36]#第一行第四只人形 
CHARACTER_5_CLICK_BOX = [0.58,0.3,0.66,0.36]#第一行第五只人形 
CHARACTER_6_CLICK_BOX = [0.70,0.3,0.78,0.36]#第一行第六只人形 
RETIRE_DRAG_BOX = [0.40,0.60,0.60,0.60]#往上拖一行
CHOOSE_FINISH_CLICK_BOX = [0.84,0.78,0.92,0.86]#完成选择
RETIRE_CLICK_BOX = [0.82,0.72,0.9,0.78]#点击拆解
CONFIRM_RETIRE_CLICK_BOX = [0.54,0.76,0.64,0.82]#确认拆解高星人形

#跳至主菜单/战斗菜单
NAVIGATE_BAR_CLICK_BOX = [0.19,0.08,0.22,0.14]#打开导航条
NAVIGATE_BAR_DRAG_BOX = [0.15,0.32,0.17,0.36]#向右拖导航条
NAVIGATE_COMBAT_CLICK_BOX = [0.15,0.32,0.17,0.36]#点击作战
NAVIGATE_MAIN_MENU_CLICK_BOX = [0.20,0.21,0.28,0.25]#返回基地

#收后勤支援
L_SUPPORT_STEP1_CLICK_BOX = [0.50,0.50,0.60,0.60]#确认后勤完成
L_SUPPORT_STEP2_CLICK_BOX = [0.53,0.62,0.62,0.67]#再次派出

#启动游戏
START_GAME_STEP1_CLICK_BOX = [0.14,0.23,0.18,0.28]#点击图标启动
START_GAME_STEP2_CLICK_BOX = [0.50,0.70,0.50,0.70]#点击一次
START_GAME_STEP3_CLICK_BOX = [0.50,0.75,0.50,0.75]#点击开始
 
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
    
#判断是否计划结束
def isPlanFinished():
    initImage = cv2.imread(IMAGE_PATH+"plan_finish.png")
    capImage  = getImage(PLAN_FINISH_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)   
         
#判断是否进入了干涉仪II地图
def isInMap():
    initImage = cv2.imread(IMAGE_PATH+"map.png")
    capImage  = getImage(MAP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是提醒强化界面
def isGotoPowerup():
    initImage = cv2.imread(IMAGE_PATH+"goto_powerup.png")
    capImage  = getImage(GOTO_POWERUP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否小节选择界面
def isEpisodeMenu():
    initImage = cv2.imread(IMAGE_PATH+"episode.png")
    capImage  = getImage(EPISODE_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否章节选择菜单
def isChapterMenu():
    initImage = cv2.imread(IMAGE_PATH+"chapter.png")
    capImage  = getImage(CHAPTER_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是主界面
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

#当不知道在哪时，判断是否有导航栏，有就可以通过导航栏回到作战菜单
def findNavigate():
    initImage = cv2.imread(IMAGE_PATH+"navigate.png")
    capImage  = getImage(NAVIGATE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
  
#从主菜单进入作战菜单
def mainMenuToActivity():
    print("ACTION: 前往活动界面")
    mouseClick(ACTIVITY_CLICK_BOX,5,6)  
    
#从章节菜单进入第二章
def chapterMenuToEpisodeMenu():
    print("ACTION: 前往第二章")
    mouseClick(CHAPTER_2_CLICK_BOX,3,4)

#开始干涉仪II
def startJS9():
    print("ACTION: 启动干涉仪II")
    mouseClick(EPISODE_CLICK_BOX,3,4)
    mouseClick(ENTER_COMBAT_CLICK_BOX,4,5)    

#放置队伍
def setTeam():
    print("ACTION: 放置队伍")
    mouseDrag(MAP_DRAG_BOX,2,1,320,0.01,1)
    mouseDrag(MAP_DRAG_BOX,0,1,160,0.01,1)
    mouseClick(AIRPORT_1_CLICK_BOX,1,2)
    mouseClick(TEAM_SET_CLICK_BOX,2,2)
    mouseClick(AIRPORT_2_CLICK_BOX,1,2)
    mouseClick(TEAM_SET_CLICK_BOX,2,2)

#开始作战
def startCombat():
    print("ACTION: 开始作战")
    mouseClick(START_COMBAT_CLICK_BOX,4,5)

#补给机场打手
def supply():
    print("ACTION: 补给打捞队")
    mouseClick(AIRPORT_1_CLICK_BOX,1,2)
    mouseClick(AIRPORT_1_CLICK_BOX,2,3)
    mouseClick(SUPPLY_STEP1_CLICK_BOX,2,3)
    #mouseClick(SUPPLY_STEP2_CLICK_BOX,1,1.5)

#计划模式
def planMode():
    print("ACTION: 计划模式")
    #mouseClick(AIRPORT_1_CLICK_BOX,0.5,1)
    mouseClick(PLAN_MODE_CLICK_BOX,1,2)
    mouseDrag(MAP_DRAG_BOX,0,1,240,0.01,1)
    mouseClick(PLAN_POINT_CLICK_BOX,0.2,0.25)
    mouseClick(PLAN_START_CLICK_BOX,0,0.01)

#在终点点击结束回合
def endAction():
    print("ACTION: 结束回合")
    mouseClick(ACTION_END_CLICK_BOX,18,19)

#撤退打捞队
def withdraw():
    print("ACTION: 撤退打捞队")
    mouseClick(DESTINATION_CLICK_BOX,0.5,1)
    mouseClick(DESTINATION_CLICK_BOX,1,2)
    mouseClick(WITHDRAW_STEP1_CLICK_BOX,1,2)
    mouseClick(WITHDRAW_STEP2_CLICK_BOX,1,2)

#重启作战
def restartCombat():
    print("ACTION: 重启作战")
    mouseClick(RESTART_STEP1_CLICK_BOX,1,2)
    mouseClick(RESTART_STEP2_CLICK_BOX,4,5)

#强化（拆解）
def gotoPowerup():  
    print("ACTION: 拆解人形") 
    mouseClick(GOTO_POWERUP_CLICK_BOX,4,5)
    mouseClick(CHOOSE_RETIRE_CLICK_BOX,1,2)
    mouseClick(CHOOSE_CHARACTER_CLICK_BOX,1,2)
    for i in range(7):
        mouseClick(CHARACTER_1_CLICK_BOX,0.15,0.2)
        mouseClick(CHARACTER_2_CLICK_BOX,0.15,0.2)
        mouseClick(CHARACTER_3_CLICK_BOX,0.15,0.2)
        mouseClick(CHARACTER_4_CLICK_BOX,0.15,0.2)
        mouseClick(CHARACTER_5_CLICK_BOX,0.15,0.2)
        mouseClick(CHARACTER_6_CLICK_BOX,0.15,0.2)
        mouseDrag(RETIRE_DRAG_BOX,0,1,300,0.025,1)
    mouseClick(CHOOSE_FINISH_CLICK_BOX,1,2)
    mouseClick(RETIRE_CLICK_BOX,1,2)
    mouseClick(CONFIRM_RETIRE_CLICK_BOX,3,4)    

#跳转至主菜单
def backToMainMenu():
    print("ACTION: 跳转至主菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,2,3)
    mouseClick(NAVIGATE_MAIN_MENU_CLICK_BOX,10,12)

#收后勤支援
def takeLSupport():
    print("ACTION: 收派后勤")
    mouseClick(L_SUPPORT_STEP1_CLICK_BOX,2,3)
    mouseClick(L_SUPPORT_STEP2_CLICK_BOX,4,5)

#启动游戏
def startGame():
    print("ACTION: 启动游戏")
    mouseClick(START_GAME_STEP1_CLICK_BOX,30,30)
    mouseClick(START_GAME_STEP2_CLICK_BOX,30,30)
    mouseClick(START_GAME_STEP3_CLICK_BOX,30,30)

#=============================================#
#                                             #
#                 本程序主函数                 #
#                                             #
#=============================================#

if __name__ == "__main__": 
    preface()
    startTime = datetime.datetime.now()
    battleCount = 0
    failCount = 0

    while True:
        if isInMap():
            print("STATE：干涉仪II地图")
            failCount = 0
            setTeam()
            startCombat()
            supply()
            planMode()
            checkCount = 0
            while (not isPlanFinished()) and checkCount < 90:
                checkCount += 1
                time.sleep(1)
            if checkCount >= 90:
                print("STATE： 战斗超时！")
                continue
            endAction()
            withdraw()
            restartCombat()
            battleCount += 2
            currentTime = datetime.datetime.now()
            runtime = currentTime - startTime
            print('> 已运行：',runtime,'  战斗次数：',battleCount)                
        elif isGotoPowerup():
            print("STATE： 提醒强化界面")
            gotoPowerup()
            backToMainMenu()
            failCount = 0
        elif isEpisodeMenu():
            print("STATE： 小节菜单界面")
            startJS9()
            failCount = 0
        elif isChapterMenu():
            print("STATE： 战斗菜单")
            chapterMenuToEpisodeMenu()
            failCount = 0
        elif isMainMenu():
            print("STATE： 主菜单界面")
            mainMenuToActivity()
            failCount = 0
        elif isLSupport():
            print("STATE： 后勤结束界面")
            takeLSupport()
            failCount = 0
        elif isDesktop():
            print("STATE： 模拟器桌面")
            startGame()
            failCount = 0
        else:#既不是后勤结束界面也不是
            print("WARNING： 当前状态未知!")
            if findNavigate():
                print("STATE：找到导航条")
                backToMainMenu()
                failCount = 0
            else: 
                failCount += 1
                if failCount == 5:  
                    print(">>> ",datetime.datetime.now()," 无法确定当前状态,程序退出！")
                    exit(0)
                else:
                    time.sleep(10)
                
            
            
