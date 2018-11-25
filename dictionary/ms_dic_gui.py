#A dictionary based on the searching pages of Bing dic
#Get the searching HTML page with requests
#parse with BeautifulSoup
#show in GUI(tkinter)
#Next: add right-click menu into GUI
#梁子轩，2018.11.21

import requests
import webbrowser
from tkinter import *
from bs4 import BeautifulSoup

class UI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('Dictionary')
        
        self.rclick = RightClick(self)
        self.bind('<Button-3>', self.rclick.popup)
        self.bind('<Button-1>', self.rclick.unpop)
        self.clipboard_clear()
        
        screen_width, screen_height = self.getScreen()
        self.window_width = 0.6 * screen_width
        self.window_height = 0.8 * screen_height
        po_x = (screen_width - self.window_width) / 2
        po_y = (screen_height - self.window_height) / 2
        self.geometry('%dx%d+%d+%d' % (self.window_width, self.window_height, po_x, po_y))
        self.bind('<Configure>', self.Resize)
        
        self.en = Entry(self, font = '微软雅黑 18', bd = 0, width = 100)
        self.en.place(bordermode=OUTSIDE,
                      width = 0.85 * self.window_width,
                      height = 0.06 * self.window_height,
                      x = 0.01 * self.window_width,
                      y = 0.01 * self.window_height)
        self.en.bind('<Return>', self.Search_word)
        self.en.focus_set()
        self.bu = Button(self, text = 'Search', command = self.Search_word, font = 'calibri 20')
        self.bu_width = 0.12 * self.window_width
        self.bu.place(bordermode=OUTSIDE,
                 width = 0.12 * self.window_width,
                 height = 0.06 * self.window_height,
                 x = 0.87 * self.window_width,
                 y = 0.01 * self.window_height) 
        
        self.text = Text(self, height = 28, width = 75, font = '微软雅黑 14', relief = FLAT)
        self.text.place(width = 0.98 * self.window_width,
                        height = 0.9 * self.window_height,
                        x = 0.01 * self.window_width,
                        y = 0.08 * self.window_height)
        self.text.config(state = DISABLED)
        self.icon_f = PhotoImage(file='arrow1.png')
        self.icon_b = PhotoImage(file='arrow2.png')
        self.memory = WordMemory()
        
    def getScreen(self):
        return self.winfo_screenwidth(), self.winfo_screenheight()
    def Resize(self, event):
        self.window_height = self.winfo_height()
        self.window_width = self.winfo_width()
        self.en.place(width = 0.97 * self.window_width - self.bu_width,
                      height = 0.06 * self.window_height,
                      x = 0.01 * self.window_width,
                      y = 0.01 * self.window_height)
        self.bu.place(width = self.bu_width,
                      height = 0.06 * self.window_height,
                      x = 0.99 * self.window_width - self.bu_width,
                      y = 0.01 * self.window_height)
        self.text.place(width = 0.98 * self.window_width,
                        height = 0.9 * self.window_height,
                        x = 0.01 * self.window_width,
                        y = 0.08 * self.window_height)
        try:
            self.flabel.winfo_parent()
            self.flabel.place(width = 48, height = 48,
                                x = 0.98 * self.window_width - 80,
                                y = 0.02 * self.window_height)
        except:
            pass
        try:
            self.blabel.winfo_parent()
            self.blabel.place(width = 48, height = 48,
                                x = 0.98 * self.window_width - 150,
                                y = 0.02 * self.window_height)
        except:
            pass
        
    def Search_word(self, ev = None):
        p = Parse()
        word = self.en.get()
        if word == '':
            return
        word = word.strip(' ')
        word = word.replace(' ', '+')
        self.result = p.get(word)
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
        if self.result[0] == '':
            self.InsertText(word + '\n' + self.result[-2] + self.result[2] + self.result[1])
        else:
            self.InsertText(word + '\n' + self.result[-2] + self.result[0])
            self.text.config(state = NORMAL)
