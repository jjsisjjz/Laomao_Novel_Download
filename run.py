import API.LaoMaoxsAPI
import API.Settings
import sys
import getopt

choice = 'h'
bookid = ''
bookname = ''
tag = ''
pool = True
help = """--max <max> pool number
--bookid = <id>
--bookname = <bookname>
--pool open Thread
--login = usernames,passwords"""
try:
    opts, args = getopt.getopt(sys.argv[1:],"hkc:o:",[
        "login=","bookname=",
        "bookid=","tag=","pool=","max="])
except getopt.GetoptError:
    print(help)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('--pool',):
        pool = False
    elif opt in ('--max',):
        choice = 'settingmax'
        max_workers_number = arg
    elif opt in ('--tagid',):
        choice = 'gettag'
        tag = arg
    elif opt == ('--bookid',):
        choice = 'bookid dwonload'
        bookid = arg
    elif opt in ('--bookname',):
        choice = 'name dwonload'
        bookname = arg
    elif opt in ('--login',):
        choice = 'login'
        user = arg
    elif opt in ('--rank',):
        choice = 'ranking'
    
def shell():
        
    match choice:
        case 'h':
            print(help)

        case 'login':
            usernames = user.split(',')[0]
            passwords = user.split(',')[1]
            Download.Login(usernames, passwords)

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
            if max_workers_number.isdigit():
                Read['max_workers_number'] = 12 if int(max_workers_number) > 12 else int(max_workers_number)
                print("线程已经设置为", Read['max_workers_number'])
                Setting.WriteSettings(Read)
            else:
                print(max_workers_number, "不是数字，请重新输入")
        case _:
            print("选项为不存在,请输入-h获取帮助")


if __name__ == '__main__':
    Download = API.LaoMaoxsAPI.Download()
    Setting = API.Settings.Set()
    Setting.NewSettings()
    Read = Setting.ReadSettings()
    shell()
