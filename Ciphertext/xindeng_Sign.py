# coding: utf-8

"""
Created on:
@brief:
@author: YangLei
@version: Python3
"""
import time
import hashlib
import requests
import re
class xindeng(object):
    payload = {"Ver": "1.0", "Language": "cn"}
    
    def __init__(self,Method,data):
        self.payload['Method']=Method
        self.data=data
        
    def get_Timestamp(self):
        """
        时间戳
        :return:
        """
        return str(int(time.time() * 1000))
        
    def get_Sign(self):
        """签名"""
        info = "Language" + self.payload['Language'] + "Method" + self.payload['Method'] + "Timestamp" + self.get_Timestamp() + "Ver" + self.payload['Ver']
        md5 = hashlib.md5()
        md5.update(info.encode())
        Sign = md5.hexdigest()
        return Sign
    
    def get_Params(self):
        """
        参数
        :return:
        """
        self.payload['Timestamp']=self.get_Timestamp()
        self.payload['Sign']=self.get_Sign()
        self.payload['BizParam']=self.data
        return self.payload
    
    def postJsonTotal(self):
        """
        post请求测试
        :return:
        """
        Payload=self.get_Params()
        r = requests.post("http://www.xindeng.wang/siteapi/api/xindeng", json=Payload)
        key=[key for key in r.json()['Data']['RetValue'].keys() if "Total" in key][0]
        return r.json()['Data']['RetValue'][key]
 
if __name__=="__main__":
    # res=xindeng("GetOrgStatisticsByOrderType","{\"entity\":\"{\\\"Id\\\":\\\"438\\\",\\\"Type\\\":0,\\\"PageIndex\\\":1,\\\"PageSize\\\":60}\"}").postJson()
    # data=res['Data']['RetValue']['Record']
    # print(len(data))
    res = xindeng("GetHomeDataMore",
                  "{\"entity\":\"{\\\"Type\\\":300,\\\"PageIndex\\\":1,\\\"PageSize\\\":2299,\\\"Spec\\\":2}\"}").get_Sign()
    print(res)