#Only show the ch-en meaning, hide others into 'more' tag
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
        
        self.memory.add(word)
        self.ArrowIcon()
    
    def ArrowIcon(self):
        if self.memory.Num_of_words() > 1:
            if self.memory.current_pointer == 0:
                self.Hide_icon('b')
                self.Show_icon('f')
                return
            if self.memory.pointer == self.memory.current_pointer + 1:
                self.Hide_icon('f')
                self.Show_icon('b')
                return
            if self.memory.current_pointer + 1 < self.memory.pointer:
                self.Show_icon('f')
                self.Show_icon('b')
                return
            
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
    def Show_icon(self, f_or_b):
        if f_or_b == 'f':
            try:
                self.flabel.winfo_parent()
            except:
                self.flabel = Label(self.text, image = self.icon_f)
                self.flabel.image = self.icon_f
                self.flabel.place(width = 48, height = 48,
                                x = 0.98 * self.window_width - 80,
                                y = 0.02 * self.window_height)
                self.flabel.bind('<Button-1>', self.Forward)
                self.flabel.bind('<Enter>', self.show_hand_cursor)
                self.flabel.bind('<Leave>', self.show_arrow_cursor)
        if f_or_b == 'b':
            try:
                self.blabel.winfo_parent()
            except:
                self.blabel = Label(self.text, image = self.icon_b)
                self.blabel.image = self.icon_b
                self.blabel.place(width = 48, height = 48,
                                x = 0.98 * self.window_width - 150,
                                y = 0.02 * self.window_height)
                self.blabel.bind('<Button-1>', self.Backward)
                self.blabel.bind('<Enter>', self.show_hand_cursor)
                self.blabel.bind('<Leave>', self.show_arrow_cursor)
    def Hide_icon(self, f_or_b):
        if f_or_b == 'f':
            try:
                self.flabel.winfo_parent()
                self.flabel.destroy()
                self.text.config(cursor='xterm')
            except:
                pass
        if f_or_b == 'b':
            try:
                self.blabel.winfo_parent()
                self.blabel.destroy()
                self.text.config(cursor='xterm')
            except:
                pass
    def Backward(self, event):
        p = Parse()
        self.result = p.get(self.memory.last_word())
        self.ReloadUI()
    def Forward(self, event):
        p = Parse()
        self.result = p.get(self.memory.next_word())
        self.ReloadUI()
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


