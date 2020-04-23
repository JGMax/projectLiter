#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymorphy2
import codecs
from natasha import NamesExtractor
from polyglot.detect import Detector
from polyglot.text import Text
import formatText

with codecs.open('text.txt', encoding='utf-8') as f:
    text = f.read()
    f.close()

detector = Detector(text)
print(detector.language)

text = formatText.remove(text, '«»,":;()\r')

text = text.replace('\n', ' ')
text = text.replace('.', ' ')
text = text.replace('!', ' ')
text = text.replace('?', ' ')
# text = text.replace('ё', 'е')


polycharacters = []
polytext = Text(text)
for entity in polytext.entities:
    if entity.tag == "I-PER":
        character = [item for item in list(polytext.words[entity.start: entity.end])
                     if item.istitle() and len(item) > 1]
        if character not in polycharacters and character:
            polycharacters.append(character)

print(polycharacters)

characters = []
extractor = NamesExtractor()
matches = extractor(text)
for match in matches:
    character = ''
    for fact in match.fact:
        if fact:
            character += str(fact).title() + ' '
    character = character.rstrip()
    if not characters:
        characters.append(character)
    else:
        wasEnter = 0
        for item in characters:
            if character in item:
                wasEnter = 1
                break
        if not wasEnter:
            characters.append(character)

print(characters)

morph = pymorphy2.MorphAnalyzer()
words = text.split(' ')
statistic = {}
posts = []
for word in words:
    analyseResult = morph.parse(word)[0]
    if analyseResult.tag.POS:
        if analyseResult.tag.POS not in posts:
            posts.append(analyseResult.tag.POS)
            statistic[analyseResult.tag.POS] = 0

        statistic[analyseResult.tag.POS] += 1
    else:
        words.remove(word)

# for post in posts:
    # print(post + ' - ' + str(statistic[post]))
# print(words)

