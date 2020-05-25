import nltk
from projectLiter.sentimental import Sentimental
from projectLiter.WordAnalyser.results_keys import positive_key
from projectLiter.WordAnalyser.results_keys import negative_key

sent = Sentimental()


def load_sentimental_words(type_of_word_list):
    frequency = nltk.FreqDist(type_of_word_list)
    top_frequency = list(frequency.most_common(400))

    cleaned_top_frequency = (top_frequency[w][0].lower() for w in range(0, len(top_frequency))
                             if len(top_frequency[w][0]) > 5)

    cleaned_top_frequency = set(cleaned_top_frequency)

    positive_cleaned_top_frequency = []
    negative_cleaned_top_frequency = []

    Dict_of_positive_and_negative = {}

    for w in cleaned_top_frequency:
        if (sent.analyze(w))[positive_key] > 0:
            # print(sentence + '- позитивное слово')
            positive_cleaned_top_frequency.append(w)
        elif (sent.analyze(w))[negative_key] < 0:
            # print(sentence + '- отрицательное слово')
            negative_cleaned_top_frequency.append(w)

    Dict_of_positive_and_negative[positive_key] = positive_cleaned_top_frequency
    Dict_of_positive_and_negative[negative_key] = negative_cleaned_top_frequency

    return Dict_of_positive_and_negative
