from apscheduler.schedulers.blocking import BlockingScheduler 
from apscheduler.schedulers.background import BackgroundScheduler 
import subprocess
from logger import Logger
from datetime import datetime, timedelta
import logging
import os
import sys

def compare_time(current_time,target_time): 
    # 判断当前时间是否在目标时间之前
    if current_time < target_time:
        print("当前时间在目标时间之前")
        return False
    else:
        print("当前时间在目标时间之后或等于目标时间")
        return True
        
def execute_program():
    logger = Logger("execute_program","./exe_schedule_log",CmdLevel=logging.DEBUG,FileLevel=logging.INFO)

    # 这里写入要执行的.exe文件路径及参数
    #program = r'C:\Users\Administrator\Desktop\my_python\dist\click_pdd\click_pdd.exe'
    # 获取exe文件所在的目录
    exe_dir = os.path.dirname(sys.argv[0])
    program=os.path.join(exe_dir,"click_pdd.exe")
    logger.info("click_pdd.exe执行路径：{}".format(program))
    
    try:
        # 调用外部程序
        subprocess.call(program)

        logger.info("Program executed successfully!（click_pdd.exe成功执行！）")
        print("Program executed successfully!（click_pdd.exe成功执行！）")
    except Exception as e:
        logger.error("An error occurred while executing the program.（click_pdd.exe执行出错！）")
        print("An error occurred while executing the program.（click_pdd.exe执行出错！）")
        print(e)

def schedule_task():
    # 创建一个BlockingScheduler对象
    #scheduler = BackgroundScheduler()
    scheduler = BlockingScheduler()

    # 获取当前时间
    current_time = datetime.now()
    #now=current_time.strftime('%Y-%m-%d %H:%M:%S')
    print("当前时间为：", current_time)

    #is_execute=compare_time(current_time,target_time)
    #start_time = '2024-02-12 06:30:00'
    # 开始时间
    start_hour = 0
    start_minute = 20
    start_time = datetime(year=current_time.year, month=current_time.month, day=current_time.day, hour=start_hour, minute=start_minute)
    print("目标时间为：", start_time)
    # 结束时间
    end_hour= 23
    end_minute= 30
    end_time = datetime(year=current_time.year, month=6, day=15, hour=end_hour, minute=end_minute)
    # 时间间隔
    interval = 60*30

    #hours minutes seconds
    scheduler.add_job(execute_program, 'interval',start_date=start_time,end_date=end_time, seconds=interval)
    print(scheduler.get_jobs())
    
    try:
        scheduler.start()
        #scheduler.shutdown(wait=False)
    except KeyboardInterrupt:
        pass
    finally:
        #scheduler.shutdown()
        print(scheduler)
        #print("定时任务结束了")


if __name__ == "__main__":

    logger = Logger("schedule","./exe_schedule_log",CmdLevel=logging.DEBUG,FileLevel=logging.INFO)
    logger.info("info message!")
    
    #logging.basicConfig()
    #logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    Logger("apscheduler","./exe_schedule_log",CmdLevel=logging.DEBUG,FileLevel=logging.INFO)

    logger.info("任务开始了")
    print("任务开始了")
    schedule_task()
    logger.info("定时任务结束了")
    print("定时任务结束了")
    
