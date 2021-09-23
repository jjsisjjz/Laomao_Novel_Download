import json
import os


class Set():

    def __init__(self):
        self.os_config = os.path.join(os.getcwd(), 'config')
        
        
    def WriteSettings(slef, info):
        with open('settings.json', 'w') as file:
            write_ = file.write(json.dumps(info, 
                indent=4, ensure_ascii=False))
        return write_
    
    def ReadSettings(slef):
        with open('settings.json', 'r') as file:
            read_ = json.loads(file.read())
        return read_
    
    
    def NewSettings(self):
        if os.path.isfile('settings.json'):
            return "配置文件已存在"
        settings_info = {}
        settings_info['max_workers_number'] = 6
        settings_info['Open_ThreadPool'] = True
        settings_info['help'] = "输入 - 加上首字母\nh \| help\\t\\t\\t\\t\\t\\t--- 显示说明\nq \| quit\\t\\t\\t\\t\\t\\t--- 退出正在运作的程序\nc \| cookie\\t\\t\\t\\t\\t\\t--- 检测本地的cookie凭证\nb \| b \+ bookid\\t\\t\\t\\t\\t\\t--- 下载指定小说章节文本\nu \| u \+ url\\t\\t\\t\\t\\t\\t--- 下载指定小说章节文本\nn \| n \+ bookname\\t\\t\\t\\t\\t--- 输入书名下载小说文本\nt \| t \+ tagname\\t\\t\\t\\t\\t\\t--- 下载全站标签书籍信息"
        print(f"已在{os.getcwd()}创建配置文件")
        self.WriteSettings(settings_info)