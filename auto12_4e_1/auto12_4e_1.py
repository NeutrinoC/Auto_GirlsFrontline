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
FIRST_LOGIN_IMAGE_BOX = [0.60,0.58,0.75,0.65]#每日第一次登录时那个确认窗口判断区域
MAIN_MENU_IMAGE_BOX = [0.65,0.50,0.75,0.58]#主界面判断区域                       
L_SUPPORT_IMAGE_BOX = [0.05,0.30,0.18,0.39]#后勤完成界面判断区域                
COMBAT_MENU_IMAGE_BOX = [0.05,0.70,0.12,0.80]#战斗菜单界面判断区域         
CHOOSE_12_4e_IMAGE_BOX = [0.52,0.71,0.60,0.74]#12-4e界面判断区域                          
MAP_12_4e_IMAGE_BOX = [0.82,0.82,0.95,0.88]#12-4e地图判断区域   
SET_TEAM_IMAGE_BOX = [0.85,0.75,0.92,0.78]#队伍放置判断区域 
SET_WE_TEAM_IMAGE_BOX = [0.12,0.28,0.20,0.32]#重装队伍队伍放置判断区域      
COMBAT_START_IMAGE_BOX = [0.82,0.82,0.95,0.88]#战役开始判断区域    
TEAM_INFO_IMAGE_BOX = [0.85,0.67,0.94,0.71]#队伍详情页判断区域                    
COMBAT_FINISH_IMAGE_BOX = [0.05,0.19,0.15,0.23]#战役完成判断区域   
GOTO_POWERUP_IMAGE_BOX = [0.58,0.60,0.68,0.64]#提醒强化判断区域               
NAVIGATE_IMAGE_BOX = [0.15,0.10,0.20,0.15]#导航条判断区域       
DESKTOP_IMAGE_BOX = [0.10,0.20,0.22,0.35]#模拟器桌面判断区域         
COMBAT_PAUSE_IMAGE_BOX = [0.45,0.62,0.55,0.67]#战斗终止提示判断区域            
RETURN_COMBAT_IMAGE_BOX = [0.75,0.65,0.90,0.68]#回到作战界面判断区域    


#=================点击拖动区域=================#

#从主菜单进入作战选择界面
COMBAT_CLICK_BOX =  [0.65,0.50,0.75,0.58]#在主菜单点击战斗（无作战进行中情况）
#[0.65,0.58,0.75,0.63]
#[0.65,0.50,0.75,0.60]
COMBAT_BREAK_CLICK_BOX = [0.65,0.50,0.75,0.58]#在主菜单点击战斗（作战中断情况）

#从作战选择界面进入12-4e界面
COMBAT_MISSION_CLICK_BOX =  [0.05,0.28,0.10,0.32]#点击作战任务
#[0.05,0.20,0.10,0.24]
#[0.05,0.28,0.10,0.32]
CHAPTER_DRAG_BOX = [0.16,0.60,0.20,0.65]#向上拖章节选择条
CHAPTER_12_CLICK_BOX = [0.16,0.52,0.20,0.57]#选择第12章
EMERGENCY_CLICK_BOX = [0.84,0.24,0.87,0.28]#选择紧急难度
EPISODE_DRAG_BOX = [0.40,0.35,0.80,0.40]#向下拖小节选择条

#开始/终止12-4e
EPISODE_4_CLICK_BOX = [0.50,0.70,0.60,0.75]#选择第4节
ENTER_COMBAT_CLICK_BOX = [0.72,0.70,0.80,0.75]#进入作战
END_COMBAT_STEP1_CLICK_BOX = [0.72,0.62,0.80,0.66]#终止作战
END_COMBAT_STEP2_CLICK_BOX = [0.52,0.60,0.60,0.65]#确认终止作战

#地图缩放、拖动区
MAP_SCALE_BOX = [0.20,0.20,0.30,0.25]
MAP_DRAG_BOX =[0.20,0.20,0.30,0.25]

#队伍放置点
AIRPORT_CLICK_BOX = [0.475,0.65,0.485,0.67]#重型机场
COMMAND_CLICK_BOX = [0.445,0.36,0.455,0.38]#指挥部

#放置队伍
TEAM_SHIFT_CLICK_BOX = [0.42,0.20,0.48,0.24]#切换成普通梯队
TEAM_SET_CLICK_BOX = [0.85,0.75,0.92,0.78]#放置梯队

