#Generate a good word cloud(in Chinese), the largest word is the name.
#jieba, wordcloud
import jieba
import wordcloud
from scipy.misc import imread

name = input('Enter the name:')
jieba.add_word(name)
f = open('good_words2.txt', 'r', encoding = 'utf-8')
t = f.read()
f.close()
t = t.replace(' ', '')
t = t.replace('、', '')
t = t.replace('\n', '')
t = t.replace(',', '')
t = t.replace('，', '')
t = t.replace(chr(12288), '')
t = t.replace('姓名', name)
wlist = jieba.lcut(t)
mask = imread('heart.png')
c = wordcloud.WordCloud(width=1200,
        height=1200,
        background_color='white',
        font_path='msyh.ttc',
        mask=mask,
        colormap='rainbow')
txt = ' '.join(wlist)
c.generate(txt)
c.to_file('test.png')
