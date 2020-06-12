def word_comparison(word1, word2):
    if (word1[:-1] == word2[:-1]) or word1[:-1] == word2 or word1 == word2[:-1]:
        return "True"
    else:
        return "False"

