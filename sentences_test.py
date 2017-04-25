import nltk
import codecs
import os
from duc_reader import *
from conf import DUC_DIR
from nltk.tokenize import RegexpTokenizer
from nlp_util import *
from JS import *

tokenizer = RegexpTokenizer(r'\w+')

if __name__ == "__main__":
    doc = """
<P>
   Speaking of playing games, is Jesse Camp for real? Is Camp,
anointed the newest idiot in MTV's village after beating 4,000
others in the network's ``I Wanna Be a VJ'' contest in April,
really the lovable geek-stoner he claims to be or is he pulling one
of his wool leg warmers over our eyes? It seems like it may be the
latter. His dad, J. Holden Camp, chairman of the humanities
department at the University of Hartford, tells Spin his son, whose
real name is Josh, ``is a good sweet kid who has created a bit of a
facade. He did well in school, and he had a lot of fun with
drama.'' Looks like he still is.......
</P>
<P>
   &QL;
----- &QC;
 &QL;
</P>
<P>
   &UR; P.O.V. &LR; , &UR;  &LR; the men's magazine which is Details without urban
cool or female readership, continues to genuflect to the guilt-free
guyness which (thankfully) hasn't been on public display since
Frank, Dean, and Sammy rampaged t
    """
    doc = doc.replace('\n    ', ' ').replace('\t', '').replace('.', '').replace('-', '')
    doc = doc.replace('\n', ' ')
    doc = re.sub(r'<.*?>', '', doc)
    doc = re.sub(r'&.*?;', '', doc)
    doc = re.sub(r'\(.*?\)', '', doc)
    sentences = splitSentence(doc.strip())
    print sentences
    for s in splitSentence(doc):
        print sentence_token(s.strip())
    words = get_all_content_words_stemmed(sentences, 2)
    print compute_word_freq(words)
    print compute_tf(sentences)
