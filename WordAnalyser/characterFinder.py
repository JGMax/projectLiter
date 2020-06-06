from projectLiter.WordAnalyser.ner_model_creating import ner

from projectLiter.WordAnalyser.utility import morphNameFilter
from projectLiter.WordAnalyser.utility import sameNameFilter
from projectLiter.WordAnalyser.utility import properNameFilter

from projectLiter.WordAnalyser.formatText import remove
from projectLiter.WordAnalyser.config import triggerSymbols

from projectLiter.WordAnalyser.ner_model_creating import extractor


def slov_NER_finder(text, wordsDict, words, morph):
    characters = []
    for span in ner(text).spans:
        if span.type == 'PER':
            parseResult = []
            namePerWord = text[span.start:span.stop].split(' ')
            for word in namePerWord:
                parseResult.append(morph.parse(word.lower()))
            parseResult = morphNameFilter(parseResult)
            if parseResult[0] == "1":
                character = text[span.start:span.stop]
                character = remove(character, triggerSymbols)
                character = properNameFilter(character, wordsDict, words, triggerSymbols, morph)
                if character:
                    sameNameFilter(characters, character, morph)

            del parseResult
    return characters
    # print(slovCharacters)


def natasha_NER_Finder(text, wordsDict, words, morph):
    characters = []
    matches = extractor(text)
    for match in matches:
        character = ''
        parseResult = []
        for fact in match.fact:
            if fact:
                parseResult.append(morph.parse(fact.lower()))
        parseResult = morphNameFilter(parseResult)
        if parseResult[0] == "1":
            for fact in match.fact:
                if fact:
                    character += fact.title() + ' '
            character = character.strip()
            character = properNameFilter(character, wordsDict, words, triggerSymbols, morph)
            if character:
                sameNameFilter(characters, character, morph)
        del parseResult
    return characters
    # print(characters)


def charactersFinderRus(text, wordsDict, words, morph):
    slovCharacters = slov_NER_finder(text, wordsDict, words, morph)
    natCharacters = natasha_NER_Finder(text, wordsDict, words, morph)
    for character in slovCharacters:
        sameNameFilter(natCharacters, character, morph)
    return natCharacters
