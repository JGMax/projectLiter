from natasha import NamesExtractor

from navec import Navec
from slovnet import NER

from projectLiter.WordAnalyser.config import nerModelPath
from projectLiter.WordAnalyser.config import nevecModelPath

navec = Navec.load(nevecModelPath)
ner = NER.load(nerModelPath)
ner.navec(navec)

extractor = NamesExtractor()  # Natasha