#扛伤位（第五个）修复
REPAIR_INTERVAL =  20#隔多少轮修一次
REPAIR_STEP1_CLICK_BOX = [0.70,0.30,0.76,0.50]#点击五号位        
REPAIR_STEP2_CLICK_BOX = [0.69,0.65,0.75,0.69]#确定修复          
REPAIR_STEP3_CLICK_BOX = [0.85,0.75,0.91,0.79]#退出2队界面         

#开始作战
START_COMBAT_CLICK_BOX = [0.85,0.82,0.92,0.86]#点击开始作战

#补给队伍
SUPPLY_STEP1_CLICK_BOX = [0.85,0.68,0.94,0.70]#点击补给
SUPPLY_STEP2_CLICK_BOX = [0.20,0.20,0.30,0.25]#取消选中

#计划模式
PLAN_MODE_CLICK_BOX = [0.04,0.77,0.10,0.79]#点击计划模式
PLAN_POINT1_CLICK_BOX = [0.545,0.485,0.555,0.495]#点击计划点1 
PLAN_POINT2_CLICK_BOX = [0.61,0.485,0.62,0.495]#点击计划点2
PLAN_START_CLICK_BOX = [0.88,0.82,0.98,0.85]#点击执行计划

#战役结算
COMBAT_END_CLICK_BOX = [0.48,0.08,0.52,0.10]#战役结算     
                
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

#强化
CHOOSE_POWERUP_CHARACTER_CLICK_BOX = [0.20,0.40,0.3,0.50]#选择被强化人形
FIRST_CHARACTER_CLICK_BOX = [0.10,0.3,0.14,0.36]#选择第一只人形 
CHOOSE_EXP_CHARACTER_CLICK_BOX = [0.40,0.32,0.43,0.36]#选择狗粮
AUTO_CHOOSE_CLICK_BOX = [0.88,0.66,0.94,0.72]#智能选择
CHOOSE_CONFIRM_CLICK_BOX = [0.88,0.66,0.94,0.72]#完成选择
POWERUP_CLICK_BOX = [0.86,0.75,0.92,0.78]#点击强化
POWERUP_FINISH_CLICK_BOX = [0.46,0.64,0.54,0.66]#完成强化

#跳至主菜单/战斗菜单/工厂菜单
NAVIGATE_BAR_CLICK_BOX = [0.15,0.10,0.18,0.15]#打开导航条
NAVIGATE_BAR_DRAG_BOX = [0.10,0.28,0.17,0.32]#向右拖导航条
NAVIGATE_COMBAT_CLICK_BOX = [0.10,0.28,0.12,0.32]#跳转至作战菜单
NAVIGATE_FACTORY_CLICK_BOX = [0.38,0.28,0.40,0.32]#跳转至工厂菜单
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

#每日第一次登录的确认
CHECK_INFORMATION_CLICK_BOX = [0.26,0.61,0.27,0.63]#勾选今日不在弹出
CONFIRM_INFORMATION_CLICK_BOX = [0.65,0.60,0.72,0.63]#点击确认

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
    
#=================状态判断区域=================#

