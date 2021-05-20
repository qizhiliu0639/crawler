# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 10:57:20 2020

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


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
base_url = 'http://www.gter.net/offer/'
filename = 'Gter_all_4.xls'
sleep = True
test_url = 'http://www.gter.net/offer/index/show.html?id=41691'

# login with cookies
def login(url):
    headers = {
        'User-Agent': user_agent,
        # How to get cookies?
        # Chrome: F12 and goto 'Network' page, login and check the Request Header in Name='bbs/', you can get cookie in Request Header section
        # Firefox: F12 and goto 'Network' page, login and check cookie page from name='bbs/', copy all cookies. You need to reformat it first from lots of 'xx:"yy"' to 'xx=yy; xxx=yyy'
    }
    session = requests.Session()
    response = session.get(url, headers=headers)
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


def get_cur_page(pager):
# =============================================================================
#     print("pager")
#     print(pager)
# =============================================================================
    cur_page_data = pager.find('strong')
    cur_page = "".join(cur_page_data.contents)
    return cur_page


def get_max_page(pager):
    max_page_data = pager.find('a', class_='last')
    max_page = "".join(max_page_data.contents)
    max_page = max_page.replace('... ', '')
    return max_page


def get_pager(soup):
    pager = soup.find('div', class_='pg')
    cur_page = get_cur_page(pager)
    next_page = str(int(cur_page) + 1)
    max_page = get_max_page(pager)
    page_info = [['当前页', '下一页', '最大页'], [cur_page, next_page, max_page]]
    return page_info


def get_posts(soup):
    posts_data = soup.find_all('tbody', id=re.compile('^normalthread_'))
    posts_info = [['标题', '帖子地址', '作者', '作者主页地址']]
    for post in posts_data:
        post_data = post.find('a', class_='s xst', href=True)
        post_title = "".join(post_data.contents)
        post_url = base_url + post_data['href']
        post_author = post.find('cite')
        if post_author.find('a', href=True) is None:
            post_author_name = '地里的匿名用户'
            post_author_url = ''
        else:
            post_author = post_author.find('a', href=True)
            post_author_name = "".join(post_author.contents)
            post_author_url = base_url + post_author['href']
        posts_info.append([post_title, post_url, post_author_name, post_author_url])
    return posts_info


def get_page_data(url):
    raw_html_info = get_html_info(url)
    if isinstance(raw_html_info, str):
        soup = bs(raw_html_info, 'html.parser')
        pager = get_pager(soup)
        posts = get_posts(soup)
        return pager, posts


def get_index(apply_info, th):
    return apply_info.index(th)

def get_offer_info(apply_table):
    offer_info = ['申请学校:','学位:','专业:','申请结果:','入学年份:','入学学期:','通知时间:','使用哪种语言成绩:']
    

def get_apply_data(post_url):
    apply_info = []
    raw_html_info = get_html_info(post_url)
    if isinstance(raw_html_info, str):
        soup = bs(raw_html_info, 'html.parser')
        #offer_summary = re.match(r'offer (.*?)')
        apply_table = soup.find_all('table', class_='cgtl mbm',summary=re.compile("offer"))
        #print(apply_table)
        offer_info = ['申请学校:','学位:','专业:','申请结果:','入学年份:','入学学期:','通知时间:','使用哪种语言成绩:']
        personal_info = ['IELTS:','LSAT:','TOEFL:','GRE:','PTE A:','GMAT:','sub:','本科学校档次:','本科专业:','本科成绩和算法、排名:','研究生专业:','研究生成绩和算法、排名:','研究生学校档次:','其他说明:','备注:']
        #print(len(apply_table))
        for i in range(len(apply_table)):
            offer_table = apply_table[i].find('tbody')
            #print(offer_table)
            offer_table = offer_table.find_all('tr')
            #print(offer_table)
            offer_line = ['' * n for n in range(len(offer_info))]
# =============================================================================
#             mark = soup.find('td', class_='t_f')
#             mark = "".join(mark.strings)
#             mark = mark.strip()
#             start = mark.find('\n\n')
#             end = mark.find('\n\n', start + 2)
#             mark = mark[start + 2:end]
# =============================================================================
            for tr in offer_table:
                th = tr.find('th')
                th = "".join(th.contents)
                #print(th)
                index = get_index(offer_info, th)

                td = tr.find('td')
                if td.find('a', href=True):
                    td = td.find('a', href=True)
                    #print(td)
                    td = td.get_text()
                    td = td.replace('\n', '').replace('\r', '')
# =============================================================================
#                     print('get_text td')
#                     print(type(td))
#                     print(td)
#                     
# =============================================================================
                    offer_line[index] = td
                else:
                    td = "".join(td.contents)
                    td = td.replace('\n', '').replace('\r', '').replace('  ', '')
# =============================================================================
#                     print('td')
#                     print(type(td))
#                     print(td)
# =============================================================================
                    offer_line[index] = td
            apply_info.append(offer_line)
        #print(apply_info)
        personal_table = soup.find('table', class_='cgtl mbm')
        personal_table = personal_table.find('tbody')
        #print(personal_table)
        personal_table = personal_table.find_all('tr')
        #print(personal_table)
        personal_line = ['' * n for n in range(len(personal_info))]
# =============================================================================
#         mark = soup.find('td', class_='t_f')
#         mark = "".join(mark.strings)
#         mark = mark.strip()
#         start = mark.find('\n\n')
#         end = mark.find('\n\n', start + 2)
#         mark = mark[start + 2:end]
#         index = get_index(personal_info, '备注:')
#         personal_line[index] = mark
# =============================================================================
        for tr in personal_table:
            th = tr.find('th')
            th = "".join(th.contents)
            #print(th)
            index = get_index(personal_info, th)

            td = tr.find('td')
            if td.find('a', href=True):
                td = td.find('a', href=True)
                #print(td)
                td = td.get_text()
                td = td.replace('\n', '').replace('\r', '').replace(' ','')
                personal_line[index] = td
            else:
                td = "".join(td.contents)
                td = td.replace('\n', '').replace('\r', '').replace(' ','')
                personal_line[index] = td
        #print(personal_line)
        print(apply_info)

        return apply_info,personal_line


def create_xls(filename):
    new_line = ['申请学校:','学位:','专业:','申请结果:','入学年份:','入学学期:','通知时间:','使用哪种语言成绩:','IELTS:','LSAT:','TOEFL:','GRE:','PTE A:','GMAT:','sub:','本科学校档次:','本科专业:','本科成绩和算法、排名:','研究生专业:','研究生成绩和算法、排名:','研究生学校档次:','其他说明:','备注:']
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
    create_xls(filename)
    for i in range(4145,4100,-1):
        url = 'http://www.gter.net/offer/index/show.html?id='+str(i)
        print(url)
        #apply_info,personal_info = get_apply_data(url)
        try:
            apply_info,personal_info = get_apply_data(url)
            for text in apply_info:
                ans = text+personal_info
                print(ans)
                write_xls_append(filename,ans)
            print('*********'+str(i)+'已爬完'+'******************')
        except :
            pass


if __name__ == '__main__':
    #print(get_apply_data(test_url))
    main()