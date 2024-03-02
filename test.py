import pygetwindow as gw
import win32api
import win32con
import subprocess

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

if __name__ == '__main__':
    windows = gw.getWindowsWithTitle("微信")[0]
    print(windows)
    print(getWxInstallPath())
    #app_path = r'E:\\WeChat\\WeChat.exe'
    #program_path=getWxInstallPath()
    #process = subprocess.Popen(program_path)
    
    # 调用函数并传入要检查的进程名称
    is_running = check_process('wechat')
    print(f"The WeChat.exe process is running: {is_running}")

