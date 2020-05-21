# import sys
import nltk
from projectLiter.WordAnalyser.config import max_freq_top_size
# from nltk.tokenize import word_tokenize # токенизиурет слова
# import chardet #определяет кодировку
# import os
# import codecs #содержит кодек BOM_UTF-8

# bytes = min(128, os.path.getsize(sys.argv[1]))
#
# raw = open(sys.argv[1], 'rb').read(bytes)
#
# if raw.startswith(codecs.BOM_UTF8):
#     encoding = 'utf-8-sig'
# else:
#     result = chardet.detect(raw)
#     encoding = result['encoding']
#
# print(result['confidence'])
# print(result['encoding'])
#
# infile = open(sys.argv[1], 'r', encoding=encoding)
# text = infile.read()
# infile.close()
#
# #text = file.read()
# words = word_tokenize(text)


def word_frequency(words):
    freq = nltk.FreqDist(words)
    top = freq.most_common(max_freq_top_size)
    max_range = range(0, max_freq_top_size) if max_freq_top_size < len(top) else range(0, len(top))
    abc = list(top[w] for w in max_range if len(top[w][0]) > 3)
    return abc
    #print(abc)

#summary = sorted(w for w in set(words) if len(w) > 6 and freq[w] > 10)
#summary = freq.keys()
#print(summary)
