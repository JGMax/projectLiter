from projectLiter.WordAnalyser.word_analyser import text_analysis
from projectLiter.WordAnalyser.results_keys import dict_of_words_key
from projectLiter.WordAnalyser.results_keys import morph_posts_key
from projectLiter.WordAnalyser.top_sentimental_words import load_sentimental_words

results = text_analysis('text.txt', language = "ru")  # загружаем книгу

dict_for_next = results[dict_of_words_key]
keys = results[morph_posts_key]

words_for_analysis = dict_for_next

adj_list = words_for_analysis['ADJF']  # лист прилагательных
adv_list = words_for_analysis['ADVB']  # лист наречий

# Adjectives
Dict_of_positive_and_negative_adj = load_sentimental_words(adj_list)  # словарь, содержащий 2 ключа: postive, negative для прилагательных

# Adverbs
Dict_of_positive_and_negative_adv = load_sentimental_words(adv_list)  # словарь, содержащий 2 ключа: postive, negative для наречий

print('Positive adjectives:')
print(Dict_of_positive_and_negative_adj['positive'][:10])  # вывод прилагателынх
print('Negative adjectives:')
print(Dict_of_positive_and_negative_adj['negative'][:10])

print('Positive adverbs:')
print(Dict_of_positive_and_negative_adv['positive'][:10])  #вывод наречий
print('Negative adverbs:')
print(Dict_of_positive_and_negative_adv['negative'][:10])



