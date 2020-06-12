def remove(value, deleteChars):
    for c in deleteChars:
        value = value.replace(c, '')
    return value


def formatText(editText, stringToRemove, listOfTriggers):
    editText = remove(editText, stringToRemove)
    for item in listOfTriggers:
        editText = editText.replace(item, f' {item} ')
    return editText


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
