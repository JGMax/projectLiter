import nltk
from projectLiter.WordAnalyser.config import max_freq_top_size


def word_frequency(words):
    freq = nltk.FreqDist(words)
    top = freq.most_common(max_freq_top_size)
    list_of_popular_words = list(top[w] for w in range(0, len(top)) if len(top[w][0]) > 6)
    return list_of_popular_words
    #print(abc)

