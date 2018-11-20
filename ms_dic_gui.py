import requests
import webbrowser
from tkinter import *
from bs4 import BeautifulSoup

class UI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('Dictionary')
        
        #self.rclick = RightClick(self)
        #self.bind('<Button-3>', self.rclick.popup)
        screen_width, screen_height = self.getScreen()
        window_width = 0.6 * screen_width
        window_height = 0.8 * screen_height
        po_x = (screen_width - window_width) / 2
        po_y = (screen_height - window_height) / 2
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, po_x, po_y))
        
        self.en = Entry(self, font = 'calibri 18', bd = 0, width = 100)
        self.en.place(bordermode=OUTSIDE,
                      width = 0.85 * window_width,
                      height = 0.06 * window_height,
                      x = 0.01 * window_width,
                      y = 0.01 * window_height)
        self.en.bind('<Return>', self.Search_word)
        bu = Button(self, text = 'Search', command = self.Search_word, font = 'calibri 20')
        bu.place(bordermode=OUTSIDE,
                 width = 0.12 * window_width,
                 height = 0.06 * window_height,
                 x = 0.87 * window_width,
                 y = 0.01 * window_height) 
        
        self.text = Text(self, height = 28, width = 75, font = '微软雅黑 14', relief = FLAT)
        self.text.place(width = 0.98 * window_width,
                        height = 0.9 * window_height,
                        x = 0.01 * window_width,
                        y = 0.08 * window_height)
        self.text.insert(INSERT, '梁子轩的小词典\n英汉、汉英均支持～')
        self.text.tag_add('init', '1.0', END)
        self.text.tag_config('init', foreground = '#E0E0E0', font = '楷体 60')
        self.text.config(state = DISABLED)
        
    def getScreen(self):
        return self.winfo_screenwidth(), self.winfo_screenheight()
    def Search_word(self, ev = None):
        p = Parse()
        if self.en.get() == '':
            return
        self.result = p.get(self.en.get())
        self.ReloadUI()
        return
    def ReloadUI(self):
        mes1 = 'There is a connection error:('
        mes2 = 'Sorry, the word cannot be found, you can check it here:'
        if self.result == -1:
            self.InsertText(mes1)
            return
        if self.result == -2:
            self.url = 'https://cn.bing.com/dict/search?q=' + self.en.get() + '&go=Search&qs=ds&form=Z9LH5'
            self.InsertText(mes2 + '\n' + self.url)
            self.text.tag_add('err_mes', '2.0', END)
            self.HyperText('err_mes')
            self.text.tag_bind('err_mes', '<Button-1>', self.click)
            self.en.delete(0, END)
            return
        word = self.result[-1]
        self.text.config(state = NORMAL)
        self.text.delete(1.0, END)
        self.Check()
        if self.result[1] == '':
            self.InsertText(word + '\n' + self.result[0])
        else:
            self.InsertText(word + '\n'+ self.result[0])
            self.text.config(state = NORMAL)
            self.text.insert(INSERT, 'more')
            self.text.config(state = DISABLED)
            self.text.tag_add('more', 'end-5c', 'end')
            self.HyperText('more')
            self.text.tag_bind('more', '<Button-1>', self.More)
        self.text.tag_add("word", "1.0", '1.%d' % len(word))
        if u'\u4e00' <= word[0] <= u'\u9fff':
            self.text.tag_config('word', font = '微软雅黑 22')
        else:
            self.text.tag_config('word', font = 'tahoma 24 bold')
        self.en.delete(0, END)
        
    def InsertText(self, mes):
        self.text.config(state = NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, mes)
        self.text.config(state = DISABLED)
    def Check(self):
        for i in self.result[0]:
            if u'\u0000' <= i <= u'\uffff':
                continue
            else:
                self.result[0] = self.result[0].replace(i, chr(12288))
        return
    def HyperText(self, name):
        self.text.tag_config(name,foreground='blue',underline=True)
        self.text.tag_bind(name,'<Enter>', self.show_hand_cursor)
        self.text.tag_bind(name,'<Leave>', self.show_arrow_cursor)
    def More(self, event):
        self.text.config(state = NORMAL)
        self.text.insert('end-5c', self.result[2] + self.result[1])
        self.text.delete('end-5c', END)
        self.text.config(state = DISABLED)
    def click(self, event):
        webbrowser.open(self.url)
    def show_hand_cursor(self, event):
        self.text.config(cursor='hand2')
    def show_arrow_cursor(self, event):
        self.text.config(cursor='xterm')


#class RightClick:
    #def __init__(self, master):
        #self.aMenu = Menu(master, tearoff=0, font = 'calibri 16', cursor = 'left_ptr')
        #self.aMenu.add_command(label = 'Cut', command = self.Copy_to_clipboard)
        #self.aMenu.add_command(label = 'Copy', command = self.Cut_to_clipboard)
        #self.aMenu.add_command(label = 'Paste', command = self.Paste_from_clipboard)
        #self.aMenu.add_separator()
        #self.aMenu.add_command(label = 'Hello', command= self.Hello)
    #def Copy_to_clipboard(self):
        #pass
    #def Cut_to_clipboard(self):
        #pass
    #def Paste_from_clipboard(self):
        #pass
    #def popup(self, event):
        #self.aMenu.post(event.x_root, event.y_root)


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
        result = ['', '', '', '']
        self.soup = BeautifulSoup(self.text, 'html.parser')
        result[-1] = self.soup.find('strong').string
        if u'\u4e00' <= self.word[0] <= u'\u9fff':
            result[0] = self.ch2en()
            self.result = result
            return
        result[0] += (self.soup.find('div', 'hd_prUS').string + '    ')
        result[0] += (self.soup.find('div', 'hd_pr').string + '\n')
        if self.soup('div', 'each_seg') == [] or self.soup('div', 'se_lis') == []:
            result[0] += self.en2en()
            self.result = result
            return
        result[0] += self.en2mix()
        result[1] += self.en2en()
        result[2] += self.en2ch()
        self.result = result
    def ch2en(self):
        result = ''
        seg = self.soup.find('div', {'id':'crossid'})
        for tag in seg('tr','def_row df_div1'):
            result += (tag.find('div', 'pos pos1').string + '\n')
            for exp in tag('div', 'de_li1 de_li3'):
                result += (exp.find('div', 'se_d').string + ' ')
                for i in exp('a'):
                    result += (i.string + ' ')
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
    
root = UI()
root.mainloop()
