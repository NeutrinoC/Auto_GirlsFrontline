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
MAIN_MENU_IMAGE_BOX = [0.65,0.52,0.75,0.60]#主界面判断区域                       
L_SUPPORT_IMAGE_BOX = [0.05,0.30,0.18,0.39]#后勤完成界面判断区域                
COMBAT_MENU_IMAGE_BOX = [0.05,0.70,0.12,0.80]#战斗菜单界面判断区域          
CHOOSE_8_1N_IMAGE_BOX = [0.50,0.32,0.60,0.40]#8-1n菜单界面判断区域                        
MAP_8_1N_IMAGE_BOX = [0.82,0.80,0.95,0.88]#进入8-1n判断区域
SET_TEAM_IMAGE_BOX = [0.85,0.75,0.92,0.78]#队伍放置判断区域 
FORM_TEAM_IMAGE_BOX = [0.28,0.38,0.38,0.50]#队伍编成判断区域                              
CHANGE_MEMBER_IMAGE_BOX = [0.90,0.30,0.95,0.40]#人员选择判断区域   
COMBAT_START_IMAGE_BOX = [0.80,0.82,0.97,0.88]#开启作战判断区域  
PLAN_FINISH_IMAGE_BOX = [0.80,0.82,0.97,0.88]#计划完成判断区域  
TEAM_INFO_IMAGE_BOX = [0.85,0.67,0.94,0.71]#队伍详情页判断区域                            
GOTO_POWERUP_IMAGE_BOX = [0.58,0.60,0.65,0.65]#提醒强化判断区域               
NAVIGATE_IMAGE_BOX = [0.15,0.10,0.20,0.15]#导航条判断区域       
DESKTOP_IMAGE_BOX = [0.10,0.20,0.22,0.35]#模拟器桌面判断区域         
COMBAT_PAUSE_IMAGE_BOX = [0.45,0.62,0.55,0.67]#战斗终止提示判断区域            
RETURN_COMBAT_IMAGE_BOX = [0.75,0.63,0.90,0.70]#回到作战界面判断区域    

#=================点击拖动区域=================#

#从主菜单进入作战选择界面
COMBAT_CLICK_BOX = [0.65,0.50,0.75,0.58]#在主菜单点击战斗
BACK_TO_COMBAT_CLICK_BOX = [0.75,0.63,0.90,0.70]#主菜单回到战斗
BACK_TO_COMBAT_AFTER_CLICK_BOX = [0.49,0.10,0.51,0.15]#战斗结束后随机点击完成结算

#从作战选择界面进入8-1n界面
COMBAT_MISSION_CLICK_BOX = [0.05,0.20,0.10,0.24]#点击作战任务
CHAPTER_DRAG_BOX = [0.16,0.75,0.22,0.80]#向上拖章节选择条
CHAPTER_8_CLICK_BOX = [0.15,0.22,0.20,0.28]#选择第8章
NIGHT_CLICK_BOX = [0.92,0.24,0.97,0.28]#选择夜战

#开始8-1n
EPISODE_1_CLICK_BOX = [0.40,0.35,0.80,0.40]#选择第1节
ENTER_COMBAT_CLICK_BOX = [0.72,0.70,0.80,0.75]#进入作战
END_COMBAT_STEP1_CLICK_BOX = [0.72,0.62,0.80,0.66]#终止作战
END_COMBAT_STEP2_CLICK_BOX = [0.52,0.60,0.60,0.65]#确认终止作战

#缩小地图，拖动地图
MAP_SCALE_BOX = [0.10,0.20,0.20,0.25]
MAP_DRAG_BOX = [0.10,0.20,0.20,0.25]

#机场位置点
AIRPORT_1_CLICK_BOX = [0.33,0.60,0.36,0.63]#下机场
AIRPORT_2_CLICK_BOX = [0.36,0.33,0.38,0.35]#上机场

#更换打手
CHANGE_FORCE_STEP1_CLICK_BOX = [0.17,0.74,0.26,0.77]#点击梯队编成
CHANGE_FORCE_STEP2_CLICK_BOX = [0.15,0.35,0.25,0.55]#点击Zas
CHANGE_FORCE_STEP3_CLICK_BOX = [0.88,0.20,0.94,0.26]#点击排序方式
CHANGE_FORCE_STEP4_CLICK_BOX = [0.72,0.63,0.78,0.68]#点击受损程度
CHANGE_FORCE_STEP5_CLICK_BOX = [0.20,0.25,0.25,0.40]#选择Zas
CHANGE_FORCE_STEP6_CLICK_BOX = [0.08,0.10,0.10,0.14]#点击返回

