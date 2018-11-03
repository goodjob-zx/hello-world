#Get data from kaola.com's searching page and show the name and price of the items.
#requests-bs4

import requests
from bs4 import BeautifulSoup

def getHTML(good):
    url = 'https://www.kaola.com/search.html?zn=top&key='+ good + '&pageSize=80&searchRefer=searchbutton&timestamp=1540992145506'
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except:
        print('error')
        return

def parsePage(text):
    plt = list()
    tlt = list()
    soup = BeautifulSoup(text, 'html.parser')
    for i in soup('span', 'cur'):
        plt.append(eval(i.contents[1]))
    for i in soup('h2'):
        if i.string == None:
            tmp_str = i.contents[0].string + i.contents[1]
            tlt.append(tmp_str)
        else:
            tlt.append(i.string)
    return (plt, tlt)

def printList(plt, tlt):
    tplt = '{:<5}{}\t{:5}'
    count = 1
    for i in plt:
        print(tplt.format(count, tlt[count - 1], i))
        count += 1

def main():
     good = input("Enter the item you wanna search:")
     printList(parsePage(getHTML(good))[0], parsePage(getHTML(good))[1])
     return

main()
