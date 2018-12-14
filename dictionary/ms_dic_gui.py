from Parse import *
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from functools import partial

class UI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title('Dictionary')

        try:
            tmp = open('config.dat', 'r')
            self.window_width = eval(tmp.readline().replace('\n', ''))
            self.window_height = eval(tmp.readline().replace('\n', ''))
            po_x = eval(tmp.readline().replace('\n', ''))
            po_y = eval(tmp.readline().replace('\n', '')) - 36
            self.root_bg = tmp.readline().replace('\n', '')
            self.widget_bg = tmp.readline().replace('\n', '')
            self.widget_fg = tmp.readline().replace('\n', '')
            if self.root_bg == '#f0f0f0':
                self.theme = 0
            else:
                self.theme = 1
            tmp.close()
        except:
            tmp = open('config.dat', 'w')
            screen_width, screen_height = self.getScreen()
            self.window_width = 0.6 * screen_width
            self.window_height = 0.8 * screen_height
            po_x = screen_width - self.window_width
            po_y = 0
            self.root_bg = '#f0f0f0'
            self.widget_bg = 'white'
            self.widget_fg = 'black'
            for item in [str(self.window_width), str(self.window_height), str(po_x),
                         str(po_y), '#f0f0f0', 'white', 'black']:
                tmp.write(item)
                tmp.write('\n')
            self.theme = 0
            tmp.close()
        
        self.config(bg = self.root_bg)
        self.geometry('%dx%d+%d+%d' % (self.window_width, self.window_height, po_x, po_y))
        self.bind('<Configure>', self.Resize)
        
        self.en = Entry(self, bg = self.widget_bg, fg = self.widget_fg,
                        font = '微软雅黑 20', bd = 0, width = 100, insertbackground = self.widget_fg)
        self.en.place(bordermode=OUTSIDE,
                      width = 0.85 * self.window_width,
                      height = 0.06 * self.window_height,
                      x = 0.01 * self.window_width,
                      y = 0.01 * self.window_height)
        self.en.bind('<Return>', self.Search_word)
        self.en.focus_set()
        self.bu = Button(self, text = '搜  索', command = self.Search_word, font = '微软雅黑 20',
                         bg = self.root_bg, fg = self.widget_fg, activebackground = self.widget_bg,
                         activeforeground = self.widget_fg)
        self.bu_width = 0.12 * self.window_width
        self.bu.place(bordermode=OUTSIDE,
                 width = 0.12 * self.window_width,
                 height = 0.06 * self.window_height,
                 x = 0.87 * self.window_width,
                 y = 0.01 * self.window_height) 
        
        self.text = ScrolledText(self, height = 28, width = 75, font = '微软雅黑 14',
                                 bg = self.widget_bg, fg = self.widget_fg, relief = FLAT)
        self.text.place(width = 0.98 * self.window_width,
                        height = 0.9 * self.window_height,
                        x = 0.01 * self.window_width,
                        y = 0.08 * self.window_height)
        self.text.insert(1.0, '欢迎，右键查看更多。')
        self.text.tag_add('wel', 1.0, END)
        self.text.tag_config('wel', font = '微软雅黑 24')
        self.text.config(state = DISABLED)
        self.icon_f = PhotoImage(file='icons/arrow1.png')
        self.icon_b = PhotoImage(file='icons/arrow2.png')
        try:
            tmp = open('history.txt', 'r')
            tmp.close()
        except:
            tmp = open('history.txt', 'w')
            tmp.close()
        self.memory = WordMemory()
        self.rclick = RightClick(self)
        self.bind('<Button-3>', self.rclick.popup)
        self.bind('<Button-1>', self.rclick.unpop)
        
    def getScreen(self):
        return self.winfo_screenwidth(), self.winfo_screenheight()
    def Resize(self, event):
        self.conf_flag = 1
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
        if word in ['梁子轩', 'lzx', 'LZX', 'Liang Zixuan', 'Zixuan', 'zixuan',
                    'Michael Liang']:
            self.InsertText('这个程序的作者\nThe Author')
            return
        self.result = p.get(word)
        self.ReloadUI()
        if self.conf_flag:
            tmp = open('config.dat', 'w')
            for item in [str(self.winfo_width()), str(self.winfo_height()),
                        str(self.winfo_rootx()), str(self.winfo_rooty()),
                        self.root_bg, self.widget_bg, self.widget_fg]:
                tmp.write(item)
                tmp.write('\n')
            tmp.close()
            self.conf_flag = 0
            tmp.close()
        return
    def ReloadUI(self):
        mes1 = '网络似乎有些问题\nThere is a connection error:('
        mes2 = '找不到输入内容的中英文释义，点击网址查看网络释义：'
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
            self.text.insert(INSERT, '更多')
            self.text.config(state = DISABLED)
            self.text.tag_add('more', 'end-3c', 'end')
            self.HyperText('more')
            self.text.tag_bind('more', '<Button-1>', self.More)
        self.text.tag_add("word", "1.0", '1.%d' % len(word))
        if u'\u4e00' <= word[0] <= u'\u9fff':
            self.text.tag_config('word', font = '微软雅黑 22')
        else:
            self.text.tag_config('word', font = 'tahoma 24 bold')
        self.en.delete(0, END)
        
        self.memory.add(word)
        self.rclick.hMenu_Reset()
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
        self.text.insert('end-3c', self.result[2] + self.result[1])
        self.text.delete('end-3c', END)
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
        self.aMenu = Menu(master, tearoff = 0, font = '微软雅黑 14', cursor = 'left_ptr',
                          bg = self.master.root_bg, activebackground = '#3daee9',
                          fg = self.master.widget_fg, activeforeground = self.master.widget_fg,
                          disabledforeground = 'grey')
        self.hMenu = Menu(self.aMenu, tearoff = 0, font = '微软雅黑 14', cursor = 'left_ptr',
                          bg = self.master.root_bg, activebackground = '#3daee9',
                          fg = self.master.widget_fg, activeforeground = self.master.widget_fg)
        self.hMenu_Reset()
        self.aMenu.add_command(label = '搜索所选内容', command = self.Search)
        self.aMenu.add_command(label = '复制', command = self.Copy_to_clipboard)
        self.aMenu.add_command(label = '粘贴', command = self.Paste_from_clipboard)
        self.aMenu.add_cascade(label = '历史', menu = self.hMenu)
        self.aMenu.add_command(label = '更换皮肤', command = self.Color_change)
        self.aMenu.add_command(label = '清空历史', command = self.Warn)
        self.aMenu.add_separator()
        self.aMenu.add_command(label = '关于', command= self.About)
        self.style_b = ttk.Style()
        self.style_b.theme_create( "black", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], 'background':'#262629'} },
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background":'#262629', 'font':'Calibri 14',
                              'foreground':'#e0ffff'},
                "map":       {"background": [("selected", '#31363b')],
                              "expand": [("selected", [1, 1, 1, 0])] } } } )
        self.style_w = ttk.Style()
        self.style_w.theme_create( "white", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], 'background':'#f0f0f0'} },
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background":'#f0f0f0', 'font':'Calibri 14',
                              'foreground':'black'},
                "map":       {"background": [("selected", 'white')],
                              "expand": [("selected", [1, 1, 1, 0])] } } } )
        


    def Search(self, word = ''):
        if word == '':
            try:
                word = self.master.text.get(SEL_FIRST, SEL_LAST)
            except:
                return
            self.master.en.delete(0, END)
            self.master.en.insert(0, word)
            self.master.Search_word()
            return
        self.master.en.delete(0, END)
        self.master.en.insert(0, word)
        self.master.Search_word()
        return
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
    def hMenu_Reset(self):
        for i in range(0, 8):
            try:
                self.hMenu.delete(0)
            except:
                break
        for word in self.master.memory.history:
            if word != ' ':
                self.hMenu.add_command(label = word, command = partial(self.Search, word))
        self.hMenu.add_separator()
        
        self.hMenu.add_command(label = '更多', command = self.hShow)
        return
    def hShow(self):
        tmp = open('history.txt', 'r')
        words = tmp.readlines()
        tmp.close()
        show_mes = ''
        for word in words:
            if word in [' ', '']:
                continue
            show_mes += word + '\n'
        self.master.InsertText('Searchng History\n\n' + show_mes)
        self.master.text.tag_add('history', 1.0, 2.0)
        self.master.text.tag_config('history', font = 'Arial 22')
    def About(self):
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        self.about = Toplevel(bg = self.master.root_bg)
        self.about.wm_attributes('-topmost', 1)
        self.about.focus_set()
        self.about.title('关于')
        self.about.wm_attributes('-topmost',1)
        self.about.geometry('%dx%d+%d+%d' % (500, 600, x, y))
        icon = PhotoImage(file='icons/About.png')
        f = Frame(self.about, bg = self.master.root_bg)
        gril = Label(f, image = icon)
        gril.image = icon
        gril.pack(side = LEFT, padx = 20, pady = 20)
        name = Label(f, text = '\n小词典\n～～～', font = '幼圆 32', fg = self.master.widget_fg,
                     bg = self.master.root_bg)
        name.pack(side = LEFT)
        f.pack(side = TOP, anchor = NW)
        
        nb = ttk.Notebook(self.about)

        if self.master.root_bg == '#f0f0f0':
            self.style_w.theme_use('white')
        else:
            self.style_b.theme_use("black")
        nb.pack(side = TOP, anchor = W, padx = 20)
        page1 = Frame(nb, bg = self.master.root_bg)
        message1 = Text(page1, height = 6, font = '微软雅黑 14', bg = self.master.widget_bg,
                        fg = self.master.widget_fg, relief = FLAT)
        message1.insert(1.0, '基于网络爬虫的词典小程序\n英汉、汉英均支持\n版本：1.2\n' + \
                        '反馈：zixuan.liang712@gmail.com\n感谢使用')
        message1.config(state = DISABLED)
        message1.pack(side = TOP, anchor = W)
        nb.add(page1, text = '关于')
        
        page2 = Frame(nb, bg = self.master.root_bg)
        message2 = Text(page2, height = 7, font = 'Times 14', bg = self.master.widget_bg,
                        fg = self.master.widget_fg, relief = FLAT)
        message2.insert(1.0, 'Version: 1.2\nAuthor: Michael Liang(UESTC)\n' + \
                        'Email: zixuan.liang712@gmail.com\nGive me feedback if you want.\n')
        message2.config(state = DISABLED)
        message2.pack(side = TOP, anchor = W)
        nb.add(page2, text = 'About')

        close_bu = Button(self.about, font = '微软雅黑 14', bg = self.master.root_bg,
                          fg = self.master.widget_fg, activebackground = self.master.widget_bg,
                          activeforeground = self.master.widget_fg, text = '关 闭',
                          command = self.Close)
        close_bu.pack(side = BOTTOM, anchor = SE, pady = 15, padx = 15)
    def Color_change(self):
        if self.master.theme == 0:
            self.master.root_bg = '#262629'
            self.master.widget_bg = '#31363b'
            self.master.widget_fg = '#E0FFFF'
            self.master.theme = 1
        else:
            self.master.root_bg = '#f0f0f0'
            self.master.widget_bg = 'white'
            self.master.widget_fg = 'black'
            self.master.theme = 0
        self.master.config(bg = self.master.root_bg)
        self.master.en.config(bg = self.master.widget_bg, fg = self.master.widget_fg,
                              insertbackground = self.master.widget_fg)
        self.master.bu.config(bg = self.master.root_bg, fg = self.master.widget_fg,
                              activebackground = self.master.widget_bg,
                              activeforeground = self.master.widget_fg)
        self.master.text.config(bg = self.master.widget_bg, fg = self.master.widget_fg)
        self.aMenu.config(bg = self.master.root_bg, fg = self.master.widget_fg,
                          activeforeground = self.master.widget_fg)
        self.hMenu.config(bg = self.master.root_bg, fg = self.master.widget_fg,
                          activeforeground = self.master.widget_fg)
        tmp = open('config.dat', 'w')
        for item in [str(self.master.winfo_width()), str(self.master.winfo_height()),
                        str(self.master.winfo_rootx()), str(self.master.winfo_rooty()),
                        self.master.root_bg, self.master.widget_bg, self.master.widget_fg]:
            tmp.write(item)
            tmp.write('\n')
        tmp.close()    
    def Warn(self):
        self.warn = Toplevel(bg = self.master.root_bg)
        self.warn.title('警告')
        self.warn.wm_attributes('-topmost', 1)
        self.warn.focus_set()
        po_x = self.master.winfo_rootx() + self.master.winfo_width() / 2 - 200
        po_y = self.master.winfo_rooty() + self.master.winfo_height() / 2 - 100
        self.warn.geometry('%dx%d+%d+%d' % (400, 200, po_x, po_y))
        mes = Label(self.warn, text = '\n该操作会清楚所有历史数据，\n是否继续?',
                    font = '微软雅黑 16', fg = self.master.widget_fg, bg = self.master.root_bg)
        mes.pack(side = TOP)
        f = Frame(self.warn, bg = self.master.root_bg)
        bu_no = Button(f, font = '微软雅黑 14', bg = self.master.root_bg,
                       fg = self.master.widget_fg, activebackground = self.master.widget_bg,
                       activeforeground = self.master.widget_fg, text = ' 否 ',
                          command = self.Warn_no)
        bu_yes = Button(f, font = '微软雅黑 14', bg = self.master.root_bg,
                        fg = self.master.widget_fg, activebackground = self.master.widget_bg,
                        activeforeground = self.master.widget_fg, text = ' 是 ',
                        command = self.Warn_yes)
        bu_yes.pack(side = RIGHT, anchor = E, padx = 5)
        bu_no.pack(side = RIGHT, anchor = E, padx = 30)
        f.pack(side = BOTTOM, anchor = SE, pady = 20)
    def Close(self):
        self.about.destroy()
        return
    def Warn_no(self):
        self.warn.destroy()
    def Warn_yes(self):
        tmp = open('history.txt', 'w')
        tmp.close()
        self.master.memory.wordlist = []
        self.master.memory.history = []
        for i in range(0, 7):
            self.master.memory.history.append(' ')
        self.master.memory.pointer = 0
        self.master.memory.current_pointer = 0
        self.hMenu_Reset()
        self.master.InsertText('')
        self.warn.destroy()
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
            self.aMenu.entryconfigure(5, state = ACTIVE)
            self.aMenu.entryconfigure(7, state = ACTIVE)
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
            self.aMenu.entryconfigure(5, state = ACTIVE)
            self.aMenu.entryconfigure(7, state = ACTIVE)
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
            self.aMenu.entryconfigure(3, state = ACTIVE)
            self.aMenu.entryconfigure(4, state = ACTIVE)
            self.aMenu.entryconfigure(5, state = ACTIVE)
            self.aMenu.entryconfigure(7, state = ACTIVE)
            self.aMenu.post(event.x_root, event.y_root)
            return
    def unpop(self, event):
        self.aMenu.unpost()
        return