#放置队伍
TEAM_SET_CLICK_BOX = [0.85,0.75,0.92,0.78]

#开始作战
START_COMBAT_CLICK_BOX = [0.85,0.82,0.92,0.86]#点击开始作战

#计划模式
PLAN_MODE_CLICK_BOX = [0.04,0.77,0.10,0.79]#点击计划模式
PLAN_POINT1_CLICK_BOX = [0.32,0.42,0.34,0.44]#点击计划点1 
PLAN_POINT2_CLICK_BOX = [0.33,0.52,0.34,0.54]#点击计划点2
PLAN_POINT3_CLICK_BOX = [0.39,0.54,0.40,0.56]#点击计划点3
PLAN_START_CLICK_BOX = [0.88,0.82,0.98,0.85]#点击执行计划

#补给Zas
SUPPLY_CLICK_BOX = [0.85,0.68,0.94,0.70]#点击补给

#撤退Zas
WITHDRAW_STEP1_CLICK_BOX = [0.72,0.76,0.78,0.78]#点击撤退
WITHDRAW_STEP2_CLICK_BOX = [0.55,0.61,0.62,0.64]#确认撤退

#重启作战
RESTART_STEP1_CLICK_BOX = [0.22,0.09,0.26,0.14]#点击终止作战
RESTART_STEP2_CLICK_BOX = [0.34,0.61,0.43,0.63]#点击重新作战

#强化（拆解）
GOTO_POWERUP_CLICK_BOX = [0.58,0.60,0.65,0.65]#前往强化界面
CHOOSE_RETIRE_CLICK_BOX = [0.06,0.46,0.12,0.50]#选择回收拆解选项
CHOOSE_EQUIPMENT_CLICK_BOX = [0.40,0.26,0.45,0.30]#选择拆解装备
CHOOSE_ORDER_CLICK_BOX = [0.87,0.52,0.93,0.55]#选择升序
EQUIPMENT_1_CLICK_BOX = [0.02,0.3,0.07,0.36]#第一行第一件装备
EQUIPMENT_2_CLICK_BOX = [0.21,0.3,0.25,0.36]#第一行第二件装备 
EQUIPMENT_3_CLICK_BOX = [0.33,0.3,0.37,0.36]#第一行第三件装备
EQUIPMENT_4_CLICK_BOX = [0.45,0.3,0.50,0.36]#第一行第四件装备 
EQUIPMENT_5_CLICK_BOX = [0.58,0.3,0.63,0.36]#第一行第五件装备
EQUIPMENT_6_CLICK_BOX = [0.73,0.3,0.76,0.36]#第一行第六件装备
RETIRE_DRAG_BOX = [0.40,0.60,0.60,0.60]#往上拖一行
CHOOSE_FINISH_CLICK_BOX = [0.88,0.80,0.92,0.86]#完成选择
RETIRE_CLICK_BOX = [0.84,0.77,0.90,0.80]#点击拆解
CONFIRM_RETIRE_CLICK_BOX = [0.54,0.74,0.64,0.78]#确认拆解高星级

