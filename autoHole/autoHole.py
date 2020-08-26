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
MAIN_MENU_IMAGE_BOX = [0.65,0.50,0.75,0.58]         #主界面判断区域          
COMBAT_MENU_IMAGE_BOX = [0.05,0.70,0.12,0.80]#战斗菜单界面判断区域                   
L_SUPPORT_IMAGE_BOX = [0.05,0.30,0.18,0.39]         #后勤完成界面判断区域                         
ACTIVITY_MENU_IMAGE_BOX = [0.01,0.15,0.10,0.20]  #活动界面判断区域        
HOLE_IMAGE_BOX = [0.78,0.38,0.88,0.42]     #活动界面判断区域      
ENTER_HOLE_IMAGE_BOX = [0.86,0.46,0.92,0.50]     #活动界面判断区域            
MAP_IMAGE_BOX = [0.82,0.80,0.95,0.88]               #进入地图判断区域
SET_TEAM_IMAGE_BOX = [0.85,0.75,0.92,0.78]          #队伍放置判断区域  
COMBAT_START_IMAGE_BOX = [0.80,0.82,0.97,0.88]      #开启作战判断区域  
PLAN_FINISH_IMAGE_BOX = [0.80,0.82,0.85,0.88]       #计划完成判断区域   
SETTLE_CONFIRM_IMAGE_BOX = [0.55,0.60,0.62,0.64]    #确认结算判断区域                   
GOTO_POWERUP_IMAGE_BOX = [0.58,0.60,0.68,0.64]     #提醒强化判断区域               
NAVIGATE_IMAGE_BOX = [0.15,0.10,0.20,0.15]          #导航条判断区域       
DESKTOP_IMAGE_BOX = [0.10,0.20,0.22,0.35]           #模拟器桌面判断区域         
COMBAT_PAUSE_IMAGE_BOX = [0.45,0.62,0.55,0.67]      #战斗终止提示判断区域            
RETURN_COMBAT_IMAGE_BOX = [0.75,0.63,0.90,0.70]     #回到作战界面判断区域    

#=================点击拖动区域=================#

#从主菜单进入作战选择界面
COMBAT_CLICK_BOX = [0.65,0.50,0.75,0.58]#在主菜单点击战斗

#从作战选择界面进入活动界面
ACTIVITY_CLICK_BOX = [0.05,0.18,0.10,0.20]

#在活动界面拖动到最左边
ACTIVITY_DRAG_BOX = [0.20,0.80,0.22,0.85]

#进入秃洞
HOLE_CLICK_BOX = [0.80,0.44,0.85,0.48]#选择秃洞
ENTER_COMBAT_CLICK_BOX = [0.86,0.46,0.92,0.50]#进入作战
END_COMBAT_STEP1_CLICK_BOX = [0.72,0.46,0.80,0.50]#终止作战
END_COMBAT_STEP2_CLICK_BOX = [0.52,0.60,0.60,0.65]#确认终止作战

#指挥部位置点
BASE_CLICK_BOX = [0.48,0.48,0.52,0.52]

#扛伤位（第一个）修复
REPAIR_INTERVAL = 20#隔多少轮修一次
REPAIR_STEP1_CLICK_BOX = [0.16,0.30,0.24,0.50]#点击一号位        
REPAIR_STEP2_CLICK_BOX = [0.69,0.65,0.75,0.69]#确定修复          
REPAIR_STEP3_CLICK_BOX = [0.75,0.75,0.81,0.79]#退出队伍界面  

#放置队伍
TEAM_SET_CLICK_BOX = [0.85,0.75,0.92,0.78]

#开始作战
START_COMBAT_CLICK_BOX = [0.85,0.82,0.92,0.86]#点击开始作战
CLOSE_ILLUSTRATION_CLICK_BOX = [0.14,0.24,0.16,0.26]#关闭作战说明

#计划模式
PLAN_MODE_CLICK_BOX = [0.04,0.77,0.10,0.79]#点击计划模式
PLAN_POINT1_CLICK_BOX = [0.18,0.64,0.20,0.68]#点击计划点1 
PLAN_POINT2_CLICK_BOX = [0.78,0.32,0.82,0.36]#点击计划点2
PLAN_START_CLICK_BOX = [0.88,0.82,0.98,0.85]#点击执行计划

