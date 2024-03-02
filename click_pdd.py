import my_auto_click as ac
from statistical_data import data_sheet as ds
import logger
import os
import sys
import pygetwindow as gw
import subprocess
import pyautogui
import time
import datetime

def get_current_window():
    return gw.getActiveWindow()

def getWindowByTitle(window_title):
    return gw.getWindowsWithTitle(window_title)

def findfree_use_more():
    #time.sleep(3.5)
    #进行延时，确保进入省钱月卡页面
    #设置while的超时时间，防止无限卡在这里
    start_time = time.time()
    timeout = 20 
    count_time=10
    while True:
        print("进入省钱月卡页面耗费时间{}秒。".format(10-count_time))
        isExist1,tagX1,tagY1=ac.findImage("save_money_title.png")
        if isExist1:
            break
        else:
            time.sleep(1)
            count_time=count_time-1

        if count_time<=0:
            raise Exception("进入省钱月卡失败！")

        # 如果超过了超时时间 跳出循环
        if time.time() - start_time > timeout:
            break
        
    #isExist2,tagX2,tagY2=ac.findImage("save_money_list.png")
    #先出现省钱月卡页面，后跳出弹框
    time.sleep(3.5)
    quxiao1_isExist,quxiao1_tagX,quxiao1_tagY=ac.findImage("quxiao1.png")
    if quxiao1_isExist:
        print("出现弹框！")
        pyautogui.click(quxiao1_tagX,quxiao1_tagY,duration=0.5)
    else:
        print("没有出现弹框！")
    
    #免费申请成功
    applyWin=ac.findImage("application_successful.png")
    if applyWin[0]:
       ac.findImageClick("application_successful_IKT_btn.png")
       print("申请成功！我知道了！")
    
    print("-----免费试用更多好货-----")
    window = getWindowByTitle("拼多多")[0]
    # 将最大化/最小化的窗口还原
    window.restore()
    # 将指定窗口设为活跃窗口（最小化时无法打开）
    window.activate()
    #pyautogui.moveTo(window.left+window.width/2,window.height/2)
    #print(window)
    #pyautogui.scroll(-100)
    #count 记录变化次数，超过设置次数，抛出异常
    count=0
    for _ in range(20):
        count+=1
        pyautogui.scroll(-350)
        time.sleep(0.5)  # 每次滚动后等待0.5秒，以便观察效果
        #free_use_btn.png 免费试用更多
        isExist,x,y = ac.findImage("free_use_btn.png")
        if(isExist):
            print("点击免费试用更多")
            pyautogui.click(x,y,duration=0.25)
            break;
    if count>20:
        raise Exception("免费试用更多没找到，进入失败！")
    time.sleep(1.5)
        
def improve_probability():
    print("-----提升概率-----")
    #window = getWindowByTitle("拼多多")[0]
    # 将最大化/最小化的窗口还原
    #window.restore()
    # 将指定窗口设为活跃窗口（最小化时无法打开）
    #window.activate()
    reward_list=[0,0]
    #increase_probability_btn.png 提升概率
    result=ac.findImages("increase_probability_btn.png")
    for index,item in enumerate(result):
        centerX,centerY=item
        print("第{}个‘提升概率’的位置为{}，{}".format((index+1),centerX,centerY))
        pyautogui.click(centerX,centerY,duration=0.25)
        time.sleep(3)
        #是否已经领取奖励
        hour=ac.getHour()
        isGetRewards=ac.findImage(str((hour+1)%24)+'.png')[0]
        if not isGetRewards:
            starttime = datetime.datetime.now()
            while(1):
                #get_rewards.png 领取奖励
                isExist,tagCenterX,tagCenterY = ac.findImage("get_rewards.png")
                #print(isExist,tagCenterX,tagCenterY)
                endtime = datetime.datetime.now()
                interval=(endtime - starttime).seconds
                if(isExist):
                    #print(tagCenterX,tagCenterY)
                    pyautogui.click(tagCenterX,tagCenterY,duration=1)
                    time.sleep(1)
                    #receive_now.png 立即领取
                    ac.findImageClick("receive_now.png")
                    reward_list[index]=1
                    break
                else:
                    if interval > 20:
                        print("领取奖励失败！")
                        break
        else:
            reward_list[index]=1
        for i in range(5):
            #come_back_tomorrow.png 明天再来
            res = ac.findImage("come_back_tomorrow.png")
            if res[0]:
                print("‘去完成’已完成，明天再来！")
                break
            time.sleep(1)
            print("第{}次".format(i+1))
            ac.findImageClick("to_complete.png")
            time.sleep(30)
            ac.findImageClick("back.png",output_text="'back.png'-浏览店铺30S页面的返回",output_error="没有找到'back.png'-浏览店铺30S页面的返回")
            time.sleep(2)
        ac.findImageClick("back.png",output_text="'back.png'-领取奖励页面的返回",output_error="没有找到'back.png'-领取奖励页面的返回")
        time.sleep(2)
        #是否出现‘排名时刻变化 记得常回来看看哦’
        i_know_dialog_isExist,i_know_dialog_tagX,i_know_dialog_tagY=ac.findImage("i_know_dialog.png")
        if i_know_dialog_isExist:
            print("出现“排名时刻变化 记得常回来看看哦”弹框")
            ac.findImageClick("i_know_btn.png")
            
            #ac.findImageClick("back.png",output_text="'back.png'-领取奖励页面的返回（出现弹框后）",output_error="没有找到'back.png'-领取奖励页面的返回（出现弹框后）")
            time.sleep(1)
        else:
            print("没有出现“排名时刻变化 记得常回来看看哦”弹框")
    if reward_list[0]!=0 or reward_list[1]!=0 :
        result = ','.join(str(x) for x in reward_list)
        ds.write_to_excel(value=result)

