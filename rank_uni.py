#Get data from zuihaodaxue.cn and print the list of universities in China.
#requests-bs4

import requests
from bs4 import BeautifulSoup
import bs4
def getData():
    try:
        r = requests.get("http://www.zuihaodaxue.cn/zuihaodaxuepaiming2018.html")
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error in getting data.")

def fillList(HTMLdata):
    soup = BeautifulSoup(HTMLdata, 'html.parser')
    ulist = list()
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string])
    return ulist

def printList(final):
    ulist = open('ulist.txt', 'w+')
    tplt = '{0:^10}\t{1:{3}^12}\t{2:^10}'
    ulist.write(tplt.format('排名', '大学名称', '省份', chr(12288)))
    ulist.write("\n")
    for i in final:
        ulist.write(tplt.format(i[0], i[1], i[2], chr(12288)))
        ulist.write("\n")

def main():
    printList(fillList(getData()))

main()

