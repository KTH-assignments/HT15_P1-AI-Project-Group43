import sys
import utils
import argparse

from nltk.parse.chart import ChartParser

def main():

    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corpus", type=str, help="The corpus to use for training")
    parser.add_argument("-n", "--N", type=int, help="N-gram factor")
    parser.add_argument("-e", "--est", type=int, help="Which estimator to use for smoothing")
    args = parser.parse_args()

    corpus = args.corpus
    N = args.N
    est = args.est

    if args.corpus is None:
        corpus = "treebank"
        print "Using treebank as the default corpus"

    if args.N is None:
        N = 3
        print "Using N = 3 as default ngram factor"

    if args.est is None:
        est = 0
        print "Not using smoothing"

    # The language and tag models, and the context free grammar induced
    # from the corpus used
    langModel, tagger_model, cfg_grammar = utils.init(corpus, N, est)

    # The conversation has to have at N-1 places at first
    conversation = ["",] * (N-1)


    print "I'm ready, let's play!"
    while True:
        try:
            # Read the user's word input
            users_word = raw_input()

            # Add it to the story
            conversation.append(users_word)

            # The last N-1 words are the context in which the next word should
            # be placed
            context = conversation[-(N-1):]

            # Predict one word, add it to the story and print the story so far
            predicted_phrase = langModel.generate(1, context)

            # The word that was predicted
            predicted_word = predicted_phrase[-1]

            conversation.append(predicted_word)

            # Tag the words in the conversation
            tagged_conversation = tagger_model.tag(conversation)

            # Extract the POS tags from the tagged conversation
            pos_tags = [pos for (token, pos) in tagged_conversation]


            # Is the sentence so far acceptable?
            parser = ChartParser(cfg_grammar)

            trees = parser.nbest_parse(pos_tags[-(N-1):])
            if trees is not None:
                print ' '.join(conversation)




        except KeyboardInterrupt:
            sys.exit(1)


if __name__ == '__main__':
    main()
