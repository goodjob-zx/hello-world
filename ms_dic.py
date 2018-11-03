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
    if soup.find('span', 'bil'):
        print(soup.find('span', 'bil').string, end = ' ')
        print(soup.find('span', 'val').string)
    print('\nE-E:', end = '')
    count = 1
    for i in soup('div', 'df_cr_w'):
        if i.contents[0].name == 'a':
            print('\n{}. '.format(count), end = '')
            count += 1
            for tag in i.children:
                print (tag.string, end = '')
    print('')
    return

def main():
    word = input()
    para = {'q':word, 'go':'Search', 'qs':'ds', 'form':'Z9LH5'}
    kv = {'user-agent':'Mozilla/5.0'}
    parsePage(getHTML('https://cn.bing.com/dict/search', para, kv))
    return
main()

