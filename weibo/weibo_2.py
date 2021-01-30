# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 11:06:02 2020

@author: qizhiliu
"""
'''
爬取微博的流程：因为微博调用接口的时候需要cookie,所以我们要用webdriver来登录微博获取cookie,微博的cookie有效期应该蛮长的，我设置过期时间6hours,未过期则去本地读取，否则重新登录获取cookie
获取cookie后则分析微博网页端的请求，找到相应接口和参数，然后去请求我们要的数据。
这个例子是去获取微博里的图片，例子爬取的微博是我伦的官方账号：MRJ台灣官方
运行代码脚本需要加5个参数 分别为 1.微博账号 2.微博密码 3.要爬取的账号的个性域名（无个性域名则输入 u/+微博id）4.要爬取的账号的ID 5.爬取页数
如：python weibo_crawler.py username password mrj168 1837498771 5
'''
from selenium import webdriver
import time
import requests
import json
from bs4 import BeautifulSoup
import os

request_params = {"ajwvr":"6","domain":"100505","domain_op":"100505","feed_type":"0","is_all":"1","is_tag":"0","is_search":"0"}
profile_request_params = {"profile_ftype":"1","is_all":"1"}

weibo_url = "http://weibo.com/"
requset_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?"


cookie_save_file = "cookie.txt"#存cookie的文件名
cookie_update_time_file = "cookie.txt"#存cookie时间戳的文件名
image_result_file = "image_result.md"#存图片结果的文件名


username = '18708130298'##你的微博账号
password = '2220718-lzqj'##你的微博密码

person_site_name = "u/1824301624"#想爬取的微博号的个性域名 无个性域名则换成: u/+"微博id" 如 u/12345678
weibo_id = "18243016241"#微博id可以在网页端打开微博，显示网页源代码，找到关键词$CONFIG['oid']='1837498771'; 
page_size = 20#你要爬取的微博的页数






headers = {#User-Agent需要根据每个人的电脑来修改
        'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
		'Cache-Control':'no-cache',
		'Connection':'keep-alive',
		'Content-Type':'application/x-www-form-urlencoded',
		'Host':'weibo.com',
		'Pragma':'no-cache',
		'Referer':'http://weibo.com/u/3278620272?profile_ftype=1&is_all=1',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		'X-Requested-With':'XMLHttpRequest'
        }

def get_timestamp():#获取当前系统时间戳
    try:
        tamp = time.time()
        timestamp = str(int(tamp))+"000"
        print (timestamp)
        return timestamp
    except Exception:
        pass
    finally:
        pass
    
def get_cookie_update_time_from_txt():#获取上一次cookie更新时间
    try:
        f = open(cookie_update_time_file)
        lines = f.readlines()
        cookie_update_time = lines[0]
        print (cookie_update_time)
        return cookie_update_time
    except Exception:
        pass
    finally:
        pass

def write_image_urls(image_list):
    try:
        f= open(image_result_file,'a+')
        for x in range(len(image_list)):
        	image = image_list[x]
        	show_image = "![]("+image+")"
        	f.write(show_image.encode("utf-8"))
        	f.write('\n')
        f.close()
    except Exception:
        pass
    finally:
        pass


def get_object_weibo_by_weibo_id_and_cookie(weibo_id,person_site_name,cookie,pagebar,page):#通过微博ID和cookie来调取接口
	try:
		headers["Cookie"] = cookie
		headers['Referer'] = weibo_url+person_site_name+"?profile_ftype=1&is_all=1"
		request_params["__rnd"] = get_timestamp()
		request_params["page"] = page
		request_params["pre_page"] = page
		request_params["pagebar"] = pagebar
		request_params["id"] = "100505"+weibo_id
		request_params["script_uri"] = "/"+person_site_name
		request_params["pl_name"] = "Pl_Official_MyProfileFeed__22"
		request_params["profile_ftype"] = 1
		response = requests.get(requset_url,headers=headers,params=request_params)
		print (response.url)
		html =  response.json()["data"]
		return html
	except Exception:
		pass
	finally:
		pass


def get_object_top_weibo_by_person_site_name_and_cookie(person_site_name,cookie,page):#每一页顶部微博
	try:
		profile_url = weibo_url+person_site_name+"?"
		headers["Cookie"] = cookie
		profile_request_params["page"] = page
		response = requests.get(profile_url,headers=headers,params=profile_request_params)
		print (response.url)
		html = response.text
		soup = BeautifulSoup(html,"html.parser")
		script_list = soup.find_all("script")
		script_size = len(script_list)
		print ("script_size:"+str(script_size))
		tag = 0
		for x in range(script_size):
			if "WB_feed WB_feed_v3 WB_feed_v4" in str(script_list[x]):
				tag = x
		print ("tag:"+str(tag))
		# print script_list[script_size-1]
		html_start = str(script_list[tag]).find("<div")
		html_end = str(script_list[tag]).rfind("div>")
		# print str(script_list[tag])[html_start:html_end+4]
		return str(str(script_list[tag])[html_start:html_end+4])
	except Exception:
		pass
	finally:
		pass




cookie = 'SINAGLOBAL=282671935354.9589.1573394474818; UOR=www.techweb.com.cn,widget.weibo.com,www.bing.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFGsoWN_llWFei0yAqaWWYw5JpX5KMhUgL.Fo-0SK5p1Ke71hz2dJLoIpYLxKnL1K5L12eLxK-LBo5L12qLxK-LBK-L1hM7Soe4; ALF=1639711365; SSOLoginState=1608175366; SCF=AiY63I_2z5w3qFbiNxJA-dym2DfguDa_NEBgkMk7c5G0HYmAVIeQJNZ_f5J1zyyk3iTb-GHDFUYrsoFWhLCZbE4.; SUB=_2A25y3r9XDeRhGeNN7lIQ-S3Mwz6IHXVRrZefrDV8PUNbmtANLU38kW9NSbjQ8Q1lDZyND6laGjld7d_4mJXqNOGo; wvr=6; _s_tentry=login.sina.com.cn; Apache=3203475290507.134.1608175370431; ULV=1608175370453:19:2:1:3203475290507.134.1608175370431:1607409369880; wb_view_log_5350193082=1920*10801.2000000476837158; webim_unReadCount=%7B%22time%22%3A1608198074161%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'
for x in range(1,page_size+1):
	profile_html = get_object_top_weibo_by_person_site_name_and_cookie(person_site_name,cookie,x)
	for y in range(0,2):#有两次下滑加载更多的操作
		print ("pagebar:"+str(y))
		html = get_object_weibo_by_weibo_id_and_cookie(weibo_id,person_site_name,cookie,y,x)