#进入微信->打开小程序->点击拼多多图标，进入小程序
def enter_weChat():
    # 定义应用程序路径
    #app_path = r'E:\\WeChat\\WeChat.exe'
    app_path=ac.getWxInstallPath()
    
    # 获取所有应用程序窗口标题
    all_windows = gw.getAllTitles()
    #微信没有打开或者微信最小化任务栏
    if "微信" not in all_windows:
        #print("微信正在打开")
        # 启动应用程序
        subprocess.Popen(app_path)
        print('打开VX')
        windows=getWindowByTitle("微信")
        
        #time.sleep(3.5)
        start_time = time.time()
        timeout = 20 
        count_time=10
        while True:
            if len(windows) == 0:
                time.sleep(1)
                count_time=count_time-1
                windows=getWindowByTitle("微信")
            else:
                break

            if count_time<=0:
                raise Exception("获取微信窗口失败！")
                #print("获取微信窗口失败！")

            # 如果超过了超时时间 跳出循环
            if time.time() - start_time > timeout:
                break
                
        #print(all_windows)
        # 获取窗口句柄
        window = getWindowByTitle("微信")[0]
        window.activate()
        left,top,width,height=window.left,window.top,window.width,window.height,
        #width 420 height 570  进入微信窗口
        if width == 420 and height == 570:
            print("正在进入微信")
            window.activate()
            pyautogui.moveTo(left+width/2,650,duration=0.25)
            pyautogui.click()
            
            #time.sleep(9)
            start_time = time.time()
            # 设置超时时间为30秒 避免while循环条件错误导致无限循环
            #多加一个保险
            timeout = 30 
            count_time=20
            while True:
                window = getWindowByTitle("微信")[0]
                width,height=window.width,window.height
                #print(count_time,width,height)
                if width>420 and height>570:
                    print("进入微信时耗费时间{}，此时的微信窗口宽：{}和高：{}".format(20-count_time,width,height))
                    break
                else:
                    time.sleep(1)
                    count_time=count_time-1

                if count_time<=0:
                    raise Exception("进入微信失败！")

                # 如果超过了超时时间 跳出循环
                if time.time() - start_time > timeout:
                    break

            time.sleep(1)
        #width 1422 height 1008 微信主窗口
        else:
            print("微信已经打开")
    else:
        print("微信窗口已存在！")
        windows = getWindowByTitle("微信")
        if len(windows):
            for window in windows:
                window.close()
        # 启动应用程序
        subprocess.Popen(app_path)

    time.sleep(1)
    print("打开小程序")
    ac.findImageClick('applet.png')

    time.sleep(2)
    current_window = get_current_window()
    #width 987 height 1020 小程序列表窗口大小
    applet_list_window = gw.getWindowsWithTitle('微信')[0]
    #print(applet_list_window)
    #window1.close()
    #width 1422 height 1008 微信主窗口
    wx_home_window = gw.getWindowsWithTitle('微信')[1]
    #print(wx_home_window)
    wx_home_window.close()

    pdd_path = r'image\target\pdd.png'
    location=pyautogui.locateOnScreen(pdd_path,confidence=0.5)
    #print(location)
    print("打开小程序拼多多")
    Center=pyautogui.center(location)
    pyautogui.click(Center)
    time.sleep(1)
    pdd_window = gw.getWindowsWithTitle('拼多多')[0]
    applet_list_window.close()
    #print(pdd_window)
    time.sleep(2)

#拼多多窗口->进入个人中心->进入省钱月卡->免费试用更多好货
#->完成提升概率->关闭窗口
def enter_pdd():
    print("点击个人中心")
    #personal_center.png
    ac.findImageClick('personal_center.png')
    time.sleep(2)
    print("点击省钱月卡")
    #save_money_monthly_card.png 省钱月卡
    ac.findImageClick('save_money_monthly_card.png')

    #免费试用更多好货
    findfree_use_more()

    #提升概率
    improve_probability()

    wx_pdd_window=gw.getWindowsWithTitle('拼多多')[0]
    wx_pdd_window.close()

def main():

    enter_weChat()

    enter_pdd()
    
if __name__ == "__main__":
    logger.record_terminal()
    new_time=logger.record_timestamp()
    print("程序开始时间：{}".format(new_time))
    main()
    end_time=logger.record_timestamp()
    print("程序结束时间：{}\n".format(end_time))
    #ac.test()
    #findfree_use_more()
    #improve_probability()
