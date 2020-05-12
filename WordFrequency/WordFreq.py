import sys
import nltk
from nltk.tokenize import word_tokenize # токенизиурет слова
import chardet #определяет кодировку
import os
import codecs #содержит кодек BOM_UTF-8

bytes = min(128, os.path.getsize(sys.argv[1]))

raw = open(sys.argv[1], 'rb').read(bytes)

if raw.startswith(codecs.BOM_UTF8):
    encoding = 'utf-8-sig'
else:
    result = chardet.detect(raw)
    encoding = result['encoding']

print(result['confidence'])
print(result['encoding'])

infile = open(sys.argv[1], 'r', encoding=encoding)
text = infile.read()
infile.close()

#text = file.read()

words = word_tokenize(text)
freq = nltk.FreqDist(words)

top = freq.most_common(500)

abc = list(top[w][0] for w in range(1,500) #topmostpopularwords
       if len(top[w][0]) > 6)
print(abc)

#summary = sorted(w for w in set(words) if len(w) > 6 and freq[w] > 10)
#summary = freq.keys()
#print(summary)



