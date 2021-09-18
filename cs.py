import json,time, os
import requests, random
import binascii
import re, json
import binascii
import struct
import base64
import hashlib
from Crypto.Cipher import AES
import logging
import sys

iv = b'8yeywyJ45esysW8M'
 
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
    
    
    def print_info(self):
        info_book = example(decrypt(requests.get('https://api.laomaoxs.com/novel/txt/0/{}/index.html'.format(self.bookid), headers=self.headers).text))['data']
        # print(info_book)
        self.novel_intro = info_book['book_desc']
        self.lastUpdateTime = info_book['update_time']
        self.bookName = info_book['book_title']
        self.authorName = info_book['book_author']
        book_type = info_book['book_type']
        self.isFinish = info_book['book_status']
        self.chapter_list = info_book['chapter_list']
        print("书名:{}\n序号:{}\n作者:{}\n分类:{}".format(self.bookName, self.bookid, self.authorName, book_type))
        print("简介:{}\n更新时间:{}\n{}".format(self.novel_intro, self.lastUpdateTime,self.isFinish))
        
        
        
    
    def chapters(self):
        number = 0
        for i in range(len(self.chapter_list)):
            """章节编号等于bookid÷1000"""
            num = int(int(self.bookid)/1000)
            # print(num)
            number += 1
            
            req = requests.get('https://api.laomaoxs.com/novel/txt/{}/{}/{}.html'.format(num, self.bookid, i), headers=self.headers).text
            content = example(decrypt(req))['data']
            if "\\n\\n  编辑正在手打中，稍后点击右上角刷新当前章节！" not in content:
                print(self.chapter_list[number-1])
                content_chap_title = ""
                content_chap_title += f"\n\n\n{self.chapter_list[number-1]}\n\n"
                for content in content.split("\n"):
                    content = re.sub(r'^\s*', "\n　　", content)
                    if re.search(r'\S', content) != None:
                        content_chap_title += content
                # time.sleep(0.5)
                with open(f"{self.bookName}.txt", 'a', encoding='utf-8', newline='') as f:
                    f.write(content_chap_title)
            else:
                print(f"{self.chapter_list[number-1]}这是屏蔽，跳过下载")
                
            

        
        

    def SearchBook(self, bookname):
        for data in example(decrypt(
                requests.get('https://api.laomaoxs.com/Search/index?key={}&page=1'.format(bookname), 
                    headers=self.headers).text))['data']:
            self.bookid = data['book_id']
            chapter_count = data['chapter_count']
            book_hits = data['book_hits']
        
        self.print_info()
        self.chapters()
        
        
        
if __name__ == '__main__':
    Download = Download()
    Download.SearchBook("不灭龙帝")