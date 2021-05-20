# -*- coding: utf-8 -*-
"""
Created on Thu May 20 12:33:43 2021

@author: qizhiliu
"""
import os
import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import urllib
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import xlrd
import xlwt
from xlutils.copy import copy




def getofferurl(url):
    res = []
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome_.exe"
    driver = webdriver.Chrome(chrome_options=options)

    #url = "https://www.compassedu.hk/offer_12"
    driver.get(url)
    def execute_times(times):
        for i in range(times + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
    execute_times(100)

    soup = bs(driver.page_source, features="lxml")
    class_link = r"trtd all(.*?) target"
    contain = soup.find_all("a", {"class": re.compile(r'(.*?)all aif(.*?)')})
    contain_1 = soup.find_all("a", {"class": re.compile(r'(.*?)lazya all hif')})
    for i in contain:
        #print(i['href'])
        url_offer = i['href']
        #print(url_offer[2:])
        res.append('https://'+url_offer[2:])

    for j in contain_1:
        url_offer = j['href']
        #print(url_offer[2:])
        res.append('https://'+url_offer[2:])
    return res

def getinfo(url):
    html = urlopen(url).read()
    soup = bs(html, features="lxml")
    name = soup.find("div", {"class": 'su-title'})
    name = name.get_text().split()
    print(name)
    contain = soup.find_all("div", {"class": 'spant'})
    contain_1 = soup.find_all("div", {"class": 'spani'})
    title = []
    subinfo = []
    for i in contain :
        subtitle = i.get_text().strip()
        title.append(subtitle)
    for j in contain_1:
        info = j.get_text().replace(" ","")
        info = info.replace("\n","")
        subinfo.append(info)
    #print(title)
    #print(subinfo)
    d = dict(zip(title,subinfo))
    res = [name[0]]
    ind = 0
    new_line = ['学生姓名','本科学校','本科专业','录取学校','录取专业','背景资料','主要经历']
    for i in new_line:
        if i in d:
            res.append(d[i])
        else:
            res.append('')
    #print(res)
    return res

def create_xls(filename):
    new_line = ['Title','学生姓名','本科学校','本科专业','录取学校','录取专业','背景资料','主要经历']
    wb = xlwt.Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    for i in range(len(new_line)):
        sheet1.write(0, i, new_line[i])
    wb.save(filename)
    print('*INFO: xls file has created.')


def write_xls_append(filename, new_line):
    workbook = xlrd.open_workbook(filename)
    sheets = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(sheets[0])
    exist_rows = worksheet.nrows
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(0)
    for i in range(len(new_line)):
        new_worksheet.write(exist_rows, i, new_line[i])
    new_workbook.save(filename)
    print('INFO: Append new line. CurLine:' + str(exist_rows))
    
def main():
    filename = 'offer.xls'
    create_xls(filename)
    #region_url = ['https://www.compassedu.hk/offer_12','https://www.compassedu.hk/offer_11','https://www.compassedu.hk/offer_7','https://www.compassedu.hk/offer_10','https://www.compassedu.hk/offer_9']
    url = 'https://www.compassedu.hk/offer_9'
    offer_url = getofferurl(url)
    for i in offer_url:
        info_list = getinfo(i)
        write_xls_append(filename, info_list)
    print('Done')
        
main()


'''

re = getofferurl("https://www.compassedu.hk/offer_12")
for j in re:
    print(j)
'''
#getinfo('https://www.compassedu.hk/newst_15499')
#getinfo('https://www.compassedu.hk/newst_15543')