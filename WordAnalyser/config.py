
import pymorphy2

nerModelPath = './WordAnalyser/models/slovnet_ner_news_v1.tar'
nevecModelPath = './WordAnalyser/models/navec_news_v1_1B_250K_300d_100q.tar'

triggerSymbols = ['.', '!', '?', '"', '«', '\n', '…']
removeSymbols = '»,\\:/;()\r'

morph = pymorphy2.MorphAnalyzer()

max_freq_top_size = 30
