import nltk
import pymorphy2
from projectLiter.WordAnalyser.search_high_register_words import upper

# file = open('book4.txt',encoding = 'utf - 8') загружаю книгу

#text = file.read() # читаю текст
words = nltk.word_tokenize(text)
High_register_words = []
i = 0
for w in words:
    i = i + 1
    if upper(w)!='False':
        if ((words[i - 2] !='.') & (words[i - 2] !='!') & (words[i - 2] !='?')):
            High_register_words.append(w)


prob_thresh = 0.4
morph = pymorphy2.MorphAnalyzer()
names = []

for word in High_register_words:
    for p in morph.parse(word):
        if 'Name' in p.tag and p.score >= prob_thresh:
            names.append(p.normal_form)
freq = nltk.FreqDist(names)

names = freq.most_common() # имена и их упоминания

#print(names) #вывод имен вместе с их количеством упоминаний

