# A dictionary based on the searching page of Bing Dic
# search specific tags in the HTML page and print out the meaning of words.
# requests, BeautifulSoup

import os
import requests
from bs4 import BeautifulSoup

def getHTML(url, para, kv):
    try:
        r = requests.get(url, para, headers = kv)
        r.raise_for_status()
        return r.text
    except:
        print('error while getting HTML page')
        return

def parsePage(demo):
    soup = BeautifulSoup(demo, 'html.parser')
    print(soup.find('div', 'hd_prUS').string, end = '    ')
    print(soup.find('div', 'hd_pr').string)
#pure English meaning
    if soup('div', 'each_seg') == [] or soup('div', 'se_lis') == []:
        seg = soup.find('div', {'id':'homoid'})
        for tag in seg('tr','def_row df_div1'):
            print(tag.find('div', 'pos pos1').string)
            for exp in tag('div', 'de_li1 de_li3'):
                print(exp.find('div', 'se_d').string, end = ' ')
                for i in exp('a'):
                    print (i.string, end = ' ')
                print('')
#Chinese and English meaning
    for seg in soup('div', 'each_seg'):
        print(seg.find('div', 'pos').string)
        for tag in seg('div', 'se_lis'):
            print(tag.find('div', 'se_d').string, end = ' ')
            if tag.find('span', 'gra'):
                print(tag.find('span','gra').string, end = ' ')
            if tag.find('span', 'comple'):
                print(tag.find('span', 'comple').string, end = ' ')
            print(tag.find('span', 'bil').string, end = ' ')
            print(tag.find('span', 'val').string)
    print('')

def main():
    os.chdir('/home/lzx/Study/English')
    record = open('test.txt', 'a')
    kv = {'user-agent':'Mozilla/5.0'}
    word = input('Enter the word, ! to quit.\n')
    while word != '!':
        para = {'q':word, 'go':'Search', 'qs':'ds', 'form':'Z9LH5'}
        demo = getHTML('https://cn.bing.com/dict/search', para, kv)
        try:
            parsePage(demo)
            record.write(word + '\n')
        except:
            print('error')
        word = input('Enter the word, ! to quit.\n')
    record.close()
    return
main()