class RightClick:
    def __init__(self, master):
        self.master = master
        self.aMenu = Menu(master, tearoff = 0, font = 'calibri 16', cursor = 'left_ptr')
        self.aMenu.add_command(label = 'Search', command = self.Search)
        self.aMenu.add_command(label = 'Copy', command = self.Copy_to_clipboard)
        self.aMenu.add_command(label = 'Paste', command = self.Paste_from_clipboard)
        self.aMenu.add_command(label = 'History')
        self.aMenu.add_command(label = 'Clear', command = self.Clear)
        self.aMenu.add_separator()
        self.aMenu.add_command(label = 'About', command= self.About)
    #0-Search   1-Copy    2-Paste    3-history     4-Clear    6-About
    def Search(self):
        try:
            word = self.master.text.get(SEL_FIRST, SEL_LAST)
        except:
            return
        self.master.en.delete(0, END)
        self.master.en.insert(0, word)
        self.master.Search_word()
    def Copy_to_clipboard(self):
        try:
            word = self.master.text.get(SEL_FIRST, SEL_LAST)
            self.master.clipboard_clear()
            self.master.clipboard_append(word)
        except:
            pass
    def Paste_from_clipboard(self):
        try:
            if self.master.en.select_present():
                self.master.en.delete(SEL_FIRST, SEL_LAST)
            self.master.en.insert(ANCHOR, self.master.clipboard_get())
        except:
            pass
    def Clear(self):
        self.master.memory.__init__()
        self.master.InsertText('')
        self.master.Hide_icon('f')
        self.master.Hide_icon('b')
    def About(self):
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        self.about = Toplevel()
        self.about.title('About')
        self.about.geometry('%dx%d+%d+%d' % (560, 600, x, y))
        icon = PhotoImage(file='menhera.png')
        f = Frame(self.about)
        gril = Label(f, image = icon)
        gril.image = icon
        gril.pack(side = LEFT, padx = 20, pady = 20)
        name = Label(f, text = '梁子轩的\n小词典\n～～～', font = '楷体 28')
        name.pack(side = LEFT)
        f.pack(side = TOP, anchor = NW)
        message = Text(self.about, height = 6, font = 'Times 14', relief = FLAT)
        message.insert(1.0, 'Version: 1.0\nAuthor: Michael Liang(UESTC)\nReport Bug: ' + \
            'zixuan.liang712@gmail.com\n2018.11\n')
        message.config(state = DISABLED)
        message.pack(side = TOP, anchor = W, padx = 20)
        close_bu = Button(self.about, font = 'Calibri 14',
                          text = 'Close', command = self.Close)
        close_bu.pack(side = BOTTOM, anchor = SE, pady = 20, padx = 20)
    def Close(self):
        self.about.destroy()
    def popup(self, event):
        #in the region of entry
        if self.master.en.winfo_rootx() + 0.97 * self.master.window_width - self.master.bu_width > event.x_root\
            and event.x_root > self.master.en.winfo_rootx()\
            and self.master.en.winfo_rooty() + 0.06 * self.master.window_height > event.y_root\
            and event.y_root > self.master.en.winfo_rooty():
            self.aMenu.entryconfigure(0, state = DISABLED)
            self.aMenu.entryconfigure(1, state = ACTIVE)
            self.aMenu.entryconfigure(2, state = ACTIVE)
            self.aMenu.entryconfigure(3, state = ACTIVE)
            self.aMenu.entryconfigure(4, state = ACTIVE)
            self.aMenu.entryconfigure(6, state = ACTIVE)
            self.aMenu.post(event.x_root, event.y_root)
            return
        #in the region of text box
        if self.master.text.winfo_rooty() + 0.9 * self.master.window_height > event.y_root\
            and event.y_root > self.master.text.winfo_rooty()\
            and self.master.text.winfo_rootx() + 0.98 * self.master.window_width > event.x_root\
            and event.x_root > self.master.text.winfo_rootx():
            self.aMenu.entryconfigure(0, state = ACTIVE)
            self.aMenu.entryconfigure(1, state = ACTIVE)
            self.aMenu.entryconfigure(2, state = DISABLED)
            self.aMenu.entryconfigure(3, state = ACTIVE)
            self.aMenu.entryconfigure(4, state = ACTIVE)
            self.aMenu.entryconfigure(6, state = ACTIVE)
            self.aMenu.post(event.x_root, event.y_root)
            return
        #in the region of button
        if self.master.bu_width > event.x_root - self.master.bu.winfo_rootx() > 0\
            and 0.06 * self.master.window_height > event.y_root - self.master.bu.winfo_rooty() > 0:
            return
        else:
            self.aMenu.entryconfigure(0, state = DISABLED)
            self.aMenu.entryconfigure(1, state = DISABLED)
            self.aMenu.entryconfigure(2, state = DISABLED)
            self.aMenu.entryconfigure(3, state = DISABLED)
            self.aMenu.entryconfigure(4, state = DISABLED)
            self.aMenu.post(event.x_root, event.y_root)
            return
    def unpop(self, event):
        self.aMenu.unpost()

class WordMemory():
    def __init__(self):
        self.wordlist = []
        self.pointer = 0
        self.current_pointer = 0
        #
        self.max_word = 50
    def add(self, word):
        if word not in self.wordlist:
            self.wordlist.append(word)
            if self.pointer < self.max_word:
                self.pointer += 1
                self.current_pointer = self.pointer - 1
            else:
                del self.wordlist[0]
    def last_word(self):
        self.current_pointer -= 1
        return self.wordlist[self.current_pointer]
    def next_word(self):
        self.current_pointer += 1
        return self.wordlist[self.current_pointer]
    def Num_of_words(self):
        return len(self.wordlist)

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
