import API.LaoMaoxsAPI
import API.Settings
import sys
import getopt


def shell(argv):
    ## 开始解析命令行参数
    choice = 'h'
    bookid = ''
    bookname = ''
    tag = ''
    pool = True
    usernames, passwords = None, None
    try:
      opts, args = getopt.getopt(argv,"hkc:o:",[
            "usernames=","passwords=","bookname=",
            "bookid=","tag=","pool=","max="])
    except getopt.GetoptError:
        print('--max <max> pool number')
        print('--bookid = <id>')
        print('--bookname = <bookname>')
        print('--pool  open Thread')
        print('--usernames # Your Account usernames')
        print('--passwords')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-help':
            print('--max <max> pool number')
            print('--bookid = <id>')
            print('--bookname = <bookname>')
            print('--pool  open Thread')
            print('--usernames # Your Account usernames')
            print('--passwords')
            sys.exit()
        elif opt in ('--pool',):
            pool = False
        elif opt in ('--max',):
            choice = 'settingmax'
            max = arg
        elif opt in ('--tagid',):
            choice = 'gettag'
            tag = arg
        elif opt == ('--bookid',):
            choice = 'bookid dwonload'
            bookid = arg
        elif opt in ('--bookname',):
            choice = 'name dwonload'
            bookname = arg
        elif opt in ('--usernames',):
            usernames = arg
        elif opt in ('--passwords',):
            passwords = arg
        elif opt in ('--rank',):
            choice = 'ranking'
    
    if usernames is not None and passwords is not None:
        Download.Login(usernames, passwords)
        
    match choice:
        case 'h':
            print('--max <max> pool number')
            print('--bookid = <id>')
            print('--bookname = <bookname>')
            print('--pool  open Thread')
            print('--usernames # Your Account usernames')
            print('--passwords')

        case 'name':
            search_book = Download.SearchBook(bookname)
            for i in search_book:
                Download.GetBook(i)
                if pool:
                    print("开启多线程")
                    Download.ThreadPool(Read['max_workers_number'])
                else:
                    Download.chapters(pool=False)

        case 'dwonloadbook':
            Download.GetBook(bookid)
            if pool:
                Download.ThreadPool(Read['max_workers_number'])
            else:
                Download.chapters(pool=False)

        case 'gettag':
            for i in Download.class_list(tag):
                Download.GetBook(i)
                if pool:
                    Download.ThreadPool(Read['max_workers_number'])
                else:
                    Download.chapters(pool=False)

        case 'ranking':
            for i in Download.ranking():
                Download.GetBook(i)
                if pool:
                    Download.ThreadPool(Read['max_workers_number'])
                else:
                    Download.chapters(pool=False)

        case 'settingmax':
            if max.isdigit():
                Read['max_workers_number'] = 12 if int(max) > 12 else int(max)
                print("线程已经设置为", Read['max_workers_number'])
                Setting.WriteSettings(Read)
            else:
                print(max, "不是数字，请重新输入")
        case _:
            print("选项为不存在,请输入-h获取帮助")


if __name__ == '__main__':
    Download = API.LaoMaoxsAPI.Download()
    Setting = API.Settings.Set()
    Setting.NewSettings()
    Read = Setting.ReadSettings()
    shell(sys.argv[1:])
