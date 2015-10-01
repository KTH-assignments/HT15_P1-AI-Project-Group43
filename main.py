from nltk import *
from nltk.probability import *
from nltk.model import NgramModel
from nltk.corpus import treebank

if __name__ == '__main__':

    # The training set
    # Treebank produces unorthodox results in the context of a usual conversation
    # because of its economic content.
    sentences = treebank.words()

    # The tokenized training set as a list
    words = []
    for sentence in sentences:
        sent = word_tokenize(sentence)
        for s in sent:
            words.append(s)

    # Smoother
    est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)

    # N-gram factor
    N = 4

    # Ngram language model based on the training set
    langModel = NgramModel(N, words, estimator=est)

    # The conversation has to have at N-1 places at first
    conversation = ["", "", ""]

    while True:

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
