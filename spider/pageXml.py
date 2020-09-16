# _author:'louqiang'
# __time__ = '2020/9/16 5:39 PM'
# !/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from lxml import etree

url = "http://www.zhongshi.net/html/category/zhuanye/page/{} "

newUrl = ''


def pageXml():
    for page in range(1, 1551):
        newUrl = url.format(page)
        response = requests.get(newUrl)
        html = etree.HTML(response.text)
        dataPid = html.xpath('//body/section/div/div/article/header/h2//a/@href')
        print(dataPid)


pageXml()
