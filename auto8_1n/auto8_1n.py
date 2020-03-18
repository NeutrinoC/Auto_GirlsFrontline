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

#下面所有的BOX都是[left,up,right,down]形式，且都是相对于窗口界面的（0~1）
#这些数据最好自己调试一下，对于不同分辨率的模拟器，位置变化会很大的


#=================截图比对区域=================#
IMAGE_PATH = 'initial_IMG/'#读取截图的路径
MAIN_MENU_IMAGE_BOX = [0.62,0.52,0.76,0.60]#主界面判断区域                       
L_SUPPORT_IMAGE_BOX = [0.02,0.30,0.18,0.37]#后勤完成界面判断区域                
COMBAT_MENU_IMAGE_BOX = [0.10,0.70,0.18,0.85]#战斗菜单界面判断区域          
CHOOSE_8_1N_IMAGE_BOX = [0.50,0.35,0.60,0.45]#8-1n菜单界面判断区域                        
MAP_8_1N_IMAGE_BOX = [0.47,0.45,0.53,0.55]#8-1n地图判断区域                             
PLAN_FINISH_IMAGE_BOX = [0.80,0.78,0.97,0.87]#计划完成判断区域  
COMBAT_START_IMAGE_BOX = [0.80,0.78,0.97,0.87]#开启作战判断区域                              
GOTO_POWERUP_IMAGE_BOX = [0.58,0.62,0.65,0.66]#提醒强化判断区域               
NAVIGATE_IMAGE_BOX = [0.18,0.10,0.22,0.17]#导航条判断区域       
DESKTOP_IMAGE_BOX = [0.10,0.20,0.22,0.40]#模拟器桌面判断区域         
COMBAT_PAUSE_IMAGE_BOX = [0.45,0.67,0.55,0.73]#战斗终止提示判断区域            
RETURN_COMBAT_IMAGE_BOX = [0.75,0.65,0.90,0.72]#回到作战界面判断区域    

#=================点击拖动区域=================#

#从主菜单进入作战选择界面
COMBAT_CLICK_BOX = [0.62,0.52,0.76,0.60]#在主菜单点击战斗
BACK_TO_COMBAT_CLICK_BOX = [0.75,0.65,0.90,0.72]#主菜单回到战斗
BACK_TO_COMBAT_AFTER_CLICK_BOX = [0.49,0.08,0.51,0.12]#战斗结束后随机点击完成结算

#从作战选择界面进入8-1n界面
COMBAT_MISSION_CLICK_BOX = [0.07,0.3,0.17,0.38]#点击作战任务
CHAPTER_DRAG_BOX = [0.19,0.65,0.25,0.75]#向上拖章节选择条
CHAPTER_8_CLICK_BOX = [0.19,0.24,0.25,0.33]#选择第8章
NIGHT_CLICK_BOX = [0.87,0.26,0.93,0.3]#选择夜战

#开始8-1n
EPISODE_1_CLICK_BOX = [0.40,0.38,0.80,0.46]#选择第1节
ENTER_COMBAT_CLICK_BOX = [0.53,0.71,0.61,0.77]#进入作战

#机场位置点
AIRPORT_1_CLICK_BOX = [0.47,0.49,0.53,0.51]#下机场
AIRPORT_2_CLICK_BOX = [0.58,0.27,0.63,0.29]#上机场
AIRPORT_3_CLICK_BOX = [0.26,0.83,0.31,0.85]#(计划完成后)下机场

#更换打手
CHANGE_FORCE_STEP1_CLICK_BOX = [0.18,0.77,0.28,0.81]#点击梯队编成
CHANGE_FORCE_STEP2_CLICK_BOX = [0.18,0.35,0.28,0.55]#点击Zas
CHANGE_FORCE_STEP3_CLICK_BOX = [0.83,0.20,0.90,0.30]#点击排序方式
CHANGE_FORCE_STEP4_CLICK_BOX = [0.72,0.70,0.78,0.78]#点击受损程度
CHANGE_FORCE_STEP5_CLICK_BOX = [0.22,0.25,0.28,0.45]#选择Zas
CHANGE_FORCE_STEP6_CLICK_BOX = [0.12,0.12,0.14,0.15]#点击返回

