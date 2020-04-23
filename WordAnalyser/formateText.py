def remove(value, deleteChars):
    for c in deleteChars:
        value = value.replace(c, '')
    return value
