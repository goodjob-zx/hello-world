import requests
from bs4 import BeautifulSoup
class Parse():
    def __init__(self):
        pass
    def get(self, word):
        self.word = word
        try:
            self.getHTML()
        except:
            #network error
            return -1
        try:
            self.parsePage()
        except:
            return -2
        if self.result[0] == '' and self.result[1] == '' and self.result[2] == '':
            return -2
        return self.result
    def getHTML(self):
        kv = {'user-agent':'Mozilla/5.0'}
        para = {'q':self.word, 'go':'Search','qs':'ds', 'form':'Z9LH5'}
        r = requests.get('https://cn.bing.com/dict/search', para, headers = kv)
        self.text = r.text
    def parsePage(self):
        result = ['', '', '', '', '']
#first: ch&en or translate from ch to en
#second: en
#third: ch
#last: the word, sometimes the searching word is not the word entered
#this is necessary
        self.soup = BeautifulSoup(self.text, 'html.parser')
        result[-1] = self.soup.find('strong').string
        if u'\u4e00' <= self.word[0] <= u'\u9fff':
            result[1] = self.ch2en()
            self.result = result
            return
        try:
            result[-2] += (self.soup.find('div', 'hd_prUS').string + '    ')
            result[-2] += (self.soup.find('div', 'hd_pr').string + '\n')
        except:
            pass
        try:
            result[0] += self.en2mix()
        except:
            pass
        try:
            result[1] += self.en2en()
        except:
            pass
        try:
            result[2] += self.en2ch()
        except:
            pass
        self.result = result
    def ch2en(self):
        result = ''
        seg = self.soup.find('div', {'id':'crossid'})
        for tag in seg('tr','def_row df_div1'):
            result += (tag.find('div', 'pos pos1').string + '\n')
            for exp in tag('div', 'def_fl'):
                for i in exp.children:
                    if i.attrs == {'class':['de_li1', 'de_li3']}:
                        result += i.find('div', 'se_d').string + ' '
                        for single_word in i('a'):
                            result += (single_word.string + ' ')
                    result += '\n'
        result += '\n'
        return result
    def en2mix(self):
        result = ''
        for seg in self.soup('div', 'each_seg'):
            result += (seg.find('div', 'pos').string + '\n')
            for tag in seg('div', 'se_lis'):
                result += (tag.find('div', 'se_d').string + ' ')
                for gra in tag('span', 'gra'):
                    result += (gra.string + ' ')
                for comple in tag('span', 'comple'):
                    result += (comple.string + ' ')
                for bv in tag('span'):
                    if bv.attrs == {'class':['bil']} or bv.attrs == {'class':['val']}:
                        result += bv.string + chr(12288)
                    elif bv.attrs == {'class':['val', 'label']}:
                        for label in bv.children:
                            result += label.string
                result += '\n'
            result += '\n'
        return result
    def en2en(self):
        result = ''
        seg = self.soup.find('div', {'id':'homoid'})
        for tag in seg('tr','def_row df_div1'):
            result += (tag.find('div', 'pos pos1').string + '\n')
            for exp in tag('div', 'def_fl'):
                for i in exp.children:
                    if i.attrs == {'class':['de_li1', 'de_li3']}:
                        result += i.find('div', 'se_d').string + ' '
                        for single_word in i('a'):
                            result += (single_word.string + ' ')
                    result += '\n'
        result += '\n'
        return result
    def en2ch(self):
        result = ''
        seg = self.soup.find('div', {'id':'crossid'})
        for tag in seg('tr','def_row df_div1'):
            result += (tag.find('div', 'pos pos1').string + '\n')
            for exp in tag('div', 'def_fl'):
                for i in exp.children:
                    if i.attrs == {'class':['de_li1', 'de_li3']}:
                        result += i.find('div', 'se_d').string + ' '
                        result += i.find('span', 'p1-1').string + '\n'
            result += '\n'
        return result
