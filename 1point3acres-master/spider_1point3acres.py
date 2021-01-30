import requests
from bs4 import BeautifulSoup
import csv


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
base_url= 'https://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&page='

f = open("0317_录取.csv", "w")
writer = csv.writer(f)
writer.writerow(['background','link'])
# give a page number from 1-1000
for num in range(1,20):
    print (num)
    r= requests.get('https://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&page='+str(num), headers = headers)
    print('https://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&page='+str(num))
    content = r.text
    soup = BeautifulSoup(content, "lxml")

    divs=soup.find_all(class_ = 'new')

    for div in divs:
        try:
            s = str(div).split('\"')
            link = ('www.1point3acres.com/bbs/'+s[7])
            for i in range(len(link)-10):
                if link[i]=='&':
                    link = link[:i+1]+link[i+5:]
            info = div.span.get_text()
            info=info.lower()
            if info is None:
                continue
            elif ("本科top30" in info or "本科top15" in info):
                writer.writerow([(info),link])
            else:
                print(info)
        except AttributeError:
            pass
        continue
f.close()

