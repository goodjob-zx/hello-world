#Generate a good word cloud(in Chinese), the largest word is the name.
#jieba, wordcloud
import jieba
import wordcloud
from scipy.misc import imread

name = input('Enter the name:')
f = open('good_words.txt', 'r', encoding = 'utf-8')
t = f.read()
f.close()
t = t.replace(' ', '')
t = t.replace('、', '')
t = t.replace('\n', '')
t = t.replace('姓名', name)
wlist = jieba.lcut(t)
mask = imread('like.png')
c = wordcloud.WordCloud(width=800, height=800, background_color='white', font_path='msyh.ttc', mask=mask)
txt = ' '.join(wlist)
c.generate(txt)
c.to_file('test.png')
