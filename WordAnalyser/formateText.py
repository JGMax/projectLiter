def remove(value, deleteChars):
    for c in deleteChars:
        value = value.replace(c, '')
    return value


def strBetween(value, between):
    string = ''
    isCopy = 0
    for c in value:
        if c == between:
            isCopy = not isCopy
            if not isCopy:
                string += ' '
        elif isCopy:
            string += c
    string = string.rstrip()
    return string

