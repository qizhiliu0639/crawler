# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:25:21 2020

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


dir_url = 'https://forum.chasedream.com/'
# =============================================================================
# #MBA申请总结
# url_MBA = 'https://www.chasedream.com/list.aspx?cid=22'
# #Master申请总结
# url_Master = 'https://www.chasedream.com/list.aspx?cid=29'
# #PHD申请总结
# url_PHD = 'https://www.chasedream.com/list.aspx?cid=51'
# =============================================================================




#录取汇总
#北美MBA申请区
url_NorthAmerica_MBA = 'https://forum.chasedream.com/forum.php?mod=forumdisplay&fid=13&filter=typeid&typeid=31'
#欧洲MBA申请
url_European_MBA = 'https://forum.chasedream.com/forum.php?mod=forumdisplay&fid=36&filter=typeid&typeid=30'
#亚太MBA申请
url_Asia='https://forum.chasedream.com/forum.php?mod=forumdisplay&fid=16&filter=typeid&typeid=33'
#Master申请
url_Master = 'https://forum.chasedream.com/forum.php?mod=forumdisplay&fid=14&filter=typeid&typeid=70'
#PHD申请
url_PHD = 'https://forum.chasedream.com/forum.php?mod=forumdisplay&fid=61&filter=typeid&typeid=68'

test_url = 'https://forum.chasedream.com/forum.php?mod=viewthread&tid=1245571&extra=page%3D1%26filter%3Dtypeid%26typeid%3D68'

#base_url = url_NorthAmerica_MBA


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57'
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
    #max_page = get_max_page(pager)
    max_page = 8
    page_info = [['当前页', '下一页', '最大页'], [cur_page, next_page, max_page]]
    return page_info


def get_posts(soup):
    posts_data = soup.find_all('td',{'class':'icn'})
    #print(posts_data)
    post=re.findall(r'href="(.*?)target',str(posts_data))
    #print(post)
    return post

def get_title(soup):
    posts_data = soup.find_all('tbody', id=re.compile('^normalthread_'))
    return_post = []
    #print(posts_data)
    for post in posts_data:
        post_data = post.find('a', class_='xst', href=True)
        #print(type(post_data))
        posts =re.findall(r'>(.*?)</a>',str(post_data))
        return_post.append(posts[0])
    #print(return_post)
    return return_post

def get_page_data(url):
    raw_html_info = get_html_info(url)
    if isinstance(raw_html_info, str):
        soup = bs(raw_html_info, 'html.parser')
        #print(soup)
        pager = get_pager(soup)
        #print(pager)
        posts = get_posts(soup)
        
        title = get_title(soup)
        return pager, posts,title


def get_index(apply_info, th):
    return apply_info.index(th)


def get_apply_data(post_url):
    raw_html_info = get_html_info(post_url)
    soup = bs(raw_html_info, 'html.parser')
    data = soup.find('td',{'class':'t_f'})
    data = data.get_text()
    #print(data)
    return data

def remove_switchline(data):
    return re.sub("[\n]+","", data)

def main():
    f=open(r'D:/University/crawler/Crawler-master/ChaseDream/Asia.txt','a+',encoding='utf-8')
    cur_page = 0
    next_page = cur_page + 1
    max_page =  8
    #create_xls(filename)
    while cur_page < max_page-1:
        try:
            page,posts,title = get_page_data(url_Asia + '&page=' + str(next_page))
            max_page = int(page[1][2])
            print('max_page')
            print(max_page)
            cur_page = int(page[1][0])
            print('cur_page')
            print(cur_page)
            next_page = int(page[1][1])
            print('next_page')
            print(next_page)                              
            for i in range(0,len(posts)):
                post = posts[i].replace(';','&',10)
                url = dir_url+post
                data = get_apply_data(url)
                #print(data)
                data = remove_switchline(data)
                #print(data)
                f.write('\n')
                f.write("**************************分割线*****************************")
                f.write('\n')
                f.write(title[i])
                f.write('\n')
                f.write(data)
                print('已完成'+url+'的爬取')
                #time.sleep(random.randint(1,3))
        except:
            
            
            pass
            
        
        print('****************************已完成'+str(cur_page)+'页的爬取************************')
    f.close()
        
        
# =============================================================================
#     for post in posts:
#         post = post.replace(';','&',10)
#         url = dir_url+post
#         print(url)
#         data = get_apply_data(url)
#         data = remove_switchline(data)
#         f.write('\n')
#         f.write("**************************分割线*****************************")
#         f.write('\n')
#         f.write(data)
#     f.close()
# =============================================================================
    
if __name__ == "__main__":
   main()