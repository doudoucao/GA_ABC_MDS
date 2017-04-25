import nltk, sys, glob
import os

reload(sys)
sys.setdefaultencoding('utf8')

lemmatize = True
rm_stopwords = True
num_sentences = 10
stopwords = nltk.corpus.stopwords.words('english')
lemmatizer = nltk.stem.WordNetLemmatizer()


def clean_sentence(tokens):
    tokens = [t.lower() for t in tokens]
    if lemmatize: tokens = [lemmatizer.lemmatize(t) for t in tokens]
    if rm_stopwords: tokens = [t for t in tokens if t not in stopwords]
    return tokens


def get_probabilities(cluster, lemmatize, rm_stopwords):
    # Store word probabilities for this cluster
    word_ps = {}
    # Keep track of the number of tokens to calculate probabilities later
    token_count = 0.0
    # Gather counts for all words in all documents
    for path in cluster:
        with open(path) as f:
            tokens = clean_sentence(nltk.word_tokenize(f.read()))
            token_count += len(tokens)
            for token in tokens:
                if token not in word_ps:
                    word_ps[token] = 1.0
                else:
                    word_ps[token] += 1.0
    # Divide word counts by the number of tokens across all files
    for word_p in word_ps:
        word_ps[word_p] /= float(token_count)
    return word_ps


def get_sentences(cluster):
    sentences = []
    for path in cluster:
        with open(path) as f:
            sentences += nltk.sent_tokenize(f.read())
    return sentences


def score_sentence(sentence, word_ps):
    score = 0.0
    num_tokens = 0.0
    sentence = nltk.word_tokenize(sentence)
    tokens = clean_sentence(sentence)
    for token in tokens:
        if token in word_ps:
            score += word_ps[token]
            num_tokens += 1.0
    return float(score) / (float(num_tokens)+1)


def max_sentence(sentences, word_ps, simplified):
    max_sentence = None
    max_score = None
    for sentence in sentences:
        score = score_sentence(sentence, word_ps)
        if score > max_score or max_score == None:
            max_sentence = sentence
            max_score = score
    if not simplified: update_ps(max_sentence, word_ps)
    return max_sentence


def update_ps(max_sentence, word_ps):
    sentence = nltk.word_tokenize(max_sentence)
    sentence = clean_sentence(sentence)
    for word in sentence:
        word_ps[word] **= 2
    return True


def orig(cluster):
    cluster = glob.glob(cluster)
    word_ps = get_probabilities(cluster, lemmatize, rm_stopwords)
    sentences = get_sentences(cluster)
    summary = []
    for i in range(num_sentences):
        summary.append(max_sentence(sentences, word_ps, False))
    return " ".join(summary)


def simplified(cluster):
    cluster = glob.glob(cluster)
    word_ps = get_probabilities(cluster, lemmatize, rm_stopwords)
    sentences = get_sentences(cluster)
    summary = []
    for i in range(num_sentences):
        summary.append(max_sentence(sentences, word_ps, True))
    return " ".join(summary)


def get_duc_basic_sum(path):
    topic_dirs = [os.path.join(path, fname) for fname in os.listdir(path)]
    for each_topic in topic_dirs:
        print '########processing  {}########'.format(each_topic.split('/')[-1])
        cluster = os.path.join(each_topic, '*.*')
        print orig(cluster)
        with open(os.path.join('./result_sumbasic', each_topic.split('/')[-1][:-1]), 'a') as f:
            f.write(orig(cluster))


path = '/home/zixuan/PycharmProjects/doudou_c/genetic-swarm-MDS/DUC2007'

get_duc_basic_sum(path)


def main():
    method = sys.argv[1]
    cluster = sys.argv[2]
    summary = eval(method + "('" + cluster + "')")
    print summary

# if __name__ == "__main__":
#     main()

# print glob.glob('./docs/doc*-*.txt')
