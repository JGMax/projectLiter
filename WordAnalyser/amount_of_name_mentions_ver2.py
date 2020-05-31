import nltk
import pymorphy2
from projectLiter.WordAnalyser.word_similarity_comparement_ver2 import word_comparison
from projectLiter.WordAnalyser.word_analyser import text_analysis
from projectLiter.WordAnalyser.results_keys import characters_key
from projectLiter.WordAnalyser.config import morph
#file = open('models/book5.txt', encoding = 'utf - 8')

#text = file.read()

results = text_analysis(text, language = "ru")  # загружаем книгу

words = nltk.word_tokenize(text)
freq = nltk.FreqDist(words)

dict_for_characters = results[characters_key]

print(dict_for_characters)

dict_mentions_of_names = {}

index1 = range(len(words))

for word in dict_for_characters:
   amount=0
   if ' ' in word:
       p = nltk.word_tokenize(word)
       index2 = range(len(p))
       amount = freq[p[0]]+freq[morph.parse(p[0])[0].normal_form]
       for a in index1:
           if word_comparison(p[1],words[a]) == 1:
               if word_comparison(p[1],words[a-1]) == 1 & a-1>=0:
                  amount = amount + 0
               elif word_comparison(p[1],words[a+1]) == 1 & a+1<=len(words)-1:
                    amount = amount + 0
               else: 
                    amount = amount + 1
               word = morph.parse(p[0])[0].normal_form + ' ' + morph.parse(p[1])[0].normal_form
               dict_mentions_of_names[word] = amount
   else:
       for a in index1:
           if word_comparison(word, words[a]) == 1:
              amount = amount + 1
       dict_mentions_of_names[word] = amount

#print(dict_mentions_of_names) словарь с упоминаниями персонажей



