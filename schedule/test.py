import datetime
import logger
import os
import win32api
import win32con

def job():
    current_time = datetime.datetime.now()
    print("当前时间为：", current_time)
    print("这是一个任务！")

def compare_time():
    # 获取当前时间
    current_time = datetime.datetime.now()
    print("当前时间为：", current_time)
 
    # 设置目标时间
    target_hour = 6   # 目标小时数
    target_minute = 30    # 目标分钟数
    target_time = datetime.datetime(year=current_time.year, month=current_time.month, day=current_time.day, hour=target_hour, minute=target_minute)
    print("目标时间为：", target_time)
 
    # 判断当前时间是否在目标时间之前
    if current_time < target_time:
        print("当前时间在目标时间之前")
    else:
        print("当前时间在目标时间之后或等于目标时间")
 
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

if __name__ == "__main__":
    compare_time()
    job()
    #record_terminal()
    print(os.path.dirname(__file__))
    print("微信路径：{}".format(getWxInstallPath()))
