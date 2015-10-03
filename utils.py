from nltk.corpus import *
from nltk.probability import *
from nltk.model import NgramModel

from nltk import *


################################################################################
# Initializes corpus, n for ngrams and the smoothing technique
################################################################################
def init_base(corpus_, N_, est_):

    # Sets the training set and extracts its contents as a list of words
    words = set_corpus(corpus_)

    # Set the N-gram N factor
    N = N_

    # Set the smoothing estimator
    estimator = set_estimator(est_, words)

    return words, N, estimator



################################################################################
# Constructs the language model
################################################################################
def init_language_model(words, N, estimator):

    # Ngram language model based on the training set
    if estimator:
        langModel = NgramModel(N, words, estimator=estimator)
    else:
        langModel = NgramModel(N, words)

    return langModel



################################################################################
# Constructs the tagging model
################################################################################
def init_tagger_model():
    pass



################################################################################
def init(corpus_, N_, est_):

    # Initialize the corpus (sentences), size N (for ngrams)
    # and the estimator (estimator) if smoothing is selected
    words, N, estimator = init_base(corpus_, N_, est_)

    # Builds the language model based on the selected base
    language_model = init_language_model(words, N, estimator)

    return language_model



################################################################################
# Sets the training set and extracts its contents as a list of words
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

    # The tokenized training set as a list
    words = []
    for sentence in sentences:
        sent = word_tokenize(sentence)
        for s in sent:
            words.append(s)

    return words



################################################################################
# Sets the estimator for smoothing
################################################################################
def set_estimator(est_, words):

    # Find how many bins we'll need
    bins = len(words)

    # Smoother selection
    if est_ == 0:
        estimator = None
    elif est_ == 1:
        print "Using LidstoneProbDist as smoother"
        estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.1)
    elif est_ == 2:
        print "Using WittenBellProbDist as smoother"
        estimator = lambda fdist, bins: WittenBellProbDist(fdist)
    elif est_ == 3:
        print "Using SimpleGoodTuringProbDist as smoother"
        estimator = lambda fdist, bins: SimpleGoodTuringProbDist(fdist)
    elif est_== 4:
        print "Using UniformProbDist as smoother"
        estimator = lambda fdist, bins: UniformProbDist(fdist)
    elif est_== 5:
        print "Using MLEProbDist as smoother"
        estimator = lambda fdist, bins: MLEProbDist(fdist)
    elif est_== 6:
        print "Using ELEProbDist as smoother"
        estimator = lambda fdist, bins: ELEProbDist(fdist)
    elif est_== 7:
        print "Using MutableProbDist as smoother" # This is vvvvvery slow
        estimator = lambda fdist, bins: MutableProbDist(UniformProbDist(words), words)
    else:
        print "Falling back to Lidstone as smoother"
        estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.1)

    return estimator
