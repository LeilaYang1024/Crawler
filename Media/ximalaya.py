# coding: utf-8

"""
Created on:
@brief:喜马拉雅音频采集
@author: YangLei
@version: Python3
"""

import requests
import urllib.request
from tqdm import tqdm
import os
import time
from Ciphertext.ximalaya_xmsign import ximalayaSign
"""
xm-sign为反爬参数，通过调试获取

音频接口：https://fdfs.xmcdn.com/group63/M00/5F/63/wKgMaF0SRcSg42PRADlZpqP1G0Q574.m4a

"""

class XimalayaCrawler(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept': 'text/html,application/xhtml+ xml,application/xml;q = 0.9,image/webp,image/apng,*/*;q=0.8, application/signe-exchange;v = b3',
        'Host': 'www.ximalaya.com'
    }
    
    def __init__(self,albumId,page):
        self.albumId=albumId
        self.page=page
        
        
    def requestJson(self,pageNum):
        """
        分页请求音频数据
        :param pageNum:
        :return:
        """
        url=f"https://www.ximalaya.com/revision/play/album?albumId={self.albumId}&pageNum={pageNum}&sort=1&pageSize=30"
        self.headers['xm-sign']=ximalayaSign().getxm_sign()
        r=requests.get(url=url,headers=self.headers)
        return r.json()
    
    def get_resource(self,url,name):
        """
        下载音频资源（断点续传）
        :param url:
        :param name:
        :return:
        """
        #创建文件路径
        filepath="../Media/zdownload_data"
        filename=name
        
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        
        file="{}{}{}{}".format(filepath,os.sep,filename,'.wav')
        #下载资源
        self.download(url,file)
        return file
    
    def download(self,url,file):
        """
        断点续传下载
        :param url:
        :param file:
        :return:
        """
        r=requests.get(url,stream=True)
        #获取资源总大小
        filesize=int(r.headers['content-length'])
        
        #如果资源已存在，获取断点，否则从头
        if os.path.exists(file):
            start=os.path.getsize(file)
        else:
            start=0
            
        if start>=filesize:
            print("资源下载完成！")
            return filesize
        
        #组装请求headers
        header = {"Range": f"bytes={start}-{filesize}"}
        
        #进度条
        pbar = tqdm(total=filesize, initial=start,unit='B', unit_scale=True, desc=file)
        req = requests.get(url, headers=header, stream=True)
        
        with(open(file, 'ab')) as f:
            for chunk in req.iter_content(chunk_size=100):
                if chunk:
                    f.write(chunk)
                    pbar.update(100)
        pbar.close()
        print("资源下载完成")
        return filesize
    
    def getAlldata(self):
        """
        获取专辑数据
        :return:
        """
        i=0
        page=self.page
        for _ in range(1,page+1):
            json=self.requestJson(_)
            if json['data']['tracksAudioPlay'] != []:
                for data in json['data']['tracksAudioPlay']:
                    albumId=data['albumId']
                    albumName=data['albumName']
                    index=data['index']
                    trackId=data['trackId']
                    trackName=data['trackName']
                    src=data['src']
                    trackCoverPath="https:"+ data['trackCoverPath']
                    filename=albumId+trackId
                    filepath=self.get_resource(src,filename)
                    print(albumId,albumName,index,trackId,trackName,src,trackCoverPath,filepath)

if __name__=="__main__":
    XimalayaCrawler(albumId=6728872,page=3).getAlldata()
