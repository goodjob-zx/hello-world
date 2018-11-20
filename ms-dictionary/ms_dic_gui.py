import requests
import webbrowser
from tkinter import *
from bs4 import BeautifulSoup

class UI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('Dictionary')
        screen_width, screen_height = self.getScreen()
        window_width = 0.6 * screen_width
        window_height = 0.8 * screen_height
        po_x = (screen_width - window_width) / 2
        po_y = (screen_height - window_height) / 2
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, po_x, po_y))
        
        self.en = Entry(self, font = 'calibri 20', bd = 0, width = 100)
        self.en.place(bordermode=OUTSIDE,
                      width = 0.85 * window_width,
                      height = 0.06 * window_height,
                      x = 0.01 * window_width,
                      y = 0.01 * window_height)
        self.en.bind('<Return>', self.Search_word)
        bu = Button(self, text = 'Search', command = self.Search_word, font = 'calibri 18')
        bu.place(bordermode=OUTSIDE,
                 width = 0.12 * window_width,
                 height = 0.06 * window_height,
                 x = 0.87 * window_width,
                 y = 0.01 * window_height) 
        
        self.text = Text(self, height = 28, width = 75, font = 'calibri 16', relief = FLAT)
        self.text.place(width = 0.98 * window_width,
                        height = 0.9 * window_height,
                        x = 0.01 * window_width,
                        y = 0.08 * window_height)
        self.text.insert(INSERT, '梁子轩的小词典\n英汉、汉英均支持')
        self.text.tag_add('init', '1.0', END)
        self.text.tag_config('init', foreground = '#E0E0E0', font = 'simkai, 45')
        self.text.config(state = DISABLED)
        
    def getScreen(self):
        return self.winfo_screenwidth(), self.winfo_screenheight()
    def Search_word(self, ev = None):
        p = Parse()
        if self.en.get() == '':
            return
        self.ReloadUI(p.get(self.en.get()))
        return
    def ReloadUI(self, result):
        mes1 = 'There is a connection error:('
        mes2 = 'Sorry, the word cannot be found, you can check it here:'
        if result == -1:
            self.InsertText(mes1)
            return
        if result == -2:
            self.url = 'https://cn.bing.com/dict/search?q=' + self.en.get() + '&go=Search&qs=ds&form=Z9LH5'
            self.InsertText(mes2 + '\n' + self.url)
            self.text.tag_add('err_mes', '2.0', END)
            self.text.tag_config('err_mes',foreground='blue',underline=True)
            self.text.tag_bind('err_mes','<Enter>', self.show_hand_cursor)
            self.text.tag_bind('err_mes','<Leave>', self.show_arrow_cursor)
            self.text.tag_bind('err_mes', '<Button-1>', self.click)
            self.en.delete(0, END)
            return
        word = self.en.get()
        self.text.config(state = NORMAL)
        self.text.delete(1.0, END)
        self.InsertText(word + '\n' + result)
        self.text.config(state = DISABLED)
        self.text.tag_add("word", "1.0", '1.%d' % len(word))
        self.text.tag_config('word', font = 'calibri 22 bold')
        self.en.delete(0, END)
    def InsertText(self, mes):
        self.text.config(state = NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, mes)
        self.text.config(state = DISABLED)
    def click(self, event):
        webbrowser.open(self.url)
    def show_hand_cursor(self, event):
        self.text.config(cursor='hand2')
    def show_arrow_cursor(self, event):
        self.text.config(cursor='xterm')

class Parse():
    def __init__(self):
        pass
    def get(self, word):
        self.word = word
        try:
            self.getHTML()
        except:
            return -1
        try:
            self.parsePage()
        except:
            return -2
        return self.result      
    def getHTML(self):
        kv = {'user-agent':'Mozilla/5.0'}
        para = {'q':self.word, 'go':'Search','qs':'ds', 'form':'Z9LH5'}
        r = requests.get('https://cn.bing.com/dict/search', para, headers = kv)
        self.text = r.text
    def parsePage(self):
        result = ''
        soup = BeautifulSoup(self.text, 'html.parser')
    #Chinese to English
        if u'\u4e00' <= self.word[0] <= u'\u9fff':
            seg = soup.find('div', {'id':'crossid'})
            for tag in seg('tr','def_row df_div1'):
                result += (tag.find('div', 'pos pos1').string + '\n')
                for exp in tag('div', 'de_li1 de_li3'):
                    result += (exp.find('div', 'se_d').string + ' ')
                    for i in exp('a'):
                        result += (i.string + ' ')
                    result += '\n'
            self.result = result
            return
    #English meaning
        result += (soup.find('div', 'hd_prUS').string + '    ')
        result += (soup.find('div', 'hd_pr').string + '\n')
    #pure English meaning
        if soup('div', 'each_seg') == [] or soup('div', 'se_lis') == []:
            seg = soup.find('div', {'id':'homoid'})
            for tag in seg('tr','def_row df_div1'):
                result += (tag.find('div', 'pos pos1').string + '\n')
                for exp in tag('div', 'de_li1 de_li3'):
                    result += (exp.find('div', 'se_d').string + ' ')
                    for i in exp('a'):
                        result += (i.string + ' ')
                    result += '\n'
            self.result = result
            return
    #Chinese and English meaning
        for seg in soup('div', 'each_seg'):
            result += (seg.find('div', 'pos').string + '\n')
            for tag in seg('div', 'se_lis'):
                result += (tag.find('div', 'se_d').string + ' ')
                if tag.find('span', 'gra'):
                    result +=(tag.find('span','gra').string + ' ')
                if tag.find('span', 'comple'):
                    result += (tag.find('span', 'comple').string + ' ')
                result += (tag.find('span', 'bil').string + ' ')
                result += (tag.find('span', 'val').string + '\n')
        result += '\n'
        self.result = result
        return

root = UI()
root.mainloop()
