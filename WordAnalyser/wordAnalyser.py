#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymorphy2
import codecs
from natasha import NamesExtractor
from natasha import SimpleNamesExtractor

from polyglot.detect import Detector
from polyglot.text import Text
from projectLiter.WordAnalyser.formatText import formatText
from projectLiter.WordAnalyser.utility import morphNameFilter
from projectLiter.WordAnalyser.utility import sameNameFilter
from projectLiter.WordAnalyser.utility import properNameFilter


def morphAnalysisText(words, postsList, statisticList, morph):
    for word in words:
        analyseResult = morph.parse(word.lower())[0]
        if analyseResult.tag.POS:
            if analyseResult.tag.POS not in posts:
                postsList.append(analyseResult.tag.POS)
                statisticList[analyseResult.tag.POS] = 0

            statisticList[analyseResult.tag.POS] += 1
        else:
            words.remove(word)


with codecs.open('text.txt', encoding='utf-8') as f:
    text = f.read()
    f.close()

morph = pymorphy2.MorphAnalyzer()

triggerSymbols = ['.', '!', '?', '"', '«']
removeSymbols = '»,:;()\r'
textFormat = formatText(text, removeSymbols, triggerSymbols)
words = textFormat.split(' ')

detector = Detector(text)  # polyglot
print(detector.language)

characters = []
extractor = NamesExtractor()  # Natasha
matches = extractor(text)
for match in matches:
    character = ''
    parseResult = []
    for fact in match.fact:
        if fact:
            parseResult.append(morph.parse(fact.lower()))
    parseResult = morphNameFilter(parseResult, 0, 0, 0, 0, 0)
    if parseResult[0] == "1":
        for fact in match.fact:
            if fact:
                character += fact.title() + ' '
        character = character.strip()
        sameNameFilter(characters, character, morph)

print(characters)

polycharacters = []
polytext = Text(text)
for entity in polytext.entities:
    if entity.tag == "I-PER":
        character_per_word = [item for item in list(polytext.words[entity.start: entity.end])
                              if item.istitle() and len(item) > 1]
        if character_per_word:
            character = ''
            parseResult = []
            for word in character_per_word:
                parseResult.append(morph.parse(word.lower()))

            parseResult = morphNameFilter(parseResult, 0, 0, 0, 0, 0)

            if parseResult[0] == "1":
                for word in character_per_word:
                    if not word == "1":
                        character += word.title() + ' '
                character = character.strip()
                sameNameFilter(polycharacters, character, morph)

extractor = SimpleNamesExtractor()  # Natasha
polycharacters = [item for item in polycharacters if not extractor(item)]

properNameFilter(polycharacters, words, triggerSymbols, morph)

print(polycharacters)

statistic = {}
posts = []
morphAnalysisText(words, posts, statistic, morph)

# for post in posts:
   # print(post + ' - ' + str(statistic[post]))
# print(words)

