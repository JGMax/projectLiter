import nltk
import pymorphy2
from projectLiter.WordAnalyser.word_similarity_comparement_ver2 import word_comparison
from projectLiter.WordAnalyser.config import morph


def amount_of_name_mentions(list_of_names_characters, words):
    freq = nltk.FreqDist(words)

    dict_mentions_of_names = {}

    index = range(len(words))

    for word in list_of_names_characters:
        amount = 0
        if ' ' in word:
            p = nltk.word_tokenize(word)
            amount = freq[p[0]]
            for a in index:
                if word_comparison(p[1], words[a]) == "True":
                    if (word_comparison(p[0], words[a - 1]) == "True") & a - 1 >= 0:
                        amount = amount
                    elif (word_comparison(p[0], words[a + 1]) == "True") & a + 1 <= len(words) - 1:
                        amount = amount
                    else:
                        amount = amount + 1
                    word = p[0] + ' ' + p[1]
                    dict_mentions_of_names[word] = amount
        else:
            for a in index:
                if word_comparison(word, words[a]) == "True":
                    amount = amount + 1
            dict_mentions_of_names[word] = amount
            # print(dict_mentions_of_names) #словарь с упоминаниями персонажей

    return dict_mentions_of_names



