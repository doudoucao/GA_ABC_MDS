# coding=utf-8

import os
import codecs
import re
import nltk
from nlp_util import *
from conf import DUC_DIR

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
    doc = re.sub(r'(.*?)', '', doc)
    return doc


def get_text(doc):
    """
    获取文本的内容
    """
    doc = doc.replace('\n', ' ').replace('\t', '')
    m = re.findall('<TEXT>.*?</TEXT>', doc)
    if m:
        doc = doc_label_filter(m[0])
        return doc
    else:
        print "can not find"


def load_docset(docset_path):
    docset_id = os.path.split(docset_path)[1]
    docs = []
    walk = os.walk(docset_path)
    for root, dirs, files in walk:
        for name in files:
            # print os.path.join(root, name)
            doc = codecs.open(os.path.join(root, name), 'r', 'utf-8', 'ignore').read()
            doc = get_text(doc)

            # print splitSentence(doc)
            docs.append(splitSentence(doc))

    return docset_id, docs


def load_docsets(duc_dir):
    docset_paths = [os.path.join(duc_dir, fname) for fname in os.listdir(duc_dir)]
    docset_paths = [path for path in docset_paths if os.path.isdir(path)]
    docsets = {}
    for docset_path in docset_paths:
        docset_id, docs = load_docset(docset_path)
        docsets[docset_id] = docs

    return docsets
