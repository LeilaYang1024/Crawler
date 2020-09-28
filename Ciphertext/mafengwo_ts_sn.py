# coding: utf-8

"""
Created on:2019/05/14
@brief:马蜂窝的请求加密参数_ts,_sn破解
@author: YangLei
@version: Python3
"""
import time
import json
import hashlib
import requests

class Mafengwo(object):
    
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.mafengwo.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3469.400',
    'X-Requested-With': 'XMLHttpRequest'}
    
    def __init__(self,params,url):
        self.url = url
        self.params = params
        
        
    def get_sn(self):
        """
        计算_ts和_sn参数，由js调试得出
        :param params:
        :return:
        """
        
        #_ts参数实际就是时间戳
        self.params['_ts'] = str(int(time.time()*1000))
        
        #参数排序并json格式化，再加上盐值
        data = json.dumps(dict(sorted(self.params.items())),separators=(',',':')) + "c9d6618dbc657b41a66eb0af952906f1"
        
        #md5加密,_sn参数为取[2:12]
        md5 = hashlib.md5()
        md5.update(data.encode())
        return md5.hexdigest()[2:12]
    
    def RequestData(self):
        """
        请求数据
        :return:
        """
        self.params['_sn'] = self.get_sn()
        r = requests.get(url=url, params=self.params, headers=self.headers)
        return r.json()

        
if __name__=="__main__":
    """
    test:
    通过更改params参数来请求数据 """
    
    params = {'iMddId': '10065',  #目的地id
        'iAreaId': '-1',
        'iRegionId': '-1',
        'iPoiId': '',
        'position_name': '',
        'nLat': '0',
        'nLng': '0',
        'iDistance': '10000',
        'sCheckIn': '2019-06-20',
        'sCheckOut': '2019-06-21',
        'iAdultsNum': '2',
        'iChildrenNum': '0',
        'sChildrenAge': '',
        'iPriceMin': '',
        'iPriceMax': '',
        'sTags': '',
        'sSortType': 'comment',
        'sSortFlag': 'DESC',
        'has_booking_rooms': '0',
        'has_faved': '0',
        'sKeyWord': '',
        'iPage': '5', #请求页数变化
        'sAction': 'getPoiList5'}
    url = "http://www.mafengwo.cn/hotel/ajax.php"
    mafengwo =  Mafengwo(params,url)
    print(mafengwo.RequestData())
    
    