#放置队伍
TEAM_SET_CLICK_BOX = [0.84,0.78,0.90,0.83]
MAP_DRAG_DOWN_BOX = [0.20,0.20,0.30,0.25]#往下拖动地图

#开始作战
START_COMBAT_CLICK_BOX = [0.82,0.78,0.95,0.85]#点击开始作战

#计划模式
PLAN_MODE_CLICK_BOX = [0.05,0.73,0.10,0.76]#点击计划模式
PLAN_POINT1_CLICK_BOX = [0.42,0.74,0.46,0.76]#点击计划点1 
MAP_DRAG_UP_BOX = [0.20,0.80,0.30,0.85]#往上拖动地图
PLAN_POINT2_CLICK_BOX = [0.45,0.65,0.49,0.67]#点击计划点2
PLAN_POINT3_CLICK_BOX = [0.69,0.77,0.74,0.79]#点击计划点3
PLAN_START_CLICK_BOX = [0.88,0.80,0.98,0.85]#点击执行计划

#补给Zas
SUPPLY_CLICK_BOX = [0.82,0.68,0.92,0.74]#点击补给

#撤退Zas
WITHDRAW_STEP1_CLICK_BOX = [0.70,0.78,0.76,0.83]#点击撤退
WITHDRAW_STEP2_CLICK_BOX = [0.55,0.62,0.62,0.67]#确认撤退

#重启作战
RESTART_STEP1_CLICK_BOX = [0.2,0.09,0.25,0.15]#点击终止作战
RESTART_STEP2_CLICK_BOX = [0.36,0.62,0.44,0.65]#点击重新作战

#强化（拆解）
GOTO_POWERUP_CLICK_BOX = [0.58,0.62,0.65,0.66]#前往强化界面
CHOOSE_RETIRE_CLICK_BOX = [0.08,0.52,0.16,0.58]#选择回收拆解选项
CHOOSE_EQUIPMENT_CLICK_BOX = [0.40,0.26,0.43,0.33]#选择拆解装备
CHOOSE_ORDER_CLICK_BOX = [0.87,0.59,0.93,0.63]#选择升序
EQUIPMENT_1_CLICK_BOX = [0.09,0.3,0.17,0.36]#第一行第一件装备
EQUIPMENT_2_CLICK_BOX = [0.21,0.3,0.29,0.36]#第一行第二件装备 
EQUIPMENT_3_CLICK_BOX = [0.33,0.3,0.41,0.36]#第一行第三件装备
EQUIPMENT_4_CLICK_BOX = [0.45,0.3,0.53,0.36]#第一行第四件装备 
EQUIPMENT_5_CLICK_BOX = [0.58,0.3,0.66,0.36]#第一行第五件装备
EQUIPMENT_6_CLICK_BOX = [0.70,0.3,0.78,0.36]#第一行第六件装备
RETIRE_DRAG_BOX = [0.40,0.60,0.60,0.60]#往上拖一行
CHOOSE_FINISH_CLICK_BOX = [0.84,0.78,0.92,0.86]#完成选择
RETIRE_CLICK_BOX = [0.82,0.72,0.9,0.78]#点击拆解
CONFIRM_RETIRE_CLICK_BOX = [0.54,0.76,0.64,0.82]#确认拆解高星级

#跳至主菜单/战斗菜单/工厂菜单
NAVIGATE_BAR_CLICK_BOX = [0.19,0.08,0.22,0.14]#打开导航条
NAVIGATE_BAR_DRAG_BOX = [0.15,0.32,0.17,0.36]#向右拖导航条
NAVIGATE_COMBAT_CLICK_BOX = [0.15,0.32,0.17,0.36]#跳转至作战菜单
NAVIGATE_FACTORY_CLICK_BOX = [0.35,0.32,0.37,0.36]#跳转至工厂菜单
NAVIGATE_MAIN_MENU_CLICK_BOX = [0.20,0.21,0.28,0.25]#跳转至主菜单

#收后勤支援
L_SUPPORT_STEP1_CLICK_BOX = [0.50,0.50,0.60,0.60]#确认后勤完成
L_SUPPORT_STEP2_CLICK_BOX = [0.53,0.62,0.62,0.67]#再次派出