#跳至主菜单/战斗菜单/工厂菜单
NAVIGATE_BAR_CLICK_BOX = [0.15,0.10,0.18,0.15]#打开导航条
NAVIGATE_BAR_DRAG_BOX = [0.10,0.28,0.17,0.32]#向右拖导航条
NAVIGATE_COMBAT_CLICK_BOX = [0.10,0.28,0.12,0.32]#跳转至作战菜单
NAVIGATE_FACTORY_CLICK_BOX = [0.32,0.28,0.34,0.32]#跳转至工厂菜单
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
def isNavigate():
    initImage = cv2.imread(IMAGE_PATH+"navigate.png")
    capImage  = getImage(NAVIGATE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#在队伍放置界面
def isSetTeam():
    initImage = cv2.imread(IMAGE_PATH+"set_team.png")
    capImage  = getImage(SET_TEAM_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#在队伍编成界面
def isFormTeam():
    initImage = cv2.imread(IMAGE_PATH+"form_team.png")
    capImage  = getImage(FORM_TEAM_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#在人员选择界面
def isChangeMember():
    initImage = cv2.imread(IMAGE_PATH+"change_member.png")
    capImage  = getImage(CHANGE_MEMBER_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
  
#在队伍详情界面
def isTeamInfo():
    initImage = cv2.imread(IMAGE_PATH+"team_info.png")
    capImage  = getImage(TEAM_INFO_IMAGE_BOX)
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
    mouseDrag(CHAPTER_DRAG_BOX,0,-1,3,400,0.001,0.8)
    mouseClick(CHAPTER_8_CLICK_BOX,1,2)
    mouseClick(NIGHT_CLICK_BOX,1,2)

#开始8-1n
def start8_1n():
    print("ACTION: 启动8-1n")
    mouseClick(EPISODE_1_CLICK_BOX,2,3)
    mouseClick(ENTER_COMBAT_CLICK_BOX,4,5)    

#终止8-1n
def end8_1n():
    print("ACTION: 终止8-1n")
    mouseClick(EPISODE_1_CLICK_BOX,2,3)
    mouseClick(END_COMBAT_STEP1_CLICK_BOX,2,3)  
    mouseClick(END_COMBAT_STEP2_CLICK_BOX,2,3)  

#战前准备，调整地图，补给1队
def combatPrepare():
    print("STATE: 战前整备")
    mouseClick(MAP_SCALE_BOX,0.5,0.6)
    scaleMap(MAP_SCALE_BOX,1,10)
    mouseDrag(MAP_DRAG_BOX,1,1,1,200,0.001,1)
    setTeam()
    startCombat()
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
    mouseClick(AIRPORT_1_CLICK_BOX,0,0)#点击下方机场
    checkCount = 0
    while not isSetTeam() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.4)
    mouseClick(CHANGE_FORCE_STEP1_CLICK_BOX,0,0)#点击队伍编成
    checkCount = 0
    while not isFormTeam() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.8)
    mouseClick(CHANGE_FORCE_STEP2_CLICK_BOX,0,0)#点击打手
    checkCount = 0
    while not isChangeMember() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.4)
    mouseClick(CHANGE_FORCE_STEP3_CLICK_BOX,0.5,1)#点击排序方式
    mouseClick(CHANGE_FORCE_STEP4_CLICK_BOX,1,1.5)#点击受损程度
    mouseClick(CHANGE_FORCE_STEP5_CLICK_BOX,0,0)#点击二号打手
    checkCount = 0
    while not isFormTeam() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.8)
    mouseClick(CHANGE_FORCE_STEP6_CLICK_BOX,0,0)#点击返回
    checkCount = 0
    while not isInMap() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.4)
    return True

