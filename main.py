import sys

from nltk import *
from nltk.probability import *
from nltk.model import NgramModel

import utils

def main():
    args = sys.argv[1:]

    sentences, N, smoother = utils.initialize(args)

    # The tokenized training set as a list
    words = []
    for sentence in sentences:
        sent = word_tokenize(sentence)
        for s in sent:
            words.append(s)

    # The frequency distribution of the training set
    fdist = FreqDist(words)

    # Smoother
    if smoother == 1:
        est = lambda fdist, bins: LidstoneProbDist(fdist, 0.1)
    elif smoother == 2:
        est = lambda fdist, bins: WittenBellProbDist(fdist, bins = 1e5)
    elif smoother == 3:
        est = lambda fdist, bins: SimpleGoodTuringProbDist(fdist, bins = 1e5)
    else:
        print "Falling back to Lidstone as smoother"
        est = lambda fdist, bins: LidstoneProbDist(fdist, 0.1)




    # Ngram language model based on the training set
    if smoother == 0:
        langModel = NgramModel(N, words)
    else:
        langModel = NgramModel(N, words, estimator=est)

    # The conversation has to have at N-1 places at first
    conversation = ["", "", ""]

    while True:
        try:
            # Read the user's word input
            user = raw_input()

            # Add it to the story
            conversation.append(user)

            # The last N-1 words are the context in which the next word should
            # be placed
            context = conversation[-(N-1):]

            # Predict one word, add it to the story and print the story so far
            predicted_phrase = langModel.generate(1, context)
            conversation.append(predicted_phrase[-1])
            print ' '.join(conversation)
        except KeyboardInterrupt:
            sys.exit(1)


if __name__ == '__main__':
  main()
