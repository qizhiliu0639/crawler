# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 10:55:35 2021

@author: qizhiliu
"""


import re
import requests
from bs4 import BeautifulSoup as bs
import xlrd
import xlwt
from xlutils.copy import copy
import time
import random
from collections import OrderedDict
from urllib3 import encode_multipart_formdata



header = {
     
    }
    
def login(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "Content-Type" : "multipart/form-data; boundary=----WebKitFormBoundarykLF1C19CAYrGkB4k------WebKitFormBoundarykLF1C19CAYrGkB4kContent-Disposition: form-data; name='id'yKQ9mk4wXhmhs9q8MQPSBW1J4xItTgNqibBtb6ICueJ6iC72JYSnZqjftfTpvvaL9JXf2QzEHjHrBBdaaBMBI7yCDgFcQITPNWPDmjE3Njc~------WebKitFormBoundarykLF1C19CAYrGkB4k--",
        'Origin':'http://bbs.gter.net',
        'Referer':'http://bbs.gter.net/thread-2453259-1-1.html'
        # How to get cookies?
        # Chrome: F12 and goto 'Network' page, login and check the Request Header in Name='bbs/', you can get cookie in Request Header section
        # Firefox: F12 and goto 'Network' page, login and check cookie page from name='bbs/', copy all cookies. You need to reformat it first from lots of 'xx:"yy"' to 'xx=yy; xxx=yyy'
    }
    session = requests.Session()
    response = session.post(url, headers=headers)
    response.text.encode('utf-8')
    if response.status_code != 200:
        print('WARNING: Login Failed!!')
    return response

def get_params(url):
    f = {
        'id':(None,'gMzqqdyzyWYKcyBr2yI8U_Z-YAE7WeUA81QOPko06sCKGLWuJSBpj2U76C40Cyt0RkNs6HkaAtNhy2Acb3GAniKC-ox0p4g6WbGsZTk5M2Q~')
        }
    
    res = requests.post(url,data=f)
    #print(res.request.body)
    return res.json()

def get_html_info(url):
    response = login(url)
    if response.status_code == 200:
        return response.text
    else:
        return response.status_code

if "__main__" == __name__:
    url = "https://offer.gter.net/details"
    result = get_params(url)
    print(len(result['data']['collegelist']))
    #print(get_html_info(url))