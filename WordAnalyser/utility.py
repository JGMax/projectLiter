
def wordsCounterDict(wordsList, morph):
    wordsDict = {}
    for i, word in enumerate(wordsList):
        word = morph.parse(word.lower())[0].normal_form
        if word in wordsDict:
            wordsDict[word][0] += 1
            wordsDict[word].append(i)
        else:
            wordsDict[word] = [1, i]
    return wordsDict


# def sameNameFilter(charactersList, characterString, morph):
#     if not charactersList:
#         charactersList.append(characterString)
#     else:
#         characterWords = characterString.split(' ')
#         doNotAdd = 0
#         for item in charactersList:
#             doNotAdd = 0
#             itemWords = item.split(' ')
#             # i = 0
#             # j = 0
#             # k = 0
#
#             for iword in itemWords:
#                 # iword = morph.parse(iword.lower())[0].normal_form
#                 for cword in characterWords:
#                     # cword = morph.parse(cword.lower())[0].normal_form
#                     if cword in iword:
#                         doNotAdd += 1
#                         break
#             if doNotAdd == len(characterWords):
#                 break
#             elif doNotAdd == len(itemWords):
#                 charactersList[charactersList.index(item)] = characterString
#                 doNotAdd = len(charactersList)
#                 break
#         if doNotAdd < len(characterWords):
#             charactersList.append(characterString)

def sameNameFilter(charactersList, characterString, morph):
    if not charactersList:
        charactersList.append(characterString)
        return charactersList
    else:
        parseResult = []
        characterWords = characterString.split(' ')

        for word in characterWords:
            parseResult.append(morph.parse(word.lower()))

        parseResult = morphNameFilter(parseResult)
        if parseResult[0] == "1":
            parseResult[0] = None
            parseResult.reverse()
            for i, normal in enumerate(parseResult):
                if normal:
                    characterWords[i] = normal
        del parseResult

        for item in charactersList:
            itemWords = item.split(' ')

            parseResult = []
            for word in itemWords:
                parseResult.append(morph.parse(word.lower()))

            parseResult = morphNameFilter(parseResult)
            if parseResult[0] == "1":
                parseResult[0] = None
                parseResult.reverse()
                for i, normal in enumerate(parseResult):
                    if normal:
                        itemWords[i] = normal
            del parseResult

            loop = enumerate(characterWords) if len(characterWords) < len(itemWords) else enumerate(itemWords)
            otherLoop = characterWords if len(characterWords) >= len(itemWords) else itemWords
            k = 0
            for i, word in loop:
                while k + min(len(characterWords), len(itemWords)) - 1 < max(len(characterWords), len(itemWords)):
                    if ((len(word) == 1 and not word == otherLoop[i + k]) or
                        word not in otherLoop[i + k]) and \
                            ((len(otherLoop[i + k]) == 1 and not otherLoop[i + k] == word) or
                             otherLoop[i + k] not in word):
                        k += 1
                    else:
                        break
                else:
                    break
            else:
                if len(itemWords) < len(characterWords):
                    charactersList[charactersList.index(item)] = characterString
                return charactersList
        else:
            charactersList.append(characterString)
            return charactersList


def morphNameFilter(resultsList, wordNumber=0, case=0, gender=0, number=0, tense=0):
    findResult = ["0"]
    if wordNumber == len(resultsList):
        if case or gender or number or tense:
            findResult[0] = "1"
        return findResult

    for result in resultsList[wordNumber]:
        if result.tag.POS:
            if "NOUN" in result.tag.POS or "ADJF" in result.tag.POS or "ADJS" in result.tag.POS:
                if wordNumber > 0:
                    if ((not case or case == result.tag.case) and (not gender or gender == result.tag.gender) and
                            (not number or number == result.tag.number) and
                            (not tense or tense == result.tag.tense)):
                        findResult = morphNameFilter(resultsList, wordNumber + 1, case, gender, number, tense)
                        if findResult[0] == "1":
                            findResult.append(result.normal_form)
                            break
                else:
                    findResult = morphNameFilter(resultsList, wordNumber + 1, result.tag.case, result.tag.gender,
                                                 result.tag.number, result.tag.tense)
                    if findResult[0] == "1":
                        findResult.append(result.normal_form)
                        break
        else:
            findResult = morphNameFilter(resultsList, wordNumber + 1, case, gender, number, tense)
            if findResult[0] == "1":
                findResult.append(result.normal_form)
                break
    return findResult


# def properNameFilter(characterList, wordsList, triggerList, morph):
#     i = 0
#     while i < len(characterList):
#         j = 0
#         while j < len(wordsList):
#             if morph.parse(wordsList[j].lower())[0].normal_form == morph.parse(characterList[i].lower())[0].normal_form:
#                 if not wordsList[j].istitle():
#                     characterList.pop(i)
#                     i -= 1
#                     break
#                 elif not j == 0:
#                     for item in triggerList:
#                         if item == wordsList[j - 1]:
#                             break
#                     else:
#                         break
#             elif not wordsList[j]:
#                 wordsList.pop(j)
#                 j -= 1
#             j += 1
#         else:
#             characterList.pop(i)
#             i -= 1
#         i += 1

def properNameFilter(characterString, wordsDict, wordsList, triggeredSymbols, morph, slice=None):
    if "\r" in characterString:
        characterString = characterString.replace("\r", ' ')
    characterWords = characterString.split(" ")
    
    characterWords[0] = characterWords[0].lower()
    if characterWords[0] not in wordsDict:
        characterWords[0] = morph.parse(characterWords[0])[0].normal_form

    if slice:
        try:
            if wordsDict[characterWords[0]][0] > 1:
                for i, word in enumerate(wordsDict[characterWords[0]]):
                    if i == 0:
                        continue
                    if not wordsList[word].istitle():
                        return None

                    for trigger in triggeredSymbols:
                        if word > 0 and trigger in wordsList[word - 1]:
                            break
                    else:
                        return characterString
                else:
                    return None
            else:
                return None
        except KeyError:
            return None
    else:
        for i, word in enumerate(wordsDict[characterWords[0]]):
            if i == 0:
                continue
            if not wordsList[word].istitle():
                return None
            for trigger in triggeredSymbols:
                if word > 0 and trigger in wordsList[word - 1]:
                    break
            else:
                return characterString
            return None
