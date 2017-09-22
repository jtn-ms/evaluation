#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 21:34:39 2017

@author: frank
"""

#from scrapy.selector import Selector  
import scrapy
import json
#from scrapy import log  
from photo.items import BaiduImageItem  
  
  
class BaiduImageSpider(scrapy.Spider):  
    name = "BaiduImageSpider"  
    start_urls = []#'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=美女&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=美女&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn=%d' %i for i in range(0,901,30)  

    def __init__(self, keyword, se = 'bing', pages = 901,  *args, **kwargs):
        super(BaiduImageSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword.lower()
        #self.searchEngine = se.lower()
        #self.selector = SearchEngineResultSelectors[self.searchEngine]
        #pageUrls = searResultPages(keyword, se, int(pages))
        for i in range(0,int(pages),30):
            url='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%s&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=%s&pn=%d' % (keyword,keyword,keyword,i)
            self.start_urls.append(url)
            
    def parse(self, response):
        imgs = json.loads(response.body)['data']
        for img in imgs:
            item = BaiduImageItem()
            try:
                item['IMG_URL'] = [img['middleURL']]
                yield item
            except Exception as e:
                print(e)
            
            