# coding=utf-8
import os

PATH = "./main"
PATH_NEW = "./DUC2007"

# walk = os.walk(PATH)
# for root, dirs, files in walk:
#     if dirs:
#         print dirs
#         for dir in dirs:
#             path = os.path.join(PATH_NEW, dir)
#             os.makedirs(path)
#     for name in files:
#         print os.path.join(root, name)


import os
import codecs
import re
import nltk
from nlp_util import *
from conf import DUC_DIR
from JS import *

__doc__ = '''
    读取DUC2007文档,以及对DUC2007进行预处理
'''


def doc_label_filter(doc):
    """
    过滤文档的标签
    """
    doc = doc.replace('\n    ', ' ').replace('\t', '').replace('.....', '')
    doc = doc.replace('\n', ' ').replace('-', '').replace('...', '')
    doc = re.sub(r'<.*?>', '', doc)
    doc = re.sub(r'&.*?;', '', doc)
    doc = re.sub(r'\(.*?\)', '', doc)
    return doc


def get_text(doc):
    """
    获取文本的内容
    """
    doc = doc.replace('\n', ' ').replace('\t', '')
    m = re.findall('<TEXT>.*?</TEXT>', doc)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    raw = m[0]
    raw = re.sub(r'<.*?>', '', raw)
    sentences = tokenizer.tokenize(raw.strip())
    doc_sentences = []
    for sentence in sentences:
        if len(sentence.split('--', 1)) > 1:
            sentence = sentence.split('--', 1)[1]
        if len(sentence.split('_', 1)) > 1:
            sentence = sentence.split('_', 1)[1]
        sentence = re.sub('\(.*?\)', '', sentence)
        doc = re.sub(r'&.*?;', '', doc)
        if len(sentence.split()) > 13:
            doc_sentences.append(sentence)
    return doc_sentences


def load_docset(docset_path):
    docset_id = os.path.split(docset_path)[1]
    docs = []
    walk = os.walk(docset_path)
    for root, dirs, files in walk:
        for name in files:
            # print os.path.join(root, name)
            doc = codecs.open(os.path.join(root, name), 'r', 'utf-8', 'ignore').read()
            dir = os.path.join(root, name).split('/')[2]
            path_1 = os.path.join(PATH_NEW, dir)
            if not os.path.exists(path_1):
                os.makedirs(path_1)
            doc_sentences = get_text(doc)
            # with open(os.path.join(path_1, name), 'a') as f:
            #     for sentence in doc_sentences:
            #         f.write(sentence+'\n')
            # print splitSentence(doc)
            docs.append(doc_sentences)

    return docset_id, docs


def load_docsets(duc_dir):
    docset_paths = [os.path.join(duc_dir, fname) for fname in os.listdir(duc_dir)]
    docset_paths = [path for path in docset_paths if os.path.isdir(path)]
    docsets = {}
    for docset_path in docset_paths:
        docset_id, docs = load_docset(docset_path)
        docsets[docset_id] = docs

    return docsets


def js_duc_models():
    docsets = load_docsets(PATH)
    topics_id = docsets.keys()
    for topic_id in topics_id:
        docs = docsets[topic_id]
        sentences = []
        for doc in docs:
            sentences.extend(doc)
        doc_freq = compute_tf(sentences)
        for file in os.listdir('./models'):
            if file.split('.')[0] == topic_id[:-1]:
                print file
                raw = codecs.open(os.path.join('./models', file), 'r', 'utf-8').read()
                print js_divergence(splitSentence(raw), doc_freq)




# load_docsets(PATH)
# print './main/D0701A/aaa.txt'.split('/')[2]
js_duc_models()
