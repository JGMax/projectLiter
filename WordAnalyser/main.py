#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs

# from polyglot.detect import Detector

from projectLiter.WordAnalyser.formatText import formatText

from projectLiter.WordAnalyser.utility import wordsCounterDict

from projectLiter.WordAnalyser.config import triggerSymbols
from projectLiter.WordAnalyser.config import removeSymbols
from projectLiter.WordAnalyser.config import morph

from projectLiter.WordAnalyser.characterFinder import charactersFinderRus
from projectLiter.WordAnalyser.morphAnalysis import morphAnalysisRus

text = ""
words = []
wordsDict = {}


def open_file():
    with codecs.open('text.txt', encoding='utf-8') as f:
        global text, words, wordsDict
        text = f.read()
        print("Подготовка текста...")
        words = formatText(text, removeSymbols, triggerSymbols).split(' ')
        words = [item for item in words if item]
        wordsDict = wordsCounterDict(words, morph)
        print("Анализ...")
        f.close()


def main():
    open_file()

    # detector = Detector(text)  # polyglot
    # print(f"Язык текста: {detector.language.name.capitalize()}")

    # if detector.language.code == "ru":
    characters = charactersFinderRus(text, wordsDict, words, morph)
    print("Найденные персонажи:")
    for character in characters:
        print(character)
    statistic = {}
    posts = []
    morphAnalysisRus(words, posts, statistic, morph)
    print("Найденные части речи:")
    for post in posts:
        print(post + ' - ' + str(statistic[post]))
    # print(words)


if __name__ == '__main__':
    main()
    del morph

