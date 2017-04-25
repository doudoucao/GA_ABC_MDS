# coding:utf-8

from __future__ import absolute_import
from __future__ import division, unicode_literals
from __future__ import print_function

from sys import version_info

import nltk

PY3 = version_info[0] == 3

from nltk.util import ngrams
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

# Use classical Snowball stemmer for english
stemmer = SnowballStemmer("english")
tokenizer = RegexpTokenizer(r'\w+')
stopset = frozenset(stopwords.words('english'))


# Convert an object to its unicode representation
def to_unicode(object):
    if isinstance(object, unicode):
        return object
    elif isinstance(object, bytes):
        return object.decode("utf-8")
    else:
        print(str(object))
        if PY3:
            if hasattr(object, "__str__"):
                return unicode(object)
            if hasattr(object, "__bytes__"):
                return bytes(object).decode("utf-8")
        else:
            if hasattr(object, "__unicode__"):
                return unicode(object)
            if hasattr(object, "__str__"):
                return bytes(object).decode("utf-8")


# convert to unicode and convert to lower case
def normalize_word(word):
    return to_unicode(word).lower()


# normalize and stem the word
def stem_word(word):
    return stemmer.stem(normalize_word(word))


# convert the sentence to a list of tokens
def sentence_token(sentence):
    tokens = tokenizer.tokenize(sentence)
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '_']
    tokens = [word.lower() for word in tokens if word not in english_punctuations]
    # remove the stop word
    tokens = [word for word in tokens if word not in stopset]
    return tokens


# split sentence
def splitSentence(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(paragraph)
    return sentences


def get_len(element):
    return len(tokenizer.tokenize(element))


def get_ngrams(sentence, N):
    tokens = tokenizer.tokenize(sentence.lower())
    clean = [stemmer.stem(token) for token in tokens]
    return [gram for gram in ngrams(clean, N)]
