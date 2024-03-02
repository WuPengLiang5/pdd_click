from time import sleep
import pyautogui
from PIL import ImageGrab, Image
import pyscreeze
import cv2
import os
import numpy as np
import time
import win32api
import win32con

def findImageClick(target_name,output_text=None,output_error=None):
    isExist,tagCenterX,tagCenterY = findImage(target_name,output_text=output_text,output_error=output_error)
    if(isExist):
        #左键点击屏幕上的这个位置
        pyautogui.click(tagCenterX,tagCenterY,button='left',duration=1)

def findImage(target_name,temp_name='my_screenshot.png',output_text=None,output_error=None):
    #拼接路径
    target_path = os.path.join(r'image\target',target_name)
    temp_path = os.path.join(r'image\temp',temp_name)
    
    # 屏幕缩放系数 mac缩放是2 windows一般是1
    screenScale=1

    #事先读取按钮截图
    target= cv2.imread(target_path,cv2.IMREAD_GRAYSCALE)
    # 先截图
    screenshot=pyscreeze.screenshot()
    screenshot.save(temp_path)
    # 读取图片 灰色会快
    temp = cv2.imread(temp_path,cv2.IMREAD_GRAYSCALE)

    theight, twidth = target.shape[:2]
    tempheight, tempwidth = temp.shape[:2]
    #print("目标图宽高："+str(twidth)+"-"+str(theight))
    #print("模板图宽高："+str(tempwidth)+"-"+str(tempheight))
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp=cv2.resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
    stempheight, stempwidth = scaleTemp.shape[:2]
    #print("缩放后模板图宽高："+str(stempwidth)+"-"+str(stempheight))
    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    isExist = False
    if(max_val>=0.9):
        # 计算出中心点
        top_left = max_loc
        bottom_right = (top_left[0] + twidth, top_left[1] + theight)
        tagHalfW=int(twidth/2)
        tagHalfH=int(theight/2)
        tagCenterX=top_left[0]+tagHalfW
        tagCenterY=top_left[1]+tagHalfH
        if output_text:
            print("{},位置为{}，{}".format(output_text,tagCenterX,tagCenterY))
        else:
            print("找到了{}，位置为{},{}".format(target_name,tagCenterX,tagCenterY))
        isExist = True
        return isExist,tagCenterX,tagCenterY
    else:
        if output_error:
            print(output_error)
        else:
            print ("没找到{}".format(target_name))
        return isExist,-1,-1
    
def findImages(target_name,temp_name='my_screenshot.png'):
    #拼接路径
    target_path = os.path.join(r'image\target',target_name)
    temp_path = os.path.join(r'image\temp',temp_name)
    
    # 屏幕缩放系数 mac缩放是2 windows一般是1
    screenScale=1

    #事先读取按钮截图
    target= cv2.imread(target_path,cv2.IMREAD_GRAYSCALE)
    # 先截图
    screenshot=pyscreeze.screenshot()
    screenshot.save(temp_path)
    # 读取图片 灰色会快
    temp = cv2.imread(temp_path)
    temp_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)


    theight, twidth = target.shape[:2]
    tempheight, tempwidth = temp.shape[:2]
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp=cv2.resize(temp_gray, (int(tempwidth / screenScale), int(tempheight / screenScale)))
    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    # 取匹配程度大于%80的坐标
    loc = np.where(res >= threshold)
    #np.where返回的坐标值(x,y)是(h,w)，注意h,w的顺序
    result = []
    for pt in zip(*loc[::-1]):
        top_left = pt
        tagHalfW=int(twidth/2)
        tagHalfH=int(theight/2)
        tagCenterX=top_left[0]+tagHalfW
        tagCenterY=top_left[1]+tagHalfH
        bottom_right = (pt[0] + twidth, pt[1] + theight)
        #pyautogui.moveTo(tagCenterX,tagCenterY,duration=1)
        #print(tagCenterX,tagCenterY)
        temp = (tagCenterX,tagCenterY)
        result.append(temp)

    return result

def getHour():
    now = time.localtime()
    return now.tm_hour

# 读取注册表找到微信的安装路径
def getWxInstallPath():
    try:
        # 注册表打开
        # RegOpenKey(key, subKey , reserved , sam)
        # key: HKEY_CLASSES_ROOT HKEY_CURRENT_USER HEKY_LOCAL_MACHINE HKEY_USERS HKEY_CURRENT_CONFIG
        # subkey: 要打开的子项
        # reserved: 必须为0
        # sam: 对打开的子项进行的操作,包括win32con.KEY_ALL_ACCESS、win32con.KEY_READ、win32con.KEY_WRITE等
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, "SOFTWARE\Tencent\WeChat", 0, win32con.KEY_ALL_ACCESS) 
        # 这里的key表示键值，后面是具体的键名，读取出来是个tuple
        value = win32api.RegQueryValueEx(key, "InstallPath")[0]
        # 用完之后记得关闭
        win32api.RegCloseKey(key)
        # 微信的路径
        value += "\\" + "WeChat.exe"
        return value
    except Exception as ex:
        logWriter(str(ex))

# 检查微信进程是否打开
def check_process(process_name):
    try:
        # 通过命令行查询正在运行的进程列表
        result = subprocess.check_output(['tasklist'],shell=True)
        
        if process_name in str(result).lower():
            return True
        else:
            return False
    
    except Exception as e:
        print("Error occurred while checking the process status.")
        print(e)
        return None

def test():
    print("测试成功！")

if __name__ == '__main__':
    #findImageClick("wangyiyoudao.png",'my_screenshot.png')
 
    hour=getHour()
    print(str((hour+1)%24)+'.png')