#战役结算
SETTLE_CLICK_BOX = [0.22,0.09,0.26,0.14]#点击结算
CONFIRM_SETTLE_CLICK_BOX = [0.55,0.60,0.62,0.64]#点击确认结算
SKIP_SETTLE_CLICK_BOX = [0.40,0.10,0.60,0.15]#随便点点

#拆解
GOTO_POWERUP_CLICK_BOX = [0.58,0.60,0.68,0.64]#前往强化界面
CHOOSE_RETIRE_CLICK_BOX = [0.06,0.46,0.12,0.50]#选择回收拆解选项
CHOOSE_RETIRE_CHARACTER_CLICK_BOX = [0.25,0.26,0.3,0.33]#选择拆解人形
RETIRE_CHARACTER_1_CLICK_BOX = [0.12,0.3,0.14,0.36]#第一行第一只人形 
RETIRE_CHARACTER_2_CLICK_BOX = [0.24,0.3,0.26,0.36]#第一行第二只人形 
RETIRE_CHARACTER_3_CLICK_BOX = [0.36,0.3,0.38,0.36]#第一行第三只人形 
RETIRE_CHARACTER_4_CLICK_BOX = [0.48,0.3,0.50,0.36]#第一行第四只人形 
RETIRE_CHARACTER_5_CLICK_BOX = [0.60,0.3,0.62,0.36]#第一行第五只人形 
RETIRE_CHARACTER_6_CLICK_BOX = [0.72,0.3,0.74,0.36]#第一行第六只人形 
RETIRE_DRAG_BOX = [0.40,0.60,0.60,0.60]#往上拖一行
CHOOSE_FINISH_RETIRE_CLICK_BOX = [0.88,0.68,0.92,0.74]#完成选择
RETIRE_CLICK_BOX = [0.84,0.77,0.90,0.80]#点击拆解
CONFIRM_RETIRE_CLICK_BOX = [0.54,0.74,0.64,0.78]#确认拆解高星人形

#跳至主菜单/战斗菜单/工厂菜单
NAVIGATE_BAR_CLICK_BOX = [0.15,0.10,0.18,0.15]#打开导航条
NAVIGATE_MAIN_MENU_CLICK_BOX = [0.20,0.18,0.28,0.20]#跳转至主菜单

#收后勤支援
L_SUPPORT_STEP1_CLICK_BOX = [0.50,0.50,0.60,0.60]#确认后勤完成
L_SUPPORT_STEP2_CLICK_BOX = [0.53,0.60,0.62,0.65]#再次派出

#启动游戏
START_GAME_STEP1_CLICK_BOX = [0.14,0.23,0.18,0.28]#点击图标启动
START_GAME_STEP2_CLICK_BOX = [0.50,0.70,0.50,0.70]#点击一次
START_GAME_STEP3_CLICK_BOX = [0.50,0.75,0.50,0.75]#点击开始 

#关闭游戏
CLOSE_GAME_CLICK_BOX = [0.56,0.02,0.57,0.04]

#关闭作战断开提醒
CLOSE_TIP_CLICK_BOX = [0.45,0.62,0.55,0.67]

#=============================================#
#                                             #
#                 基本功能函数                 #
#                                             #
#=============================================#

#一个好程序都应该有一个较为优雅的启动提醒界面？
def preface():    
    for x in range(3,-1,-1):
        mystr =">>> "+str(x)+"s 后将开始操作，请切换至模拟器界面"
        print(mystr,end="")
        print("\b" * (len(mystr)*2),end = "",flush=True)
        time.sleep(1)
    print(">>> 开始操作,现在是",datetime.datetime.now(),"\n")


#随机等待一段时间,控制在minTime~maxTime之间
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
    imgLeft   = windowData[0] + int(windowData[4] * box[0])
    imgTop    = windowData[1] + int(windowData[5] * box[1])
    imgRight  = windowData[0] + int(windowData[4] * box[2])
    imgBottom = windowData[1] + int(windowData[5] * box[3])
    img = ImageGrab.grab((imgLeft,imgTop,imgRight,imgBottom))
    return img
    
    