class WordMemory():
    def __init__(self):
        self.wordlist = []
        self.pointer = 0
        self.current_pointer = 0
        self.max_word = 50
        self.history = []
        h = open('history.txt', 'r')
        s = h.readlines()
        h.close()
        for i in range(0, 7):
            try:
                self.history.append(s[-1 - i])
            except:
                self.history.append(' ')
            self.history[i] = self.history[i].rstrip('\n')
    def add(self, word):
        if word not in self.wordlist:
            self.wordlist.append(word)
            if self.pointer < self.max_word:
                self.pointer += 1
                self.current_pointer = self.pointer - 1
            else:
                del self.wordlist[0]
        for i in range(0, 7):
            if self.history[i] == word:
                del self.history[i]
                self.history.insert(0, word)
                break
        else:
            del self.history[-1]
            self.history.insert(0, word)
        self.his_add(word)
    def last_word(self):
        self.current_pointer -= 1
        return self.wordlist[self.current_pointer]
    def next_word(self):
        self.current_pointer += 1
        return self.wordlist[self.current_pointer]
    def Num_of_words(self):
        return len(self.wordlist)
    def his_add(self, word):
        flag = 1
        h = open('history.txt', 'a+')
        h.seek(0)
        for h_word in h.readlines():
            if h_word == word + '\n':
                flag = 0
                break
        if flag:
            h.seek(2)
            h.write(word + '\n')
        h.close()
        
root = UI()
root.mainloop()
