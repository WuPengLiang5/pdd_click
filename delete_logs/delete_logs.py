import tkinter as tk
from tkinter import filedialog,Frame,NSEW,INSERT,messagebox
import glob
import os
import time
from progress.bar import IncrementalBar

def main():
    # 创建主窗口对象
    window = tk.Tk()
    window.title("删除日志")

    # 设置窗口大小和位置
    # 主窗口的尺寸，长x宽
    width = 500
    height = 300

    # 读取屏幕的宽度和高度
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    
    # 这里的乘是小x
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
    window.geometry(alignstr)
    #window.geometry("300x200+500+300")

    #在Tkinter中，可以使用grid()方法来设置网格布局，
    #并使用rowconfigure()和columnconfigure()方法来调整网格的大小。
    #window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    #window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(1, weight=1)

    frame_1 = Frame(window,highlightbackground="black"
                  , highlightthickness=1)
    frame_2 = Frame(window,bg='blue',highlightbackground="black"
                  , highlightthickness=1)

    frame_1.grid(row=0,column=0,sticky=NSEW)
    frame_2.grid(row=1,column=0,sticky=NSEW)
    # frame_1.grid(row=0,column=0,columnspan=2,sticky=NSEW)
    # columnspan参数代表frame占几列的网格长度若设置为2就横跨2格
    #frame_3.grid(row=1,column=0,sticky=NSEW)

    path_text = tk.StringVar()    
    path_entry=tk.Entry(frame_1,textvariable=path_text)
    path_entry.grid(row=0,column=0,sticky=NSEW)
    frame_1.columnconfigure(0,weight=1)
    browse_bt=tk.Button(frame_1,text="浏览",font=("Arial", 10))
    browse_bt.grid(row=0,column=1)
    browse_bt.config(command=lambda: get_folder_path(path_entry))

    entry_text = tk.StringVar()
    entry_path = tk.Entry(frame_1, show='',  bg='white', highlightcolor='red', relief='raised',
                      textvariable=entry_text)
    entry_path.grid(row=1,column=0,padx=5,pady=5,sticky=tk.E)
    entry_bt = tk.Button(frame_1,text="搜索",font=("Arial", 10))
    entry_bt.grid(row=1,column=1,columnspan=2,padx=5,pady=5,sticky=tk.E)

    sv_lang_list = tk.StringVar()
    list_box=tk.Listbox(frame_2,listvariable=sv_lang_list)
    list_box.grid(row=0,column=0,columnspan=3,padx=5,pady=5,sticky=tk.NSEW)
    frame_2.columnconfigure(0,weight=1)
        
    #entry_path_text=entry_path.get()
    entry_bt.config(command=lambda: search(path_text.get(),entry_text.get(),sv_lang_list))

    delete_bt = tk.Button(frame_2,text="全部删除",font=("Arial", 10),command=lambda:delete_popup(list_box.get(0,list_box.size()-1)))
    delete_bt.grid(row=1,column=0,columnspan=2,padx=5,pady=5)

    
    # 添加Label组件并显示文本内容
    #tk.Label(window, text="Hello World!", font=("Arial", 16)).grid(row=1,column=0,columnspan=5, padx=5, pady=5)

    #window.withdraw()

    #print("所选文件夹路径为：", folder_path)
    
    # 运行主事件循环
    window.mainloop()
    
def get_folder_path(path_entry):
    print("打开文件夹")
    folder_path = filedialog.askdirectory(title='选择文件夹')
    if folder_path:
        print("你选择了文件: %s" % folder_path)
        if path_entry.get():
             path_entry.delete(0,"end")
        path_entry.insert('end',folder_path)
    else:
        print("你取消了文件选择。文件夹：%s"%folder_path)
        path_entry.insert(INSERT,"")

def search(folder_path,filename_path,sv_lang_list):
    if folder_path:
        # 指定要搜索的目录路径 folder_path
        # 2024-02-14
        print(folder_path)
        date_str=filename_path+"*"
        full_path=folder_path + "/" + date_str + ".log"
        print("完整路径：%s"%full_path)
        # 通过glob函数获取所有符合条件的文件名列表
        #file_list = glob.glob(f"{folder_path}/*.log")
        file_list = glob.glob(full_path)
     
        print("共有%s个文件，找到的日志文件如下："%len(file_list))
        for file in file_list:
            print(file)
        sv_lang_list.set(tuple(file_list))
    else:
        print("所选文件夹为空！")

def delete_popup(list_data):
    #print(list_data)
    if len(list_data) != 0:
        result = messagebox.askyesno('询问', '您是否确定全部删除？')
        if result == True:
            print('您选择了“是”按钮，确认删除！')
            bar = IncrementalBar('Countdown', max = len(list_data))
            for item in list_data:
                os.remove(item)
                bar.next()
                time.sleep(1)
                bar.finish()
            print("全部文件删除成功！")
        else:
            print('您选择了“否”按钮，取消删除！')
    else:
        print("删除的文件路径为空！")
    
if __name__ == "__main__":
    main()