#放置队伍
def setTeam():
    print("ACTION: 放置队伍")
    mouseClick(AIRPORT_1_CLICK_BOX,0,0)#点击下方机场
    checkCount = 0
    while not isSetTeam() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    mouseClick(TEAM_SET_CLICK_BOX,0,0)#点击放置队伍
    checkCount = 0
    while not isInMap() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    mouseClick(AIRPORT_2_CLICK_BOX,0,0)#点击上方机场
    checkCount = 0
    while not isSetTeam() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    mouseClick(TEAM_SET_CLICK_BOX,0,0)#点击放置队伍
    checkCount = 0
    while not isInMap() and checkCount < 20:
        wait(0.3,0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    return True

#开始作战
def startCombat():
    print("ACTION: 开始作战")
    mouseClick(START_COMBAT_CLICK_BOX,0,0) 
    checkCount = 0
    while not isCombatStart() and checkCount < 20:
        wait(0.4,0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(2)
    return True

#计划模式
def planMode():
    print("ACTION: 计划模式")
    mouseClick(AIRPORT_2_CLICK_BOX,0.8,1)
    mouseClick(PLAN_MODE_CLICK_BOX,1,1.5)
    mouseClick(PLAN_POINT1_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_POINT2_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_POINT3_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_START_CLICK_BOX,0,0)
    
#补给休息队
def supplyRest():
    print("ACTION: 补给Zas")
    mouseClick(AIRPORT_1_CLICK_BOX,1,1)
    mouseClick(AIRPORT_1_CLICK_BOX,0,0)
    checkCount = 0
    while not isTeamInfo() and checkCount < 20:
        wait(0.4,0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    mouseClick(SUPPLY_CLICK_BOX,0,0)
    checkCount = 0
    while not isPlanFinished(False) and checkCount < 20:
        wait(0.4,0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.5)
    return True
    
#撤退休息队
def withdraw():
    print("ACTION: 撤退Zas")
    mouseClick(AIRPORT_1_CLICK_BOX,0,0)
    checkCount = 0
    while not isTeamInfo() and checkCount < 20:
        time.sleep(0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    mouseClick(WITHDRAW_STEP1_CLICK_BOX,2,2)
    mouseClick(WITHDRAW_STEP2_CLICK_BOX,0,0)
    checkCount = 0
    while not isPlanFinished(False) and checkCount < 20:
        wait(0.4,0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.5)
    return True

#重启作战
def restartCombat():
    print("ACTION: 重启作战")
    mouseClick(RESTART_STEP1_CLICK_BOX,1,1.5)
    mouseClick(RESTART_STEP2_CLICK_BOX,0,0)
    checkCount = 0
    while not isInMap() and checkCount < 20:
        wait(0.4,0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(1)
    return True

#强化（拆解）
def gotoPowerup():  
    print("ACTION: 拆解装备") 
    mouseClick(GOTO_POWERUP_CLICK_BOX,6,6)
    gotoFactory()
    mouseClick(CHOOSE_RETIRE_CLICK_BOX,1,2)
    mouseClick(CHOOSE_EQUIPMENT_CLICK_BOX,1,2)
    mouseClick(CHOOSE_ORDER_CLICK_BOX,1,2)
    for i in range(15):
        mouseClick(EQUIPMENT_1_CLICK_BOX,0.25,0.3)#选六个
        mouseClick(EQUIPMENT_2_CLICK_BOX,0.25,0.3)
        mouseClick(EQUIPMENT_3_CLICK_BOX,0.25,0.3)
        mouseClick(EQUIPMENT_4_CLICK_BOX,0.25,0.3)
        mouseClick(EQUIPMENT_5_CLICK_BOX,0.25,0.3)
        mouseClick(EQUIPMENT_6_CLICK_BOX,0.25,0.3)
        mouseDrag(RETIRE_DRAG_BOX,0,-1,1,325,0.005,1)#往上拖一行
    mouseClick(CHOOSE_FINISH_CLICK_BOX,1,2)
    mouseClick(RETIRE_CLICK_BOX,1,2)
    mouseClick(CONFIRM_RETIRE_CLICK_BOX,0.5,1)    
    mouseClick(CONFIRM_RETIRE_CLICK_BOX,3.5,4)

#跳转至主菜单(回主菜单收后勤)
def backToMainMenu():
    print("ACTION: 跳转至主菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseClick(NAVIGATE_MAIN_MENU_CLICK_BOX,5,6)

#跳转至工厂
def gotoFactory():
    print("ACTION: 跳转至工厂")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseClick(NAVIGATE_FACTORY_CLICK_BOX,6,6)

#跳转至战斗菜单(暂时不用)
def backToCombatMenu():
    print("ACTION: 跳转至战斗菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
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
            print("STATE：进入地图")
            failCount = 0
            if firstCombat:
                firstCombat = False
                combatPrepare()
                continue
            if not changeForce():
                print("ERROR：更换打手失败")
                closeGame()
                continue                
            if not setTeam():
                print("ERROR：队伍放置失败")
                closeGame()
                continue
            if not startCombat():
                print("ERROR：战役启动失败")
                continue
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
            if not supplyRest():
                print("ERROR：补给失败")
                closeGame()
                continue
            if not withdraw():
                print("ERROR：撤退失败")
                closeGame()
                continue
            if not restartCombat():
                print("ERROR：作战重启失败")
                closeGame()
                continue
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
            firstCombat = True
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
            mainMenuToCombatMenu()
            combatMenuTo8_1n()
            end8_1n()
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
            failCount = 0
            startGame()
            continue
        else:#不知道在哪
            print("ERROR： 当前状态未知!")
            failCount += 1
            if failCount == 4:
                mouseClick([0.3,0.45,0.4,0.55],1,1)
            if failCount >= 5:  
                print(">>> ",datetime.datetime.now()," 无法确定当前状态,关闭重启！")
                closeGame()
            else:
                time.sleep(5)
                
            
            
