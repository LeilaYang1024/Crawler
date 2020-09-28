# coding: utf-8

"""
Created on:
@brief:喜马拉雅请求参数xm-sign破解
@author: YangLei
@version: Python3
"""
import requests
import execjs

"""
xm-sign:e77103f11d826e92c04768aed32a0074(72)1566525709228(75)1566525704840

其中:
e77103f11d826e92c04768aed32a0074:32位

2个（）:产生0-100随机整数 random.randint(0,100)
1566525709228:从喜马拉雅获取的时间戳
1566525704840:now的时间戳

"""
import hashlib
import requests
import random
import time

class ximalayaSign(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept': 'text/html,application/xhtml+ xml,application/xml;q = 0.9,image/webp,image/apng,*/*;q=0.8, application/signe-exchange;v = b3',
        'Host': 'www.ximalaya.com'
    }
    
    def getxmtime(self):
        url = "https://www.ximalaya.com/revision/time"
        response = requests.get(url, headers=self.headers)
        html = response.text
        return html
    
    def getsign(self):
        xm_time = self.getxmtime()
        str = "ximalaya-" + xm_time
        md5 = hashlib.md5()
        md5.update(str.encode())
        Sign = md5.hexdigest()
        return xm_time,Sign
    
    def getxm_sign(self):
        xm_time, Sign=self.getsign()
        S = f'{Sign}({random.randint(0, 100)}){xm_time}({random.randint(0, 100)}){int(time.time() * 1000)}'
        return S
    
if __name__=="__main__":
    print(ximalayaSign().getxm_sign())
