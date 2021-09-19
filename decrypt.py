import base64
import hashlib
from Crypto.Cipher import AES

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
if __name__ == '__main__':
    data = 'ONQbi8M2g102SqsivYhvjeWnxDYwS6i7/QoWjwsmhxriSPsy3EhDQh3kpXYpXpXt'
    
    decrypts = example(decrypt(data))
    print(decrypts)
    
    
"""
:/novel/lists?order=2&sex=1&status=0&type=0&page={{page}}
奇幻玄幻::/novel/lists?order=0&status=0&sex=1&page={{page}}&type=3
武侠修真::/novel/lists?order=0&status=0&sex=1&page={{page}}&type=4
都市娱乐::/novel/lists?order=0&status=0&sex=1&page={{page}}&type=5
历史军事::/novel/lists?order=0&status=0&sex=1&page={{page}}&type=6
科幻玄幻::/novel/lists?order=0&status=0&sex=1&page={{page}}&type=7
游戏动漫::/novel/lists?order=0&status=0&sex=1&page={{page}}&type=8
其他类型::/novel/lists?order=0&status=0&sex=1&page={{page}}&type=9

                                        
::/novel/lists?order=2&sex=2&status=0&type=0&page={{page}}
  人气榜  ::/novel/ranking?sex=2&page={{page}}&order=0
  完结榜  ::/novel/ranking?sex=2&page={{page}}&order=1
  收藏榜  ::/novel/ranking?sex=2&page={{page}}&order=2
  热搜榜  ::/novel/ranking?sex=2&page={{page}}&order=3
  新书榜  ::/novel/ranking?sex=2&page={{page}}&order=4
"""