#启动游戏
START_GAME_STEP1_CLICK_BOX = [0.14,0.23,0.18,0.28]#点击图标启动
START_GAME_STEP2_CLICK_BOX = [0.50,0.70,0.50,0.70]#点击一次
START_GAME_STEP3_CLICK_BOX = [0.50,0.75,0.50,0.75]#点击开始 

#关闭游戏
CLOSE_GAME_CLICK_BOX = [0.52,0.03,0.53,0.04]

#关闭作战断开提醒
CLOSE_TIP_CLICK_BOX = [0.45,0.67,0.55,0.73]

#=============================================#
#                                             #
#                 基本功能函数                 #
#                                             #
#=============================================#

#一个好程序都应该有一个较为优雅的启动提醒界面？
def preface():    
    for x in range(5,-1,-1):
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
    imgTop  = windowData[1] + int(windowData[5] * box[1])
    imgRight  = windowData[0] + int(windowData[4] * box[2])
    imgBottom = windowData[1] + int(windowData[5] * box[3])
    img = ImageGrab.grab((imgLeft,imgTop,imgRight,imgBottom))
    return img
    
    
#点击box内随机一点，点完后会随机等待一段时间
def mouseClick(box,minTime,maxTime):
    #box = [left,top,right,bottom]
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    clickX = windowData[0] + int(windowData[4] * box[0]) + int(windowData[4] * width  * random.random())
    clickY = windowData[1] + int(windowData[5] * box[1]) + int(windowData[5] * height * random.random())
    clickPos = (clickX,clickY)
    win32api.SetCursorPos(clickPos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    wait(minTime,maxTime)#等待minTime~maxTime的时间


#模拟鼠标拖动，box为起始区域,times为拖动次数,distance为单次拖动距离
#frame_interval为鼠标拖动帧间隔,越小鼠标拖动越快
#multi_interval为连续拖动时的时间间隔
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
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        time.sleep(multi_interval)


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
def isPlanFinished():
    initImage = cv2.imread(IMAGE_PATH+"plan_finish.png")
    capImage  = getImage(PLAN_FINISH_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)   
         
#判断是否进入了8-1n地图
def isInMap():
    initImage = cv2.imread(IMAGE_PATH+"map.png")
    capImage  = getImage(MAP_8_1N_IMAGE_BOX)
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

#判断是否是可以选择8-1n的界面
def is8_1n():
    initImage = cv2.imread(IMAGE_PATH+"_8_1n.png")
    capImage  = getImage(CHOOSE_8_1N_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是战斗选择菜单
def isCombatMenu():
    initImage = cv2.imread(IMAGE_PATH+"combat_menu.png")
    capImage  = getImage(COMBAT_MENU_IMAGE_BOX)
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

#当不知道在哪时，判断是否有导航栏，有就可以通过导航栏回到作战菜单
def findNavigate():
    initImage = cv2.imread(IMAGE_PATH+"navigate.png")
    capImage  = getImage(NAVIGATE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
  
#从主菜单进入作战菜单
def mainMenuToCombatMenu():
    print("ACTION: 前往作战菜单")
    mouseClick(COMBAT_CLICK_BOX,5,6)  

#从主菜单回到作战
def mainMenuBackToCombat():
    print("ACTION: 回到作战")
    mouseClick(BACK_TO_COMBAT_CLICK_BOX,60,60)  
    for i in range(8):
        mouseClick(BACK_TO_COMBAT_AFTER_CLICK_BOX,0.6,0.7)    

#从作战菜单进入8-1n界面
def combatMenuTo8_1n():
    print("ACTION: 前往8-1n选择界面")
    mouseClick(COMBAT_MISSION_CLICK_BOX,1,2)
    mouseDrag(CHAPTER_DRAG_BOX,0,3,500,0.001,2)
    mouseClick(CHAPTER_8_CLICK_BOX,1,2)
    mouseClick(NIGHT_CLICK_BOX,1,2)

#开始8-1n
def start8_1n():
    print("ACTION: 启动8-1n")
    mouseClick(EPISODE_1_CLICK_BOX,2,3)
    mouseClick(ENTER_COMBAT_CLICK_BOX,4,5)    

#战前准备，给一队补给
def combatPrepare():
    print("STATE: 战前整备")
    setTeam()
    startCombat()
    mouseDrag(MAP_DRAG_UP_BOX,0,2,500,0.002,1)
    mouseClick(AIRPORT_1_CLICK_BOX,1,2)
    mouseClick(AIRPORT_1_CLICK_BOX,1,2)
    mouseClick(SUPPLY_CLICK_BOX,2,3)
    mouseClick(AIRPORT_1_CLICK_BOX,1,2)
    mouseClick(WITHDRAW_STEP1_CLICK_BOX,2,3)
    mouseClick(WITHDRAW_STEP2_CLICK_BOX,2,3)
    restartCombat()

#更换打手
def changeForce():
    print("ACTION: 更换打手")
    mouseClick(AIRPORT_1_CLICK_BOX,2,2.5)
    mouseClick(CHANGE_FORCE_STEP1_CLICK_BOX,3.5,4)
    mouseClick(CHANGE_FORCE_STEP2_CLICK_BOX,3.5,4)
    mouseClick(CHANGE_FORCE_STEP3_CLICK_BOX,0.5,1)
    mouseClick(CHANGE_FORCE_STEP4_CLICK_BOX,1,1.5)
    mouseClick(CHANGE_FORCE_STEP5_CLICK_BOX,2.5,3)
    mouseClick(CHANGE_FORCE_STEP6_CLICK_BOX,4.5,5)

#放置队伍
def setTeam():
    print("ACTION: 放置队伍")
    mouseClick(AIRPORT_1_CLICK_BOX,1.2,1.5)
    mouseClick(TEAM_SET_CLICK_BOX,2,2.5)
    mouseDrag(MAP_DRAG_DOWN_BOX,1,2,500,0.002,1)
    mouseClick(AIRPORT_2_CLICK_BOX,1.2,1.5)
    mouseClick(TEAM_SET_CLICK_BOX,2,2.5)

#开始作战
def startCombat():
    print("ACTION: 开始作战")
    mouseClick(START_COMBAT_CLICK_BOX,4,5) 

#计划模式
def planMode():
    print("ACTION: 计划模式")
    mouseClick(AIRPORT_2_CLICK_BOX,0.8,1)
    mouseClick(PLAN_MODE_CLICK_BOX,1,1.5)
    mouseClick(PLAN_POINT1_CLICK_BOX,0.8,1)
    mouseDrag(MAP_DRAG_UP_BOX,0,1,500,0.002,1)
    mouseClick(PLAN_POINT2_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_POINT3_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_START_CLICK_BOX,0,0)
    
#补给休息队
def supplyRest():
    print("ACTION: 补给Zas")
    mouseClick(AIRPORT_3_CLICK_BOX,1.5,2)
    mouseClick(AIRPORT_3_CLICK_BOX,2,3)
    mouseClick(SUPPLY_CLICK_BOX,2,3)
    
#撤退休息队
def withdraw():
    print("ACTION: 撤退Zas")
    mouseClick(AIRPORT_3_CLICK_BOX,1.5,2)
    mouseClick(WITHDRAW_STEP1_CLICK_BOX,2,3)
    mouseClick(WITHDRAW_STEP2_CLICK_BOX,2,2)

#重启作战
def restartCombat():
    print("ACTION: 重启作战")
    mouseClick(RESTART_STEP1_CLICK_BOX,1,1.5)
    mouseClick(RESTART_STEP2_CLICK_BOX,4.5,5)

#强化（拆解）
def gotoPowerup():  
    print("ACTION: 拆解装备") 
    mouseClick(GOTO_POWERUP_CLICK_BOX,4,5)
    gotoFactory()
    mouseClick(CHOOSE_RETIRE_CLICK_BOX,1,2)
    mouseClick(CHOOSE_EQUIPMENT_CLICK_BOX,1,2)
    mouseClick(CHOOSE_ORDER_CLICK_BOX,1,2)
    for i in range(10):
        mouseClick(EQUIPMENT_1_CLICK_BOX,0.2,0.3)#选六个
        mouseClick(EQUIPMENT_2_CLICK_BOX,0.2,0.3)
        mouseClick(EQUIPMENT_3_CLICK_BOX,0.2,0.3)
        mouseClick(EQUIPMENT_4_CLICK_BOX,0.2,0.3)
        mouseClick(EQUIPMENT_5_CLICK_BOX,0.2,0.3)
        mouseClick(EQUIPMENT_6_CLICK_BOX,0.2,0.3)
        mouseDrag(RETIRE_DRAG_BOX,0,1,300,0.025,1)#往上拖一行
    mouseClick(CHOOSE_FINISH_CLICK_BOX,1,2)
    mouseClick(RETIRE_CLICK_BOX,1,2)
    mouseClick(CONFIRM_RETIRE_CLICK_BOX,3,4)    

#跳转至主菜单(回主菜单收后勤)
def backToMainMenu():
    print("ACTION: 跳转至主菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseClick(NAVIGATE_MAIN_MENU_CLICK_BOX,5,6)

#跳转至工厂
def gotoFactory():
    print("ACTION: 跳转至工厂")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseClick(NAVIGATE_FACTORY_CLICK_BOX,5,6)

#跳转至战斗菜单(暂时不用)
def backToCombatMenu():
    print("ACTION: 跳转至战斗菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseDrag(NAVIGATE_BAR_DRAG_BOX,3,1,150,0.01,1)
    mouseClick(NAVIGATE_COMBAT_CLICK_BOX,5,6)

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
    firstCombat = True#启动时会给一队单独补给并重开
    failCount = 0
    combatPause = False

    while True:
        if isInMap():
            print("STATE：8-1n地图")
            failCount = 0
            if firstCombat:
                firstCombat = False
                combatPrepare()
                continue
            changeForce()
            setTeam()
            startCombat()
            checkCount = 0
            while not isCombatStart() and checkCount < 50:#防止网络卡顿，最多等10s
                if isGotoPowerup():
                    break
                checkCount += 1
                time.sleep(0.2)
            if isGotoPowerup():
                gotoPowerup()
                backToMainMenu()
                firstCombat = True
                continue
            if checkCount >= 50:#过了10s还是卡着，启动失败，直接关闭窗口重启
                print("ERROR：作战启动超时！")
                closeGame()
                continue
            time.sleep(0.2)
            planMode()
            checkCount = 0
            while (not isPlanFinished()) and checkCount < 200:#计划开始后200s还没打完，一般是出问题了（比方说卡了一下导致流程漏了）
                checkCount += 1
                time.sleep(1)
            if checkCount >= 200:#过了200s还没结束，直接关闭窗口重启
                print("ERROR：战斗超时！")
                closeGame()
                continue
            time.sleep(0.2)
            supplyRest()
            withdraw()
            restartCombat()
            combatCount += 1
            currentTime = datetime.datetime.now()
            runtime = currentTime - startTime
            print('> 已运行：',runtime,'  8-1n轮次：',combatCount)                
        elif is8_1n():
            print("STATE： 8-1n界面")
            start8_1n()
            failCount = 0
        elif isGotoPowerup():
            print("STATE： 强化提醒界面")
            gotoPowerup()
            backToMainMenu()
        elif isCombatMenu():
            print("STATE： 战斗菜单")
            combatMenuTo8_1n()
            failCount = 0
        elif isCombatPause():
            print("STATE： 战斗中断提醒界面")
            failCount = 0
            closeTip()
        elif isReturnCombat():
            print("STATE： 返回作战界面")
            failCount = 0
            mainMenuBackToCombat()
            restartCombat()
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
            failCount = 0
            startGame()
            continue
        else:#不知道在哪
            print("ERROR： 当前状态未知!")
            if findNavigate():
                print("STATE：找到导航条")
                backToMainMenu()
                failCount = 0
            else: 
                failCount += 1
                if failCount == 5:  
                    print(">>> ",datetime.datetime.now()," 无法确定当前状态,关闭重启！")
                    closeGame()
                else:
                    time.sleep(5)
                
            
            
