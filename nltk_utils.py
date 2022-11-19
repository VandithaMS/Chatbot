import numpy as np
import nltk
import re
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    l=re.findall(r"[\w']+", sentence)
    return l


def stem(word):
    a = [stemmer.stem(i) for i in word] 
    return a


def bag_of_words(tokenized_sentence, words):
    tokenized_sentence=stem(tokenized_sentence)
    bag=np.zeros(len(words), dtype=np.float32)

    for ind,w in enumerate(words):
        if w in tokenized_sentence:
            bag[ind]=1.0

    return bag