#判断是否战役结束
def isCombatFinished():
    initImage = cv2.imread(IMAGE_PATH+"combat_finish.png")
    capImage  = getImage(COMBAT_FINISH_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
         
#判断是否进入了12-4e地图
def isInMap():
    initImage = cv2.imread(IMAGE_PATH+"map.png")
    capImage  = getImage(MAP_12_4e_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是提醒强化界面
def isGotoPowerup():
    initImage = cv2.imread(IMAGE_PATH+"goto_powerup.png")
    capImage  = getImage(GOTO_POWERUP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是可以选择12-4e的界面
def is12_4e():
    initImage = cv2.imread(IMAGE_PATH+"_12_4e.png")
    capImage  = getImage(CHOOSE_12_4e_IMAGE_BOX)
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
    
#判断是否是每日第一次登录的确认界面
def isFirstLogin():
    initImage = cv2.imread(IMAGE_PATH+"first_login.png")
    capImage  = getImage(FIRST_LOGIN_IMAGE_BOX)
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

#判断战斗是否正常开始
def isCombatStart():
    initImage = cv2.imread(IMAGE_PATH+"combat_start.png")
    capImage  = getImage(COMBAT_START_IMAGE_BOX)
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

#在布置重装的界面
def isSetWETeam():
    initImage = cv2.imread(IMAGE_PATH+"set_we_team.png")
    capImage  = getImage(SET_WE_TEAM_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#在队伍详情界面
def isTeamInfo():
    initImage = cv2.imread(IMAGE_PATH+"team_info.png")
    capImage  = getImage(TEAM_INFO_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)


#=================动作区域=================#

#从主菜单进入作战菜单（无战斗进行中情况）
def mainMenuToCombatMenu():
    print("ACTION: 前往作战菜单")
    mouseClick(COMBAT_CLICK_BOX,5,6)  

#从主菜单进入作战菜单（战斗中断情况）
def mainMenuToCombatMenu_combatOn():
    print("ACTION: 前往作战菜单-战斗中断")
    mouseClick(COMBAT_BREAK_CLICK_BOX,5,6)  
    
#从作战菜单进入12-4e界面
def combatMenuTo12_4e():
    print("ACTION: 前往12-4e选择界面")
    mouseClick(COMBAT_MISSION_CLICK_BOX,1,2)
    mouseDrag(CHAPTER_DRAG_BOX,0,-1,3,400,0.001,1)
    mouseClick(CHAPTER_12_CLICK_BOX,1,2)
    mouseClick(EMERGENCY_CLICK_BOX,1,2)
    mouseDrag(EPISODE_DRAG_BOX,0,1,1,300,0.001,1)

#开始12-4e
def start12_4e():
    print("ACTION: 启动12-4e")
    mouseClick(EPISODE_4_CLICK_BOX,2,3)
    mouseClick(ENTER_COMBAT_CLICK_BOX,4,5)    

#终止12-4e
def end12_4e():
    print("ACTION: 终止12-4e")
    mouseClick(EPISODE_4_CLICK_BOX,2,3)
    mouseClick(END_COMBAT_STEP1_CLICK_BOX,2,3)  
    mouseClick(END_COMBAT_STEP2_CLICK_BOX,2,3)  

#调整地图
def adjustMap(tiny = False):
    print("STATE：调整地图")
    if tiny:
        scaleMap(MAP_SCALE_BOX,1,1)
        mouseDrag(MAP_DRAG_BOX,1,1,1,400,0.001,1)
    else:
        scaleMap(MAP_SCALE_BOX,1,8)
        mouseDrag(MAP_DRAG_BOX,1,1,1,400,0.001,1)

#放置队伍
def setTeam():
    print("ACTION: 放置队伍")
    mouseClick(COMMAND_CLICK_BOX,0,0)#点击指挥部
    checkCount = 0
    while not isSetTeam() and checkCount < 20:
        time.sleep(0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    mouseClick(TEAM_SET_CLICK_BOX,0,0)#点击放置
    checkCount = 0
    while not isInMap() and checkCount < 20:
        time.sleep(0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    mouseClick(AIRPORT_CLICK_BOX,0,0)#点击机场
    checkCount = 0
    while not (isSetTeam() or isSetWETeam()) and checkCount < 20:
        time.sleep(0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    if isSetWETeam():
        mouseClick(TEAM_SHIFT_CLICK_BOX,0,0)#切换普通队伍
    checkCount = 0
    while not isSetTeam() and checkCount < 10:
        time.sleep(0.4)
        checkCount += 1
    if checkCount >= 20:
        return False    
    mouseClick(TEAM_SET_CLICK_BOX,0,0)#点击放置
    checkCount = 0
    while not isInMap() and checkCount < 20:
        time.sleep(0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    
    return True

#扛伤位修复
def repair():
    print("ACTION: 修复")
    mouseClick(AIRPORT_CLICK_BOX,2,3)
    mouseClick(REPAIR_STEP1_CLICK_BOX,1,2)
    mouseClick(REPAIR_STEP2_CLICK_BOX,1,2)
    mouseClick(REPAIR_STEP3_CLICK_BOX,2,3)

#开始作战
def startCombat():
    print("ACTION: 开始作战")
    mouseClick(START_COMBAT_CLICK_BOX,0,0)#点击开始作战
    checkCount = 0
    while not isCombatStart() and checkCount < 20:
        time.sleep(0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(2)
    return True

#补给打捞队伍
def supplyTeam():
    print("ACTION: 补给打捞队")
    mouseClick(AIRPORT_CLICK_BOX,1.5,2)#点击机场队
    mouseClick(AIRPORT_CLICK_BOX,0,0)
    checkCount = 0
    while not isTeamInfo() and checkCount < 20:
        time.sleep(0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    mouseClick(SUPPLY_STEP1_CLICK_BOX,0,0)#点击补给
    checkCount = 0
    while not isCombatStart() and checkCount < 20:
        time.sleep(0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.5)
    return True
    
#计划模式
def planMode():
    print("ACTION: 计划模式")
    mouseClick(PLAN_MODE_CLICK_BOX,1,2)
    mouseClick(PLAN_POINT1_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_POINT2_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_START_CLICK_BOX,0,0)

#战役结算
def endCombat():
    print("ACTION: 战役结算")
    checkCount = 0
    while not is12_4e() and checkCount < 100:
        mouseClick(COMBAT_END_CLICK_BOX,0.2,0.3)
        checkCount += 1
    if checkCount >= 100:
        return False
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

#强化
def gotoPowerup(): 
    print("ACTION: 强化人形") 
    mouseClick(GOTO_POWERUP_CLICK_BOX,5,6)
    mouseClick(CHOOSE_POWERUP_CHARACTER_CLICK_BOX,1,2)
    mouseClick(FIRST_CHARACTER_CLICK_BOX,1,2)
    mouseClick(CHOOSE_EXP_CHARACTER_CLICK_BOX,2,3)
    mouseClick(AUTO_CHOOSE_CLICK_BOX,1,2)
    mouseClick(CHOOSE_CONFIRM_CLICK_BOX,1,2)
    mouseClick(POWERUP_CLICK_BOX,3,4)
    mouseClick(POWERUP_FINISH_CLICK_BOX,3,4)

#跳转至主菜单(回主菜单收后勤)
def backToMainMenu():
    print("ACTION: 跳转至主菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseClick(NAVIGATE_MAIN_MENU_CLICK_BOX,5,6)

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
    print("ACTION: 关闭作战断开提示")
    mouseClick(CLOSE_TIP_CLICK_BOX,5,5)

#关闭游戏
def closeGame():
    print("ACTION: 关闭游戏")
    mouseClick(CLOSE_GAME_CLICK_BOX,5,5)

#确认每日第一次登录的公告
def confirmAnnouncement():
    mouseClick(CHECK_INFORMATION_CLICK_BOX,2,2)
    mouseClick(CONFIRM_INFORMATION_CLICK_BOX,2,2)
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

    while True:
        if isInMap():
            print("STATE：已进入地图")
            failCount = 0
            if firstCombat:#初次进入地图
                firstCombat = False
                adjustMap()#大幅缩放
            else:
                adjustMap(True)#少量缩放
            if not setTeam():#放置队伍
                print("ERROR：放置队伍失败")
                closeGame()
                continue
            if combatCount % REPAIR_INTERVAL == 0:
                repair()
            if not startCombat():#开始作战
                print("ERROR：开始作战失败")
                closeGame()
                continue
            if not supplyTeam():#补给机场队  
                print("ERROR：补给失败")
                closeGame()
                continue   
            planMode()
            checkCount = 0
            while (not isCombatFinished()) and checkCount < 300:#计划开始后300s还没打完，一般是出问题了（比方说卡了一下导致流程漏了）
                checkCount += 1
                time.sleep(1)
            if checkCount >= 300:
                print("STATE：战斗超时！")
                closeGame()
                continue
            if not endCombat():#结束战役
                print("ERROR：战役结束失败")
                closeGame()
                continue
            combatCount += 1
            currentTime = datetime.datetime.now()
            runtime = currentTime - startTime
            print('> 已运行：',runtime,'  12-4e轮次：',combatCount)                
        elif isGotoPowerup():
            print("STATE： 提醒强化界面")
            #gotoPowerup()
            gotoRetire()
            backToMainMenu()
            failCount = 0
        elif is12_4e():
            print("STATE： 12-4e界面")
            start12_4e()
            failCount = 0
        elif isCombatMenu():
            print("STATE： 战斗菜单")
            combatMenuTo12_4e()
            failCount = 0
        elif isCombatPause():
            print("STATE： 战斗中断提醒界面")
            failCount = 0
            closeTip()
        elif isReturnCombat():
            print("STATE： 返回作战界面")
            failCount = 0
            mainMenuToCombatMenu_combatOn()
            combatMenuTo12_4e()
            end12_4e()
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
            print("STATE：模拟器界面")
            failCount = 0
            firstCombat = True
            startGame()
            continue
        elif isFirstLogin():
            print("STATE：公告确认")
            failCount = 0
            confirmAnnouncement()
            continue
        else:#既不是后勤结束界面也不是
            print("ERROR： 当前状态未知!")
            failCount += 1
            if failCount == 4:
                mouseClick([0.3,0.45,0.4,0.55],1,1)
            if failCount >= 5:  
                print(">>> ",datetime.datetime.now()," 无法确定当前状态,关闭重启！")
                closeGame()
            else:
                time.sleep(5)
            
            
