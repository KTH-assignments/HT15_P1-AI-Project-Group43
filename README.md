HT15_AI_Project_Group43
=======================

Construct a one-word-at-a-time story with an AI agent.

You'll need NLTK v.2.0.4 (NOT the pip version) and

language-check (pip install 3to2, pip install language-check).
More at https://pypi.python.org/pypi/language-check


Command line usage:

python main.py [-c CORPUS] [-cc CORPUS_CATEGORY] [-n N] [-e EST]
               [-g CHECK_GRAMMAR] [-r RECORD] [-d RECORD_DIRECTORY]


               -c CORPUS : A string identifier for the corpus used to train the
                  language model. Treebank acts as the default corpus.

               -cc CORPUS_CATEGORY : A string specifying which section of CORPUS
                   to use as the training corpus. News is the default category.

               -n N : An integer specifying the order of the language model.
                  N = 3 by default.

               -e EST : An integer specifying the smoothing operator. Use 1 for
                  the Lidstone smoothing technique, 2 for the ELE one.
                  The Maximum Likelihood Estimator will be used as the default
                  smoothing operator.

               -g GRAMMAR : An integer specifying the use of grammar checking.
                  Use 0 to disable. Enabled by default.

               -r RECORD : An integer specifying whether to record the story
                  or not. Use 1 to enable. 0 By default.

               -d RECORD_DIRECTORY : A string specifying which directory to
                  choose for storing the story. "stories" by default
