import sys
import time
import datetime
import nltk_utils
import language_check_utils
import argparse

from nltk.parse.chart import ChartParser


def main():

    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corpus", type=str, help="The corpus to use for training")
    parser.add_argument("-cc", "--corpus_category", type=str, help="The specific categories of the corpus to use for training")
    parser.add_argument("-n", "--N", type=int, help="N-gram factor")
    parser.add_argument("-e", "--est", type=int, help="Which estimator to use for smoothing")
    parser.add_argument("-g", "--check_grammar", type=int, help="Whether to check for grammatical errors")
    parser.add_argument("-r", "--record", type=int, help="Record the story")
    parser.add_argument("-d", "--record_directory", type=str, help="The directory in which the story is recorded")
    args = parser.parse_args()

    corpus = args.corpus
    corpus_category = args.corpus_category
    N = args.N
    est = args.est
    record = args.record
    record_directory = args.record_directory


    if args.corpus is None:
        corpus = "treebank"
        print "--Using treebank as the default corpus"

    if args.corpus_category is None:
        corpus_category = "news"
        if corpus == "brown":
            print "--Using news as the default corpus category"

    if args.N is None:
        N = 3
        print "--Using N = 3 as default ngram factor"

    if args.est is None:
        est = 0
        print "--Not using smoothing by default"

    if args.check_grammar is None:
        check_grammar = True
        print "--Using grammar checks by default"
    else:
        if args.check_grammar == 0:
            check_grammar = False
            print "--Not using grammar checks"
        else:
            check_grammar = True
            print "--Using grammar checks"

    if args.record is None:
        record = 0
        print "--The story below will remain strictly between us"
    elif record > 0:
        # Default directory in which the story will be recorded
        record_directory = "stories/"

    if args.record_directory is not None:
        record_directory += "/"
        record = 1


    if record > 0:
        # The name of the file in which the story is recorded
        file_name = record_directory + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S') + '.txt'
        print "--Story recorded in", file_name



    # The language and tag models, and the context free grammar induced
    # from the corpus used
    langModel = nltk_utils.init(corpus, corpus_category, N, est)

    #parser = ChartParser(cfg_grammar)

    # The conversation has to have N-1 places in the beginning
    conversation = ["",] * (N-1)


    print "It took a while, but I'm ready; let's play!"
    while True:

        try:

            conversation = user_says(conversation, check_grammar)

            conversation = agent_says(conversation, N, langModel, check_grammar)

            print " ".join(conversation)

            log_conversation(file_name, " ".join(conversation))


        except KeyboardInterrupt:
            sys.exit(1)



################################################################################
# The user's response. It returns the conversation in full.
################################################################################
def user_says(conversation, check_grammar):

    # Keep a backup of the so far conversation
    if check_grammar:
        valid_conversation = list(conversation)

    # Read the user's word and check the validity of the so far conversation
    users_input_is_correct = False
    while not users_input_is_correct:

        # Read the user's word input
        users_word = raw_input()

        # Add it to the story, but keep a backup of the story so far,
        # maybe the user's input is incorrect.
        conversation.append(users_word)

        if check_grammar:

            # Check the conversation's correctness
            users_input_is_correct = language_check_utils.check(conversation)

            if not users_input_is_correct:
                print "Unacceptable input. Please try again."
                conversation = list(valid_conversation)
        else:
            users_input_is_correct = True

    return conversation



################################################################################
# The agent's response. The agent returns the conversation in full.
################################################################################
def agent_says(conversation, N, langModel, check_grammar):

    # Keep a backup of the so far conversation
    if check_grammar:
        valid_conversation = list(conversation)

    sentence_is_correct = False

    while not sentence_is_correct:

        # The last N-1 words are the context in which the next word should
        # be placed
        if N == 1:
            context = [""]
        else:
            context = conversation[-(N-1):]

        # Predict one word, add it to the story and print the story so far

        predicted_phrase = langModel.generate(1, context)

        predicted_word = predicted_phrase[-1]

        # Add the predicted word to the story,
        # but keep a backup of the story so far,
        # maybe the agent's guess is incorrect
        conversation.append(predicted_word)

        if check_grammar:

            sentence_is_correct = language_check_utils.check(conversation)

            if not sentence_is_correct:
                conversation = list(valid_conversation)
        else:
            sentence_is_correct = True

    return conversation



################################################################################
# Records conversation `conversation_` in the directory `filename_`
################################################################################
def log_conversation(filename_, conversation_):

    with open(filename_, 'a') as f:
        f.write(conversation_ + "\n")


if __name__ == '__main__':
    main()
