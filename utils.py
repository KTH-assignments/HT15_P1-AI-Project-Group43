from nltk.corpus import *
from nltk.probability import *
from nltk.model import NgramModel

from nltk import *

################################################################################
# Initializes corpus, n for ngrams and the smoothing technique
################################################################################
def init_base(corpus_, N_, est_):

    # Sets the training set and extracts its contents
    sentences = set_corpus(corpus_)

    # Set the N-gram N factor
    N = N_

    # Set the smoothing estimator
    estimator = set_estimator(est_)

    return sentences, N, estimator



################################################################################
# Initiates the language model
################################################################################
def init_language_model(sentences, N, estimator):

    # The tokenized training set as a list
    words = []
    for sentence in sentences:
        sent = word_tokenize(sentence)
        for s in sent:
            words.append(s)


    # Ngram language model based on the training set
    if estimator:
        langModel = NgramModel(N, words, estimator=estimator)
    else:
        langModel = NgramModel(N, words)

    return langModel



def init_tagger_model():
    pass



################################################################################
def init(corpus_, N_, est_):

    # Initialize the corpus (sentences), size N (for ngrams)
    # and the estimator (estimator) if smoothing is selected
    sentences, N, estimator = init_base(corpus_, N_, est_)

    # Builds the language model based on the selected base
    language_model = init_language_model(sentences, N, estimator)

    return language_model



################################################################################
# Sets the corpus and extracts its contents
################################################################################
def set_corpus(corpus_):

    sentences = ""

    # Set the training set
    # Treebank produces unorthodox results in the context of a usual conversation
    # because of its economic content.
    if corpus_ == "treebank":
        sentences = treebank.words()
    elif corpus_ == "brown":
        sentences = brown.words()
    elif corpus_ == "shakespeare":
        sentences = shakespeare.words() # TODO Review this, not compatible
    else:
        print "Falling back to treebank as training set"
        sentences = treebank.words()

    return sentences



################################################################################
# Sets the estimator for smoothing
################################################################################
def set_estimator(est_):

    # Smoother selection
    if est_ == 0:
        estimator = None
    elif est_ == 1:
        estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.1)
    elif est_ == 2:
        estimator = lambda fdist, bins: WittenBellProbDist(fdist, bins = 1e5)
    elif est_ == 3:
        estimator = lambda fdist, bins: SimpleGoodTuringProbDist(fdist, bins = 1e5)
    else:
        print "Falling back to Lidstone as smoother"
        estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.1)

    return estimator
