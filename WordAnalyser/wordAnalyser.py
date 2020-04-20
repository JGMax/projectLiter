#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymorphy2
import codecs
from natasha import NamesExtractor
from polyglot.detect import Detector
from polyglot.text import Text

from WordAnalyser import formateText

with codecs.open('text.txt', encoding='utf-8') as f:
    text = f.read()
    f.close()


detector = Detector(text)
print(detector.language)

text1 = Text(text)
print(text1.entities)

text = formateText.remove(text, '«»,":;()\r')

text = text.replace('\n', ' ')
text = text.replace('.', ' . ')
text = text.replace('!', ' ! ')
text = text.replace('?', ' ? ')
text = text.replace('ё', 'е')

characters = []
extractor = NamesExtractor()
matches = extractor(text)
for match in matches:
    #character = formateText.strBetween(str(match.fact), "'").title()
    print(str(match.fact))
    #if character not in characters:
        #characters.append(character)

morph = pymorphy2.MorphAnalyzer()
words = text.split(' ')
statistic = {}
posts = []
index = 0
for i in words:
    analyseResult = morph.parse(words[index])[0]
    if analyseResult.tag.POS:
        if analyseResult.tag.POS not in posts:
            posts.append(analyseResult.tag.POS)
            statistic[analyseResult.tag.POS] = 0

        statistic[analyseResult.tag.POS] += 1
        index += 1
    else:
        words.pop(index)

index = 0
for i in posts:
    print(posts[index] + ' - ' + str(statistic[i]))
    index += 1
#print(characters)
print(words)

