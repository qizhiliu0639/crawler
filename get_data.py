# -- coding:utf-8 --
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import csv
for i in range(23224,23225):
    try:
        file_name = str(i)+".txt"
        with open(file_name,"w") as f:
            base = "http://www.gter.net/offer/index/show.html?id=" + str(i)
            url = base
            html = urlopen(url).read()
            soup = BeautifulSoup(html, features="lxml")
            contain = soup.find_all("div", {"class": 'typeoption'})
            for s in contain:
                txt = str(s.get_text())
                f.write(txt)
            print(i,"done")
            f.close()
    except:
        pass
    continue
