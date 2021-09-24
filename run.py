import API.LaoMaoxsAPI
import API.Settings
import sys
import os


# 实例化类
Download = API.LaoMaoxsAPI.Download()
Setting = API.Settings.Set()



def shell():
    Setting.NewSettings()
    Read = Setting.ReadSettings()
    try:
        Options = sys.argv[1]
    except IndexError:
        print(Read['help'])
        quit("你没有输入任何命令")
        
    if Options == '-h':
        print(Read['help'])
        quit("退出程序")

    elif Options == '-n':
        try:
            bookname = sys.argv[2]
        except IndexError as e:
            bookname = Download.inputs(f'Error {e} input bookname:')
        try:
            Open_ThreadPool = bool(sys.argv[3])
        except IndexError:
            Open_ThreadPool = Read['Open_ThreadPool']
        search_book = Download.SearchBook(bookname)
        for i in search_book:
            Download.GetBook(i)
            if Open_ThreadPool:
                print("开启多线程")
                Download.ThreadPool(Read['max_workers_number'])
            else:
                Download.chapters(Open_ThreadPool=False)
            
           
    elif Options == '-b':
        try:
            bookid = sys.argv[2]
        except IndexError as e:
            bookid = Download.inputs(f'Error {e} input bookid:')
        try:
            Open_ThreadPool = sys.argv[3]
        except IndexError:
            print('默认以多线程方式下载')
            Open_ThreadPool = Read['Open_ThreadPool']
        finally:
            Download.GetBook(bookid)
            if Open_ThreadPool:
                Download.ThreadPool(Read['max_workers_number'])
            else:
                Download.chapters(Open_ThreadPool=False)

    elif Options == '-t':
        try:
            Tag_Number = sys.argv[2]
        except IndexError as e:
            Tag_Number = Download.inputs(f'Error {e} input Tag Number:')
        try:
            Open_ThreadPool = sys.argv[3]
        except IndexError:
            print('默认以多线程方式下载')
            Open_ThreadPool = Read['Open_ThreadPool']
        finally:
            for i in Download.class_list(Tag_Number):
                Download.GetBook(i)
                if Open_ThreadPool:
                    Download.ThreadPool(Read['max_workers_number'])
                else:
                    Download.chapters(Open_ThreadPool=False)
                    
    elif Options == '-max':
        max = sys.argv[2]
        if max.isdigit():
            Read['max_workers_number'] = 14 if int(max) > 14 else int(max)
            print("线程已经设置为", Read['max_workers_number'])
            Setting.WriteSettings(Read)
        else:
            print(max, "不是数字，请重新输入")
    else:
        print("选项为不存在,请输入-h获取帮助")
            
shell()