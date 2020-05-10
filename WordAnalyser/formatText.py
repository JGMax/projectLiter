def remove(value, deleteChars):
    for c in deleteChars:
        value = value.replace(c, '')
    return value


def formatText(editText, stringToRemove, listOfTriggers):
    editText = remove(editText, stringToRemove)
    editText = editText.replace('\n', ' ')
    for item in listOfTriggers:
        editText = editText.replace(item, f' {item} ')
    return editText