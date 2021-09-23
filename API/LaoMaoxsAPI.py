import requests
import os, re, sys
import time, json
from .AesDecrypt import *
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, as_completed


class Download():
    def __init__(self):
        self.bookid = ''
        self.bookName = ""
        self.novel_intro = ""
        self.charCount = ""
        self.authorName = ""
        self.chapter_list = []
        self.os_config_json = os.path.join(os.getcwd(), 'config')
        self.lastUpdateTime = ""
        self.authorName = ""
        self.headers = {
            "Host": "api.laomaoxs.com",
            "Keep-Alive": "300",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

    def inputs(self, name):
        inp = input(name)
        while not inp:
            inp = input(name)
        else:
            return inp

    def filedir(self):
        meragefiledir = os.path.join(
            'config', self.bookName)  # 获取当前文件夹中的文件名称列表
        filenames = os.listdir(meragefiledir)
        filenames.sort(key=lambda x: int(x.split('.')[0]))
        file = open(os.path.join(
            'Download', f'{self.bookName}.txt'), 'a', encoding='utf-8')
        for filename in filenames:  # 先遍历文件名
            filepath = os.path.join(meragefiledir, filename)
            #遍历单个文件，读取行数
            for line in open(filepath, encoding='utf-8'):
                file.writelines(line)
            file.write('\n')
        file.close()

    def os_file(self):
        self.main_path = os.getcwd()  # 项目路径
        # 创建Download文件夹
        self.os_novel_download = os.path.join(self.main_path, "Download")
        if not os.path.exists(self.os_novel_download):
           os.mkdir(self.os_novel_download)
           print(f'已在{self.main_path}创建Download文件夹')

        # 创建config_json文件夹
        if not os.path.exists(self.os_config_json):
           os.mkdir(self.os_config_json)
           print(f'已在{self.main_path}创建config文件夹')

        if not os.path.exists(os.path.join('config', self.bookName)):
            os.makedirs(os.path.join('config', self.bookName))

        # 创建list文本
        if not (os.path.join(self.main_path, "list.txt")):
           file = open(os.path.join(self.main_path, "list.txt"),
                       'a', encoding='utf-8')

        # 创建txt文本
        if not os.path.exists(os.path.join(self.os_novel_download, f"{self.bookName}.txt")):
            file = open(os.path.join(self.os_novel_download,
                        f"{self.bookName}.txt"), "a", encoding='utf-8')

    def write_txt(self, write_txt_info, number):  # 将信息写入TXT文件
        """删去windowns不规范字符"""
        self.chapter_list[number -
                          1] = re.sub(r'[？?\*|“<>:/]', '', str(self.chapter_list[number-1]))
        with open(os.path.join('config', self.bookName, f"{number}.{self.chapter_list[number-1]}.txt"), 'w', encoding='utf-8', newline='') as fb:
            fb.write(str(write_txt_info))

    def read_config_name(self):
        # config读取文件名
        read_name = os.listdir(os.path.join('config', self.bookName))
        return read_name

    def GetBook(self, bookid):
        self.bookid = bookid
        info_book = example(decrypt(requests.get(
            'https://api.laomaoxs.com/novel/txt/0/{}/index.html'.format(self.bookid), headers=self.headers).text))['data']
        # print(info_book)
        self.novel_intro = info_book['book_desc']
        self.lastUpdateTime = info_book['update_time']
        self.bookName = info_book['book_title']
        self.authorName = info_book['book_author']
        book_type = info_book['book_type']
        self.isFinish = info_book['book_status']
        self.chapter_list = info_book['chapter_list']
        print("\n\n书名:{}\n序号:{}\n作者:{}\n分类:{}".format(
            self.bookName, self.bookid, self.authorName, book_type))
        print("简介:{}\n更新时间:{}\n{}".format(
            self.novel_intro, self.lastUpdateTime, self.isFinish))
        """建立文件夹和文件"""
        self.os_file()

    def chapters(self, Open_ThreadPool=False):
        number = 0
        chapters_list = []
        print('开始下载{} ,一共{}章'.format(self.bookName, len(self.chapter_list)))
        if Open_ThreadPool:
            for i in track(range(len(self.chapter_list))):
                number += 1
                """跳过已经下载的章节"""
                if self.chapter_list[number-1] in ''.join(self.read_config_name()):
                    print(self.chapter_list[number-1], '已经下载过')
                    continue
                else:
                    num = int(int(self.bookid)/1000)  # 书本编号等于bookid÷1000
                    chapters_list.append(
                        'https://api.laomaoxs.com/novel/txt/{}/{}/{}.html'.format(num, self.bookid, i))
                    # print(chapters_list[-1])
            return chapters_list
        if not Open_ThreadPool:
            for i in track(range(len(self.chapter_list))):
                num = int(int(self.bookid)/1000)  # 书本编号等于bookid÷1000
                number += 1
                """跳过已经下载的章节"""
                if self.chapter_list[number-1] in ''.join(self.read_config_name()):
                    print(self.chapter_list[number-1], '已经下载过')
                    continue
                req = requests.get('https://api.laomaoxs.com/novel/txt/{}/{}/{}.html'.format(
                    num, self.bookid, i), headers=self.headers).text
                content = example(decrypt(req))['data']
                """跳过屏蔽章节"""
                if "\\n\\n  编辑正在手打中，稍后点击右上角刷新当前章节！" not in content:
                    # print(self.chapter_list[number-1])
                    content_chap_title = ""
                    content_chap_title += f"\n\n\n{self.chapter_list[number-1]}\n\n"
                    for content in content.split("\n"):
                        content = re.sub(r'^\s*', "\n　　", content)
                        if re.search(r'\S', content) != None:
                            content_chap_title += content
                    self.write_txt(content_chap_title, number)
                else:
                    print(f"{self.chapter_list[number-1]}这是屏蔽章节，跳过下载")
            with open(os.path.join("Download", self.bookName + '.txt'), 'w') as f:
                self.filedir()
                print(f'\n小说 {self.bookName} 下载完成')

    def ThreadPool_download(self, urls, number):
        """多线程下载函数"""
        req = requests.get(urls, headers=self.headers).text
        content = example(decrypt(req))['data']
        """跳过屏蔽章节"""
        if "\\n\\n  编辑正在手打中，稍后点击右上角刷新当前章节！" not in content:
            print(self.chapter_list[number-1])
            content_chap_title = ""
            content_chap_title += f"\n\n\n{self.chapter_list[number-1]}\n\n"
            for content in content.split("\n"):
                content = re.sub(r'^\s*', "\n　　", content)
                if re.search(r'\S', content) != None:
                    content_chap_title += content
            # time.sleep(0.01)
            self.write_txt(content_chap_title, number)
        else:
            print(f"{self.chapter_list[number-1]}这是屏蔽章节，跳过下载")

    def SearchBook(self, bookname, max_workers_number, Open_ThreadPool=False):
        url_list = []
        for i in range(100):
            response = requests.get('https://api.laomaoxs.com/Search/index?key={}&page={}'.format(bookname, i)).text
            if not example(decrypt(response))['data']:
                break
            for data in example(decrypt(response))['data']:
                self.bookid = data['book_id']
                self.book_hits = data['book_hits']  # 排行榜
                if Open_ThreadPool:
                    self.GetBook(self.bookid)
                    self.chapters(Open_ThreadPool=True)
                    self.ThreadPool(max_workers_number)
                else:
                    self.GetBook(self.bookid)
                    self.chapters(Open_ThreadPool=False)

    def class_list(self, Tag_Number):
        class_list_bookid = []
        for i in range(10000):
            response = requests.get(f'https://api.laomaoxs.com/novel/lists?order=0&status=0&sex=1&page={i}&type={Tag_Number}', 
                    headers=self.headers).text
            if not example(decrypt(response))['data']:
                return '分类已经下载完毕'
            for data in example(decrypt(response))['data']:
                self.bookName = data['book_title']
                print(self.bookName)
                class_list_bookid.append(data['book_id'])
            return class_list_bookid
            # for bookid in class_list_bookid:
                # if Open_ThreadPool:
                    # self.GetBook(bookid)
                    # self.chapters(Open_ThreadPool=True)
                    # self.ThreadPool()
                # else:
                    # self.GetBook(bookid)
                    # self.chapters(Open_ThreadPool=False)
                
                

        # print(type(example(decrypt(tag.text))))

    def ThreadPool(self, max_workers_number):
        """多线程并发实现"""
        with ThreadPoolExecutor(max_workers=max_workers_number) as t:
            obj_list, number = [], 0
            # print(len(self.chapters(Open_ThreadPool=True)))
            for book_url in self.chapters(True):
                # print(book_url)
                number += 1
                obj = t.submit(self.ThreadPool_download, book_url, number)
                obj_list.append(obj)
            for future in as_completed(obj_list):
                data = future.result()

        with open(os.path.join("Download", self.bookName + '.txt'), 'w') as f:
            self.filedir()
            print(f'\n小说 {self.bookName} 下载完成')


    