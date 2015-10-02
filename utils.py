from nltk.corpus import *

# Initializes corpus, n for ngrams and the smoothing technique
def initialize(args):

    if not args:
        print 'usage: [--corpus] [--n (for ngrams)] [--smoother]'
        print 'Using treebank as corpus, n = 4, no smoothing'
        sentences = treebank.words()
        N = 4
        smoother = 0
    else:
        # The training set
        # Treebank produces unorthodox results in the context of a usual conversation
        # because of its economic content.
        if args[0] == "--treebank":
            sentences = treebank.words()
        elif args[0] == "--brown":
            sentences = brown.words()
        elif args[0] == "--shakespeare":
            sentences = shakespeare.words() # TODO Review this, not compatible
        else:
            print "Falling back to treebank as training set"
            sentences = treebank.words()

        N = int(args[1][-1])

        smoother = int(args[2][-1])

    return sentences, N, smoother
