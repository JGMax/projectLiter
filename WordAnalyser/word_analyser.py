#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs

from projectLiter.WordAnalyser.formatText import formatText

from projectLiter.WordAnalyser.utility import wordsCounterDict

from projectLiter.WordAnalyser.config import triggerSymbols
from projectLiter.WordAnalyser.config import removeSymbols
from projectLiter.WordAnalyser.config import morph

from projectLiter.WordAnalyser.characterFinder import charactersFinderRus
from projectLiter.WordAnalyser.morphAnalysis import morphAnalysisRus

from projectLiter.WordFrequency.WordFreq import word_frequency

from projectLiter.WordAnalyser.results_keys import morph_statistic_key
from projectLiter.WordAnalyser.results_keys import morph_posts_key
from projectLiter.WordAnalyser.results_keys import characters_key
from projectLiter.WordAnalyser.results_keys import frequency_key
from projectLiter.WordAnalyser.results_keys import dict_of_words_key

# import nltk

# nltk.download('averaged_perceptron_tagger')
text = ""
words = []
wordsDict = {}
mor = morph


def open_file(file_name):
    with codecs.open(file_name, encoding='utf-8') as f:
        global text, words, wordsDict
        text = f.read()
        print("Подготовка текста...")
        words = formatText(text, removeSymbols, triggerSymbols).split(' ')
        words = [item for item in words if item]
        wordsDict = wordsCounterDict(words, morph)
        print("Анализ...")
        f.close()


def text_analysis(file_name, language="ru"):
    global mor, top_of_words, characters, posts, statistic, dict_for_next_analysis
    resultDict = {}
    open_file(file_name)

    top_of_words = word_frequency(words)

    if language == "ru":
        characters = charactersFinderRus(text, wordsDict, words, morph)
        statistic = {}
        posts = []
        dict_for_next_analysis = morphAnalysisRus(words, posts, statistic, morph)
    elif language == "en":
        top_of_words = word_frequency(words)
    del mor

    resultDict[frequency_key] = top_of_words
    resultDict[characters_key] = characters
    resultDict[morph_posts_key] = posts
    resultDict[morph_statistic_key] = statistic
    resultDict[dict_of_words_key] = dict_for_next_analysis
    return resultDict
    # print(words)


if __name__ == '__main__':
    results = text_analysis("text.txt", "ru")

    # print("Частотность:")
    # for word in results[frequency_key]:
    #     print(word)
    print("Найденные персонажи:")
    for character in results[characters_key]:
        print(character)
    print("Найденные части речи:")
    for post in results[morph_posts_key]:
        print(post + ' - ' + str(results[morph_statistic_key][post]))
