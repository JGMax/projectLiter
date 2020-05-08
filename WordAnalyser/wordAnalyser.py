#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from navec import Navec
from slovnet import NER

import pymorphy2
import codecs
from natasha import NamesExtractor

from polyglot.detect import Detector
from polyglot.text import Text

from projectLiter.WordAnalyser.formatText import formatText
from projectLiter.WordAnalyser.formatText import remove

from projectLiter.WordAnalyser.utility import morphNameFilter
from projectLiter.WordAnalyser.utility import sameNameFilter
from projectLiter.WordAnalyser.utility import properNameFilter
from projectLiter.WordAnalyser.utility import wordsCounterDict

from projectLiter.WordAnalyser.config import triggerSymbols
from projectLiter.WordAnalyser.config import removeSymbols
from projectLiter.WordAnalyser.config import nerModelPath
from projectLiter.WordAnalyser.config import nevecModelPath
from projectLiter.WordAnalyser.morphAnalysis import morphAnalysisRusText

from nltk.tokenize import word_tokenize

morph = pymorphy2.MorphAnalyzer()

with codecs.open('text.txt', encoding='utf-8') as f:
    text = f.read()
    print("Подготовка текста...")
    textFormat = formatText(text, removeSymbols, triggerSymbols)
    words = word_tokenize(text)
    wordsDict = wordsCounterDict(words, morph)
    print("Анализ...")
    f.close()


navec = Navec.load(nevecModelPath)
ner = NER.load(nerModelPath)
ner.navec(navec)

slovCharacters = []
for span in ner(text).spans:
    if span.type == 'PER':
        parseResult = []
        character = ""
        namePerWord = text[span.start:span.stop].split(' ')
        for word in namePerWord:
            parseResult.append(morph.parse(word.lower()))
        parseResult = morphNameFilter(parseResult, 0, 0, 0, 0, 0)
        if parseResult[0] == "1":
            character = text[span.start:span.stop]
            character = remove(character, triggerSymbols)
            character = properNameFilter(character, text, wordsDict, triggerSymbols, morph, [span.start, span.stop])
            if character:
                sameNameFilter(slovCharacters, character, morph)


# extractor = SimpleNamesExtractor()  # Natasha
# simpleCharacters = [item for item in slovCharacters if extractor(item)]
# slovCharacters = [item for item in slovCharacters if not extractor(item)]

# print(simpleCharacters)
print(slovCharacters)

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

# extractor = SimpleNamesExtractor()  # Natasha
# polycharacters = [item for item in polycharacters if not extractor(item)]

# properNameFilter(polycharacters, words, triggerSymbols, morph)

# print(polycharacters)

statistic = {}
posts = []
morphAnalysisRusText(words, posts, statistic, morph)

del morph

# for post in posts:
   # print(post + ' - ' + str(statistic[post]))
# print(words)

