# -*- coding: utf-8 -*-

import os
from JS import js_divergence, compute_tf

from GeneticOptimizer import GeneticOptimizer
from SwarmOptimizer import SwarmOptimizer
from duc_reader import load_docsets
from conf import DUC_DIR
import pylab as pl


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
                                     survival_rate=0.4,
                                     mutation_rate=0.2,
                                     reproduction_rate=0.4,
                                     maximization=False)

    return gen_optimizer.evolve(epoch)


def JS_Swarm(docs, length_max, mfe=80000, number_locations=1000):
    sentences = []
    for doc in docs:
        sentences.extend(doc)

    doc_freq = compute_tf(sentences)

    swarm_optimizer = SwarmOptimizer(fitness_fun=js_divergence,
                                     docs=docs,
                                     docs_representation=doc_freq,
                                     max_length=length_max,
                                     number_locations=number_locations,
                                     trial_limit=400,
                                     mfe=mfe,

                                     maximization=False)

    return swarm_optimizer.swarm_disperse()


def write_file(name, i):
    # 将文件写到summy
    with open(name, 'a') as f:
        f.write(i)
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
        Y.append(y)

        pl.plot(X, y, 'g')
        pl.title('genetic convergence')
        pl.xlabel('epoch')
        pl.ylabel('divergence')
        pl.show()
        for i in best_individual[0]:
            print i
            # write_file(os.path.join('./genetic_summy_result', topic_id_name[:-1]), i+'\n')
            # for y in Y:
            #     pl.plot(X, y, 'g')
            #     pl.title('genetic convergence')
            #     pl.xlabel('epoch')
            #     pl.ylabel('divergence')
            #     pl.show()


def get_swarm_result():
    docsets = load_docsets(DUC_DIR)
    topic_id = docsets.keys()
    for topic_id_name in topic_id:
        docs = docsets[topic_id_name]
        print "########processing {} topic docs#########".format(topic_id_name)
        length_max = 200
        mfe = 1000
        number_locations = 40  # equal to population_size
        print "Swarm Intelligence example:"
        best_location, epoch, y = JS_Swarm(docs, length_max, mfe, number_locations)
        print y[1:]
        X = [x for x in xrange(0, epoch-1)]
        # for j in JS_Swarm(docs, length_max, mfe, number_locations)[0]:
        #     print j
            # write_file(os.path.join('./swarm_summy_result', topic_id_name[:-1]), j)
        pl.plot(X, y[1:], 'r')
        pl.title('swarm convergence')
        pl.xlabel('epoch')
        pl.ylabel('divergence')
        pl.show()


if __name__ == '__main__':
    # genetic
    # get_genetic_result()
    # swarm
    get_swarm_result()

    # if __name__ == '__main__':
    #     doc_1 = ["first sentence of first doc", "second sentence", "third sentence of the first document here",
    #               "another one", "what is going on "]
    #     doc_2 = ["one sentnece quite random", "here is another one completely random", "sentence here", "que pasa",
    #               "a sentence in an other document"]
    #     doc_3 =  ["it will be a short docuemnt", "only two sentences"]
    #     docs = [doc_1, doc_2, doc_3]
    #
    #     length_max = 10
    #     epoch = 20
    #     population_size = 10
    #     print "Genetic Algorithm example:"
    #     print JS_Gen(docs, length_max, epoch, population_size)
    #
    #     print "\n==================\n"
    #     mfe = 400
    #     number_locations = population_size
    #     print "Swarm Intelligence example:"
    #     print JS_Swarm(docs, length_max, mfe, number_locations)