#点击box内随机一点，如果提供具体xy偏量，则点击精确的点
def mouseClick(box,minTime,maxTime,exact_x = 0,exact_y = 0):
    #box = [left,top,right,bottom]
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    if exact_x == 0 and exact_y == 0:
        clickX = windowData[0] + (int)(windowData[4] * box[0] + windowData[4] * width  * random.random())
        clickY = windowData[1] + (int)(windowData[5] * box[1] + windowData[5] * height * random.random())
    else:
        clickX = windowData[0] + (int)(windowData[4] * box[0]) + exact_x
        clickY = windowData[1] + (int)(windowData[5] * box[1]) + exact_y
    clickPos = (clickX,clickY)
    win32api.SetCursorPos(clickPos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    wait(minTime,maxTime)


#模拟鼠标拖动，box为起始区域,times为拖动次数,distance为单次拖动距离
#dx,dy为组成移动方向向量，frame_interval为鼠标拖动帧间隔,越小鼠标拖动越快
#multi_interval为连续拖动时的时间间隔
def mouseDrag(box,dx,dy,times,distance,frame_interval,multi_interval):
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    for i in range(times):
        dragX = windowData[0] + int(windowData[4] * box[0] + windowData[4] * width  * random.random())
        dragY = windowData[1] + int(windowData[5] * box[1] + windowData[5] * height * random.random())
        dragPos = (dragX, dragY)
        win32api.SetCursorPos(dragPos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        for i in range(distance):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,dx,dy,0,0)
            time.sleep(frame_interval)
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        time.sleep(multi_interval)


#模拟Ctrl和滚轮实现缩放地图
#direct = 0 : 放大      direct = 1 : 缩小   times为连续缩放次数
def scaleMap(box,direct,times):
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    scaleX = windowData[0] + int(windowData[4] * box[0] + windowData[4] * width  * random.random())
    scaleY = windowData[1] + int(windowData[5] * box[1] + windowData[5] * height * random.random())
    scalePos = (scaleX, scaleY)
    win32api.SetCursorPos(scalePos)
    win32api.keybd_event(0x11,0,0,0)#按下Ctrl键
    for i in range(times):
        if direct == 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,1)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,-1)
        wait(0.5,0.7)
    win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP,0)    
    time.sleep(1)
        

