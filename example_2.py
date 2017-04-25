# coding=utf-8
from JS import js_divergence, compute_tf
from GeneticOptimizer import GeneticOptimizer
from SwarmOptimizer import SwarmOptimizer
from main2duc import load_docsets
import pylab as pl
import os
from conf import DUC_DIR


def JS_Gen(docs, length_max, epoch, population_size=1000):
    sentences = []
    for doc in docs:
        sentences.extend(doc)

    doc_freq = compute_tf(sentences)

    gen_optimizer = GeneticOptimizer(fitness_fun=js_divergence,
                                     docs=docs,
                                     docs_representation=doc_freq,
                                     max_length=length_max,
                                     population_size=population_size,
                                     survival_rate=0.5,
                                     mutation_rate=0.2,
                                     reproduction_rate=0.4,
                                     maximization=False)

    return gen_optimizer.evolve(epoch)


def write_file(name, i):
    # 将文件写到summy
    with open(name, 'a') as f:
        f.write(i+'\n')
    f.close()


def get_genetic_result():
    docsets = load_docsets(DUC_DIR)
    topic_id = docsets.keys()
    X = [x for x in xrange(0, 200)]
    Y = []
    for topic_id_name in topic_id:
        docs = docsets[topic_id_name]
        print "########processing {} topic docs#########".format(topic_id_name)
        length_max = 200
        epoch = 200
        population_size = 50
        print "Genetic Algorithm example: "
        best_individual, y = JS_Gen(docs, length_max, epoch, population_size)
        # Y.append(y)
        #
        # pl.plot(X, y, 'g')
        # pl.title('genetic convergence')
        # pl.xlabel('epoch')
        # pl.ylabel('divergence')
        # pl.show()
        for i in best_individual[0]:
            print i
            write_file(os.path.join('./genetic_summy_result', topic_id_name[:-1]), i)

get_genetic_result()