# coding:utf-8
import codecs
import sumpy
import io
import nltk
import itertools
from operator import itemgetter
import networkx as nx
import os

PATH = '/home/zixuan/PycharmProjects/doudou_c/genetic-swarm-MDS/DUC2007'


def load_docset(docset_path):
    docset_id = os.path.split(docset_path)[1]
    docs = []
    walk = os.walk(docset_path)
    for root, dirs, files in walk:
        for name in files:
            # print os.path.join(root, name)
            doc = codecs.open(os.path.join(root, name), 'r', 'utf-8', 'ignore').read().strip()
            docs.append(doc)
    return docs


def load_docsets(duc_dir):
    docset_paths = [os.path.join(duc_dir, fname) for fname in os.listdir(duc_dir)]
    docset_paths = [path for path in docset_paths if os.path.isdir(path)]
    docsets = {}
    for docset_path in docset_paths:
        text = load_docset(docset_path)
        summary = sumpy.textrank(text)
        print summary
        print '--------------------'


load_docsets(PATH)