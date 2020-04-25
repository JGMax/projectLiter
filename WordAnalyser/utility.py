def sameNameFilter(charactersList, character):
    if not charactersList:
        charactersList.append(character)
    else:
        characterWords = character.split(' ')
        doNotAdd = 0
        for item in charactersList:
            doNotAdd = 0
            itemWords = item.split(' ')
            for iword in itemWords:
                for cword in characterWords:
                    if cword in iword:
                        doNotAdd += 1
                        break
            if doNotAdd == len(characterWords):
                break
            elif doNotAdd == len(itemWords):
                charactersList[charactersList.index(item)] = character
                doNotAdd = len(charactersList)
                break
        if doNotAdd < len(characterWords):
            charactersList.append(character)


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
