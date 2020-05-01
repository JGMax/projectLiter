def sameNameFilter(charactersList, characterString, morph):
    if not charactersList:
        charactersList.append(characterString)
    else:
        characterWords = characterString.split(' ')
        doNotAdd = 0
        for item in charactersList:
            doNotAdd = 0
            itemWords = item.split(' ')
            # i = 0
            # j = 0
            # k = 0

            for iword in itemWords:
                # iword = morph.parse(iword.lower())[0].normal_form
                for cword in characterWords:
                    # cword = morph.parse(cword.lower())[0].normal_form
                    if cword in iword:
                        doNotAdd += 1
                        break
            if doNotAdd == len(characterWords):
                break
            elif doNotAdd == len(itemWords):
                charactersList[charactersList.index(item)] = characterString
                doNotAdd = len(charactersList)
                break
        if doNotAdd < len(characterWords):
            charactersList.append(characterString)


def morphNameFilter(resultsList, wordNumber, case, gender, number, tense):
    findResult = ["0"]
    if wordNumber == len(resultsList):
        findResult[0] = "1"
        return findResult

    for result in resultsList[wordNumber]:
        if result.tag.POS:
            if "NOUN" in result.tag.POS or "ADJF" in result.tag.POS or "ADJS" in result.tag.POS:
                if wordNumber > 0:
                    if (case == result.tag.case and gender == result.tag.gender and number == result.tag.number
                            and tense == result.tag.tense):
                        findResult = morphNameFilter(resultsList, wordNumber + 1, case, gender,
                                                                  number, tense)
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


def properNameFilter(characterList, wordsList, triggerList, morph):
    i = 0
    while i < len(characterList):
        j = 0
        while j < len(wordsList):
            if morph.parse(wordsList[j].lower())[0].normal_form == morph.parse(characterList[i].lower())[0].normal_form:
                if not wordsList[j].istitle():
                    characterList.pop(i)
                    i -= 1
                    break
                elif not j == 0:
                    for item in triggerList:
                        if item == wordsList[j - 1]:
                            break
                    else:
                        break
            elif not wordsList[j]:
                wordsList.pop(j)
                j -= 1
            j += 1
        else:
            characterList.pop(i)
            i -= 1
        i += 1
