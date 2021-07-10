# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 22:14:51 2021

@author: qizhiliu
"""
import requests
from bs4 import BeautifulSoup as bs
import xlrd
import xlwt
from xlutils.copy import copy
import time
import random
import re

def login(url):
    session = requests.Session()
    response = session.get(url)
    response.text.encode('utf-8')
    if response.status_code != 200:
        print('WARNING: Login Failed!!')
    return response

def get_html_info(url):
    response = login(url)
    if response.status_code == 200:
        return response.text
    else:
        return response.status_code
    
def get_apply_data(post_url):
    apply_info = []
    raw_html_info = get_html_info(post_url)
    if isinstance(raw_html_info, str):
        soup = bs(raw_html_info, 'html.parser')
        #offer_summary = re.match(r'offer (.*?)')
        apply_table = soup.find_all('script')
        res = str(apply_table)
        #print(res)
        #ret_test = re.search(r'api(.*)net',res).group(1)
        #print(ret_test)
        ret = re.search("id:'(.*)'",res).group(1)
        return ret

def get_params(identifier):
    url = "https://offer.gter.net/details"
    f = {
        'id':(None,identifier)
        }
    
    res = requests.post(url,data=f)
    #print(res.request.body)
    main_res = res.json()
    #print(main_res['data']['info'])
    offer_number = len(main_res['data']['collegelist'])
    d = {'申请学校:':"",'学位:':"",\
         '专业:':"",'申请结果:':"",'入学年份:':"",\
         '入学学期:':"",'通知时间:':"",\
         'IELTS:':"",\
         'TOEFL:':"",'GRE:':"",'GMAT:':"",\
         '本科学校档次:':"",'本科专业:':"",'本科成绩和算法、排名:':"",\
         '研究生专业:':"",'研究生成绩和算法、排名:':"",'研究生学校档次:':"",\
         '其他说明:':"",'备注:':""}
    line = ['申请学校:','学位:','专业:','申请结果:','入学年份:','入学学期:','通知时间:','IELTS:','TOEFL:','GRE:','GMAT:','本科学校档次:','本科专业:','本科成绩和算法、排名:','研究生专业:','研究生成绩和算法、排名:','研究生学校档次:','其他说明:','备注:']
    apply_line = []
    for i in range(offer_number):
        
        d['申请学校:'] = main_res['data']['collegelist'][i]['schoolname']
        d['学位:'] = main_res['data']['collegelist'][i]['degree']
        d['专业:'] = main_res['data']['collegelist'][i]['professional']
        d['申请结果:'] = main_res['data']['collegelist'][i]['apply_results']
        d['入学年份:'] = main_res['data']['collegelist'][i]['year']
        d['入学学期:'] =  main_res['data']['collegelist'][i]['semester']
        d['通知时间:'] = main_res['data']['collegelist'][i]['noticedate']
        d['IELTS:'] = str(main_res['data']['offeruser']['ielts'])
        d['GMAT:'] = str(main_res['data']['offeruser']['gmat'])
        d['TOEFL:'] = str(main_res['data']['offeruser']['gre'])
        d['本科学校档次:'] = main_res['data']['offeruser']['undergraduate'].get('raw_school',"") if main_res['data']['offeruser']['undergraduate'] else None
        d['本科专业:'] = main_res['data']['offeruser']['undergraduate'].get('subject',"") if main_res['data']['offeruser']['undergraduate']  else None 
        d['本科成绩和算法、排名:'] = main_res['data']['offeruser']['undergraduate'].get('gpa',"") if main_res['data']['offeruser']['undergraduate'] else None
        d['研究生学校档次:'] = main_res['data']['offeruser']['graduate'].get('raw_school',"") if main_res['data']['offeruser']['graduate'] else None
        d['研究生专业:'] = main_res['data']['offeruser']['graduate'].get('subject',"") if main_res['data']['offeruser']['graduate'] else None
        d['研究生成绩和算法、排名:'] = main_res['data']['offeruser']['graduate'].get('gpa',"") if main_res['data']['offeruser']['graduate'] else None
        d['其他说明:'] = main_res['data']['info']['background'] if main_res['data']['info']['background'] else None
        d['备注:'] = main_res['data']['info']['content'] if main_res['data']['info']['content'] else None
        temp = ["" for _ in range(len(line))]
        for i in range(len(line)):
            temp[i] = d[line[i]]
        #print(temp)
        apply_line.append(temp)
    print(apply_line)
    return apply_line
        

def create_xls(filename):
    new_line = ['申请学校:','学位:','专业:','申请结果:','入学年份:','入学学期:','通知时间:','IELTS:','TOEFL:','GRE:','GMAT:','本科学校档次:','本科专业:','本科成绩和算法、排名:','研究生专业:','研究生成绩和算法、排名:','研究生学校档次:','其他说明:','备注:']
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
    filename = 'Gter_all_new.xls'
    #create_xls(filename)
    for i in range(42976,41650,-1):
        url = 'http://www.gter.net/offer/index/show.html?id='+str(i)
        print(url)
        #apply_info,personal_info = get_apply_data(url)
        try:
            ide = get_apply_data(url)
        
            apply_info = get_params(ide)
            for text in apply_info:
                ans = text
            
                #print(type(ans))
                write_xls_append(filename,ans)
            print('*********'+str(i)+'已爬完'+'******************')
        except:
            continue
if "__main__" == __name__:
    #user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    '''
    test_url = 'http://www.gter.net/offer/index/show.html?id=43154'
    #rea = re.search(r'bbs(.*)net',test_url).group(0)
    #print(rea)
    try:
        ide = get_apply_data(test_url)
    except:
        pass
    get_params(ide)
    '''
    main()