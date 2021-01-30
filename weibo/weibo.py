# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 15:10:23 2020

@author: qizhiliu
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 13:11:58 2018

@author: qizhiliu
"""
import time
#import jieba


f=open(r'D:/University/crawler/Crawler-master/weibo/test9.txt','a+',encoding='utf-8')
import requests#requests是一个兼容的库
import json
#from lastLine import get_last_line
#import os
import re #解析不规则文本
from lxml import html
import math
#uid=2803301701
start=time.clock()
class weibo(object):
    
    def get_weibo(self,id,page_id,page):
        url='https://m.weibo.cn/api/container/getIndex?uid={}&type=uid&value={}&containerid={}&page={}'.format(id,id,page_id,page)
        print(url)
        response=requests.get(url)
        ob_json =json.loads(response.text)
        #print (response.text)
        #print (ob_json)
        list_cards=ob_json.get('data').get('cards')
        #list_text=ob_json.get('text')
        #print (list_text)
        #print(list_cards)
        return list_cards

    def get_comments(self,id,page):
        url='https://m.weibo.cn/api/comments/show?id={}&page={}'.format(id,page)
        response=requests.get(url)
        ob_json =json.loads(response.text)
        if len(ob_json)<3:
            list_comments=''
        else:
            list_comments=ob_json.get('data').get('data')
       # print (list_comments)
        
        return list_comments
    def main(self,id,page,page_id):
        list_cards  = self.get_weibo(id,page_id,page)
        #print (list_cards)
        for card in list_cards:
            if card.get('card_type')==9:  #等于9的微博才不是广告
                id = card.get('mblog').get('id')
                text= card.get('mblog').get('text')
                if text!='':
                    tree=html.fromstring(text)
                    text=tree.xpath('string(.)')                  
                    text=re.sub(r'回复.*?:','',text)
                    text=re.sub(r' ',' ',text)
                    text=re.sub(r"@.* ",'',text)
                    #text = jieba.cut(text)
                    text="".join(text)
                    #print(text)
                    #f.write("***")
                    #f.write('@@@微博')
                    if "Offer" in text:
                        print(text)
                        f.write(text)
                        f.write('\n')
                else:
                    pass
# =============================================================================
#                 b=1
#                 #tree=html.fromstring(text)
#                 #text=tree.xpath('string(.)')
#                 while True:
#                     list_comments=weibo.get_comments(id,b)#获取博文对应的评论界面
#                     b+=1
#                     if b+1%10==0:
#                         print('成功爬取100页评论')
#                     if len(list_comments)<1:
#                         break
#                     else:
#                         
#                         count_hotcomments = 1
#                         for comment in list_comments:
#                  #           user_id = comment.get('user_id')
#                   #          created_at = comment.get('created_at')
#                             #link_counts = comment.get('like_counts')
#                             text = comment.get('text')
#                             tree=html.fromstring(text)
#                             text=tree.xpath('string(.)')#用string过滤多余标签
#                             text=re.sub(r"@.* ",'',text)
#                             text=re.sub(r'回复.*?:','',text)
#                             #text=jieba.cut(text)                    
#                             text=" ".join(text)
# 
#                             
#                    #         name_user= comment.get('user').get('screen_name')
#                     #        source= comment.get('source')
#                      #       if source=='':
#                       #          source="未知"
#                             
#                             
#                            # f.write(str(count_hotcomments))
#                      #       f.write('|||')
#                             #f.write(name_user)
#                             #f.write(created_at)
#                          #   f.write(str(link_counts))
#                            # f.write(str(user_id))
#                             f.write (text)
#                             f.write('\n')
#                             f.flush()
#                             count_hotcomments +=1
#                # f.write ('====================')
# =============================================================================
            else :
              #  f.write('error')
                f.flush()
                    
                    

if __name__=='__main__':
    weibo=weibo()
    uid=1824301624
    d={}
    #f1=open(r'D:\test\ID2.txt','a+',encoding='utf-8')
    #fr = os.path.getsize(r'D:\test\ID2.txt')
    #if fr != 0 :
    #    a = int(get_last_line(r'D:\test\ID2.txt'))
    #    a += 1
    #print(a)
    #f1.close()
    while uid<1824301625:
        uid_str=str(uid)
        containerid=1076030000000000+uid
        f.write(str(uid))
        f.write('\n')

    #c=str(c)
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}'.format(uid,containerid)
        response=requests.get(url)
        ob_json =json.loads(response.text)
        list_cards=ob_json.get('data').get('cards')
        cardlistInfo=ob_json.get('data').get('cardlistInfo')
        time.sleep(5)
        #print(cardlistInfo)
        totalnumber=cardlistInfo.get('total')
        totalnumber=int(totalnumber)
        page_number=math.ceil(totalnumber/10)
        print(page_number)
        
    #print(b)
        if len(list_cards)<1:
            pass
        else :
            containerid=str(containerid)
            d[uid_str]=containerid
            print('成功')
     #       f=open(r'D:\test\ID2.txt','a+',encoding='utf-8')
      #      f.write(str(a))
       #     f.write('\n')
        #    f.close()
        
        if uid%100==1:
            print('已经爬取100条了')
            print('已经成功',len(d),'条')
 
        
        else:
            pass
        uid=uid+1
    #weibo.get_weibo('2803301701','1076032803301701')
        a=1
        while a <page_number:
            try:   
                weibo.main(uid,a,containerid)
                f.write(str(a))
                f.write('\n')
                a+=1
            except:
                pass
    #weibo.get_comments('2803301701',1)
print ('down')
f.close()
end = time.clock()
print('Running time: %s Seconds'%(end-start))