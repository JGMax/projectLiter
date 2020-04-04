#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymorphy2
import formateText
import codecs
from natasha import NamesExtractor

with codecs.open('text.txt', encoding='utf-8') as f:
    text = f.read()
    f.close()

text = formateText.remove(text, '«»,":;()\r')

text = text.replace('\n', ' ')
text = text.replace('.', ' . ')
text = text.replace('!', ' ! ')
text = text.replace('?', ' ? ')


characters = []
extractor = NamesExtractor()
matches = extractor(text)
for match in matches:
    character = formateText.strBetween(str(match.fact), "'").title()

    if character not in characters:
        characters.append(character)

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
    elif '-' in words[index]:
        words.pop(index)
    else:
        index += 1

index = 0
for i in posts:
    print(posts[index] + ' - ' + str(statistic[i]))
    index += 1
print(characters)
# print(words)