#比较两图片吻合度，结构相似性比较法（真的好用）
def imageCompare(img1,img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
    return score > 0.95

#=============================================#
#                                             #
#                 高级功能函数                 #
#                                             #
#=============================================#
    
#判断是否计划结束
def isPlanFinished(doubleCheck = True):
    initImage = cv2.imread(IMAGE_PATH+"plan_finish.png")
    capImage  = getImage(PLAN_FINISH_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    #双重判断
    if imageCompare(initImage,capImage):
        if not doubleCheck:
            return True
        time.sleep(5)
        capImage  = getImage(PLAN_FINISH_IMAGE_BOX)
        capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
        if imageCompare(initImage,capImage):
            return True
    return False
         
#判断是否进入了秃洞地图
def isInMap():
    initImage = cv2.imread(IMAGE_PATH+"map.png")
    capImage  = getImage(MAP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否作战正常开启
def isCombatStart():
    initImage = cv2.imread(IMAGE_PATH+"combat_start.png")
    capImage  = getImage(COMBAT_START_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是提醒强化界面
def isGotoPowerup():
    initImage = cv2.imread(IMAGE_PATH+"goto_powerup.png")
    capImage = getImage(GOTO_POWERUP_IMAGE_BOX)
    capImage = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是可以选择秃洞的界面
def isHole():
    initImage = cv2.imread(IMAGE_PATH+"hole.png")
    capImage  = getImage(HOLE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是活动菜单界面
def isActivityMenu():
    initImage = cv2.imread(IMAGE_PATH+"activity_menu.png")
    capImage  = getImage(ACTIVITY_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是战斗选择菜单
def isCombatMenu():
    initImage = cv2.imread(IMAGE_PATH+"combat_menu.png")
    capImage  = getImage(COMBAT_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否可以确认出击
def isEnterHole():
    initImage = cv2.imread(IMAGE_PATH+"enter_hole.png")
    capImage  = getImage(ENTER_HOLE_IMAGE_BOX)
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

#判断是否是战斗中断提示界面
def isCombatPause():
    initImage = cv2.imread(IMAGE_PATH+"combat_pause.png")
    capImage  = getImage(COMBAT_PAUSE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否有回到作战界面
def isReturnCombat():
    initImage = cv2.imread(IMAGE_PATH+"return_combat.png")
    capImage  = getImage(RETURN_COMBAT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#在队伍放置界面
def isSetTeam():
    initImage = cv2.imread(IMAGE_PATH+"set_team.png")
    capImage  = getImage(SET_TEAM_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#在确认结算界面
def isConfirmSettle():
    initImage = cv2.imread(IMAGE_PATH+"settle_confirm.png")
    capImage  = getImage(SETTLE_CONFIRM_IMAGE_BOX )
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#从主菜单进入作战菜单
def mainMenuToCombatMenu():
    print("ACTION: 前往作战菜单")
    mouseClick(COMBAT_CLICK_BOX,0,0)  
    checkCount = 0
    while not isCombatMenu() and checkCount < 20:
        wait(0.75,1)
        checkCount += 1
    time.sleep(0.5)

#从作战菜单进入活动菜单
def combatMenuToActivityMenu():
    print("ACTION：前往活动菜单")
    mouseClick(ACTIVITY_CLICK_BOX,0,0)
    checkCount = 0
    while not isActivityMenu() and checkCount < 20:
        wait(0.75,1)
        checkCount += 1
    time.sleep(0.5)

#拖动活动菜单
def toTheLeft():
    print("ACTION：拖动活动菜单")
    mouseDrag(ACTIVITY_DRAG_BOX,1,0,1,1000,0.0002,0.1)

#进入秃洞
def startHole():
    print("ACTION: 进入秃洞")
    mouseClick(HOLE_CLICK_BOX,0,0)
    checkCount = 0
    while not isEnterHole() and checkCount < 20:
        time.sleep(0.25)
        checkCount += 1
    time.sleep(0.25)
    mouseClick(ENTER_COMBAT_CLICK_BOX,0,0)
    checkCount = 0
    while not isInMap() and checkCount < 50:
        wait(0.2,0.4)
        checkCount += 1
    time.sleep(0.2)
   
#终止已开始的秃洞
def endHole():
    print("ACTION: 终止8-1n")
    mouseClick(HOLE_CLICK_BOX,2,3)
    mouseClick(END_COMBAT_STEP1_CLICK_BOX,2,3)  
    mouseClick(END_COMBAT_STEP2_CLICK_BOX,2,3)  

#放置队伍
def setTeam():
    print("ACTION: 放置队伍")
    mouseClick(BASE_CLICK_BOX,0,0)#点击指挥部
    checkCount = 0
    while not isSetTeam() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.3)
    mouseClick(TEAM_SET_CLICK_BOX,0,0)#点击放置队伍
    checkCount = 0
    while not isInMap() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    return True

#扛伤位修复
def repair():
    print("ACTION: 修复扛伤位")
    mouseClick(BASE_CLICK_BOX,0,0)#点击指挥部
    checkCount = 0
    while not isSetTeam() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.1)
    mouseClick(REPAIR_STEP1_CLICK_BOX,1.5,2)
    mouseClick(REPAIR_STEP2_CLICK_BOX,1,2)
    mouseClick(REPAIR_STEP3_CLICK_BOX,2,3)
    return True

#开始作战
def startCombat():
    print("ACTION: 开始作战")
    mouseClick(START_COMBAT_CLICK_BOX,0,0) 
    checkCount = 0
    while not isCombatStart() and checkCount < 40:
        wait(0.25,0.3)
        checkCount += 1
    if checkCount >= 40:
        return False
    time.sleep(2)
    mouseClick(CLOSE_ILLUSTRATION_CLICK_BOX,1,2) 
    return True

#计划模式
def planMode():
    print("ACTION: 计划模式")
    mouseClick(PLAN_MODE_CLICK_BOX,0.3,0.35)    
    mouseClick(BASE_CLICK_BOX,0.25,0.28)
    mouseClick(PLAN_POINT1_CLICK_BOX,0.25,0.28)
    mouseClick(PLAN_POINT2_CLICK_BOX,0.25,0.28)
    mouseClick(PLAN_START_CLICK_BOX,0,0)
    
#战役结算
def settleCombat():
    print("ACTION: 战役结算")
    mouseClick(SETTLE_CLICK_BOX,0,0)
    checkCount = 0
    while not isConfirmSettle() and checkCount < 20:
        wait(0.5,0.6)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.5)
    print("ACTION: 确认结算")
    mouseClick(CONFIRM_SETTLE_CLICK_BOX,0.5,0.5)
    checkCount = 0
    while not isActivityMenu() and checkCount < 20:
        mouseClick(SKIP_SETTLE_CLICK_BOX,0.5,0.6)
        checkCount += 1
    return True

#拆解
def gotoRetire():  
    print("ACTION: 拆解人形") 
    mouseClick(GOTO_POWERUP_CLICK_BOX,5,6)
    mouseClick(CHOOSE_RETIRE_CLICK_BOX,1,2)
    mouseClick(CHOOSE_RETIRE_CHARACTER_CLICK_BOX,1,2)
    for i in range(8):
        mouseClick(RETIRE_CHARACTER_1_CLICK_BOX,0.2,0.3)#选六个
        mouseClick(RETIRE_CHARACTER_2_CLICK_BOX,0.2,0.3)
        mouseClick(RETIRE_CHARACTER_3_CLICK_BOX,0.2,0.3)
        mouseClick(RETIRE_CHARACTER_4_CLICK_BOX,0.2,0.3)
        mouseClick(RETIRE_CHARACTER_5_CLICK_BOX,0.2,0.3)
        mouseClick(RETIRE_CHARACTER_6_CLICK_BOX,0.2,0.3)
        mouseDrag(RETIRE_DRAG_BOX,0,-1,1,325,0.005,1)#往上拖一行
    mouseClick(CHOOSE_FINISH_RETIRE_CLICK_BOX,1,2)
    mouseClick(RETIRE_CLICK_BOX,1,2)
    mouseClick(CONFIRM_RETIRE_CLICK_BOX,3,4)   

#跳转至主菜单(回主菜单收后勤)
def backToMainMenu():
    print("ACTION: 跳转至主菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseClick(NAVIGATE_MAIN_MENU_CLICK_BOX,5,6)

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

#关闭作战断开提醒
def closeTip():
    mouseClick(CLOSE_TIP_CLICK_BOX,5,5)

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
    startTime = datetime.datetime.now()
    combatCount = 0
    firstCombat = True
    failCount = 0
    dragCount = 0

    while True:
        if isInMap():
            print("STATE：进入地图")
            failCount = 0 
            if combatCount % REPAIR_INTERVAL == 0 or firstCombat:
                if not repair():
                   print("ERROR：扛伤位修复失败")
                   closeGame()
                   continue     
                firstCombat = False     
            if not setTeam():
                print("ERROR：队伍放置失败")
                closeGame()
                continue
            if not startCombat():
                print("ERROR：战役启动失败")
                continue
            planMode()
            checkCount = 0
            while (not isPlanFinished()) and checkCount < 150:#计划开始后150s还没打完，一般是出问题了（比方说卡了一下导致流程漏了）
                checkCount += 1
                time.sleep(1)
            if checkCount >= 150:#过了150s还没结束，直接关闭窗口重启
                print("ERROR：战斗超时！")
                closeGame()
                continue
            time.sleep(0.2)
            if not settleCombat():
                print("ERROR：作战重启失败")
                closeGame()
                continue
            combatCount += 1
            currentTime = datetime.datetime.now()
            runtime = currentTime - startTime
            print('> 已运行：',runtime,'  轮次：',combatCount)                
        elif isHole():
            print("STATE： 可以进入秃洞")
            startHole()
            dragCount = 0
            failCount = 0
        elif isActivityMenu():
            print("STATE： 活动菜单界面")
            toTheLeft()
            dragCount += 1
            if dragCount > 5:
                closeGame()
                continue
            failCount = 0
        elif isGotoPowerup():
            print("STATE： 强化提醒界面")
            firstCombat = True
            gotoRetire()
            backToMainMenu()
        elif isCombatMenu():
            print("STATE： 战斗菜单")
            combatMenuToActivityMenu()
            failCount = 0
        elif isCombatPause():
            print("STATE： 战斗中断提醒界面")
            failCount = 0
            closeTip()
        elif isReturnCombat():
            print("STATE： 返回作战界面")
            failCount = 0
            mainMenuToCombatMenu()
            combatMenuToActivityMenu()
            time.sleep(6)
            toTheLeft()
            toTheLeft()
            toTheLeft()
            endHole()
            firstCombat = True
        elif isMainMenu():
            print("STATE： 主菜单界面")
            mainMenuToCombatMenu()
            failCount = 0
        elif isLSupport():
            print("STATE： 后勤结束界面")
            takeLSupport()
            failCount = 0
        elif isDesktop():
            print("STATE：模拟器桌面")
            firstCombat = True
            dragCount = 0
            failCount = 0
            startGame()
            continue
        else:#不知道在哪
            print("ERROR： 当前状态未知!")
            failCount += 1
            if failCount >= 5:  
                print(">>> ",datetime.datetime.now()," 无法确定当前状态,关闭重启！")
                closeGame()
            else:
                time.sleep(5)
                
            
            
