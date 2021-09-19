import json
import time
import os, re
import requests
import random
# import Threading
import json
import binascii
import base64
import hashlib
from Crypto.Cipher import AES
import sys

iv = b'8yeywyJ45esysW8M'
# https://api.laomaoxs.com/novel/txt/novel/lists?order=0&status=0&sex=1&page=0&type=4
# def encrypt(text, key):
# aes_key = hashlib.sha256(key.encode('utf-8')).digest()
# aes_key = AES.new(aes_key, AES.MODE_CFB, iv)
# return base64.b64encode(aes.encrypt(text))


def decrypt(encrypted, key='b23c159r9t88hl2q'):
    aes_key = hashlib.sha256(key.encode('utf-8')).digest()
    aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    return pkcs7un_padding(aes.decrypt(base64.b64decode(encrypted)))


def pkcs7un_padding(data):
    length = len(data)
    un_padding = ord(chr(data[length - 1]))
    return data[0:length - un_padding]


def example(express, result=None):
    result = eval(express)
    return result


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
        # self.path_config = os.path.join("config", self.bookName)
        # self.path_novel = os.path.join("novel", self.bookName)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Keep-Alive": "300",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
            "Host": "api.laomaoxs.com",
            "Accept-Encoding": "gzip",
        }

    def filedir(self):
        meragefiledir = os.path.join('config', self.bookName)  # 获取当前文件夹中的文件名称列表
        filenames = os.listdir(meragefiledir)
        filenames.sort(key=lambda x: int(x.split('.')[0]))
        file = open(os.path.join('Download', f'{self.bookName}.txt'), 'a', encoding='utf-8')
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
        self.chapter_list[number-1] = re.sub(r'[？?\*|“<>:/]', '', str(self.chapter_list[number-1]))
        with open(os.path.join('config', self.bookName, f"{number}.{self.chapter_list[number-1]}.txt"), 'w', encoding='utf-8', newline='') as fb:
            fb.write(str(write_txt_info))

    def read_config_name(self):
        # config读取文件名
        read_name = os.listdir(os.path.join('config', self.bookName))
        return read_name


    def print_info(self, bookid):
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
        print("书名:{}\n序号:{}\n作者:{}\n分类:{}".format(
            self.bookName, self.bookid, self.authorName, book_type))
        print("简介:{}\n更新时间:{}\n{}".format(
            self.novel_intro, self.lastUpdateTime, self.isFinish))

    def chapters(self):
        number = 0
        print('开始下载{} ,一共{}章'.format(self.bookName, len(self.chapter_list)))
        for i in range(len(self.chapter_list)):
            """书本编号等于bookid÷1000"""
            num = int(int(self.bookid)/1000)
            number += 1
            """跳过已经下载的章节"""
            if self.chapter_list[number-1]  in ''.join(self.read_config_name()):
                print(self.chapter_list[number-1], '已经下载过')
                continue
            req = requests.get('https://api.laomaoxs.com/novel/txt/{}/{}/{}.html'.format(
                num, self.bookid, i), headers=self.headers).text
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

    def SearchBook(self, bookname):
        for data in example(decrypt(
                requests.get('https://api.laomaoxs.com/Search/index?key={}&page=1'.format(bookname),
                             headers=self.headers).text))['data']:
            self.bookid = data['book_id']
            self.chapter_count = data['chapter_count']  # 字数
            self.book_hits = data['book_hits']  # 排行榜
            self.print_info(self.bookid)
            # print('chapter_count  book_hits', self.chapter_count, self.book_hits)

        self.print_info()
    def class_list(self):
        tag = requests.get('https://api.laomaoxs.com/novel/lists?order=0&status=0&sex=1&page=0&type=4', headers=self.headers)
        for data in example(decrypt(tag.text))['data']:
            
            self.bookName = (data['book_title'])
            self.bookid = data['book_id']
            self.print_info(self.bookid)
        # print(type(example(decrypt(tag.text))))
        
    # def ThreadPool(self):
    #     self.os_meragefiledir()
    #     with ThreadPoolExecutor(max_workers=self.Pool) as t:
    #         obj_list = []
    #         for url in track(self.chapters_id_list):
    #             """url          小说完整序号"""
    #             """len_number   小说单章号码"""
    #             """filenames    小说单章名字"""
    #             len_number = url.split('/')[1]
    #             filenames = self.os_meragefiledir()
    #             """跳过已经下载的章节"""
    #             # print("开始检查本地缓存文件")
    #             if len_number in ''.join(filenames):
    #                 # print(len_number, '已经下载过')
    #                 continue
    #             else:
    #                 obj = t.submit(self.download, url, len_number)
    #                 obj_list.append(obj)
    #         for future in as_completed(obj_list):
    #             data = future.result()

    #     with open(os.path.join("novel", self.bookName + '.txt'), 'w') as f:
    #         self.filedir()
    #         print(f'\n小说 {self.bookName} 下载完成')
    
    # https://api.laomaoxs.com/novel/lists?order=0&status=0&sex=1&page=0&type=4
if __name__ == '__main__':
    Download = Download()
    Download.class_list()
    # Download.SearchBook("不灭龙帝")
    Download.os_file()
    Download.chapters()
    Download.filedir()
