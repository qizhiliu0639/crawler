import requests
from bs4 import BeautifulSoup
import codecs


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
base_url= 'https://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&page='

f = codecs.open("录取.txt", "wb", "utf-8")
# give a page number from 1-1000
for num in range(1,500):
    print (num)
    r= requests.get('https://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&page='+str(num), headers = headers)
    content = r.text
    soup = BeautifulSoup(content, "lxml")

    divs=soup.find_all(class_ = 'new')

    for div in divs:
        try:
            info = div.span.get_text()
            info=info.lower()
            if info is None:
                continue
            #filter schools & programs' informaton you want to get
            elif '19fall' in info and 'cs@usc' in info:
                print (info)
                f.write(info)
        except AttributeError:
            pass
        continue
f.close()

